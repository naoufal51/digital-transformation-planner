import asyncio
from typing import Dict, List, Any, Optional, TypedDict
import logging
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from langchain_core.messages import AIMessage
from langgraph.pregel import RetryPolicy

from digital_transformation.schema.state import DigitalTransformationState, ConsultationState, add_messages, DomainExpert, Recommendation, TransformationAspect, TransformationPlan, update_entity, update_references
from digital_transformation.schema.assessment import MaturityAssessment
from digital_transformation.agents.interview_graph import interview_graph, create_interview_graph
from digital_transformation.agents.persona_generator import persona_generator
from digital_transformation.agents.transformation_analyzer import transformation_analyzer
from digital_transformation.agents.recommendation_generator import recommendation_generator
from digital_transformation.agents.plan_generator import plan_generator
from digital_transformation.agents.maturity_assessor import maturity_assessor
from digital_transformation.agents.expert_agents import sanitize_name
from digital_transformation.agents.technology_recommender import TechnologyRecommender
from digital_transformation.agents.readiness_assessor import ReadinessAssessor
from digital_transformation.schema.technology import TechnologyStack, TechnologyCategory
from digital_transformation.schema.readiness import OrganizationalReadinessAssessment


async def assess_maturity(state: DigitalTransformationState) -> DigitalTransformationState:
    """
    Assess the company's digital transformation maturity across key dimensions.
    
    Args:
        state: Current state with company information
        
    Returns:
        Updated state with maturity assessment results
    """
    # Extract company information as a dict for easy access
    company_info = {
        "company_name": state["company_name"],
        "company_description": state["company_description"],
        "industry": state["industry"],
        "transformation_goals": state["transformation_goals"],
        "business_challenges": state["business_challenges"],
        "current_technologies": state["current_technologies"]
    }
    
    # Perform maturity assessment
    assessment = await maturity_assessor.assess_maturity(company_info)
    
    # Initialize optional lists if they don't exist in the state
    updated_state = {**state}
    
    # Ensure lists are initialized
    if "transformation_aspects" not in updated_state:
        updated_state["transformation_aspects"] = []
    if "experts" not in updated_state:
        updated_state["experts"] = []
    if "consultation_results" not in updated_state:
        updated_state["consultation_results"] = []
    if "recommendations" not in updated_state:
        updated_state["recommendations"] = []
    
    # Add the assessment
    updated_state["maturity_assessment"] = assessment
    
    return updated_state


async def initialize_analysis(state: DigitalTransformationState) -> DigitalTransformationState:
    """
    Initialize the digital transformation analysis by identifying key aspects to focus on.
    
    Args:
        state: Current state with company information and maturity assessment
        
    Returns:
        Updated state with transformation aspects
    """
    # Extract company information as a dict for easy access
    company_info = {
        "company_name": state["company_name"],
        "company_description": state["company_description"],
        "industry": state["industry"],
        "transformation_goals": state["transformation_goals"],
        "business_challenges": state["business_challenges"],
        "current_technologies": state["current_technologies"]
    }
    
    # Add maturity assessment for context if available
    if "maturity_assessment" in state:
        assessment = state["maturity_assessment"]
        company_info["maturity_level"] = assessment.maturity_level
        company_info["maturity_score"] = assessment.overall_score
        company_info["maturity_strengths"] = assessment.top_strengths
        company_info["maturity_gaps"] = assessment.top_gaps
    
    # Identify transformation aspects
    aspects = await transformation_analyzer.identify_aspects(company_info)
    
    return {**state, "transformation_aspects": aspects}


async def generate_experts(state: DigitalTransformationState) -> DigitalTransformationState:
    """
    Generate expert personas based on company context and identified aspects.
    
    Args:
        state: Current state with company information and aspects
        
    Returns:
        Updated state with expert personas
    """
    # Extract company information
    company_info = {
        "company_name": state["company_name"],
        "company_description": state["company_description"],
        "industry": state["industry"],
        "transformation_goals": state["transformation_goals"],
        "business_challenges": state["business_challenges"],
        "current_technologies": state["current_technologies"]
    }
    
    # Add maturity assessment for context if available
    if "maturity_assessment" in state:
        assessment = state["maturity_assessment"]
        company_info["maturity_level"] = assessment.maturity_level
        company_info["maturity_score"] = assessment.overall_score
        company_info["maturity_strengths"] = assessment.top_strengths
        company_info["maturity_gaps"] = assessment.top_gaps
    
    # Generate expert personas
    experts = await persona_generator.generate_experts(
        company_info,
        state["transformation_aspects"]
    )
    
    return {**state, "experts": experts}


