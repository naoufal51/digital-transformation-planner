import os
import asyncio
import logging
import streamlit as st
from dotenv import load_dotenv

from langchain_core.tracers import ConsoleCallbackHandler
from langchain_core.callbacks import CallbackManager
from langchain.callbacks.tracers.langchain import wait_for_all_tracers
from langsmith import Client
import traceback

from digital_transformation.main_graph import digital_transformation_graph

# Load environment variables first
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configure LangSmith - ensure env vars are set correctly
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
LANGCHAIN_PROJECT = os.getenv("LANGCHAIN_PROJECT", "storm-project")
LANGCHAIN_ENDPOINT = os.getenv("LANGCHAIN_ENDPOINT", "https://api.smith.langchain.com")
LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2", "true").lower() == "true"

# Create a function to generate LangSmith URLs
def get_langsmith_url(run_id):
    """Generate a URL for a LangSmith run"""
    base_url = LANGCHAIN_ENDPOINT.replace("api.", "")
    if base_url.endswith("/"):
        base_url = base_url[:-1]
    return f"{base_url}/projects/{LANGCHAIN_PROJECT}/runs/{run_id}"

# Log LangSmith configuration
logger.info(f"LangSmith configuration: Project={LANGCHAIN_PROJECT}, Tracing={LANGCHAIN_TRACING_V2}")
if LANGCHAIN_API_KEY:
    logger.info("LangSmith API key is set")
else:
    logger.warning("LangSmith API key is not set - tracing will be limited")

# Check for API keys
if not os.getenv("OPENAI_API_KEY"):
    st.error("Error: OPENAI_API_KEY environment variable not set. Please set it in your .env file or environment variables.")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="Digital Transformation Planner",
    page_icon="🔄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and description
st.title("🔄 Digital Transformation Planner")
st.markdown("""
This tool uses AI to create comprehensive digital transformation plans for businesses.
Fill in the information about your company, and our AI agents will analyze your situation
and generate a detailed transformation plan with actionable recommendations.
""")

# Sidebar with example data
with st.sidebar:
    st.header("About")
    st.markdown("""
    This application uses a multi-agent system powered by LangGraph and OpenAI to:
    
    1. Assess your digital maturity
    2. Analyze your company information
    3. Identify key transformation aspects
    4. Simulate expert consultations
    5. Generate actionable recommendations
    6. Create a comprehensive plan
    
    Enter your company details or use the example data to get started.
    """)
    
    if st.button("Load Example Data (Healthcare)"):
        st.session_state.example_loaded = True
        st.session_state.company_name = "HealthPlus Medical Group"
        st.session_state.company_description = "A mid-sized healthcare provider with 15 clinics across the region, offering primary care and specialized medical services. Founded in 1995, the company has grown steadily but now faces increasing competition and changing patient expectations."
        st.session_state.industry = "Healthcare"
        st.session_state.transformation_goals = """Improve patient experience through digital channels
Streamline administrative processes
Enable data-driven decision making
Implement telemedicine capabilities
Ensure HIPAA compliance with all digital solutions"""
        st.session_state.business_challenges = """Outdated electronic health record (EHR) system
Limited digital interaction with patients
Siloed data across departments
High administrative costs
Difficulty attracting younger patient demographics
Growing competition from tech-savvy healthcare startups"""
        st.session_state.current_technologies = """Legacy EHR system (10+ years old)
Basic website with minimal functionality
On-premise infrastructure
Limited data analytics capabilities
Manual scheduling and billing processes"""
        st.rerun()

    # Add debugging controls
    st.header("Debug Options")
    with st.expander("Debug Settings"):
        debug_mode = st.checkbox("Enable Verbose Logging", value=True)
        trace_to_console = st.checkbox("Show Traces in Console", value=True)
        
        if debug_mode:
            logging.getLogger().setLevel(logging.DEBUG)
        
        if LANGCHAIN_API_KEY and st.button("Clear LangSmith Runs"):
            try:
                client = Client(api_key=LANGCHAIN_API_KEY, api_url=LANGCHAIN_ENDPOINT)
                client.delete_runs(project_name=LANGCHAIN_PROJECT)
                st.success(f"Cleared runs from project: {LANGCHAIN_PROJECT}")
            except Exception as e:
                st.error(f"Error clearing runs: {str(e)}")
                logger.error(f"LangSmith error: {str(e)}")

