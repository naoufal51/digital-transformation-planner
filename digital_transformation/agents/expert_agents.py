from typing import Dict, List, Any, Optional
import json
import re
import logging
import uuid

from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableConfig
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableLambda, chain as as_runnable
from pydantic import BaseModel, Field

from digital_transformation.schema.state import ConsultationState, DomainExpert
from digital_transformation.agents.search_tools import get_search_tools

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create LLM instances with named runs for better tracing
fast_llm = ChatOpenAI(
    model="gpt-4o-mini", 
    temperature=0.2,
    model_kwargs={"response_format": {"type": "text"}},  # Ensure we get valid text format
    tags=["expert_consultation", "question_generation"]
)
expert_llm = ChatOpenAI(
    model="gpt-4o", 
    temperature=0.1,
    model_kwargs={"response_format": {"type": "text"}},  # Ensure we get valid text format
    tags=["expert_consultation", "answer_generation"]
)


class QueryList(BaseModel):
    """List of search queries to find information for answering a question."""
    queries: List[str] = Field(..., description="List of search queries to execute")


class ExpertAnswer(BaseModel):
    """Expert answer to a digital transformation query."""
    answer: str = Field(..., description="The expert's answer to the consultant's question")
    cited_urls: List[str] = Field(default_factory=list, description="URLs cited in the answer")


def sanitize_name(name: str) -> str:
    """Sanitize a name to only include alphanumeric characters, underscores, and hyphens."""
    # Replace spaces and other invalid characters with underscores
    sanitized = re.sub(r'[^a-zA-Z0-9_-]', '_', name)
    logger.info(f"Sanitized name: {name} -> {sanitized}")
    return sanitized


def tag_with_name(ai_message: AIMessage, name: str):
    """Tag an AI message with a name."""
    sanitized_name = sanitize_name(name)
    ai_message.name = sanitized_name
    logger.info(f"Tagged message with name: {sanitized_name}")
    return ai_message


def swap_roles(state: ConsultationState, name: str):
    """Swap the roles in the messages to maintain conversation flow."""
    converted = []
    sanitized_name = sanitize_name(name)
    for message in state["messages"]:
        if isinstance(message, AIMessage) and message.name != sanitized_name:
            message = HumanMessage(**message.model_dump(exclude={"type"}))
        converted.append(message)
    return {"messages": converted}


# Define the prompts for the question generator
gen_question_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are a strategic consultant analyzing a company for digital transformation opportunities. 
You're conducting an interview with a subject matter expert to gather insights. 
Remain focused on your specific area of expertise while exploring the company details provided.

When you have no more questions to ask, say "Thank you for your insights. This concludes our interview."
Ask one focused question at a time, and don't repeat questions you've already asked.
Your questions should be relevant to digital transformation challenges and opportunities.
Be thorough and curious, extracting as much valuable insight as possible.

IMPORTANT: Keep your response concise, professional, and factual. Avoid creative elaboration.

Stay true to your specific domain expertise:

{persona}

