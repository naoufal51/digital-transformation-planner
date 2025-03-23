from typing import List, Dict, Any

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from digital_transformation.schema.state import Recommendation, TransformationPlan


class PlanGenerator:
    """Generator for comprehensive digital transformation plans."""
    
    def __init__(self, model_name: str = "gpt-4o"):
        self.llm = ChatOpenAI(model=model_name, temperature=0.3)
    
    def _format_recommendations(self, recommendations: List[Recommendation]) -> str:
        """Format the recommendations for the prompt."""
        return "\n\n".join([
            f"## {rec.title}\n"
            f"Details: {rec.details}\n"
            f"Rationale: {rec.rationale}\n"
            f"Implementation Steps: {', '.join(rec.implementation_steps)}\n"
            f"Impact: {rec.estimated_impact}\n"
            f"Effort: {rec.estimated_effort}\n"
            f"Priority: {rec.priority}"
            for rec in recommendations
        ])
    
    async def generate_plan(
        self, 
        company_info: Dict[str, Any],
        recommendations: List[Recommendation]
    ) -> TransformationPlan:
        """
        Generate a comprehensive digital transformation plan.
        
        Args:
            company_info: Dictionary with company information
            recommendations: List of recommendations
            
        Returns:
            Comprehensive transformation plan
        """
        # Format the recommendations
        formatted_recs = self._format_recommendations(recommendations)
        
        # Create the prompt
        prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                """You are a digital transformation strategist creating a comprehensive transformation plan for a company.
Based on the company information and recommendations provided, create a detailed transformation plan.

Your plan should include:
1. A compelling title for the transformation plan
2. An executive summary that outlines the key points and expected outcomes
3. Business context that frames the transformation within the company's goals and challenges
4. The prioritized recommendations (these will be provided to you)
5. An implementation roadmap showing the phased approach for executing the recommendations
6. Success metrics to measure the effectiveness of the transformation

The plan should be strategic, practical, and tailored to the company's specific situation.
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

Recommendations:
{recommendations}

Create a comprehensive digital transformation plan for this company.
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
            "recommendations": formatted_recs
        }
        
        # Generate the plan
        plan_output = await self.llm.with_structured_output(
            TransformationPlan
        ).ainvoke(prompt.format(**context))
        
        # For this plan, we want to keep the existing recommendations
        plan_output.recommendations = recommendations
        
        return plan_output


# Create singleton instance
plan_generator = PlanGenerator() 