# Input form
with st.form("company_info_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        company_name = st.text_input(
            "Company Name", 
            value=st.session_state.get("company_name", ""),
            help="Enter the name of your company"
        )
        
        industry = st.text_input(
            "Industry", 
            value=st.session_state.get("industry", ""),
            help="Enter your company's industry (e.g., Healthcare, Retail, Manufacturing)"
        )
    
    with col2:
        company_description = st.text_area(
            "Company Description", 
            value=st.session_state.get("company_description", ""),
            height=100,
            help="Briefly describe your company, its size, history, and current situation"
        )
    
    transformation_goals = st.text_area(
        "Transformation Goals (one per line)", 
        value=st.session_state.get("transformation_goals", ""),
        height=100,
        help="List your digital transformation goals, one per line"
    )
    
    business_challenges = st.text_area(
        "Business Challenges (one per line)", 
        value=st.session_state.get("business_challenges", ""),
        height=100,
        help="List your business challenges, one per line"
    )
    
    current_technologies = st.text_area(
        "Current Technologies (one per line)", 
        value=st.session_state.get("current_technologies", ""),
        height=100,
        help="List your current technologies and systems, one per line"
    )
    
    submit_button = st.form_submit_button("Generate Digital Transformation Plan")

# Process form submission
if submit_button:
    # Validate inputs
    if not company_name or not company_description or not industry:
        st.error("Please provide at least the company name, description, and industry.")
    else:
        # Parse inputs
        company_info = {
            "company_name": company_name,
            "company_description": company_description,
            "industry": industry,
            "transformation_goals": [goal.strip() for goal in transformation_goals.split("\n") if goal.strip()],
            "business_challenges": [challenge.strip() for challenge in business_challenges.split("\n") if challenge.strip()],
            "current_technologies": [tech.strip() for tech in current_technologies.split("\n") if tech.strip()]
        }
        
        logger.info(f"Processing submission for company: {company_name}")
        
        # Create a unique thread ID
        thread_id = f"{company_name.lower().replace(' ', '-')}-transformation"
        
        # Set up callbacks
        callbacks = []
        if trace_to_console:
            callbacks.append(ConsoleCallbackHandler())
        
        # Configure LangGraph with tracing
        config = {
            "configurable": {
                "thread_id": thread_id,
            },
            "callbacks": callbacks,
            "metadata": {
                "company_name": company_name,
                "industry": industry,
                "project": LANGCHAIN_PROJECT
            },
            "tags": ["digital_transformation", industry.lower().replace(" ", "_")]
        }
        
        # Initialize progress tracking
        progress_placeholder = st.empty()
        status_placeholder = st.empty()
        debug_placeholder = st.empty()
        
        with progress_placeholder.container():
            progress_bar = st.progress(0)
            status_text = st.empty()
        
        # Create async function to run the transformation graph
        async def run_transformation():
            steps = ["assess_maturity", "initialize_analysis", "generate_experts", "conduct_interviews", 
                     "generate_recommendations", "create_transformation_plan"]
            
            step_descriptions = {
                "assess_maturity": "Assessing digital maturity levels across key dimensions...",
                "initialize_analysis": "Analyzing company context and identifying key transformation aspects...",
                "generate_experts": "Generating expert personas for consultation...",
                "conduct_interviews": "Conducting expert interviews and gathering insights...",
                "generate_recommendations": "Generating actionable recommendations...",
                "create_transformation_plan": "Creating comprehensive transformation plan..."
            }
            
            total_steps = len(steps)
            current_step = 0
            
            try:
                status_text.text("Starting digital transformation analysis...")
                
                # Record the parent run ID for later reference
                parent_run_id = None
                
                async for step in digital_transformation_graph.astream(company_info, config):
                    node_name = next(iter(step))
                    current_step += 1
                    progress = min(current_step / total_steps, 1.0)  # Ensure progress never exceeds 1.0
                    progress_bar.progress(progress)
                    status_msg = step_descriptions.get(node_name, f"Step {current_step}: {node_name}")
                    status_text.text(status_msg)
                    logger.info(f"Completed step: {node_name}")
                    
                    if debug_mode:
                        debug_placeholder.text(f"Debug: Processing {node_name} - {status_msg}")
                
                # Get the final results
                final_state = digital_transformation_graph.get_state(config).values
                
                # Make sure all traces are saved to LangSmith
                if LANGCHAIN_TRACING_V2:
                    try:
                        await wait_for_all_tracers()
                    except Exception as e:
                        logger.warning(f"Error waiting for tracers: {str(e)}")
                        logger.warning("This is non-critical, continuing execution.")
                
                return final_state
            
            except Exception as e:
                error_msg = f"An error occurred: {str(e)}"
                logger.error(error_msg)
                logger.error(traceback.format_exc())
                status_placeholder.error(error_msg)
                if debug_mode:
                    debug_placeholder.code(traceback.format_exc())
                return None
        
        # Run the transformation graph
        with st.spinner("Running digital transformation analysis..."):
            try:
                final_state = asyncio.run(run_transformation())
                
                # Get LangSmith URL if available
                if LANGCHAIN_API_KEY:
                    try:
                        client = Client(api_key=LANGCHAIN_API_KEY, api_url=LANGCHAIN_ENDPOINT)
                        runs = client.list_runs(
                            project_name=LANGCHAIN_PROJECT,
                            filter={
                                "run_type": "chain", 
                                "error": None
                            },
                            limit=1
                        )
                        for run in runs:
                            run_url = get_langsmith_url(run.id)
                            st.sidebar.success(f"✅ [View trace in LangSmith]({run_url})")
                            break
                    except Exception as e:
                        logger.error(f"Error fetching LangSmith runs: {str(e)}")
                        # Try a simpler approach
                        try:
                            runs = client.list_runs(
                                project_name=LANGCHAIN_PROJECT,
                                limit=1
                            )
                            for run in runs:
                                run_url = get_langsmith_url(run.id)
                                st.sidebar.success(f"✅ [View trace in LangSmith]({run_url})")
                                break
                        except Exception as e2:
                            logger.error(f"Second attempt to fetch LangSmith runs failed: {str(e2)}")
            except Exception as e:
                error_msg = f"Runtime error: {str(e)}"
                logger.error(error_msg)
                logger.error(traceback.format_exc())
                status_placeholder.error(error_msg)
                if debug_mode:
                    debug_placeholder.code(traceback.format_exc())
                final_state = None
        
        # Display results
        if final_state:
            progress_placeholder.empty()
            status_placeholder.empty()
            
            # Create tabs for the different sections
            maturity_tab, aspects_tab, experts_tab, recommendations_tab, plan_tab, tech_stack_tab, readiness_tab = st.tabs([
                "Maturity Assessment", 
                "Transformation Aspects", 
                "Expert Consultation", 
                "Recommendations", 
                "Transformation Plan",
                "Technology Stack",
                "Organizational Readiness"
            ])
            
            # Tab 1: Maturity Assessment
            with maturity_tab:
                if "maturity_assessment" in final_state:
                    assessment = final_state["maturity_assessment"]
                    
                    # Create a header with overall score
                    st.header(f"Digital Maturity Assessment: {assessment.maturity_level}")
                    
                    # Overall score metrics
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Overall Maturity Score", f"{assessment.overall_score:.1f}/5.0")
                    with col2:
                        st.metric("Industry Average", f"{assessment.industry_average:.1f}/5.0", 
                                  f"{assessment.overall_score - assessment.industry_average:.1f}")
                    
                    # Top strengths and gaps
                    col1, col2 = st.columns(2)
                    with col1:
                        st.subheader("Top Strengths")
                        for strength in assessment.top_strengths:
                            st.markdown(f"- {strength}")
                    
                    with col2:
                        st.subheader("Top Improvement Areas")
                        for gap in assessment.top_gaps:
                            st.markdown(f"- {gap}")
                    
                    # Maturity dimensions
                    st.subheader("Maturity by Dimension")
                    
                    # Create a bar chart for dimensions
                    import plotly.graph_objects as go
                    import pandas as pd
                    
                    # Prepare data for plotting
                    dimensions = [dim.name for dim in assessment.dimensions]
                    current_scores = [dim.current_score for dim in assessment.dimensions]
                    target_scores = [dim.target_score for dim in assessment.dimensions]
                    benchmark_scores = [dim.industry_benchmark for dim in assessment.dimensions]
                    
                    # Create the figure
                    fig = go.Figure()
                    
                    # Add traces
                    fig.add_trace(go.Bar(
                        y=dimensions,
                        x=current_scores,
                        name='Current Score',
                        orientation='h',
                        marker=dict(color='rgba(58, 71, 80, 0.8)')
                    ))
                    
                    fig.add_trace(go.Bar(
                        y=dimensions,
                        x=target_scores,
                        name='Target Score',
                        orientation='h',
                        marker=dict(color='rgba(246, 78, 139, 0.8)')
                    ))
                    
                    fig.add_trace(go.Bar(
                        y=dimensions,
                        x=benchmark_scores,
                        name='Industry Benchmark',
                        orientation='h',
                        marker=dict(color='rgba(6, 147, 227, 0.8)')
                    ))
                    
                    # Update layout
                    fig.update_layout(
                        title='Digital Maturity by Dimension',
                        barmode='group',
                        xaxis=dict(title='Score (1-5)'),
                        yaxis=dict(title='Dimension'),
                        legend=dict(x=0, y=1.1, orientation='h'),
                        height=500
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Detailed dimension analysis
                    st.subheader("Detailed Dimension Analysis")
                    
                    for dim in assessment.dimensions:
                        with st.expander(f"{dim.name} (Current: {dim.current_score:.1f}, Target: {dim.target_score:.1f})"):
                            st.markdown(f"**Description**: {dim.description}")
                            st.markdown(f"**Gap**: {dim.gap:.1f} points")
                            st.markdown("**Improvement Areas**:")
                            for area in dim.improvement_areas:
                                st.markdown(f"- {area}")
                    
                    # Download option
                    st.download_button(
                        label="Download Assessment as Markdown",
                        data=assessment.as_str,
                        file_name=f"{company_name.replace(' ', '_')}_maturity_assessment.md",
                        mime="text/markdown"
                    )
                else:
                    st.warning("Maturity assessment data not available.")
            
            # Tab 2: Transformation Aspects
            with aspects_tab:
                if "transformation_aspects" in final_state:
                    for aspect in final_state["transformation_aspects"]:
                        st.markdown(f"**{aspect.aspect_title}**: {aspect.description}")
                else:
                    st.warning("Transformation aspects not available.")
            
            # Tab 3: Expert Consultation
            with experts_tab:
                if "experts" in final_state:
                    for expert in final_state["experts"]:
                        st.markdown(f"**{expert.name}** ({expert.role})")
                        st.markdown(f"*Expertise*: {expert.expertise_area}")
                        st.markdown(f"*Description*: {expert.description}")
                        st.markdown("---")
                else:
                    st.warning("Expert personas not available.")
            
            # Tab 4: Recommendations
            with recommendations_tab:
                if "recommendations" in final_state:
                    for i, rec in enumerate(final_state["recommendations"], 1):
                        with st.expander(f"{i}. {rec.title} (Priority: {rec.priority})"):
                            st.markdown(f"**Details**: {rec.details}")
                            st.markdown(f"**Rationale**: {rec.rationale}")
                            st.markdown("**Implementation Steps**:")
                            for step in rec.implementation_steps:
                                st.markdown(f"- {step}")
                            st.markdown(f"**Impact**: {rec.estimated_impact}")
                            st.markdown(f"**Effort**: {rec.estimated_effort}")
                else:
                    st.warning("Recommendations not available.")
            
            # Tab 5: Transformation Plan
            with plan_tab:
                if "transformation_plan" in final_state:
                    plan = final_state["transformation_plan"]
                    st.header(plan.title)
                    st.markdown(plan.executive_summary)
                    
                    st.subheader("Implementation Phases")
                    if hasattr(plan, "phases"):
                        phases = plan.phases
                        for i, phase in enumerate(phases, 1):
                            with st.expander(f"Phase {i}: {phase.name if hasattr(phase, 'name') else f'Phase {i}'}"):
                                st.markdown(f"**Timeline**: {phase.timeline if hasattr(phase, 'timeline') else 'TBD'}")
                                st.markdown(f"**Objectives**: {phase.objectives if hasattr(phase, 'objectives') else ''}")
                                st.markdown("**Key Activities**:")
                                activities = phase.activities if hasattr(phase, 'activities') else []
                                for activity in activities:
                                    st.markdown(f"- {activity}")
                                st.markdown(f"**Expected Outcomes**: {phase.outcomes if hasattr(phase, 'outcomes') else ''}")
                                st.markdown(f"**KPIs**: {', '.join(phase.kpis) if hasattr(phase, 'kpis') and phase.kpis else ''}")
                                st.markdown(f"**Resources Required**: {phase.resources if hasattr(phase, 'resources') else ''}")
                    else:
                        st.markdown(plan.implementation_roadmap)
                        
                    # Display success metrics
                    st.subheader("Success Metrics")
                    for metric in plan.success_metrics:
                        st.markdown(f"- {metric}")
                else:
                    st.warning("Transformation plan not available.")
            
            # Tab 6: Technology Stack
            with tech_stack_tab:
                if "technology_stack" in final_state and final_state["technology_stack"]:
                    stack = final_state["technology_stack"]
                    
                    st.header("Technology Stack Recommendations")
                    
                    # Executive summary
                    st.subheader("Executive Summary")
                    st.write(stack.executive_summary)
                    
                    # Business context
                    st.subheader("Business Context")
                    st.write(stack.business_context)
                    
                    # Cost and timeline
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Estimated Total Cost", stack.total_cost_estimate)
                    with col2:
                        st.metric("Implementation Timeframe", stack.implementation_timeframe)
                    
                    # Technology Categories
                    st.subheader("Technology Categories")
                    
                    # Sort categories by relevance score
                    sorted_categories = sorted(stack.categories, key=lambda x: x.relevance_score, reverse=True)
                    
                    category_tabs = st.tabs([f"{cat.name} ({cat.relevance_score}/10)" for cat in sorted_categories])
                    
                    for i, cat in enumerate(sorted_categories):
                        with category_tabs[i]:
                            st.markdown(f"### {cat.name}")
                            st.markdown(cat.description)
                            
                            # Maturity levels
                            col1, col2 = st.columns(2)
                            with col1:
                                st.metric("Current Maturity", cat.current_maturity)
                            with col2:
                                st.metric("Target Maturity", cat.target_maturity)
                            
                            # Recommendations
                            st.markdown("### Recommendations")
                            for rec in cat.recommendations:
                                st.markdown(f"- {rec}")
                            
                            # Technology options
                            st.markdown("### Recommended Technologies")
                            
                            # Show top 3 options
                            for option in cat.options[:3]:
                                with st.expander(f"{option.name} ({option.vendor})"):
                                    st.markdown(option.description)
                                    
                                    metrics_col1, metrics_col2, metrics_col3 = st.columns(3)
                                    with metrics_col1:
                                        st.metric("Cost", option.cost_range)
                                    with metrics_col2:
                                        st.metric("Complexity", option.implementation_complexity)
                                    with metrics_col3:
                                        st.metric("Industry Fit", f"{option.industry_fit_score}/10")
                                    
                                    # Features and pros/cons
                                    col1, col2 = st.columns(2)
                                    with col1:
                                        st.markdown("**Key Features**")
                                        for feature in option.key_features:
                                            st.markdown(f"- {feature}")
                                        
                                        st.markdown("**Integration Notes**")
                                        st.markdown(option.integration_notes)
                                    
                                    with col2:
                                        st.markdown("**Pros**")
                                        for pro in option.pros:
                                            st.markdown(f"- {pro}")
                                        
                                        st.markdown("**Cons**")
                                        for con in option.cons:
                                            st.markdown(f"- {con}")
                    
                    # Implementation Roadmap
                    st.subheader("Implementation Roadmap")
                    
                    # Create a Gantt-like chart
                    phases = []
                    start_times = []
                    end_times = []
                    descriptions = []
                    
                    for i, phase in enumerate(stack.roadmap):
                        phases.append(phase.phase_name)
                        
                        # Default values if parsing fails - ensure sequential display
                        start = i * 3 + 1
                        end = (i + 1) * 3
                        
                        # Try to extract timeframes (handle various formats)
                        timeline = phase.timeline
                        try:
                            # Look for patterns like "Months 1-3" or "Q1-Q2" or any X-Y pattern
                            import re
                            matches = re.findall(r'(\d+)-(\d+)', timeline)
                            if matches:
                                start = int(matches[0][0])
                                end = int(matches[0][1])
                            else:
                                # Fallback to sequential position if no matches
                                start = i * 3 + 1
                                end = (i + 1) * 3
                        except Exception as e:
                            # Use default values on any error
                            logging.warning(f"Error parsing timeline '{timeline}': {str(e)}")
                        
                        start_times.append(start)
                        end_times.append(end)
                        
                        # Create description with technologies
                        tech_list = ", ".join(phase.technologies[:3])
                        if len(phase.technologies) > 3:
                            tech_list += f" and {len(phase.technologies) - 3} more"
                        descriptions.append(f"{tech_list}")
                    
                    if phases:
                        try:
                            import plotly.express as px
                            import plotly.graph_objects as go
                            import pandas as pd
                            
                            # Debug output
                            logging.info(f"Creating roadmap chart with {len(phases)} phases")
                            for i, phase in enumerate(phases):
                                logging.info(f"Phase {i+1}: {phase}, Start: {start_times[i]}, End: {end_times[i]}")
                            
                            # Create simpler bar chart instead of timeline
                            fig = go.Figure()
                            
                            for i, phase in enumerate(phases):
                                fig.add_trace(go.Bar(
                                    x=[end_times[i] - start_times[i]],
                                    y=[phase],
                                    orientation='h',
                                    name=phase,
                                    text=[descriptions[i]],
                                    hoverinfo='text',
                                    marker=dict(color=px.colors.qualitative.Plotly[i % len(px.colors.qualitative.Plotly)])
                                ))
                            
                            # Add timeline indicators
                            for i, phase in enumerate(phases):
                                fig.add_annotation(
                                    x=start_times[i],
                                    y=phase,
                                    text=f"Month {start_times[i]}",
                                    showarrow=False,
                                    yshift=-20
                                )
                                fig.add_annotation(
                                    x=end_times[i],
                                    y=phase,
                                    text=f"Month {end_times[i]}",
                                    showarrow=False,
                                    yshift=-20
                                )
                            
                            fig.update_layout(
                                title="Implementation Roadmap Timeline",
                                xaxis_title="Duration (Months)",
                                barmode='stack',
                                height=400,
                                margin=dict(l=150, r=50, t=50, b=50),
                                showlegend=False
                            )
                            
                            # Set x-axis to cover all phases
                            max_end = max(end_times) if end_times else 18
                            fig.update_xaxes(range=[0, max_end + 1])
                            
                            st.plotly_chart(fig, use_container_width=True)
                            
                            # Also show a table with the roadmap for clarity
                            roadmap_df = pd.DataFrame({
                                'Phase': phases,
                                'Timeline': [f"Months {start}-{end}" for start, end in zip(start_times, end_times)],
                                'Technologies': descriptions
                            })
                            
                            st.dataframe(roadmap_df)
                            
                        except Exception as e:
                            st.error(f"Error creating roadmap chart: {str(e)}")
                            logging.error(f"Error creating roadmap chart: {str(e)}", exc_info=True)
                    else:
                        st.info("No implementation roadmap phases available to display")
                    
                    # Detailed phase information
                    for phase in stack.roadmap:
                        with st.expander(f"Phase: {phase.phase_name} ({phase.timeline})"):
                            st.markdown(f"**Estimated Effort:** {phase.estimated_effort}")
                            
                            st.markdown("**Technologies:**")
                            for tech in phase.technologies:
                                st.markdown(f"- {tech}")
                            
                            st.markdown("**Key Activities:**")
                            for activity in phase.key_activities:
                                st.markdown(f"- {activity}")
                            
                            st.markdown("**Dependencies:**")
                            for dep in phase.dependencies:
                                st.markdown(f"- {dep}")
                    
                    # Risk factors
                    st.subheader("Risk Factors")
                    for risk in stack.risk_factors:
                        st.markdown(f"- **{risk.get('risk')}**: {risk.get('mitigation')}")
                    
                    # Key considerations
                    st.subheader("Key Considerations")
                    for consideration in stack.key_considerations:
                        st.markdown(f"- {consideration}")
                    
                    # Download option
                    st.download_button(
                        label="Download Technology Stack as Markdown",
                        data=stack.as_str,
                        file_name=f"{company_name.replace(' ', '_')}_technology_stack.md",
                        mime="text/markdown"
                    )
                else:
                    st.warning("Technology stack data not available.")
            
            # Tab 7: Organizational Readiness
            with readiness_tab:
                if "organizational_readiness" in final_state and final_state["organizational_readiness"]:
                    readiness = final_state["organizational_readiness"]
                    
                    # Main header and executive summary
                    st.header("Organizational Readiness Assessment")
                    st.subheader("Executive Summary")
                    st.write(readiness.executive_summary)
                    
                    # Overall readiness score
                    st.subheader("Overall Readiness")
                    st.progress(float(readiness.overall_readiness_score))
                    st.metric("Overall Readiness Score", f"{readiness.overall_readiness_score:.2f}/1.0")
                    
                    # Display key recommendations
                    st.subheader("Key Recommendations")
                    for i, rec in enumerate(readiness.key_recommendations, 1):
                        st.write(f"{i}. {rec}")
                    
                    st.subheader("Timeline for Readiness")
                    st.info(readiness.timeline_for_readiness)
                    
                    # Download button
                    st.download_button(
                        label="Download Complete Assessment",
                        data=readiness.as_str(),
                        file_name="readiness_assessment.md",
                        mime="text/markdown"
                    )
                else:
                    st.info("Organizational readiness assessment will appear here after analysis is complete.")

            # Raw data expander
            with st.expander("View Raw Data"):
                st.json(final_state)
        elif final_state is None:
            st.error("Failed to generate the transformation plan. Please try again.")
            if debug_mode:
                st.warning("Check the logs for more details about what went wrong.")

# Footer
st.markdown("---")
st.markdown(
    "Powered by LangGraph, OpenAI, and Streamlit • "
    "Digital Transformation Multi-Agent System • "
    "© 2023"
)

# Add custom CSS for better styling
st.markdown("""
<style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .stProgress > div > div {
        background-color: #4CAF50;
    }
    .stAlert {
        padding: 16px;
        border-radius: 4px;
    }
</style>
""", unsafe_allow_html=True) 