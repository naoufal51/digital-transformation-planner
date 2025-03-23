import logging
import uuid
from typing import Dict, List, Any, Optional, Tuple

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

from digital_transformation.schema.technology import (
    TechnologyOption,
    TechnologyCategory,
    TechnologyRoadmap,
    TechnologyStack
)
from digital_transformation.schema.assessment import MaturityAssessment
from digital_transformation.agents.tech_categories import (
    get_standard_categories,
    get_industry_specific_categories
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create LLM instance with named runs for better tracing
tech_llm = ChatOpenAI(
    model="gpt-4o", 
    temperature=0.2,
    model_kwargs={"response_format": {"type": "text"}},
    tags=["technology_recommendation"]
)

class TechnologyRecommender:
    """Agent that recommends technology stack based on company context and maturity"""
    
    def __init__(self, openai_api_key: Optional[str] = None, model: str = "gpt-4-turbo"):
        """Initialize the technology recommender agent with optional API key"""
        self.llm = ChatOpenAI(
            model=model,
            temperature=0.2,
            openai_api_key=openai_api_key
        )
        logger.info("TechnologyRecommender initialized with model: %s", model)
    
    def _get_relevant_categories(self, industry: str) -> List[Dict]:
        """Get technology categories relevant to the industry"""
        standard_categories = get_standard_categories()
        industry_specific = get_industry_specific_categories(industry)
        
        # Combine standard and industry-specific categories
        relevant_categories = standard_categories + industry_specific
        logger.info("Retrieved %d relevant technology categories for %s industry", 
                   len(relevant_categories), industry)
        
        return relevant_categories
    
    def evaluate_category(self, 
                         category: Dict, 
                         company_info: Dict, 
                         maturity_assessment: MaturityAssessment) -> TechnologyCategory:
        """Evaluate a technology category for the company based on context and maturity"""
        logger.info("Evaluating technology category: %s", category.get("name"))
        
        # Determine relevance score based on company goals and challenges
        industry = company_info.get("industry", "")
        goals = company_info.get("transformation_goals", [])
        challenges = company_info.get("business_challenges", [])
        current_tech = company_info.get("current_technologies", [])
        
        # Find current maturity level for this category from assessment
        category_dimension = category.get("related_dimension", "")
        current_maturity_score = None
        
        for dimension in maturity_assessment.dimensions:
            if dimension.name.lower() in category_dimension.lower() or category_dimension.lower() in dimension.name.lower():
                current_maturity_score = dimension.current_score
                break
        
        if current_maturity_score is None:
            current_maturity_score = maturity_assessment.overall_score
            
        # Map maturity score (1-5) to maturity level
        maturity_levels = ["Initial", "Developing", "Defined", "Managed", "Optimized"]
        current_maturity = maturity_levels[min(int(current_maturity_score) - 1, 4)]
        
        # Target maturity is usually 1-2 levels higher, capped at 5
        target_index = min(int(current_maturity_score) + 1, 4)
        target_maturity = maturity_levels[target_index]
        
        # Generate technology options for this category
        technology_options = []
        for tech_option in category.get("sample_technologies", []):
            # Evaluate each technology option based on company context
            option = TechnologyOption(
                name=tech_option.get("name"),
                vendor=tech_option.get("vendor"),
                description=tech_option.get("description"),
                key_features=tech_option.get("key_features"),
                pros=tech_option.get("pros"),
                cons=tech_option.get("cons"),
                cost_range=tech_option.get("cost_range"),
                implementation_complexity=tech_option.get("implementation_complexity"),
                integration_notes=self._generate_integration_notes(tech_option, current_tech),
                industry_fit_score=self._calculate_industry_fit(tech_option, industry, goals, challenges),
                url=tech_option.get("url")
            )
            technology_options.append(option)
        
        # Sort options by industry fit score (descending)
        technology_options.sort(key=lambda x: x.industry_fit_score, reverse=True)
        
        # Generate specific recommendations for this category
        recommendations = self._generate_category_recommendations(
            category, technology_options, company_info, current_maturity, target_maturity
        )
        
        # Create and return the evaluated category
        return TechnologyCategory(
            name=category.get("name"),
            description=category.get("description"),
            relevance_score=self._calculate_relevance_score(category, goals, challenges),
            current_maturity=current_maturity,
            target_maturity=target_maturity,
            options=technology_options,
            recommendations=recommendations
        )
    
    def _generate_integration_notes(self, technology: Dict, current_technologies: List[str]) -> str:
        """Generate notes on integration with existing systems"""
        # For now, a simple implementation - in real application, would use LLM here
        if not current_technologies:
            return "No existing systems information provided for integration analysis."
        
        tech_name = technology.get("name", "")
        integrations = technology.get("integrations", [])
        
        integration_points = []
        for current_tech in current_technologies:
            if current_tech.lower() in [i.lower() for i in integrations]:
                integration_points.append(f"Direct integration available with {current_tech}")
        
        if integration_points:
            notes = "Integration opportunities: " + "; ".join(integration_points)
        else:
            notes = f"Custom integration may be required between {tech_name} and existing systems."
            
        return notes
    
    def _calculate_industry_fit(self, technology: Dict, industry: str, goals: List[str], challenges: List[str]) -> int:
        """Calculate how well the technology fits the company's industry and needs"""
        # Base score starts at 5 (middle of 1-10 scale)
        score = 5
        
        # Industry alignment
        industry_focus = technology.get("industry_focus", [])
        if industry.lower() in [i.lower() for i in industry_focus] or "all" in [i.lower() for i in industry_focus]:
            score += 2
        
        # Goal alignment
        for goal in goals:
            for supported_goal in technology.get("supports_goals", []):
                if goal.lower() in supported_goal.lower() or supported_goal.lower() in goal.lower():
                    score += 1
                    break
        
        # Challenge alignment
        for challenge in challenges:
            for addressed_challenge in technology.get("addresses_challenges", []):
                if challenge.lower() in addressed_challenge.lower() or addressed_challenge.lower() in challenge.lower():
                    score += 1
                    break
        
        # Cap at 10
        return min(score, 10)
    
    def _calculate_relevance_score(self, category: Dict, goals: List[str], challenges: List[str]) -> int:
        """Calculate relevance score for a category based on company goals and challenges"""
        # Base score starts at 5 (middle of 1-10 scale)
        score = 5
        
        # Goal alignment
        supported_goals = category.get("supports_goals", [])
        for goal in goals:
            for supported_goal in supported_goals:
                if goal.lower() in supported_goal.lower() or supported_goal.lower() in goal.lower():
                    score += 1
                    break
        
        # Challenge alignment
        addresses_challenges = category.get("addresses_challenges", [])
        for challenge in challenges:
            for addressed_challenge in addresses_challenges:
                if challenge.lower() in addressed_challenge.lower() or addressed_challenge.lower() in challenge.lower():
                    score += 1
                    break
        
        # Cap at 10
        return min(score, 10)
    
    def _generate_category_recommendations(self, 
                                          category: Dict, 
                                          options: List[TechnologyOption], 
                                          company_info: Dict,
                                          current_maturity: str,
                                          target_maturity: str) -> List[str]:
        """Generate specific recommendations for a technology category"""
        # Initialize recommendations
        recommendations = []
        
        # If current maturity is low, recommend foundational technologies
        if current_maturity in ["Initial", "Developing"]:
            recommendations.append(f"Focus on establishing foundational {category.get('name')} capabilities before advanced solutions")
            
            # Recommend simple, low-complexity options first
            simple_options = [o for o in options if o.implementation_complexity == "Low"]
            if simple_options:
                top_simple = simple_options[0]
                recommendations.append(f"Start with {top_simple.name} as an entry-level solution to build basic capabilities")
        
        # For any maturity level, recommend the top-ranked option
        if options:
            top_option = options[0]
            recommendations.append(f"Consider {top_option.name} as a primary solution for {category.get('name')}")
            
            # If there's a cost-effective alternative
            budget_options = [o for o in options if o.cost_range == "$" and o.industry_fit_score > 5]
            if budget_options and budget_options[0].name != top_option.name:
                recommendations.append(f"{budget_options[0].name} offers a cost-effective alternative with acceptable capabilities")
        
        # Add integration recommendations if there are current technologies
        current_tech = company_info.get("current_technologies", [])
        if current_tech and options:
            recommendations.append(f"Ensure integration planning between new {category.get('name')} solutions and existing systems")
        
        return recommendations
    
    def create_implementation_roadmap(self, 
                                     evaluated_categories: List[TechnologyCategory], 
                                     company_info: Dict) -> List[TechnologyRoadmap]:
        """Create a phased implementation roadmap for recommended technologies"""
        logger.info("Creating implementation roadmap with %d categories", len(evaluated_categories))
        
        # Sort categories by relevance score (descending)
        sorted_categories = sorted(evaluated_categories, key=lambda x: x.relevance_score, reverse=True)
        
        # Define implementation phases
        phases = [
            {"name": "Foundation Building", "timeline": "Months 1-3", "max_complexity": "Low"},
            {"name": "Core Implementation", "timeline": "Months 4-9", "max_complexity": "Medium"},
            {"name": "Advanced Capabilities", "timeline": "Months 10-18", "max_complexity": "High"}
        ]
        
        roadmap = []
        
        # Category and technology dependencies
        dependencies = {
            "Data Management & Analytics": ["Core Systems Modernization"],
            "Advanced AI & Automation": ["Data Management & Analytics"],
            "Customer Experience Platforms": ["Core Systems Modernization"]
        }
        
        # Assign technologies to phases based on complexity and dependencies
        for phase in phases:
            phase_technologies = []
            phase_dependencies = []
            phase_activities = []
            
            for category in sorted_categories:
                # Skip if category has low relevance
                if category.relevance_score < 5:
                    continue
                    
                # Check if this category has dependencies
                has_unmet_dependency = False
                for dep_category in dependencies.get(category.name, []):
                    if dep_category not in [tech.split(" (")[0] for tech in phase_technologies] and \
                       dep_category not in [p_tech for phase_item in roadmap for p_tech in phase_item.technologies]:
                        has_unmet_dependency = True
                        phase_dependencies.append(dep_category)
                
                # Skip if dependency not met and not in foundation phase
                if has_unmet_dependency and phase["name"] != "Foundation Building":
                    continue
                    
                # Add top technology options that match phase complexity
                for option in category.options:
                    complexity_map = {"Low": 1, "Medium": 2, "High": 3}
                    phase_complexity = complexity_map.get(phase["max_complexity"], 0)
                    option_complexity = complexity_map.get(option.implementation_complexity, 0)
                    
                    if option_complexity <= phase_complexity:
                        tech_entry = f"{option.name} ({category.name})"
                        if tech_entry not in phase_technologies and \
                           tech_entry not in [p_tech for phase_item in roadmap for p_tech in phase_item.technologies]:
                            phase_technologies.append(tech_entry)
                            
                            # Add implementation activities
                            if option.implementation_complexity == "Low":
                                phase_activities.append(f"Implement basic {option.name} capabilities")
                            elif option.implementation_complexity == "Medium":
                                phase_activities.append(f"Deploy and integrate {option.name} with existing systems")
                            else:
                                phase_activities.append(f"Full enterprise rollout of {option.name} with advanced features")
                            
                            # Only take top 2 options per category per phase
                            if len([t for t in phase_technologies if f"({category.name})" in t]) >= 2:
                                break
            
            # Determine effort based on technologies and complexity
            if phase["name"] == "Foundation Building":
                effort = "Medium (3-4 FTEs)"
            elif phase["name"] == "Core Implementation":
                effort = "High (5-7 FTEs)"
            else:
                effort = "Very High (8-10 FTEs)"
                
            # Create roadmap phase
            if phase_technologies:
                roadmap_phase = TechnologyRoadmap(
                    phase_name=phase["name"],
                    timeline=phase["timeline"],
                    technologies=phase_technologies,
                    dependencies=phase_dependencies,
                    key_activities=phase_activities,
                    estimated_effort=effort
                )
                roadmap.append(roadmap_phase)
        
        return roadmap
    
    def generate_executive_summary(self, 
                                  categories: List[TechnologyCategory], 
                                  roadmap: List[TechnologyRoadmap],
                                  company_info: Dict) -> Dict:
        """Generate executive summary and additional info for technology stack"""
        logger.info("Generating executive summary for technology recommendations")
        
        # Sort categories by relevance score
        top_categories = sorted(categories, key=lambda x: x.relevance_score, reverse=True)[:3]
        
        # Create executive summary
        company_name = company_info.get("company_name", "your organization")
        industry = company_info.get("industry", "your industry")
        
        exec_summary = (
            f"Based on {company_name}'s current digital maturity assessment and business goals, "
            f"we recommend a phased technology implementation approach focusing on "
            f"{', '.join([cat.name for cat in top_categories])}. "
            f"These technologies will address key challenges in {industry} while "
            f"building a foundation for long-term digital transformation success. "
            f"The proposed implementation spans {roadmap[-1].timeline if roadmap else '12-18 months'}, "
            f"with early wins achievable in the first 90 days."
        )
        
        # Create business context
        goals = company_info.get("transformation_goals", [])
        challenges = company_info.get("business_challenges", [])
        
        business_context = (
            f"This technology stack recommendation is designed to help {company_name} achieve "
            f"its digital transformation goals of {', '.join(goals)}. "
            f"The recommended solutions specifically address business challenges including "
            f"{', '.join(challenges)}. The technology selection considers current systems, "
            f"industry best practices, and a pragmatic implementation approach."
        )
        
        # Determine total cost estimate
        cost_indicators = []
        for cat in categories:
            for opt in cat.options[:1]:  # Just use top option
                cost_indicators.append(opt.cost_range)
        
        # Count $ symbols
        total_dollar_signs = sum(cost_range.count('$') for cost_range in cost_indicators)
        avg_cost = total_dollar_signs / len(cost_indicators) if cost_indicators else 0
        
        if avg_cost < 1.5:
            total_cost = "$250,000 - $500,000"
        elif avg_cost < 2.5:
            total_cost = "$500,000 - $1,000,000"
        else:
            total_cost = "$1,000,000+"
            
        # Implementation timeframe
        if roadmap:
            last_phase = roadmap[-1].timeline
            implementation_timeframe = f"Full implementation: {roadmap[0].timeline} to {last_phase}"
        else:
            implementation_timeframe = "12-18 months with phased approach"
            
        # Key considerations
        key_considerations = [
            f"Integration with existing systems is critical for {company_name}'s technology stack",
            "Cross-functional teams should be involved in selection and implementation",
            "Consider change management needs for user adoption",
            "Regular progress reviews against business outcomes are essential",
            f"Build internal capabilities aligned with new technologies"
        ]
        
        # Risk factors
        risk_factors = [
            {"risk": "Integration Complexity", "mitigation": "Detailed technical discovery and integration planning before implementation"},
            {"risk": "User Adoption", "mitigation": "Robust change management and training program"},
            {"risk": "Budget Overruns", "mitigation": "Phased approach with clear success criteria before proceeding to next phase"},
            {"risk": "Vendor Lock-in", "mitigation": "Evaluate exit costs and data portability before selection"},
            {"risk": "Implementation Delays", "mitigation": "Agile methodology with regular milestones review"}
        ]
        
        return {
            "executive_summary": exec_summary,
            "business_context": business_context,
            "total_cost_estimate": total_cost,
            "implementation_timeframe": implementation_timeframe,
            "key_considerations": key_considerations,
            "risk_factors": risk_factors
        }
        
    def recommend_technology_stack(self, 
                                  company_info: Dict, 
                                  maturity_assessment: MaturityAssessment) -> TechnologyStack:
        """Generate a complete technology stack recommendation"""
        logger.info("Generating technology stack recommendation for %s", 
                   company_info.get("company_name", "company"))
        
        # Get relevant technology categories for the company's industry
        industry = company_info.get("industry", "")
        category_data = self._get_relevant_categories(industry)
        
        # Evaluate each category
        evaluated_categories = []
        for category in category_data:
            evaluated_category = self.evaluate_category(category, company_info, maturity_assessment)
            evaluated_categories.append(evaluated_category)
            
        # Sort categories by relevance score
        evaluated_categories.sort(key=lambda x: x.relevance_score, reverse=True)
        
        # Create implementation roadmap
        roadmap = self.create_implementation_roadmap(evaluated_categories, company_info)
        
        # Generate executive summary and additional information
        summary_info = self.generate_executive_summary(evaluated_categories, roadmap, company_info)
        
        # Create and return the complete technology stack
        technology_stack = TechnologyStack(
            executive_summary=summary_info["executive_summary"],
            business_context=summary_info["business_context"],
            categories=evaluated_categories,
            roadmap=roadmap,
            total_cost_estimate=summary_info["total_cost_estimate"],
            implementation_timeframe=summary_info["implementation_timeframe"],
            key_considerations=summary_info["key_considerations"],
            risk_factors=summary_info["risk_factors"]
        )
        
        logger.info("Generated technology stack recommendation with %d categories and %d roadmap phases",
                   len(technology_stack.categories), len(technology_stack.roadmap))
        
        return technology_stack


# Create the recommender instance
technology_recommender = TechnologyRecommender() 