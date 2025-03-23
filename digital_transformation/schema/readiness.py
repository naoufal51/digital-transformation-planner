from typing import Dict, List, Optional, Union
from pydantic import BaseModel, Field


class SkillGap(BaseModel):
    """Represents a skill gap identified in the organization."""
    skill_area: str = Field(..., description="The area or domain of the skill")
    current_proficiency: float = Field(..., description="Current proficiency level (0-1)")
    required_proficiency: float = Field(..., description="Required proficiency level for successful transformation (0-1)")
    gap_score: float = Field(..., description="The gap between current and required proficiency")
    impact_level: str = Field(..., description="High/Medium/Low impact on transformation success")
    affected_roles: List[str] = Field(..., description="Job roles affected by this skill gap")
    training_recommendations: List[str] = Field(..., description="Recommended training interventions")


class CulturalFactor(BaseModel):
    """Represents a cultural factor affecting digital transformation readiness."""
    factor_name: str = Field(..., description="Name of the cultural factor")
    current_state: str = Field(..., description="Description of the current state")
    target_state: str = Field(..., description="Description of the desired state")
    alignment_score: float = Field(..., description="How aligned current culture is with digital transformation needs (0-1)")
    improvement_strategies: List[str] = Field(..., description="Strategies to improve this cultural factor")
    potential_barriers: List[str] = Field(..., description="Potential barriers to changing this cultural factor")


class ChangeReadinessMetric(BaseModel):
    """Represents a metric measuring the organization's readiness for change."""
    metric_name: str = Field(..., description="Name of the readiness metric")
    score: float = Field(..., description="Score between 0-1")
    interpretation: str = Field(..., description="Interpretation of the score")
    risk_level: str = Field(..., description="High/Medium/Low risk level")
    improvement_actions: List[str] = Field(..., description="Actions to improve this metric")


class TrainingNeed(BaseModel):
    """Represents a specific training need for the organization."""
    topic: str = Field(..., description="Training topic")
    priority: str = Field(..., description="High/Medium/Low priority")
    target_audience: List[str] = Field(..., description="Roles or departments that need this training")
    delivery_methods: List[str] = Field(..., description="Recommended delivery methods")
    estimated_duration: str = Field(..., description="Estimated duration of training")
    prerequisites: List[str] = Field(default_factory=list, description="Prerequisites for this training")
    expected_outcomes: List[str] = Field(..., description="Expected outcomes from this training")
    alignment_with_technology: List[str] = Field(..., description="How this training aligns with recommended technologies")


class LeadershipReadiness(BaseModel):
    """Assesses leadership readiness for digital transformation."""
    vision_clarity: float = Field(..., description="How clear leadership's vision for digital transformation is (0-1)")
    commitment_level: float = Field(..., description="Level of leadership commitment to transformation (0-1)")
    digital_fluency: float = Field(..., description="Leadership's understanding of digital concepts (0-1)")
    change_management_capability: float = Field(..., description="Leadership's change management capability (0-1)")
    strengths: List[str] = Field(..., description="Leadership strengths for digital transformation")
    development_areas: List[str] = Field(..., description="Areas where leadership needs development")
    recommendations: List[str] = Field(..., description="Recommendations for leadership development")


