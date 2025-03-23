# Digital Transformation Planner

An AI-powered application that generates comprehensive digital transformation plans for businesses using multi-agent systems and LLMs.

![Digital Transformation Planner](https://img.shields.io/badge/Application-Digital_Transformation-blue)
![Python](https://img.shields.io/badge/Python-3.10_|_3.11-blue)
![LangGraph](https://img.shields.io/badge/Framework-LangGraph-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## Overview

The Digital Transformation Planner is an advanced application that leverages AI to help organizations plan and execute successful digital transformations. By analyzing company information, industry context, and business challenges, the system generates detailed transformation plans with specific recommendations, technology stacks, and organizational readiness assessments.

## Features

- **Digital Maturity Assessment**: Evaluate organization's current digital maturity across key dimensions
- **Technology Stack Recommendation**: AI-powered suggestions for appropriate technologies and implementation roadmaps
- **Organizational Readiness Assessment**: Evaluate company readiness for transformation with specific recommendations
- **Expert Consultation Simulation**: Generate insights from virtual domain experts
- **Comprehensive Transformation Plans**: Create actionable plans with phased implementation approaches
- **Interactive Visualizations**: Visual representations of maturity scores, implementation timelines, and more
- **LangSmith Integration**: Full tracing and observability of the AI reasoning process

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/digital-transformation-planner.git
   cd digital-transformation-planner
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file with required API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key
   LANGCHAIN_API_KEY=your_langchain_api_key  # Optional, for LangSmith tracing
   LANGCHAIN_PROJECT=your_project_name  # Optional, for LangSmith tracing
   ```

## Usage

1. Start the Streamlit application:
   ```bash
   python -m streamlit run digital_transformation/app.py
   ```

2. Navigate to the application in your browser (usually http://localhost:8501)

3. Enter your company information:
   - Company name and description
   - Industry
   - Transformation goals
   - Business challenges
   - Current technologies

4. Click "Generate Digital Transformation Plan" and wait for the process to complete

5. Explore the results across different tabs:
   - Maturity Assessment
   - Transformation Aspects
   - Expert Consultation
   - Recommendations
   - Transformation Plan
   - Technology Stack
   - Organizational Readiness

## Project Structure

```
digital_transformation/
├── agents/                # AI agents for different processing stages
│   ├── expert_agents.py   # Simulated domain experts
│   ├── maturity.py        # Digital maturity assessment
│   ├── readiness.py       # Organizational readiness assessment
│   └── technology_recommender.py  # Technology stack recommendations
├── schema/                # Data models and schemas
│   ├── assessment.py      # Maturity assessment schemas
│   ├── readiness.py       # Organizational readiness schemas
│   ├── state.py           # LangGraph state definitions
│   └── technology.py      # Technology stack schemas
├── app.py                 # Streamlit user interface
└── main_graph.py          # LangGraph orchestration

requirements.txt           # Project dependencies
.env                       # Environment variables (not in repo)
```

## Technologies

- **Python**: Core programming language
- **LangGraph**: Orchestration of multi-agent AI system
- **LangChain**: LLM framework and components
- **OpenAI**: LLM provider (GPT-4)
- **Streamlit**: User interface
- **Plotly**: Interactive data visualizations
- **LangSmith**: Observability and tracing (optional)

## Configuration

The application can be configured using the following environment variables:

- `OPENAI_API_KEY`: Required for LLM capabilities
- `LANGCHAIN_API_KEY`: Optional, for LangSmith tracing
- `LANGCHAIN_PROJECT`: Optional, project name for LangSmith
- `LANGCHAIN_ENDPOINT`: Optional, default is "https://api.smith.langchain.com"
- `LANGCHAIN_TRACING_V2`: Optional, enables/disables tracing (default: true)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- OpenAI for providing the LLM capabilities
- LangChain for the LangGraph framework
- Streamlit for the interactive web interface 