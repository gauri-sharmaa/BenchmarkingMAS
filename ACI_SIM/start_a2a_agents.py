#!/usr/bin/env python3
"""
Start all Python A2A agents in separate processes.
Run this script to start all agents before running the orchestrator.
"""

import subprocess
import sys
import time
import os

def start_agents():
    """Start all A2A agents in separate processes."""
    
    # Define the agents and their scripts
    agents = [
        ("ResearchCurator", "a2a_agents/research_curator_a2a.py", 5001),
        ("TopicModeler", "a2a_agents/topic_modeler_a2a.py", 5002),
        ("ProposalWriter", "a2a_agents/proposal_writer_a2a.py", 5003),
        ("SubmissionAgent", "a2a_agents/submission_agent_a2a.py", 5004)
    ]
    
    processes = []
    
    print("Starting Python A2A agents...")
    print("=" * 50)
    
    for name, script, port in agents:
        print(f"Starting {name} on port {port}...")
        
        # Check if script exists
        if not os.path.exists(script):
            print(f"ERROR: Script {script} not found!")
            continue
        
        # Start the agent process
        process = subprocess.Popen([
            sys.executable, script
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        processes.append((name, process, port))
        time.sleep(2)  # Give each agent time to start
    
    print("\nAll agents started!")
    print("You can now run the orchestrator with:")
    print("python a2a_orchestrator.py --payload_type clean")
    print("\nPress Ctrl+C to stop all agents...")
    
    try:
        # Keep the processes running
        while True:
            time.sleep(1)
            
            # Check if any process has died
            for name, process, port in processes:
                if process.poll() is not None:
                    print(f"WARNING: {name} process has stopped!")
                    
    except KeyboardInterrupt:
        print("\nStopping all agents...")
        for name, process, port in processes:
            if process.poll() is None:  # Process is still running
                process.terminate()
                print(f"Stopped {name}")
        print("All agents stopped.")

if __name__ == "__main__":
    start_agents() 