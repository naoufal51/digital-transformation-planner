# Digital Transformation Multi-Agent System

A LangGraph-based multi-agent system designed to analyze and create comprehensive digital transformation plans for businesses.

## Overview

This system uses a series of specialized agents to:

1. Analyze company data and identify key digital transformation aspects
2. Generate expert personas with diverse specialties
3. Conduct simulated interviews between consultants and domain experts
4. Generate actionable recommendations based on expert insights
5. Create a comprehensive digital transformation plan

The system is inspired by the STORM architecture (paper: https://arxiv.org/abs/2402.14207) but adapted specifically for digital transformation planning.

## Architecture

```
┌─────────────────────┐     ┌─────────────────────┐     ┌─────────────────────┐
│  Company Analysis   │     │   Expert Persona    │     │  Expert Interviews  │
│  & Aspect Mapping   │────▶│      Generation     │────▶│   (Multi-Agent)     │
└─────────────────────┘     └─────────────────────┘     └──────────┬──────────┘
                                                                   │
┌─────────────────────┐     ┌─────────────────────┐                │
│  Transformation     │     │   Recommendation    │                │
│    Plan Creation    │◀────│     Generation      │◀───────────────┘
└─────────────────────┘     └─────────────────────┘
```

## Key Components

- **StateGraph**: The main orchestration flow using LangGraph's StateGraph
- **Multi-Agent Consultation**: Simulated conversations between consultants and experts
- **SearchTools**: Domain-specific search tools for digital transformation research
- **Structured Outputs**: Pydantic models for structured data handling

## Installation

1. Create a virtual environment:
   ```
   python -m venv .venv
   source .venv/bin/activate   # On Windows: .venv\Scripts\activate
   ```

2. Install requirements:
   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   Create a `.env` file with:
   ```
   OPENAI_API_KEY=your_openai_api_key
   ```

## Usage

### Web Interface

The easiest way to use the system is through the Streamlit web interface:

```bash
# Navigate to the project directory and run:
streamlit run app.py
```

This will open a web interface where you can:
- Enter your company information
- Generate a digital transformation plan
- View recommendations and insights
- Download the plan as a markdown file

### Command Line Example

You can also run the example script from the command line:

```bash
python run_example.py
```

### Programmatic Usage

For integration with your own application:

```python
from digital_transformation.main_graph import digital_transformation_graph

# Define your company information
company_info = {
    "company_name": "Your Company",
    "company_description": "Description of your company",
    "industry": "Your Industry",
    "transformation_goals": ["Goal 1", "Goal 2"],
    "business_challenges": ["Challenge 1", "Challenge 2"],
    "current_technologies": ["Technology 1", "Technology 2"]
}

# Create a configuration with a thread ID
config = {"configurable": {"thread_id": "your-company-transformation"}}

# Run the analysis
async for step in digital_transformation_graph.astream(company_info, config):
    # Process each step as needed
    pass

# Get final results
final_state = digital_transformation_graph.get_state(config).values
transformation_plan = final_state["transformation_plan"]

# Use the transformation plan
print(transformation_plan.as_str)
```

## Customization

- Modify the number of experts by changing the `num_experts` parameter in `persona_generator.generate_experts()`
- Adjust the interview depth by modifying `max_turns` in `create_interview_graph()`
- Change LLM models by updating the model names in the respective agent files

## License

MIT 