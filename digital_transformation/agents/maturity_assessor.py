import logging
import uuid
from typing import Dict, List, Any, Optional

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableLambda
from pydantic import BaseModel, Field

from digital_transformation.schema.assessment import (
    MaturityDimension, 
    MaturityAssessment,
    IndustryBenchmark
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create LLM instance with named runs for better tracing
assessment_llm = ChatOpenAI(
    model="gpt-4o", 
    temperature=0.1,
    model_kwargs={"response_format": {"type": "text"}},
    tags=["maturity_assessment"]
)

# Define standard maturity dimensions
MATURITY_DIMENSIONS = [
    {
        "name": "Digital Strategy",
        "description": "The extent to which digital transformation is aligned with business objectives and formalized in strategy"
    },
    {
        "name": "Customer Experience",
        "description": "How effectively digital channels are used to enhance customer engagement and satisfaction"
    },
    {
        "name": "Operations & Processes",
        "description": "The degree of process automation and operational efficiency through digital tools"
    },
    {
        "name": "Technology Infrastructure",
        "description": "The modernity, flexibility, and integration of technology systems and platforms"
    },
    {
        "name": "Data Management & Analytics",
        "description": "Capabilities for collecting, analyzing, and deriving insights from data"
    },
    {
        "name": "Organizational Culture",
        "description": "The organization's readiness for digital change and innovation mindset"
    },
    {
        "name": "Digital Skills & Talent",
        "description": "The availability of necessary digital skills and talent development programs"
    }
]

# Define industry benchmarks (simplified example data)
INDUSTRY_BENCHMARKS = {
    "Healthcare": {
        "overall_average": 2.8,
        "dimension_averages": {
            "Digital Strategy": 2.9,
            "Customer Experience": 2.7,
            "Operations & Processes": 2.5,
            "Technology Infrastructure": 2.6,
            "Data Management & Analytics": 3.1,
            "Organizational Culture": 2.4,
            "Digital Skills & Talent": 2.5
        },
        "maturity_distribution": {
            "Initial": 0.30,
            "Developing": 0.45,
            "Advanced": 0.20,
            "Leading": 0.05
        }
    },
    "Manufacturing": {
        "overall_average": 2.6,
        "dimension_averages": {
            "Digital Strategy": 2.7,
            "Customer Experience": 2.4,
            "Operations & Processes": 3.1,
            "Technology Infrastructure": 2.5,
            "Data Management & Analytics": 2.4,
            "Organizational Culture": 2.3,
            "Digital Skills & Talent": 2.2
        },
        "maturity_distribution": {
            "Initial": 0.35,
            "Developing": 0.40,
            "Advanced": 0.20,
            "Leading": 0.05
        }
    },
    "Retail": {
        "overall_average": 3.0,
        "dimension_averages": {
            "Digital Strategy": 3.2,
            "Customer Experience": 3.5,
            "Operations & Processes": 2.8,
            "Technology Infrastructure": 2.9,
            "Data Management & Analytics": 3.2,
            "Organizational Culture": 2.5,
            "Digital Skills & Talent": 2.7
        },
        "maturity_distribution": {
            "Initial": 0.20,
            "Developing": 0.40,
            "Advanced": 0.30,
            "Leading": 0.10
        }
    },
    "Financial Services": {
        "overall_average": 3.3,
        "dimension_averages": {
            "Digital Strategy": 3.5,
            "Customer Experience": 3.4,
            "Operations & Processes": 3.0,
            "Technology Infrastructure": 3.2,
            "Data Management & Analytics": 3.8,
            "Organizational Culture": 2.8,
            "Digital Skills & Talent": 3.1
        },
        "maturity_distribution": {
            "Initial": 0.15,
            "Developing": 0.35,
            "Advanced": 0.35,
            "Leading": 0.15
        }
    },
    "Education": {
        "overall_average": 2.5,
        "dimension_averages": {
            "Digital Strategy": 2.6,
            "Customer Experience": 2.5,
            "Operations & Processes": 2.4,
            "Technology Infrastructure": 2.5,
            "Data Management & Analytics": 2.3,
            "Organizational Culture": 2.5,
            "Digital Skills & Talent": 2.7
        },
        "maturity_distribution": {
            "Initial": 0.35,
            "Developing": 0.45,
            "Advanced": 0.15,
            "Leading": 0.05
        }
    }
}

# For industries not in our benchmark data
DEFAULT_BENCHMARK = {
    "overall_average": 2.7,
    "dimension_averages": {
        "Digital Strategy": 2.8,
        "Customer Experience": 2.7,
        "Operations & Processes": 2.7,
        "Technology Infrastructure": 2.6,
        "Data Management & Analytics": 2.5,
        "Organizational Culture": 2.5,
        "Digital Skills & Talent": 2.6
    },
    "maturity_distribution": {
        "Initial": 0.30,
        "Developing": 0.40,
        "Advanced": 0.25,
        "Leading": 0.05
    }
}


class DimensionScoreResponse(BaseModel):
    """Response format for dimension scoring"""
    current_score: float = Field(..., description="Current maturity score (1-5)")
    target_score: float = Field(..., description="Target maturity score (1-5)")
    improvement_areas: List[str] = Field(..., description="Areas that need improvement")


class MaturityAssessor:
    """Agent for assessing digital transformation maturity"""
    
    def __init__(self):
        self.dimensions = MATURITY_DIMENSIONS
    
    def get_industry_benchmark(self, industry: str) -> IndustryBenchmark:
        """Get benchmark data for a specific industry"""
        # Normalize industry name to match our keys
        normalized_industry = industry.lower()
        
        # Find the best match
        for benchmark_industry in INDUSTRY_BENCHMARKS:
            if benchmark_industry.lower() in normalized_industry or normalized_industry in benchmark_industry.lower():
                benchmark_data = INDUSTRY_BENCHMARKS[benchmark_industry]
                return IndustryBenchmark(
                    industry=benchmark_industry,
                    overall_average=benchmark_data["overall_average"],
                    dimension_averages=benchmark_data["dimension_averages"],
                    maturity_distribution=benchmark_data["maturity_distribution"]
                )
        
        # If no match, use default benchmark
        return IndustryBenchmark(
            industry="Cross-Industry Average",
            overall_average=DEFAULT_BENCHMARK["overall_average"],
            dimension_averages=DEFAULT_BENCHMARK["dimension_averages"],
            maturity_distribution=DEFAULT_BENCHMARK["maturity_distribution"]
        )
    
    async def evaluate_dimension(
        self, 
        dimension: Dict[str, str],
        company_info: Dict[str, Any],
        run_id: str = ""
    ) -> DimensionScoreResponse:
        """Evaluate a single maturity dimension"""
        try:
            logger.info(f"[{run_id}] Evaluating dimension: {dimension['name']}")
            
            # Create prompt for dimension evaluation
            dimension_prompt = ChatPromptTemplate.from_messages([
                (
                    "system",
                    """You are a digital transformation maturity assessor. 
Your task is to evaluate a company's maturity level for a specific dimension of digital transformation.
Score their current maturity on a scale of 1-5 where:
1 = Initial (basic/ad hoc)
2 = Developing (defined but limited implementation)
3 = Established (implemented with some success)
4 = Advanced (well-integrated and data-driven)
5 = Leading (innovative and creating competitive advantage)

Also recommend a realistic target score they should aim for (also 1-5) based on their industry, 
challenges, and goals. Then list 3-5 specific areas they need to improve to reach that target.

Format your response as valid JSON with these fields:
- current_score: A float between 1 and 5
- target_score: A float between 1 and 5
- improvement_areas: A list of strings describing improvement areas

Dimension to evaluate: {dimension_name}
Dimension description: {dimension_description}"""
                )
            ])
            
            # Format company information for prompt
            company_context = f"""
Company: {company_info.get('company_name', 'Unknown')}
Industry: {company_info.get('industry', 'Unknown')}
Description: {company_info.get('company_description', 'Unknown')}
Transformation Goals: {', '.join(company_info.get('transformation_goals', []))}
Current Challenges: {', '.join(company_info.get('business_challenges', []))}
Current Technologies: {', '.join(company_info.get('current_technologies', []))}
"""
            
            # Add metadata for better tracing
            config = {
                "metadata": {
                    "process": "maturity_assessment",
                    "dimension": dimension["name"],
                    "run_id": run_id
                }
            }
            
            # Execute the assessment for this dimension
            response = await assessment_llm.with_structured_output(
                DimensionScoreResponse
            ).ainvoke(
                dimension_prompt.format(
                    dimension_name=dimension["name"],
                    dimension_description=dimension["description"]
                ) + company_context,
                config=config
            )
            
            logger.info(f"[{run_id}] {dimension['name']} assessment complete: Current={response.current_score}, Target={response.target_score}")
            return response
            
        except Exception as e:
            logger.error(f"[{run_id}] Error evaluating dimension {dimension['name']}: {str(e)}", exc_info=True)
            # Return a fallback response
            return DimensionScoreResponse(
                current_score=2.0,
                target_score=3.0,
                improvement_areas=["Unable to assess - insufficient data"]
            )
    
    async def assess_maturity(self, company_info: Dict[str, Any]) -> MaturityAssessment:
        """Perform a complete maturity assessment"""
        run_id = str(uuid.uuid4())[:8]  # Generate a short run ID for tracing
        logger.info(f"[{run_id}] Starting maturity assessment for {company_info.get('company_name', 'Unknown')}")
        
        # Get industry benchmarks
        industry = company_info.get("industry", "Unknown")
        benchmark = self.get_industry_benchmark(industry)
        logger.info(f"[{run_id}] Using benchmark data for {benchmark.industry}")
        
        # Assess each dimension in parallel
        dimensions = []
        overall_score = 0.0
        
        for dimension in self.dimensions:
            # Evaluate this dimension
            response = await self.evaluate_dimension(dimension, company_info, run_id)
            
            # Get benchmark score for this dimension
            benchmark_score = benchmark.dimension_averages.get(
                dimension["name"], 
                benchmark.overall_average
            )
            
            # Calculate gap
            gap = response.target_score - response.current_score
            
            # Create dimension object
            maturity_dimension = MaturityDimension(
                name=dimension["name"],
                description=dimension["description"],
                current_score=response.current_score,
                target_score=response.target_score,
                industry_benchmark=benchmark_score,
                gap=gap,
                improvement_areas=response.improvement_areas
            )
            
            dimensions.append(maturity_dimension)
            overall_score += response.current_score
        
        # Calculate overall score
        if dimensions:
            overall_score = overall_score / len(dimensions)
        
        # Determine overall maturity level
        maturity_level = "Initial"
        if overall_score >= 4.0:
            maturity_level = "Leading"
        elif overall_score >= 3.0:
            maturity_level = "Advanced"
        elif overall_score >= 2.0:
            maturity_level = "Developing"
        
        # Identify top strengths (highest current scores)
        sorted_by_strength = sorted(dimensions, key=lambda d: d.current_score, reverse=True)
        top_strengths = [
            f"{dim.name} ({dim.current_score:.1f}/5.0): {dim.description}"
            for dim in sorted_by_strength[:3]
        ]
        
        # Identify top gaps (largest gaps between current and target)
        sorted_by_gap = sorted(dimensions, key=lambda d: d.gap, reverse=True)
        top_gaps = [
            f"{dim.name} (Gap: {dim.gap:.1f}): {dim.improvement_areas[0] if dim.improvement_areas else 'Need improvement'}"
            for dim in sorted_by_gap[:3]
        ]
        
        # Create assessment result
        assessment = MaturityAssessment(
            overall_score=overall_score,
            industry_average=benchmark.overall_average,
            dimensions=dimensions,
            top_strengths=top_strengths,
            top_gaps=top_gaps,
            maturity_level=maturity_level
        )
        
        logger.info(f"[{run_id}] Completed maturity assessment. Overall score: {overall_score:.1f}/5.0")
        return assessment


# Create the assessor instance
maturity_assessor = MaturityAssessor() 