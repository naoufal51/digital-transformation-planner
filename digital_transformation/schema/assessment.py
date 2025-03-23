from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class MaturityDimension(BaseModel):
    """A dimension of digital maturity assessment"""
    name: str = Field(..., description="Name of the maturity dimension")
    description: str = Field(..., description="Description of what this dimension measures")
    current_score: float = Field(..., description="Current score from 1-5")
    target_score: float = Field(..., description="Target score from 1-5")
    industry_benchmark: float = Field(..., description="Industry benchmark score")
    gap: float = Field(..., description="Gap between current and target scores")
    improvement_areas: List[str] = Field(..., description="Areas to improve to reach target")


class MaturityAssessment(BaseModel):
    """Complete maturity assessment results"""
    overall_score: float = Field(..., description="Overall maturity score from 1-5")
    industry_average: float = Field(..., description="Industry average maturity score")
    dimensions: List[MaturityDimension] = Field(..., description="Individual maturity dimensions")
    top_strengths: List[str] = Field(..., description="Top strengths identified")
    top_gaps: List[str] = Field(..., description="Top gaps or weaknesses identified")
    maturity_level: str = Field(..., description="Overall maturity level (e.g., 'Initial', 'Developing', 'Advanced')")
    
    @property
    def as_str(self) -> str:
        dimension_sections = "\n\n".join([
            f"## {dim.name}\n\n{dim.description}\n\n"
            f"Current Score: {dim.current_score:.1f}/5.0 | Target: {dim.target_score:.1f}/5.0 | "
            f"Industry Benchmark: {dim.industry_benchmark:.1f}/5.0\n\n"
            f"Gap: {dim.gap:.1f} points\n\n"
            f"Improvement Areas:\n" + "\n".join([f"- {area}" for area in dim.improvement_areas])
            for dim in self.dimensions
        ])
        
        strengths = "\n".join([f"- {strength}" for strength in self.top_strengths])
        gaps = "\n".join([f"- {gap}" for gap in self.top_gaps])
        
        return (f"# Digital Transformation Maturity Assessment\n\n"
                f"## Overall Maturity: {self.maturity_level}\n\n"
                f"Overall Score: {self.overall_score:.1f}/5.0 | Industry Average: {self.industry_average:.1f}/5.0\n\n"
                f"## Top Strengths\n\n{strengths}\n\n"
                f"## Top Gaps\n\n{gaps}\n\n"
                f"# Detailed Dimension Analysis\n\n{dimension_sections}")


class AssessmentQuestion(BaseModel):
    """A question used in the maturity assessment"""
    id: str = Field(..., description="Unique identifier for the question")
    dimension: str = Field(..., description="The maturity dimension this question evaluates")
    text: str = Field(..., description="The text of the question")
    help_text: Optional[str] = Field(None, description="Optional help text explaining the question")
    weight: float = Field(1.0, description="Weight of this question in the dimension score calculation")


class IndustryBenchmark(BaseModel):
    """Industry benchmark data for maturity assessment"""
    industry: str = Field(..., description="Industry name")
    overall_average: float = Field(..., description="Overall average maturity across all dimensions")
    dimension_averages: Dict[str, float] = Field(..., description="Average scores by dimension")
    maturity_distribution: Dict[str, float] = Field(..., description="Distribution of companies across maturity levels") 