async def conduct_interviews(state: DigitalTransformationState) -> DigitalTransformationState:
    """
    Conduct interviews with each expert.
    
    Args:
        state: Current state with experts
        
    Returns:
        Updated state with interview results
    """
    # Extract company information for context
    company_info = {
        "company_name": state["company_name"],
        "company_description": state["company_description"],
        "industry": state["industry"],
        "transformation_goals": state["transformation_goals"],
        "business_challenges": state["business_challenges"],
        "current_technologies": state["current_technologies"]
    }
    
    # Add maturity assessment for context if available
    if "maturity_assessment" in state:
        assessment = state["maturity_assessment"]
        company_info["maturity_level"] = assessment.maturity_level
        company_info["maturity_score"] = assessment.overall_score
        company_info["maturity_strengths"] = assessment.top_strengths
        company_info["maturity_gaps"] = assessment.top_gaps
    
    # Initialize interview states for each expert
    initial_states = [
        {
            "expert": expert,
            "messages": [
                AIMessage(
                    content=f"I'm here to discuss digital transformation strategies for {state['company_name']}. What questions do you have?",
                    name="Digital_Transformation_Expert"
                )
            ],
            "company_context": company_info  # Add company context directly to the initial state
        }
        for expert in state["experts"]
    ]
    
    # Run interviews in parallel
    interview_tasks = []
    for i, initial_state in enumerate(initial_states):
        # Create a unique thread ID for each interview
        config = {"configurable": {"thread_id": f"expert-interview-{i}"}}
        interview_tasks.append(
            interview_graph.ainvoke(
                initial_state,
                config
            )
        )
    
    # Gather results
    interview_results = await asyncio.gather(*interview_tasks)
    
    return {**state, "consultation_results": interview_results}


async def generate_recommendations(state: DigitalTransformationState) -> DigitalTransformationState:
    """
    Generate recommendations based on expert interviews.
    
    Args:
        state: Current state with interview results
        
    Returns:
        Updated state with recommendations
    """
    # Extract company information
    company_info = {
        "company_name": state["company_name"],
        "company_description": state["company_description"],
        "industry": state["industry"],
        "transformation_goals": state["transformation_goals"],
        "business_challenges": state["business_challenges"],
        "current_technologies": state["current_technologies"]
    }
    
    # Add maturity assessment for context if available
    if "maturity_assessment" in state:
        assessment = state["maturity_assessment"]
        company_info["maturity_level"] = assessment.maturity_level
        company_info["maturity_score"] = assessment.overall_score
        company_info["maturity_strengths"] = assessment.top_strengths
        company_info["maturity_gaps"] = assessment.top_gaps
    
    # Generate recommendations
    recommendations = await recommendation_generator.generate_recommendations(
        company_info,
        state["consultation_results"]
    )
    
    return {**state, "recommendations": recommendations}


async def create_transformation_plan(state: DigitalTransformationState) -> DigitalTransformationState:
    """
    Create a comprehensive digital transformation plan.
    
    Args:
        state: Current state with recommendations
        
    Returns:
        Updated state with transformation plan
    """
    # Extract company information
    company_info = {
        "company_name": state["company_name"],
        "company_description": state["company_description"],
        "industry": state["industry"],
        "transformation_goals": state["transformation_goals"],
        "business_challenges": state["business_challenges"],
        "current_technologies": state["current_technologies"]
    }
    
    # Add maturity assessment for context if available
    if "maturity_assessment" in state:
        assessment = state["maturity_assessment"]
        company_info["maturity_level"] = assessment.maturity_level
        company_info["maturity_score"] = assessment.overall_score
        company_info["maturity_strengths"] = assessment.top_strengths
        company_info["maturity_gaps"] = assessment.top_gaps
    
    # Generate plan
    plan = await plan_generator.generate_plan(
        company_info,
        state["recommendations"]
    )
    
    return {**state, "transformation_plan": plan}


async def recommend_technology_stack(state: DigitalTransformationState) -> DigitalTransformationState:
    """Generate technology stack recommendations based on company info and maturity assessment"""
    # Extract company information for context
    company_info = {
        "company_name": state.get("company_name", ""),
        "company_description": state.get("company_description", ""),
        "industry": state.get("industry", ""),
        "transformation_goals": state.get("transformation_goals", []),
        "business_challenges": state.get("business_challenges", []),
        "current_technologies": state.get("current_technologies", [])
    }
    
    # Ensure maturity assessment exists
    maturity_assessment = state.get("maturity_assessment")
    if not maturity_assessment:
        logging.warning("No maturity assessment found. Running maturity assessment first.")
        updated_state = await assess_maturity(state)
        maturity_assessment = updated_state.get("maturity_assessment")
    
    # Initialize technology recommender
    technology_recommender = TechnologyRecommender()
    
    # Generate technology stack recommendation
    try:
        technology_stack = technology_recommender.recommend_technology_stack(
            company_info=company_info,
            maturity_assessment=maturity_assessment
        )
        logging.info("Generated technology stack recommendation with %d categories", 
                    len(technology_stack.categories))
    except Exception as e:
        logging.error("Error generating technology stack recommendation: %s", str(e))
        return state
    
    # Return updated state with technology stack
    return {**state, "technology_stack": technology_stack}


