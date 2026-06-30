# graph.py - Multi-Agent System (No LangGraph)
"""
Multi-Agent System - Sequential Flow
Purpose: Connect all agents in sequence
"""

from typing import Dict, List, Any, Optional
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import all agents
from agents.planner_agent import planner_agent
from agents.retriver_agent import retriever_agent
from agents.research_agent import research_agent
from agents.answer_agent import answer_agent


def build_research_graph():
    """
    Build a simple sequential workflow.
    Returns a function that runs all agents in sequence.
    """
    
    def run_workflow(state: Dict) -> Dict:
        """Run all agents in sequence."""
        print("\n" + "=" * 60)
        print("🚀 STARTING MULTI-AGENT WORKFLOW")
        print("=" * 60)
        
        # Step 1: Planner
        print("\n📍 STEP 1: Planner Agent")
        print("-" * 40)
        state = planner_agent(state)
        print(f"Task: {state.get('task', 'Unknown')}")
        print(f"Plan: {state.get('plan', [])}")
        
        # Step 2: Retriever
        print("\n📍 STEP 2: Retriever Agent")
        print("-" * 40)
        state = retriever_agent(state)
        print(f"Retrieved: {len(state.get('retrieved_docs', []))} documents")
        
        # Step 3: Research
        print("\n📍 STEP 3: Research Agent")
        print("-" * 40)
        state = research_agent(state)
        print(f"Research output: {len(state.get('research_output', ''))} characters")
        
        # Step 4: Answer
        print("\n📍 STEP 4: Answer Agent")
        print("-" * 40)
        state = answer_agent(state)
        print(f"Final answer: {len(state.get('final_answer', ''))} characters")
        
        print("\n" + "=" * 60)
        print("✅ WORKFLOW COMPLETE")
        print("=" * 60)
        
        return state
    
    return run_workflow


def run_research_assistant(
    query: str,
    db: Any,
    chunks: List[Any],
    config: Dict = None
) -> Dict:
    """
    Run the complete research assistant workflow.
    """
    # Build the workflow
    workflow = build_research_graph()
    
    # Prepare initial state
    initial_state = {
        "query": query,
        "task": "",
        "plan": [],
        "db": db,
        "chunks": chunks,
        "retrieved_docs": [],
        "research_output": "",
        "final_answer": ""
    }
    
    # Run the workflow
    result = workflow(initial_state)
    
    return result


def streamlit_integration(
    query: str,
    task: str,
    db: Any,
    chunks: List[Any],
    graph: callable = None
) -> str:
    """
    Helper function for Streamlit integration.
    """
    # Build workflow if not provided
    if graph is None:
        graph = build_research_graph()
    
    # Prepare initial state
    initial_state = {
        "query": query,
        "task": task,
        "plan": [],
        "db": db,
        "chunks": chunks,
        "retrieved_docs": [],
        "research_output": "",
        "final_answer": ""
    }
    
    # Run the workflow
    result = graph(initial_state)
    
    # Return only the final answer
    return result.get("final_answer", "No answer generated.")


def run_step_by_step(
    query: str,
    db: Any,
    chunks: List[Any]
) -> Dict:
    """
    Run the workflow step by step for debugging.
    """
    print("\n" + "=" * 60)
    print("🔍 STEP-BY-STEP DEBUGGING MODE")
    print("=" * 60)
    
    # Initialize state
    state = {
        "query": query,
        "task": "",
        "plan": [],
        "db": db,
        "chunks": chunks,
        "retrieved_docs": [],
        "research_output": "",
        "final_answer": ""
    }
    
    # Step 1: Planner
    print("\n📍 STEP 1: Planner Agent")
    print("-" * 40)
    state = planner_agent(state)
    print(f"Query: {state['query']}")
    print(f"Task: {state['task']}")
    print(f"Plan: {state['plan']}")
    
    # Step 2: Retriever
    print("\n📍 STEP 2: Retriever Agent")
    print("-" * 40)
    state = retriever_agent(state)
    print(f"Retrieved: {len(state.get('retrieved_docs', []))} documents")
    
    # Step 3: Research
    print("\n📍 STEP 3: Research Agent")
    print("-" * 40)
    state = research_agent(state)
    print(f"Research output: {len(state.get('research_output', ''))} characters")
    
    # Step 4: Answer
    print("\n📍 STEP 4: Answer Agent")
    print("-" * 40)
    state = answer_agent(state)
    print(f"Final answer: {len(state.get('final_answer', ''))} characters")
    
    print("\n" + "=" * 60)
    print("✅ STEP-BY-STEP COMPLETE")
    print("=" * 60)
    
    return state


print("✅ graph.py loaded successfully")