Company Information:
Company Name: {company_name}
Industry: {industry}
Description: {company_description}
Current Challenges: {business_challenges}
Current Technologies: {current_technologies}
Transformation Goals: {transformation_goals}
"""
    ),
    MessagesPlaceholder(variable_name="messages", optional=True),
])


@as_runnable
async def generate_question(state: ConsultationState, 
                           company_context: Dict[str, Any] = None):
    """Generate a question from the consultant to the expert."""
    run_id = str(uuid.uuid4())[:8]  # Generate a short run ID for tracing
    try:
        expert = state["expert"]
        sanitized_name = sanitize_name(expert.name)
        logger.info(f"[{run_id}] Generating question with expert: {sanitized_name}")
        
        # Add company context if available
        context = {
            "company_name": "Unknown",
            "industry": "Unknown",
            "company_description": "Unknown",
            "business_challenges": "Unknown",
            "current_technologies": "Unknown",
            "transformation_goals": "Unknown"
        }
        
        if company_context:
            context = {
                "company_name": company_context.get("company_name", "Unknown"),
                "industry": company_context.get("industry", "Unknown"),
                "company_description": company_context.get("company_description", "Unknown"),
                "business_challenges": ", ".join(company_context.get("business_challenges", [])),
                "current_technologies": ", ".join(company_context.get("current_technologies", [])),
                "transformation_goals": ", ".join(company_context.get("transformation_goals", []))
            }
        
        # Add metadata for better tracing
        config = {"metadata": {"expert": sanitized_name, "run_id": run_id}}
        
        # Create the question generation chain
        question_chain = (
            RunnableLambda(swap_roles).bind(name=sanitized_name)
            | gen_question_prompt.partial(persona=expert.persona, **context)
            | fast_llm
            | RunnableLambda(tag_with_name).bind(name=sanitized_name)
        )
        
        result = await question_chain.ainvoke(state, config=config)
        logger.info(f"[{run_id}] Generated question: {result.content[:100]}...")
        return {"messages": [result]}
    except Exception as e:
        logger.error(f"[{run_id}] Error generating question: {str(e)}", exc_info=True)
        # Return a fallback question to avoid breaking the flow
        fallback_message = AIMessage(
            name=sanitized_name,
            content="Could you tell me more about how your company approaches digital transformation? What are your main priorities?"
        )
        return {"messages": [fallback_message]}


class ExpertAnswerGenerator:
    """Generator for expert answers using search tools."""
    
    def __init__(self):
        self.search_tools = get_search_tools()
        self.max_str_len = 15000  # Max length for search results
    
    async def generate_queries(self, messages: List[Any], run_id: str = "") -> List[str]:
        """Generate search queries based on the consultant's question."""
        try:
            logger.info(f"[{run_id}] Generating search queries")
            query_gen_prompt = ChatPromptTemplate.from_messages([
                (
                    "system",
                    """You are a research assistant helping a digital transformation expert.
Generate search queries to find relevant information to answer the consultant's question.
Create 2-3 specific search queries that will help find the most relevant information.
Each query should be concise (under 15 words) and focused on one specific aspect of the question."""
                ),
                MessagesPlaceholder(variable_name="messages")
            ])
            
            config = {"metadata": {"process": "query_generation", "run_id": run_id}}
            
            response = await fast_llm.with_structured_output(
                QueryList, 
                include_raw=True
            ).ainvoke(query_gen_prompt.format(messages=messages), config=config)
            
            queries = response["parsed"].queries
            logger.info(f"[{run_id}] Generated {len(queries)} search queries")
            return queries
        except Exception as e:
            logger.error(f"[{run_id}] Error generating queries: {str(e)}", exc_info=True)
            # Fall back to simple queries if there's an error
            return ["digital transformation best practices", "business digital modernization"]
    
    async def gen_expert_answer(
        self,
        state: ConsultationState,
        config: Optional[RunnableConfig] = None,
        name: str = "Digital_Transformation_Expert",
    ):
        """Generate an expert answer using search tools."""
        run_id = str(uuid.uuid4())[:8]  # Generate a short run ID for tracing
        try:
            sanitized_name = sanitize_name(name)
            logger.info(f"[{run_id}] Generating expert answer with name: {sanitized_name}")
            
            # Merge configs if needed
            if config is None:
                config = {}
            
            # Add metadata for better tracing
            if "metadata" not in config:
                config["metadata"] = {}
            config["metadata"].update({
                "expert": sanitized_name,
                "run_id": run_id,
                "process": "expert_answer"
            })
            
            # Swap roles to prepare for response generation
            swapped_state = swap_roles(state, sanitized_name)
            
            # Generate search queries
            queries = await self.generate_queries(swapped_state["messages"], run_id)
            
            # Execute searches using the first search tool (general search)
            search_tool = self.search_tools[0]
            query_results = await search_tool.abatch(queries, config, return_exceptions=True)
            
            # Filter out exceptions and prepare results
            successful_results = [res for res in query_results if not isinstance(res, Exception)]
            logger.info(f"[{run_id}] Got {len(successful_results)} successful search results")
            
            # Handle case of no successful results
            if not successful_results:
                logger.warning(f"[{run_id}] No successful search results - using fallback response")
                formatted_message = AIMessage(
                    name=sanitized_name,
                    content="Based on my expertise, I recommend focusing on a clear digital transformation strategy aligned with your business goals. Start with a thorough assessment of your current systems and processes before implementing any new technologies."
                )
                return {"messages": [formatted_message], "references": {}}
            
            all_query_results = {
                res["url"]: res["content"] 
                for results in successful_results 
                for res in results
            }
            
            # Truncate to avoid token limits
            dumped = json.dumps(all_query_results)[:self.max_str_len]
            
            # Format for answer generation
            expert_role = state["expert"]
            answer_prompt = ChatPromptTemplate.from_messages([
                (
                    "system",
                    f"""You are {sanitize_name(expert_role.name)}, a digital transformation expert specializing in {expert_role.expertise_area}.
{expert_role.description}

You are responding to a consultant's question about digital transformation.
Use the search results below to inform your answer, but respond in your own expert voice.
Always cite your sources with numbered footnotes [1], [2], etc.

IMPORTANT: Keep your response clear, direct, and fact-based. Avoid excessive details or creative flourishes.
Focus on providing concrete, actionable recommendations based on established best practices.

Search Results:
{{search_results}}"""
                ),
                MessagesPlaceholder(variable_name="messages")
            ])
            
            # Create the answer chain
            answer_chain = (
                answer_prompt.partial(search_results=dumped)
                | expert_llm.with_structured_output(
                    ExpertAnswer, 
                    include_raw=True
                )
            )
            
            # Generate the answer
            logger.info(f"[{run_id}] Generating structured answer")
            generated = await answer_chain.ainvoke({"messages": swapped_state["messages"]}, config=config)
            
            # Extract cited URLs
            cited_urls = set(generated["parsed"].cited_urls)
            logger.info(f"[{run_id}] Answer cites {len(cited_urls)} URLs")
            
            # Save only the cited references to the shared state
            cited_references = {k: v for k, v in all_query_results.items() if k in cited_urls}
            
            # Format the answer with citations
            answer_content = (
                f"{generated['parsed'].answer}\n\nCitations:\n" + 
                "\n".join(f"[{i+1}]: {url}" for i, url in enumerate(cited_urls))
            )
            
            formatted_message = AIMessage(name=sanitized_name, content=answer_content)
            logger.info(f"[{run_id}] Answer generated with length: {len(answer_content)}")
            
            return {"messages": [formatted_message], "references": cited_references}
        except Exception as e:
            logger.error(f"[{run_id}] Error in expert answer generation: {str(e)}", exc_info=True)
            # Create a safe fallback answer if there's an error
            formatted_message = AIMessage(
                name=sanitized_name,
                content="I recommend focusing on implementing digital solutions that directly address your business challenges. This typically involves modernizing legacy systems, improving data integration, and enhancing customer-facing digital channels. For more specific advice, I would need additional details about your particular situation."
            )
            return {"messages": [formatted_message], "references": {}}


# Create the expert answer generator instance
expert_answer_generator = ExpertAnswerGenerator()
generate_answer = expert_answer_generator.gen_expert_answer 