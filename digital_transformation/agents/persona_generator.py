from typing import List

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

from digital_transformation.schema.state import DomainExpert, TransformationAspect


class ExpertList(BaseModel):
    """List of domain experts for digital transformation consultation."""
    experts: List[DomainExpert] = Field(..., description="List of domain experts")


class PersonaGenerator:
    """Generator for digital transformation expert personas."""
    
    def __init__(self, model_name: str = "gpt-4o-mini"):
        self.llm = ChatOpenAI(model=model_name, temperature=0.5)
    
    async def generate_experts(
        self, 
        company_info: dict, 
        transformation_aspects: List[TransformationAspect],
        num_experts: int = 5
    ) -> List[DomainExpert]:
        """
        Generate digital transformation expert personas based on company context.
        
        Args:
            company_info: Dictionary with company information
            transformation_aspects: List of transformation aspects to be addressed
            num_experts: Number of experts to generate
            
        Returns:
            List of DomainExpert personas
        """
        # Create a comprehensive prompt for the LLM
        aspects_text = "\n".join([
            f"- {aspect.aspect_title}: {aspect.description}" 
            for aspect in transformation_aspects
        ])
        
        # Create the prompt template
        prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                """You are tasked with creating diverse digital transformation expert personas 
who can provide valuable insights for a company's transformation journey.
Each expert should have a unique area of expertise covering different aspects of digital transformation.

Create experts with the following traits:
1. A distinctive name that reflects their professional background
2. A specific area of expertise (e.g., cloud migration, AI integration, change management)
3. A professional role that aligns with their expertise
4. A detailed description of their background, perspective, and approach to digital transformation

Consider the company's industry, challenges, and transformation goals when creating these experts.
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

Transformation Aspects to Address:
{aspects}

Please generate {num_experts} digital transformation expert personas that would be most helpful 
for this company's transformation journey. Each should offer a unique perspective and expertise.
"""
            )
        ])
        
        # Extract context from company_info
        context = {
            "company_name": company_info.get("company_name", ""),
            "industry": company_info.get("industry", ""),
            "company_description": company_info.get("company_description", ""),
            "business_challenges": ", ".join(company_info.get("business_challenges", [])),
            "current_technologies": ", ".join(company_info.get("current_technologies", [])),
            "transformation_goals": ", ".join(company_info.get("transformation_goals", [])),
            "aspects": aspects_text,
            "num_experts": num_experts
        }
        
        # Create structured output for the experts
        response = await self.llm.with_structured_output(ExpertList).ainvoke(prompt.format(**context))
        
        return response.experts


# Create a singleton instance
persona_generator = PersonaGenerator() 