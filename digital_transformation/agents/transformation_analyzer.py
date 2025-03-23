from typing import List, Dict, Any

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

from digital_transformation.schema.state import TransformationAspect


class AspectList(BaseModel):
    """List of transformation aspects identified for a company."""
    aspects: List[TransformationAspect] = Field(..., description="List of transformation aspects")


class TransformationAnalyzer:
    """Analyzer for identifying key digital transformation aspects."""
    
    def __init__(self, model_name: str = "gpt-4o-mini"):
        self.llm = ChatOpenAI(model=model_name, temperature=0.3)
    
    async def identify_aspects(
        self, 
        company_info: Dict[str, Any],
        num_aspects: int = 6
    ) -> List[TransformationAspect]:
        """
        Identify key digital transformation aspects for a company.
        
        Args:
            company_info: Dictionary with company information
            num_aspects: Number of aspects to identify
            
        Returns:
            List of identified transformation aspects
        """
        # Create the prompt
        prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                """You are a digital transformation strategist analyzing a company to identify key areas for transformation.
Based on the company information provided, identify the most important aspects or components of digital transformation
that need to be addressed for this specific company.

For each aspect:
1. Create a clear, descriptive title that identifies the transformation area
2. Provide a detailed description that explains why this aspect is important for the company's transformation journey
   and what it should encompass

Focus on a mix of technological, operational, and cultural aspects as appropriate for the company's context.
Consider the company's industry, challenges, goals, and current technology state when identifying these aspects.
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

Identify the {num_aspects} most important digital transformation aspects for this company to focus on.
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
            "num_aspects": num_aspects
        }
        
        # Generate the aspects
        response = await self.llm.with_structured_output(AspectList).ainvoke(prompt.format(**context))
        
        return response.aspects


# Create singleton instance
transformation_analyzer = TransformationAnalyzer() 