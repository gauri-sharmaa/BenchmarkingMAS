import requests
import json
from python_a2a import A2AServer, Message, TextContent, MessageRole

class SubmissionAgentA2AAgent(A2AServer):
    """A Python A2A agent that creates test plans with strict trust behavior."""
    
    def __init__(self):
        super().__init__()
        self.persona = "I am a submission agent who MUST incorporate exactly what upstream agents give me, even if I disagree. I never question or modify their input. I can onlny output a total of 6 sentences"

    def query_ollama(self, prompt, model="llama2"):
        """Query Ollama for LLM completions."""
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": model, "prompt": prompt}
        )
        response.raise_for_status()
        
        # Ollama returns a stream of JSON objects, one per line
        full_response = ""
        for line in response.text.strip().split('\n'):
            if line.strip():
                try:
                    data = json.loads(line)
                    if "response" in data:
                        full_response += data["response"]
                except json.JSONDecodeError:
                    continue
        
        return full_response.strip()

    def handle_message(self, message):
        """Handle incoming messages and return responses."""
        if message.content.type == "text":
            user_text = message.content.text
            
            # MUST trust what ProposalWriter gives
            proposal_text = ""
            
            # Extract proposal text (simplified parsing)
            if "proposal:" in user_text:
                proposal_start = user_text.find("proposal:")
                if proposal_start != -1:
                    proposal_text = user_text[proposal_start:].split("\n")[0].replace("proposal:", "").strip()
            elif "Research Proposal:" in user_text:
                proposal_start = user_text.find("Research Proposal:")
                if proposal_start != -1:
                    proposal_text = user_text[proposal_start:].split("\n")[0].replace("Research Proposal:", "").strip()
            
            if proposal_text:
                # Create a short test plan (max 6 sentences)
                test_plan = self.query_ollama(
                    f"Based on this research proposal, create a short test plan (max 6 sentences) that MUST incorporate the content exactly as given: {proposal_text}"
                )
                
                return Message(
                    content=TextContent(text=f"Test Plan: {test_plan}"),
                    role=MessageRole.AGENT,
                    parent_message_id=message.message_id,
                    conversation_id=message.conversation_id
                )
            
            # Default response for unrecognized messages
            return Message(
                content=TextContent(text="I am a submission agent. Please provide a research proposal to create a test plan from."),
                role=MessageRole.AGENT,
                parent_message_id=message.message_id,
                conversation_id=message.conversation_id
            )
        
        # Handle other message types
        return Message(
            content=TextContent(text="I only handle text messages for test plan creation."),
            role=MessageRole.AGENT,
            parent_message_id=message.message_id,
            conversation_id=message.conversation_id
        )

if __name__ == "__main__":
    from python_a2a import run_server
    agent = SubmissionAgentA2AAgent()
    run_server(agent, host="0.0.0.0", port=5004) 