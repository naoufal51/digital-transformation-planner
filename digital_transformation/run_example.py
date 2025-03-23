import asyncio
import os
from dotenv import load_dotenv

from digital_transformation.main_graph import digital_transformation_graph


# Load environment variables from .env file (API keys)
load_dotenv()


async def run_digital_transformation_analysis():
    """Run a complete digital transformation analysis for a sample company."""
    
    # Sample company information
    company_info = {
        "company_name": "HealthPlus Medical Group",
        "company_description": "A mid-sized healthcare provider with 15 clinics across the region, "
                              "offering primary care and specialized medical services. Founded in 1995, "
                              "the company has grown steadily but now faces increasing competition and "
                              "changing patient expectations.",
        "industry": "Healthcare",
        "transformation_goals": [
            "Improve patient experience through digital channels",
            "Streamline administrative processes",
            "Enable data-driven decision making",
            "Implement telemedicine capabilities",
            "Ensure HIPAA compliance with all digital solutions"
        ],
        "business_challenges": [
            "Outdated electronic health record (EHR) system",
            "Limited digital interaction with patients",
            "Siloed data across departments",
            "High administrative costs",
            "Difficulty attracting younger patient demographics",
            "Growing competition from tech-savvy healthcare startups"
        ],
        "current_technologies": [
            "Legacy EHR system (10+ years old)",
            "Basic website with minimal functionality",
            "On-premise infrastructure",
            "Limited data analytics capabilities",
            "Manual scheduling and billing processes"
        ]
    }
    
    print(f"Starting digital transformation analysis for {company_info['company_name']}...")
    
    # Create a configuration with a thread ID for persistence
    config = {"configurable": {"thread_id": "health-plus-transformation"}}
    
    # Track the execution of the graph
    step_count = 0
    async for step in digital_transformation_graph.astream(company_info, config):
        step_count += 1
        node_name = next(iter(step))
        print(f"Step {step_count}: Completed '{node_name}'")
    
    # Retrieve the final state
    final_state = digital_transformation_graph.get_state(config).values
    
    # Display transformation plan
    plan = final_state["transformation_plan"]
    print("\n" + "="*80)
    print(f"DIGITAL TRANSFORMATION PLAN: {plan.title}")
    print("="*80)
    print(f"\nExecutive Summary:\n{plan.executive_summary}")
    
    print("\nRecommendations:")
    for i, rec in enumerate(plan.recommendations, 1):
        print(f"\n{i}. {rec.title} (Priority: {rec.priority})")
        print(f"   Impact: {rec.estimated_impact}")
        print(f"   Effort: {rec.estimated_effort}")
    
    # Provide an option to save the complete plan to file
    save_path = "digital_transformation_plan.md"
    with open(save_path, "w") as f:
        f.write(plan.as_str)
    
    print(f"\nComplete transformation plan saved to {save_path}")


if __name__ == "__main__":
    # Check for API keys
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable not set.")
        print("Please set your OpenAI API key in an .env file or environment variable.")
        exit(1)
    
    # Run the analysis
    asyncio.run(run_digital_transformation_analysis()) 