class OrganizationalReadinessAssessment(BaseModel):
    """Comprehensive assessment of an organization's readiness for digital transformation."""
    executive_summary: str = Field(..., description="Executive summary of readiness assessment")
    overall_readiness_score: float = Field(..., description="Overall readiness score (0-1)")
    skill_gaps: List[SkillGap] = Field(..., description="Identified skill gaps")
    cultural_factors: List[CulturalFactor] = Field(..., description="Cultural factors affecting readiness")
    change_readiness_metrics: List[ChangeReadinessMetric] = Field(..., description="Change readiness metrics")
    training_needs: List[TrainingNeed] = Field(..., description="Identified training needs")
    leadership_readiness: LeadershipReadiness = Field(..., description="Leadership readiness assessment")
    key_recommendations: List[str] = Field(..., description="Key recommendations to improve readiness")
    readiness_by_department: Dict[str, float] = Field(..., description="Readiness scores by department")
    priority_actions: List[str] = Field(..., description="Priority actions to take")
    timeline_for_readiness: str = Field(..., description="Estimated timeline to achieve sufficient readiness")
    
    def as_str(self) -> str:
        """Returns a markdown representation of the readiness assessment."""
        md = f"# Organizational Readiness Assessment\n\n"
        md += f"## Executive Summary\n{self.executive_summary}\n\n"
        md += f"## Overall Readiness Score: {self.overall_readiness_score:.2f} / 1.0\n\n"
        
        md += f"## Key Recommendations\n"
        for i, rec in enumerate(self.key_recommendations, 1):
            md += f"{i}. {rec}\n"
        md += "\n"
        
        md += f"## Readiness by Department\n"
        for dept, score in sorted(self.readiness_by_department.items(), key=lambda x: x[1], reverse=True):
            md += f"- **{dept}**: {score:.2f} / 1.0\n"
        md += "\n"
        
        md += f"## Leadership Readiness\n"
        md += f"- Vision Clarity: {self.leadership_readiness.vision_clarity:.2f} / 1.0\n"
        md += f"- Commitment Level: {self.leadership_readiness.commitment_level:.2f} / 1.0\n"
        md += f"- Digital Fluency: {self.leadership_readiness.digital_fluency:.2f} / 1.0\n"
        md += f"- Change Management Capability: {self.leadership_readiness.change_management_capability:.2f} / 1.0\n\n"
        
        md += f"### Leadership Strengths\n"
        for strength in self.leadership_readiness.strengths:
            md += f"- {strength}\n"
        md += "\n"
        
        md += f"### Leadership Development Areas\n"
        for area in self.leadership_readiness.development_areas:
            md += f"- {area}\n"
        md += "\n"
        
        md += f"## Top Skill Gaps\n"
        for gap in sorted(self.skill_gaps, key=lambda x: x.gap_score, reverse=True)[:5]:
            md += f"### {gap.skill_area} (Gap: {gap.gap_score:.2f})\n"
            md += f"- Current Proficiency: {gap.current_proficiency:.2f} / Required: {gap.required_proficiency:.2f}\n"
            md += f"- Impact Level: {gap.impact_level}\n"
            md += f"- Affected Roles: {', '.join(gap.affected_roles)}\n"
            md += f"- Training Recommendations: {', '.join(gap.training_recommendations)}\n\n"
        
        md += f"## Cultural Factors\n"
        for factor in sorted(self.cultural_factors, key=lambda x: x.alignment_score):
            md += f"### {factor.factor_name} (Alignment: {factor.alignment_score:.2f})\n"
            md += f"- Current State: {factor.current_state}\n"
            md += f"- Target State: {factor.target_state}\n"
            md += f"- Improvement Strategies: {', '.join(factor.improvement_strategies)}\n\n"
        
        md += f"## Priority Training Needs\n"
        high_priority = [t for t in self.training_needs if t.priority == "High"]
        for training in high_priority:
            md += f"### {training.topic} (Priority: {training.priority})\n"
            md += f"- Target Audience: {', '.join(training.target_audience)}\n"
            md += f"- Delivery Methods: {', '.join(training.delivery_methods)}\n"
            md += f"- Duration: {training.estimated_duration}\n"
            md += f"- Expected Outcomes: {', '.join(training.expected_outcomes)}\n\n"
        
        md += f"## Timeline for Readiness\n{self.timeline_for_readiness}\n\n"
        
        md += f"## Priority Actions\n"
        for i, action in enumerate(self.priority_actions, 1):
            md += f"{i}. {action}\n"
        
        return md 