from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class TechnologyOption(BaseModel):
    """Represents a technology option with details about features, cost, etc."""
    name: str = Field(..., description="Name of the technology")
    vendor: str = Field(..., description="Vendor or provider of the technology")
    description: str = Field(..., description="Description of the technology and its purpose")
    key_features: List[str] = Field(..., description="Key features of the technology")
    pros: List[str] = Field(..., description="Advantages of the technology")
    cons: List[str] = Field(..., description="Disadvantages or limitations of the technology")
    cost_range: str = Field(..., description="Estimated cost range (e.g., '$', '$$', '$$$')")
    implementation_complexity: str = Field(..., description="Complexity of implementation (Low/Medium/High)")
    integration_notes: str = Field(..., description="Notes on integration with existing systems")
    industry_fit_score: int = Field(..., description="Score from 1-10 indicating fit for the industry")
    url: Optional[str] = Field(None, description="URL for more information")


class TechnologyCategory(BaseModel):
    """Represents a category of technologies with options and recommendations"""
    name: str = Field(..., description="Name of the technology category")
    description: str = Field(..., description="Description of the technology category")
    relevance_score: int = Field(..., description="Score from 1-10 indicating relevance to the company")
    current_maturity: str = Field(..., description="Current maturity level in this category")
    target_maturity: str = Field(..., description="Target maturity level in this category")
    options: List[TechnologyOption] = Field(..., description="List of technology options in this category")
    recommendations: List[str] = Field(..., description="Specific recommendations for this category")


class TechnologyRoadmap(BaseModel):
    """Represents a phased implementation roadmap for recommended technologies"""
    phase_name: str = Field(..., description="Name of the implementation phase")
    timeline: str = Field(..., description="Timeline for this phase (e.g., 'Q1-Q2 2023')")
    technologies: List[str] = Field(..., description="Technologies to implement in this phase")
    dependencies: List[str] = Field(..., description="Dependencies for this phase")
    key_activities: List[str] = Field(..., description="Key activities in this phase")
    estimated_effort: str = Field(..., description="Estimated effort for this phase")


class TechnologyStack(BaseModel):
    """Represents the complete technology stack recommendation"""
    executive_summary: str = Field(..., description="Executive summary of the technology recommendations")
    business_context: str = Field(..., description="Business context and goals")
    categories: List[TechnologyCategory] = Field(..., description="List of technology categories")
    roadmap: List[TechnologyRoadmap] = Field(..., description="Implementation roadmap")
    total_cost_estimate: str = Field(..., description="Total estimated cost range")
    implementation_timeframe: str = Field(..., description="Overall implementation timeframe")
    key_considerations: List[str] = Field(..., description="Key considerations for implementation")
    risk_factors: List[Dict[str, str]] = Field(..., description="Risk factors and mitigation strategies")
    
    @property
    def as_str(self) -> str:
        """Return a markdown representation of the technology stack"""
        categories_md = "\n\n".join([
            f"## {cat.name} (Relevance: {cat.relevance_score}/10)\n\n"
            f"{cat.description}\n\n"
            f"**Current Maturity:** {cat.current_maturity}\n"
            f"**Target Maturity:** {cat.target_maturity}\n\n"
            f"### Recommended Technologies:\n\n" +
            "\n\n".join([
                f"#### {opt.name} ({opt.vendor})\n\n"
                f"{opt.description}\n\n"
                f"**Key Features:**\n" + "\n".join([f"- {feature}" for feature in opt.key_features]) + "\n\n"
                f"**Pros:**\n" + "\n".join([f"- {pro}" for pro in opt.pros]) + "\n\n"
                f"**Cons:**\n" + "\n".join([f"- {con}" for con in opt.cons]) + "\n\n"
                f"**Cost:** {opt.cost_range} | **Complexity:** {opt.implementation_complexity} | **Industry Fit:** {opt.industry_fit_score}/10\n\n"
                f"**Integration Notes:** {opt.integration_notes}"
                for opt in cat.options[:3]  # Limit to top 3 options
            ]) +
            "\n\n**Recommendations:**\n" + "\n".join([f"- {rec}" for rec in cat.recommendations])
            for cat in self.categories
        ])
        
        roadmap_md = "\n\n".join([
            f"### Phase: {phase.phase_name} ({phase.timeline})\n\n"
            f"**Technologies:** {', '.join(phase.technologies)}\n\n"
            f"**Key Activities:**\n" + "\n".join([f"- {activity}" for activity in phase.key_activities]) + "\n\n"
            f"**Dependencies:** {', '.join(phase.dependencies)}\n\n"
            f"**Estimated Effort:** {phase.estimated_effort}"
            for phase in self.roadmap
        ])
        
        risks_md = "\n".join([
            f"- **{risk.get('risk', 'Risk')}**: {risk.get('mitigation', 'No mitigation strategy provided')}"
            for risk in self.risk_factors
        ])
        
        return (f"# Technology Stack Recommendations\n\n"
                f"## Executive Summary\n\n{self.executive_summary}\n\n"
                f"## Business Context\n\n{self.business_context}\n\n"
                f"# Technology Categories\n\n{categories_md}\n\n"
                f"# Implementation Roadmap\n\n{roadmap_md}\n\n"
                f"## Total Cost Estimate\n\n{self.total_cost_estimate}\n\n"
                f"## Implementation Timeframe\n\n{self.implementation_timeframe}\n\n"
                f"## Key Considerations\n\n" + "\n".join([f"- {consideration}" for consideration in self.key_considerations]) + "\n\n"
                f"## Risk Factors\n\n{risks_md}") 