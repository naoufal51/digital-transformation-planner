from langgraph.graph import END, StateGraph, START
from langgraph.pregel import RetryPolicy

from digital_transformation.schema.state import ConsultationState
from digital_transformation.agents.expert_agents import generate_question, generate_answer, sanitize_name


def create_interview_graph(max_turns: int = 5):
    """
    Create a graph for the expert consultation process.
    
    Args:
        max_turns: Maximum number of conversation turns
        
    Returns:
        The compiled interview graph
    """
    
    def route_messages(state: ConsultationState, name: str = "Digital_Transformation_Expert"):
        """
        Route messages based on conversation state.
        
        Args:
            state: Current consultation state
            name: Name of the expert persona
            
        Returns:
            Next node to execute or END
        """
        sanitized_name = sanitize_name(name)
        messages = state["messages"]
        num_responses = len(
            [m for m in messages if m.name == sanitized_name]
        )
        
        # Stop if maximum turns reached
        if num_responses >= max_turns:
            return END
        
        # Check if the consultant has concluded the interview
        last_question = messages[-2] if len(messages) > 1 else None
        if last_question and "This concludes our interview" in last_question.content:
            return END
            
        return "ask_question"
    
    # Build the interview graph
    builder = StateGraph(ConsultationState)
    
    # Add nodes for asking questions and generating answers
    builder.add_node("ask_question", generate_question, retry=RetryPolicy(max_attempts=3))
    builder.add_node("answer_question", generate_answer, retry=RetryPolicy(max_attempts=3))
    
    # Add conditional edges for routing
    builder.add_conditional_edges("answer_question", route_messages)
    builder.add_edge("ask_question", "answer_question")
    
    # Add start edge
    builder.add_edge(START, "ask_question")
    
    # Compile the graph
    return builder.compile(checkpointer=False)


# Create the interview graph with default parameters
interview_graph = create_interview_graph() 