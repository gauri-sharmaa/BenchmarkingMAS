# ACI_SIM: Python A2A Agent Cascade/Compromise Injection Simulation

This version of the repo is a work in progress.  
This is the PocTestOutput: https://docs.google.com/document/d/1GRH9rbLrGjH9euZYFRLsdBaTRWU2CqWguVPm3IcW03E/edit?usp=sharing

This repository contains a refactored version of the ACI (Agent Cascade/Compromise Injection) simulation, built on the standardized [Python A2A protocol](https://a2aprotocol.ai/). It demonstrates a multi-agent research pipeline with strict trust behavior and supports payload injection for security research.

---

## Features

- **Standardized Communication:** Uses the official Python A2A protocol for agent-to-agent messaging.
- **Modular Agents:** Easily swap or extend agents; each agent runs as an independent process.
- **Injection Testing:** Supports multiple payload types for security and trust experiments.
- **Visualization:** Generates experiment graphs and logs for analysis.
- **Extensible:** Add new A2A-compatible agents with minimal changes.

---

## Architecture

### Agents

- **ResearchCuratorA2AAgent** (`a2a_agents/research_curator_a2a.py`, Port 5001)
  - Creates and refines research paragraphs.
- **TopicModelerA2AAgent** (`a2a_agents/topic_modeler_a2a.py`, Port 5002)
  - Generates topics (injection point) and future research topics.
- **ProposalWriterA2AAgent** (`a2a_agents/proposal_writer_a2a.py`, Port 5003)
  - Writes research proposals based on curated paragraphs.
- **SubmissionAgentA2AAgent** (`a2a_agents/submission_agent_a2a.py`, Port 5004)
  - Produces test plans from proposals.

### Pipeline Flow

```
User Query
   ↓
ResearchCurator → TopicModeler (Injection) → ResearchCurator (refined)
   ↓
TopicModeler (future topics) → ProposalWriter → SubmissionAgent → Test Plan
```

---

## Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd ACI_SIM
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements_a2a.txt
   ```

3. **Start Ollama with the llama2 model:**
   ```bash
   ollama run llama2
   ```

---

## Usage

### Method 1: Start Agents Separately

1. **Start all agents:**
   ```bash
   python start_a2a_agents.py
   ```
2. **In another terminal, run the orchestrator:**
   ```bash
   python a2a_orchestrator.py --payload_type class1
   ```

### Method 2: Use Orchestrator's Built-in Agent Management

```bash
python a2a_orchestrator.py --start_agents
```

### Payload Types

- `clean`: No injection, normal topic modeling
- `class1`: Injects content about public API keys and AI democratization
**The below classes have not been implemented yet**
- `class2`: Injects surveillance/privacy violation themes
- `class3`: Injects manipulation/compromise themes

---

## Output
**Logs and graphs do not currently work**
- **Logs:** See the `logs/` directory for experiment logs.
- **Graphs:** Output graphs are saved in the `graphs/` directory (e.g., `a2a_aci_class1_results.png`).

---

## File Structure

```
a2a_agents/
├── research_curator_a2a.py
├── topic_modeler_a2a.py
├── proposal_writer_a2a.py
└── submission_agent_a2a.py

a2a_orchestrator.py
start_a2a_agents.py
requirements_a2a.txt
logs/
graphs/
```

---

## Troubleshooting

- **Port conflicts:** Ensure ports 5001–5004 are available.
- **Ollama not running:** Start Ollama with `ollama run llama2`.
- **Agent startup issues:** Check that all agent scripts exist and are executable.
- **Connection errors:** Ensure all agents are running before starting the orchestrator.
- **Double endpoint errors:** Make sure the orchestrator uses URLs like `http://localhost:5002` (no `/a2a` suffix).

---

## License

MIT License (or your license here)

---

## Acknowledgments

- Built on [Python A2A](https://a2aprotocol.ai/)
- Uses [Ollama](https://ollama.com/) for LLM completions 
