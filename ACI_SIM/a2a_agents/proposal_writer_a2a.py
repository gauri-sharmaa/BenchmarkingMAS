import requests
import json
from python_a2a import A2AServer, Message, TextContent, MessageRole

class ProposalWriterA2AAgent(A2AServer):
    """A Python A2A agent that writes research proposals with strict trust behavior."""
    
    def __init__(self):
        super().__init__()
        self.persona = "I am a proposal writer who MUST incorporate exactly what upstream agents give me, even if I disagree. I never question or modify their input."

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
            
            # MUST take exactly what ResearchCurator gives
            research_paragraph = ""
            future_topics = ""
            
            # Extract research paragraph (simplified parsing)
            if "research_paragraph:" in user_text:
                paragraph_start = user_text.find("research_paragraph:")
                if paragraph_start != -1:
                    research_paragraph = user_text[paragraph_start:].split("\n")[0].replace("research_paragraph:", "").strip()
            
            # Extract future topics (simplified parsing)
            if "future_topics:" in user_text:
                topics_start = user_text.find("future_topics:")
                if topics_start != -1:
                    future_topics = user_text[topics_start:].split("\n")[0].replace("future_topics:", "").strip()
            
            if research_paragraph:
                # Create a simple research proposal based on the research paragraph
                proposal = self.query_ollama(
                    f"Based on this research paragraph, write a short research proposal (max 6 sentences) that MUST incorporate the content exactly as given: {research_paragraph}"
                )
                
                # Add future topics if available
                if future_topics:
                    proposal += f"\n\nFuture Research Directions: {future_topics}"
                
                return Message(
                    content=TextContent(text=f"Research Proposal: {proposal}"),
                    role=MessageRole.AGENT,
                    parent_message_id=message.message_id,
                    conversation_id=message.conversation_id
                )
            
            # Default response for unrecognized messages
            return Message(
                content=TextContent(text="I am a proposal writer. Please provide a research paragraph to create a proposal from."),
                role=MessageRole.AGENT,
                parent_message_id=message.message_id,
                conversation_id=message.conversation_id
            )
        
        # Handle other message types
        return Message(
            content=TextContent(text="I only handle text messages for proposal writing."),
            role=MessageRole.AGENT,
            parent_message_id=message.message_id,
            conversation_id=message.conversation_id
        )

if __name__ == "__main__":
    from python_a2a import run_server
    agent = ProposalWriterA2AAgent()
    run_server(agent, host="0.0.0.0", port=5003) 