async def assess_organizational_readiness(state: Dict) -> Dict:
    """
    Assess the organization's readiness for digital transformation.
    
    Args:
        state: The current state.
    
    Returns:
        Updated state with organizational readiness assessment added.
    """
    # Initialize optional fields if they don't exist
    for field in ["transformation_aspects", "experts", "consultation_results", "recommendations"]:
        if field not in state:
            state[field] = []
    
    if "technology_stack" not in state:
        state["technology_stack"] = None
    
    company_info = state.get("company_information", {})
    company_name = company_info.get("company_name", "Unknown")
    maturity_assessment = state.get("maturity_assessment", {})
    technology_stack = state.get("technology_stack", None)
    
    logging.info(f"Starting organizational readiness assessment for {company_name}")
    
    # Perform the organizational readiness assessment
    assessor = ReadinessAssessor(model="gpt-4-turbo")
    readiness_assessment = assessor.assess_organization(
        company_info=company_info,
        maturity_assessment=maturity_assessment,
        technology_stack=technology_stack
    )
    
    logging.info(f"Completed organizational readiness assessment with score: {readiness_assessment.overall_readiness_score:.2f}")
    
    # Update the state with the assessment results
    state["organizational_readiness"] = readiness_assessment
    
    return state


def create_main_graph():
    """
    Create the main digital transformation graph.
    
    Returns:
        The LangGraph workflow for digital transformation.
    """
    # Create a new graph
    builder = StateGraph(DigitalTransformationState)
    
    # Add nodes for each step with retry policies
    builder.add_node("assess_maturity", assess_maturity, retry=RetryPolicy(max_attempts=3))
    builder.add_node("initialize_analysis", initialize_analysis, retry=RetryPolicy(max_attempts=3))
    builder.add_node("generate_experts", generate_experts, retry=RetryPolicy(max_attempts=3))
    builder.add_node("conduct_interviews", conduct_interviews, retry=RetryPolicy(max_attempts=3))
    builder.add_node("generate_recommendations", generate_recommendations, retry=RetryPolicy(max_attempts=3))
    builder.add_node("create_transformation_plan", create_transformation_plan, retry=RetryPolicy(max_attempts=3))
    builder.add_node("recommend_technology_stack", recommend_technology_stack, retry=RetryPolicy(max_attempts=3))
    builder.add_node("assess_organizational_readiness", assess_organizational_readiness, retry=RetryPolicy(max_attempts=3))
    
    # Define the edges (connections between nodes)
    builder.add_edge(START, "assess_maturity")
    builder.add_edge("assess_maturity", "initialize_analysis")
    builder.add_edge("initialize_analysis", "generate_experts")
    builder.add_edge("generate_experts", "conduct_interviews")
    builder.add_edge("conduct_interviews", "generate_recommendations")
    builder.add_edge("generate_recommendations", "create_transformation_plan")
    builder.add_edge("create_transformation_plan", "recommend_technology_stack")
    builder.add_edge("recommend_technology_stack", "assess_organizational_readiness")
    builder.add_edge("assess_organizational_readiness", END)
    
    # Compile the graph with memory checkpointer
    return builder.compile(checkpointer=MemorySaver())


# Create and export the main graph
digital_transformation_graph = create_main_graph()

# Define the state schema
class DigitalTransformationState(TypedDict, total=False):
    """State for the digital transformation graph."""
    # Required fields
    company_information: dict  # Company information
    
    # Optional fields, using plain types as State doesn't handle well with Annotated
    maturity_assessment: Optional[dict]  # Results from maturity assessment
    transformation_aspects: Optional[List[dict]]  # Aspects to transform
    experts: Optional[List[str]]  # Expert role(s) to consult
    consultation_results: Optional[List[dict]]  # Results from expert consultation
    recommendations: Optional[List[dict]]  # Final transformation recommendations
    transformation_plan: Optional[dict]  # Transformation plan 
    technology_stack: Optional[TechnologyStack]  # Technology stack recommendations
    organizational_readiness: Optional[OrganizationalReadinessAssessment]  # Organizational readiness assessment 