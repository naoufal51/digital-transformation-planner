from typing import List, Dict, Any

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage
from pydantic import BaseModel, Field

from digital_transformation.schema.state import Recommendation, ConsultationState


class RecommendationList(BaseModel):
    """List of recommendations for digital transformation."""
    recommendations: List[Recommendation] = Field(..., description="List of digital transformation recommendations")


class RecommendationGenerator:
    """Generator for digital transformation recommendations."""
    
    def __init__(self, model_name: str = "gpt-4o"):
        self.llm = ChatOpenAI(model=model_name, temperature=0.3)
    
    def _format_conversation(self, interview_state: ConsultationState) -> str:
        """Format the conversation for the prompt."""
        messages = interview_state["messages"]
        expert = interview_state["expert"]
        
        convo = "\n".join([
            f"{m.name}: {m.content}" for m in messages
        ])
        
        return f"""Conversation with {expert.name} (Expert in {expert.expertise_area}):
{convo}
"""
    
    async def generate_recommendations(
        self, 
        company_info: Dict[str, Any],
        interview_results: List[ConsultationState]
    ) -> List[Recommendation]:
        """
        Generate recommendations based on expert interviews.
        
        Args:
            company_info: Dictionary with company information
            interview_results: Results from expert interviews
            
        Returns:
            List of recommendations
        """
        # Format all conversations
        all_interviews = "\n\n".join([
            self._format_conversation(interview) 
            for interview in interview_results
        ])
        
        # Create the prompt
        prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                """You are a digital transformation strategist creating actionable recommendations for a company.
Based on the expert interviews provided, identify the most valuable opportunities for digital transformation.

For each recommendation:
1. Create a clear, concise title
2. Provide detailed explanation of what should be implemented
3. Explain the rationale behind this recommendation
4. List concrete implementation steps
5. Estimate the impact (High/Medium/Low and why)
6. Estimate the implementation effort (High/Medium/Low and why)
7. Assign a priority level (High/Medium/Low)

Focus on actionable, specific recommendations that address the company's goals and challenges.
Ensure recommendations are backed by insights from the expert interviews.
"""
            ),
            (
                "user",
                """Company Information:
Company: {company_name}
Industry: {industry}
Description: {company_description}
Current Challenges: {business_challenges}
Current Technologies: {current_technologies}
Transformation Goals: {transformation_goals}

Expert Interviews:
{interviews}

Based on these expert interviews, generate specific, actionable recommendations for this company's digital transformation.
"""
            )
        ])
        
        # Extract context
        context = {
            "company_name": company_info.get("company_name", ""),
            "industry": company_info.get("industry", ""),
            "company_description": company_info.get("company_description", ""),
            "business_challenges": ", ".join(company_info.get("business_challenges", [])),
            "current_technologies": ", ".join(company_info.get("current_technologies", [])),
            "transformation_goals": ", ".join(company_info.get("transformation_goals", [])),
            "interviews": all_interviews
        }
        
        # Generate the recommendations
        response = await self.llm.with_structured_output(RecommendationList).ainvoke(prompt.format(**context))
        
        return response.recommendations


# Create singleton instance
recommendation_generator = RecommendationGenerator() 