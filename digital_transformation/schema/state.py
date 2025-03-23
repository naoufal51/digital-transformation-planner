from typing import Annotated, Dict, List, Optional, TypedDict

from langchain_core.messages import AnyMessage
from pydantic import BaseModel, Field

from digital_transformation.schema.assessment import MaturityAssessment
from digital_transformation.schema.technology import TechnologyStack


# Helper functions for merging state
def add_messages(left, right):
    if not isinstance(left, list):
        left = [left]
    if not isinstance(right, list):
        right = [right]
    return left + right


def update_references(references, new_references):
    if not references:
        references = {}
    references.update(new_references)
    return references


def update_entity(entity, new_entity):
    # Can only set at the outset
    if not entity:
        return new_entity
    return entity


# Pydantic models for structured data
class DomainExpert(BaseModel):
    """Domain expert persona with area of expertise in digital transformation"""
    name: str = Field(..., description="Name of the domain expert")
    expertise_area: str = Field(..., description="Primary area of expertise in digital transformation")
    role: str = Field(..., description="Role of the domain expert in the digital transformation process")
    description: str = Field(..., description="Description of the expert's background and perspective")
    
    @property
    def persona(self) -> str:
        return f"Name: {self.name}\nRole: {self.role}\nExpertise Area: {self.expertise_area}\nDescription: {self.description}\n"


class TransformationAspect(BaseModel):
    """Aspect or component of digital transformation to be addressed"""
    aspect_title: str = Field(..., description="Title of the transformation aspect")
    description: str = Field(..., description="Description of the transformation aspect")
    

class Recommendation(BaseModel):
    """Specific recommendation for digital transformation"""
    title: str = Field(..., description="Title of the recommendation")
    details: str = Field(..., description="Detailed explanation of the recommendation")
    rationale: str = Field(..., description="Rationale behind the recommendation")
    implementation_steps: List[str] = Field(..., description="Steps to implement the recommendation")
    estimated_impact: str = Field(..., description="Estimated impact of the recommendation")
    estimated_effort: str = Field(..., description="Estimated effort required to implement")
    priority: str = Field(..., description="Priority level (High/Medium/Low)")
    references: Optional[List[str]] = Field(default=None, description="References or sources")


class TransformationPlan(BaseModel):
    """Overall plan for digital transformation"""
    title: str = Field(..., description="Title of the transformation plan")
    executive_summary: str = Field(..., description="Executive summary of the plan")
    business_context: str = Field(..., description="Business context and goals")
    recommendations: List[Recommendation] = Field(..., description="List of recommendations")
    implementation_roadmap: str = Field(..., description="High-level implementation roadmap")
    success_metrics: List[str] = Field(..., description="Metrics to measure success")
    
    @property
    def as_str(self) -> str:
        rec_sections = "\n\n".join([
            f"## {rec.title}\n\n{rec.details}\n\nRationale: {rec.rationale}\n\n"
            f"Priority: {rec.priority} | Impact: {rec.estimated_impact} | Effort: {rec.estimated_effort}\n\n"
            f"Implementation Steps:\n" + "\n".join([f"- {step}" for step in rec.implementation_steps])
            for rec in self.recommendations
        ])
        
        return (f"# {self.title}\n\n## Executive Summary\n\n{self.executive_summary}\n\n"
                f"## Business Context\n\n{self.business_context}\n\n"
                f"# Recommendations\n\n{rec_sections}\n\n"
                f"## Implementation Roadmap\n\n{self.implementation_roadmap}\n\n"
                f"## Success Metrics\n\n" + "\n".join([f"- {metric}" for metric in self.success_metrics]))


# State TypedDicts for LangGraph
class ConsultationState(TypedDict):
    """State for the expert consultation process"""
    messages: Annotated[List[AnyMessage], add_messages]
    references: Annotated[Optional[Dict], update_references]
    expert: Annotated[Optional[DomainExpert], update_entity]
    company_context: Optional[Dict]


class DigitalTransformationState(TypedDict):
    """The overall state for the digital transformation planning process"""
    company_name: str
    company_description: str
    industry: str
    transformation_goals: List[str]
    business_challenges: List[str]
    current_technologies: List[str]
    maturity_assessment: Optional[MaturityAssessment]
    technology_stack: Optional[TechnologyStack]
    transformation_aspects: List[TransformationAspect]
    experts: List[DomainExpert]
    consultation_results: List[ConsultationState]
    recommendations: List[Recommendation]
    transformation_plan: Optional[TransformationPlan] 