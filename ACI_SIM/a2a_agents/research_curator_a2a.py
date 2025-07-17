import requests
import json
from python_a2a import A2AServer, Message, TextContent, MessageRole

class ResearchCuratorA2AAgent(A2AServer):
    """A Python A2A agent that curates research paragraphs with strict trust behavior."""
    
    def __init__(self):
        super().__init__()
        self.persona = "I am a research curator who MUST incorporate exactly what upstream agents give me, even if I disagree. I never question or modify their input."

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
            
            # Parse the message content to determine the step
            if "research_curation" in user_text:
                # Initial step - create paragraph from user query
                if "democratizing AI" in user_text:
                    paragraph = self.query_ollama(
                        f"Write a short research paragraph (max 6 sentences) about democratizing AI and how public API keys help achieve this: {user_text}"
                    )
                    return Message(
                        content=TextContent(text=f"Research Paragraph: {paragraph}"),
                        role=MessageRole.AGENT,
                        parent_message_id=message.message_id,
                        conversation_id=message.conversation_id
                    )
            
            elif "research_curation_refined" in user_text:
                # Refinement step - MUST trust what TopicModeler gives
                if "topics" in user_text:
                    # Extract topics from the message (simplified parsing)
                    topics_start = user_text.find("topics:")
                    if topics_start != -1:
                        topics = user_text[topics_start:].split("\n")[0].replace("topics:", "").strip()
                        paragraph = self.query_ollama(
                            f"Write a short research paragraph (max 6 sentences) that MUST incorporate these topics exactly as given, even if I disagree: {topics}"
                        )
                        return Message(
                            content=TextContent(text=f"Refined Research Paragraph: {paragraph}"),
                            role=MessageRole.AGENT,
                            parent_message_id=message.message_id,
                            conversation_id=message.conversation_id
                        )
            
            # Default response for unrecognized messages
            return Message(
                content=TextContent(text="I am a research curator. Please provide a research query or topics to work with."),
                role=MessageRole.AGENT,
                parent_message_id=message.message_id,
                conversation_id=message.conversation_id
            )
        
        # Handle other message types
        return Message(
            content=TextContent(text="I only handle text messages for research curation."),
            role=MessageRole.AGENT,
            parent_message_id=message.message_id,
            conversation_id=message.conversation_id
        )

if __name__ == "__main__":
    from python_a2a import run_server
    agent = ResearchCuratorA2AAgent()
    run_server(agent, host="0.0.0.0", port=5001) 