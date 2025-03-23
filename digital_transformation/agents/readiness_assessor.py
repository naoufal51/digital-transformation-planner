import logging
from typing import Dict, List, Optional, Any
import uuid

from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from digital_transformation.schema.readiness import (
    OrganizationalReadinessAssessment,
    SkillGap,
    CulturalFactor,
    ChangeReadinessMetric,
    TrainingNeed,
    LeadershipReadiness,
)

logger = logging.getLogger(__name__)

class ReadinessAssessor:
    """
    Agent for assessing organizational readiness for digital transformation.
    """
    
    def __init__(self, model: str = "gpt-4-turbo"):
        self.model = model
        self.llm = ChatOpenAI(model=model, temperature=0.2)
        logger.info(f"ReadinessAssessor initialized with model: {model}")
        
    def _extract_from_company_info(self, company_info: Dict[str, Any]) -> Dict[str, Any]:
        """Extract relevant information from company data."""
        size = company_info.get("size", "Unknown")
        industry = company_info.get("industry", "Unknown")
        maturity = company_info.get("maturity", {})
        org_structure = company_info.get("organizational_structure", "Unknown")
        tech_stack = company_info.get("current_tech_stack", [])
        challenges = company_info.get("challenges", [])
        
        return {
            "size": size,
            "industry": industry,
            "maturity": maturity,
            "org_structure": org_structure,
            "tech_stack": tech_stack,
            "challenges": challenges
        }
    
    def _assess_skill_gaps(self, company_info: Dict[str, Any], maturity_assessment: Dict[str, Any]) -> List[SkillGap]:
        """Assess skill gaps based on company info and maturity assessment."""
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert in digital transformation and organizational development. 
            Your task is to identify skill gaps within an organization based on their company information and digital maturity assessment.
            
            Analyze the company information and maturity assessment to identify the key skill gaps that could impede their digital transformation.
            
            For each skill gap, provide:
            1. The skill area
            2. Current proficiency level (0-1 scale)
            3. Required proficiency level (0-1 scale)
            4. Gap score (difference between required and current)
            5. Impact level (High/Medium/Low)
            6. Affected roles
            7. Training recommendations
            
            Return the response as a JSON list of skill gaps, properly formatted according to the SkillGap schema.
            """),
            ("human", """Company Information: {company_info}
            
            Maturity Assessment: {maturity_assessment}
            
            Identify the skill gaps for this organization.""")
        ])
        
        response = self.llm.invoke(prompt.format_messages(
            company_info=company_info,
            maturity_assessment=maturity_assessment
        ))
        
        logger.info(f"Generated skill gaps assessment")
        # Process the response to create SkillGap objects
        try:
            from langchain_core.output_parsers import JsonOutputParser
            parser = JsonOutputParser()
            skill_gaps_data = parser.parse(response.content)
            skill_gaps = []
            for gap_data in skill_gaps_data:
                skill_gaps.append(SkillGap(**gap_data))
            return skill_gaps
        except Exception as e:
            logger.error(f"Error parsing skill gaps: {str(e)}")
            # Return a minimal set of skill gaps if parsing fails
            return [
                SkillGap(
                    skill_area="Digital Literacy",
                    current_proficiency=0.4,
                    required_proficiency=0.8,
                    gap_score=0.4,
                    impact_level="High",
                    affected_roles=["All Staff"],
                    training_recommendations=["Basic Digital Skills Training"]
                )
            ]
    
    def _assess_cultural_factors(self, company_info: Dict[str, Any], maturity_assessment: Dict[str, Any]) -> List[CulturalFactor]:
        """Assess cultural factors affecting readiness."""
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert in organizational culture and digital transformation. 
            Your task is to identify cultural factors that will affect an organization's readiness for digital transformation.
            
            Analyze the company information and maturity assessment to identify key cultural factors.
            
            For each cultural factor, provide:
            1. Factor name
            2. Current state
            3. Target state
            4. Alignment score (0-1, how aligned current culture is with digital transformation needs)
            5. Improvement strategies
            6. Potential barriers
            
            Return the response as a JSON list of cultural factors, properly formatted according to the CulturalFactor schema.
            """),
            ("human", """Company Information: {company_info}
            
            Maturity Assessment: {maturity_assessment}
            
            Identify the cultural factors affecting this organization's digital transformation readiness.""")
        ])
        
        response = self.llm.invoke(prompt.format_messages(
            company_info=company_info,
            maturity_assessment=maturity_assessment
        ))
        
        logger.info(f"Generated cultural factors assessment")
        # Process the response to create CulturalFactor objects
        try:
            from langchain_core.output_parsers import JsonOutputParser
            parser = JsonOutputParser()
            cultural_factors_data = parser.parse(response.content)
            cultural_factors = []
            for factor_data in cultural_factors_data:
                cultural_factors.append(CulturalFactor(**factor_data))
            return cultural_factors
        except Exception as e:
            logger.error(f"Error parsing cultural factors: {str(e)}")
            # Return a minimal set if parsing fails
            return [
                CulturalFactor(
                    factor_name="Change Resistance",
                    current_state="High resistance to change",
                    target_state="Embracing continuous improvement",
                    alignment_score=0.3,
                    improvement_strategies=["Change Management Program"],
                    potential_barriers=["Long-tenured employees"]
                )
            ]
    
    def _assess_change_readiness(self, company_info: Dict[str, Any]) -> List[ChangeReadinessMetric]:
        """Assess change readiness metrics."""
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert in change management and digital transformation. 
            Your task is to assess an organization's readiness for change based on their company information.
            
            For each change readiness metric, provide:
            1. Metric name
            2. Score (0-1)
            3. Interpretation
            4. Risk level (High/Medium/Low)
            5. Improvement actions
            
            Return the response as a JSON list of change readiness metrics, properly formatted according to the ChangeReadinessMetric schema.
            """),
            ("human", """Company Information: {company_info}
            
            Assess this organization's readiness for change.""")
        ])
        
        response = self.llm.invoke(prompt.format_messages(
            company_info=company_info
        ))
        
        logger.info(f"Generated change readiness assessment")
        # Process the response to create ChangeReadinessMetric objects
        try:
            from langchain_core.output_parsers import JsonOutputParser
            parser = JsonOutputParser()
            metrics_data = parser.parse(response.content)
            metrics = []
            for metric_data in metrics_data:
                metrics.append(ChangeReadinessMetric(**metric_data))
            return metrics
        except Exception as e:
            logger.error(f"Error parsing change readiness metrics: {str(e)}")
            # Return a minimal set if parsing fails
            return [
                ChangeReadinessMetric(
                    metric_name="Leadership Sponsorship",
                    score=0.6,
                    interpretation="Moderate leadership support",
                    risk_level="Medium",
                    improvement_actions=["Executive alignment workshop"]
                )
            ]
    
    def _identify_training_needs(self, skill_gaps: List[SkillGap], tech_stack: Dict[str, Any]) -> List[TrainingNeed]:
        """Identify training needs based on skill gaps and technology stack."""
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert in learning and development for digital transformation. 
            Your task is to identify specific training needs based on identified skill gaps and the planned technology stack.
            
            For each training need, provide:
            1. Topic
            2. Priority (High/Medium/Low)
            3. Target audience (roles or departments)
            4. Delivery methods
            5. Estimated duration
            6. Prerequisites (if any)
            7. Expected outcomes
            8. Alignment with technology
            
            Return the response as a JSON list of training needs, properly formatted according to the TrainingNeed schema.
            """),
            ("human", """Skill Gaps: {skill_gaps}
            
            Technology Stack: {tech_stack}
            
            Identify the specific training needs for this organization.""")
        ])
        
        response = self.llm.invoke(prompt.format_messages(
            skill_gaps=skill_gaps,
            tech_stack=tech_stack
        ))
        
        logger.info(f"Generated training needs assessment")
        # Process the response to create TrainingNeed objects
        try:
            from langchain_core.output_parsers import JsonOutputParser
            parser = JsonOutputParser()
            training_needs_data = parser.parse(response.content)
            training_needs = []
            for need_data in training_needs_data:
                training_needs.append(TrainingNeed(**need_data))
            return training_needs
        except Exception as e:
            logger.error(f"Error parsing training needs: {str(e)}")
            # Return a minimal set if parsing fails
            return [
                TrainingNeed(
                    topic="Digital Basics",
                    priority="High",
                    target_audience=["All Staff"],
                    delivery_methods=["Online Course", "Workshops"],
                    estimated_duration="4 weeks",
                    prerequisites=[],
                    expected_outcomes=["Basic digital literacy"],
                    alignment_with_technology=["Core Systems"]
                )
            ]
    
    def _assess_leadership_readiness(self, company_info: Dict[str, Any], maturity_assessment: Dict[str, Any]) -> LeadershipReadiness:
        """Assess leadership readiness for digital transformation."""
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert in leadership development and digital transformation. 
            Your task is to assess an organization's leadership readiness for digital transformation.
            
            Provide an assessment that includes:
            1. Vision clarity score (0-1)
            2. Commitment level (0-1)
            3. Digital fluency (0-1)
            4. Change management capability (0-1)
            5. Strengths
            6. Development areas
            7. Recommendations
            
            Return the response as a JSON object, properly formatted according to the LeadershipReadiness schema.
            """),
            ("human", """Company Information: {company_info}
            
            Maturity Assessment: {maturity_assessment}
            
            Assess this organization's leadership readiness for digital transformation.""")
        ])
        
        response = self.llm.invoke(prompt.format_messages(
            company_info=company_info,
            maturity_assessment=maturity_assessment
        ))
        
        logger.info(f"Generated leadership readiness assessment")
        # Process the response to create LeadershipReadiness object
        try:
            from langchain_core.output_parsers import JsonOutputParser
            parser = JsonOutputParser()
            leadership_data = parser.parse(response.content)
            return LeadershipReadiness(**leadership_data)
        except Exception as e:
            logger.error(f"Error parsing leadership readiness: {str(e)}")
            # Return a default object if parsing fails
            return LeadershipReadiness(
                vision_clarity=0.5,
                commitment_level=0.6,
                digital_fluency=0.4,
                change_management_capability=0.5,
                strengths=["Business domain expertise"],
                development_areas=["Digital knowledge"],
                recommendations=["Digital leadership training"]
            )
    
    def _generate_department_readiness(self, company_info: Dict[str, Any], skill_gaps: List[SkillGap]) -> Dict[str, float]:
        """Generate readiness scores by department."""
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert in organizational development and digital transformation. 
            Your task is to assess the readiness of different departments for digital transformation.
            
            Analyze the company information and skill gaps to estimate readiness scores for each department.
            
            Return the response as a JSON object mapping department names to readiness scores (0-1).
            """),
            ("human", """Company Information: {company_info}
            
            Skill Gaps: {skill_gaps}
            
            Assess the readiness of each department for digital transformation.""")
        ])
        
        response = self.llm.invoke(prompt.format_messages(
            company_info=company_info,
            skill_gaps=skill_gaps
        ))
        
        logger.info(f"Generated department readiness assessment")
        # Process the response to create a dictionary of department readiness scores
        try:
            from langchain_core.output_parsers import JsonOutputParser
            parser = JsonOutputParser()
            readiness_data = parser.parse(response.content)
            return readiness_data
        except Exception as e:
            logger.error(f"Error parsing department readiness: {str(e)}")
            # Return a default dictionary if parsing fails
            return {
                "IT": 0.7,
                "Operations": 0.5,
                "Sales": 0.4,
                "HR": 0.3,
                "Finance": 0.5
            }
    
    def _generate_executive_summary(self, overall_score: float, key_findings: Dict[str, Any]) -> str:
        """Generate an executive summary of the readiness assessment."""
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert in digital transformation and organizational change. 
            Your task is to create a concise, insightful executive summary of an organization's readiness for digital transformation.
            
            The summary should cover:
            1. Overall readiness assessment
            2. Key strengths and gaps
            3. Critical focus areas
            4. Strategic importance of addressing readiness issues
            
            Write in a clear, executive-friendly style with actionable insights.
            """),
            ("human", """Overall Readiness Score: {overall_score}
            
            Key Findings: {key_findings}
            
            Create an executive summary of this organization's readiness for digital transformation.""")
        ])
        
        response = self.llm.invoke(prompt.format_messages(
            overall_score=overall_score,
            key_findings=key_findings
        ))
        
        logger.info(f"Generated executive summary")
        return response.content
    
    def _calculate_overall_readiness(self, assessments: Dict[str, Any]) -> float:
        """Calculate overall readiness score from various assessments."""
        # Extract scores from different components
        leadership_scores = [
            assessments["leadership_readiness"].vision_clarity,
            assessments["leadership_readiness"].commitment_level,
            assessments["leadership_readiness"].digital_fluency,
            assessments["leadership_readiness"].change_management_capability
        ]
        
        # Average leadership score
        leadership_score = sum(leadership_scores) / len(leadership_scores)
        
        # Average cultural alignment
        cultural_score = sum(cf.alignment_score for cf in assessments["cultural_factors"]) / len(assessments["cultural_factors"])
        
        # Average skill gap (inverted since higher gap = lower readiness)
        skill_gap_scores = [1 - gap.gap_score for gap in assessments["skill_gaps"]]
        skill_score = sum(skill_gap_scores) / len(skill_gap_scores)
        
        # Average change readiness
        change_score = sum(m.score for m in assessments["change_readiness"]) / len(assessments["change_readiness"])
        
        # Average department readiness
        dept_score = sum(assessments["readiness_by_department"].values()) / len(assessments["readiness_by_department"])
        
        # Calculate weighted average
        weights = {
            "leadership": 0.25,
            "cultural": 0.20,
            "skills": 0.20,
            "change": 0.15,
            "department": 0.20
        }
        
        overall_score = (
            weights["leadership"] * leadership_score +
            weights["cultural"] * cultural_score +
            weights["skills"] * skill_score +
            weights["change"] * change_score +
            weights["department"] * dept_score
        )
        
        # Ensure score is between 0 and 1
        return max(0.0, min(1.0, overall_score))
    
    def _generate_recommendations_and_timeline(self, assessments: Dict[str, Any]) -> Dict[str, Any]:
        """Generate recommendations and timeline based on all assessments."""
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert in digital transformation and change management. 
            Your task is to generate key recommendations and a timeline for an organization to improve its readiness for digital transformation.
            
            Based on the assessments, provide:
            1. A list of key recommendations (prioritized actions)
            2. A timeline for achieving sufficient readiness
            
            Return the response as a JSON object with 'key_recommendations' (list of strings) and 'timeline' (string).
            """),
            ("human", """Assessment Data: {assessments}
            
            Generate key recommendations and a timeline for improving this organization's readiness for digital transformation.""")
        ])
        
        response = self.llm.invoke(prompt.format_messages(
            assessments=assessments
        ))
        
        logger.info(f"Generated recommendations and timeline")
        # Process the response to extract recommendations and timeline
        try:
            from langchain_core.output_parsers import JsonOutputParser
            parser = JsonOutputParser()
            result_data = parser.parse(response.content)
            return result_data
        except Exception as e:
            logger.error(f"Error parsing recommendations and timeline: {str(e)}")
            # Return default values if parsing fails
            return {
                "key_recommendations": [
                    "Conduct digital literacy training",
                    "Establish change management program",
                    "Develop digital leadership capabilities"
                ],
                "timeline": "6-12 months to achieve sufficient readiness"
            }
    
    def assess_organization(self, company_info: Dict[str, Any], 
                           maturity_assessment: Dict[str, Any] = None,
                           technology_stack: Dict[str, Any] = None) -> OrganizationalReadinessAssessment:
        """
        Perform a comprehensive organizational readiness assessment.
        
        Args:
            company_info: Information about the company
            maturity_assessment: Maturity assessment results (optional)
            technology_stack: Technology stack recommendations (optional)
            
        Returns:
            OrganizationalReadinessAssessment: Comprehensive readiness assessment
        """
        logger.info(f"Generating organizational readiness assessment for {company_info.get('name', 'Unknown')}")
        
        # Extract relevant information
        extracted_info = self._extract_from_company_info(company_info)
        
        # Default maturity assessment if not provided
        if maturity_assessment is None:
            maturity_assessment = company_info.get("maturity", {})
        
        # Default technology stack if not provided
        if technology_stack is None:
            technology_stack = {}
        
        # Perform various assessments
        skill_gaps = self._assess_skill_gaps(extracted_info, maturity_assessment)
        cultural_factors = self._assess_cultural_factors(extracted_info, maturity_assessment)
        change_readiness = self._assess_change_readiness(extracted_info)
        leadership_readiness = self._assess_leadership_readiness(extracted_info, maturity_assessment)
        training_needs = self._identify_training_needs(skill_gaps, technology_stack)
        readiness_by_department = self._generate_department_readiness(extracted_info, skill_gaps)
        
        # Compile all assessments
        assessments = {
            "skill_gaps": skill_gaps,
            "cultural_factors": cultural_factors,
            "change_readiness": change_readiness,
            "leadership_readiness": leadership_readiness,
            "training_needs": training_needs,
            "readiness_by_department": readiness_by_department
        }
        
        # Calculate overall readiness score
        overall_readiness_score = self._calculate_overall_readiness(assessments)
        
        # Generate recommendations and timeline
        rec_and_timeline = self._generate_recommendations_and_timeline(assessments)
        key_recommendations = rec_and_timeline.get("key_recommendations", [])
        timeline_for_readiness = rec_and_timeline.get("timeline", "12 months")
        
        # Generate priority actions (combination of recommendations from various assessments)
        leadership_recs = leadership_readiness.recommendations
        cultural_recs = [strategy for factor in cultural_factors for strategy in factor.improvement_strategies]
        change_recs = [action for metric in change_readiness for action in metric.improvement_actions]
        
        # Combine and prioritize
        all_recs = leadership_recs + cultural_recs + change_recs
        priority_actions = key_recommendations if key_recommendations else all_recs[:10]
        
        # Generate executive summary
        key_findings = {
            "overall_score": overall_readiness_score,
            "leadership_score": sum([
                leadership_readiness.vision_clarity,
                leadership_readiness.commitment_level,
                leadership_readiness.digital_fluency,
                leadership_readiness.change_management_capability
            ]) / 4,
            "cultural_alignment": sum(cf.alignment_score for cf in cultural_factors) / len(cultural_factors),
            "skill_gaps": [{"area": gap.skill_area, "score": gap.gap_score} for gap in skill_gaps[:3]],
            "department_readiness": readiness_by_department
        }
        executive_summary = self._generate_executive_summary(overall_readiness_score, key_findings)
        
        # Create and return comprehensive assessment
        assessment = OrganizationalReadinessAssessment(
            executive_summary=executive_summary,
            overall_readiness_score=overall_readiness_score,
            skill_gaps=skill_gaps,
            cultural_factors=cultural_factors,
            change_readiness_metrics=change_readiness,
            training_needs=training_needs,
            leadership_readiness=leadership_readiness,
            key_recommendations=key_recommendations,
            readiness_by_department=readiness_by_department,
            priority_actions=priority_actions,
            timeline_for_readiness=timeline_for_readiness
        )
        
        logger.info(f"Generated organizational readiness assessment with score: {overall_readiness_score:.2f}")
        return assessment 