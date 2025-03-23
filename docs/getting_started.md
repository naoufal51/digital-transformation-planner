# Getting Started with Digital Transformation Planner

This guide will help you quickly set up and start using the Digital Transformation Planner application.

## Prerequisites

Before you begin, ensure you have:

- Python 3.10 or higher installed
- An OpenAI API key (required for LLM functionality)
- Git (optional, for cloning the repository)

## Quick Start

### 1. Installation

First, set up the application:

```bash
# Clone the repository
git clone https://github.com/yourusername/digital-transformation-planner.git
cd digital-transformation-planner

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Create a `.env` file in the project root:

```
# Required
OPENAI_API_KEY=your_openai_api_key

# Optional - for LangSmith tracing
LANGCHAIN_API_KEY=your_langchain_api_key
LANGCHAIN_PROJECT=digital-transformation
LANGCHAIN_TRACING_V2=true
```

### 3. Running the Application

Start the Streamlit application:

```bash
python -m streamlit run digital_transformation/app.py
```

Navigate to http://localhost:8501 in your web browser.

### 4. Using the Demo Company Data

For a quick demonstration, you can use the sample company data:

1. Open the application in your browser
2. Click on "Use example data" or copy the content from `example_company.json`
3. Click "Generate Digital Transformation Plan"

## Understanding the Results

After processing, the application will display results across several tabs:

### Maturity Assessment

Displays the current digital maturity of the organization across dimensions like:
- Customer Experience
- Operations
- Technology Infrastructure
- Data Capabilities
- Organizational Culture

### Technology Stack

Provides technology recommendations including:
- Recommended technology categories
- Specific vendor options
- Implementation roadmap
- Cost estimates and risk factors

### Organizational Readiness

Analyzes how prepared the organization is for transformation:
- Overall readiness score
- Cultural factors
- Skill gaps
- Training needs
- Leadership readiness

### Transformation Plan

Provides a comprehensive plan including:
- Executive summary
- Phased implementation approach
- Specific recommendations
- Success metrics

## Next Steps

After generating your first plan:

1. **Explore Different Scenarios**: Try modifying company information to explore different transformation paths
2. **Export Results**: Use the download options to save results for offline viewing
3. **Iterate**: Refine your inputs based on feedback from stakeholders

## Troubleshooting

If you encounter issues:

- **API Key Errors**: Ensure your OpenAI API key is valid and has sufficient quota
- **Missing Dependencies**: Try running `pip install -r requirements.txt` again
- **Application Errors**: Check the console output for error messages

For additional help, check the project's [GitHub Issues](https://github.com/yourusername/digital-transformation-planner/issues) or submit a new issue. 