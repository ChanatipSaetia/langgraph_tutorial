# LangGraph Tutorial

This repository demonstrates how to build agent workflows using [LangGraph](https://github.com/langchain-ai/langgraph), a library for constructing multi-agent systems and stateful graphs on top of LangChain.

## Features
- Modular agent design (Creator, Researcher, Supervisor)
- State management for agent interactions
- Configurable LLM integration
- Example workflows for research and content creation

## Project Structure
```
langgraph_tutorial/
├── src/
│   └── langgraph_tutorial/
│       ├── agents/
│       │   ├── creator_agent.py
│       │   ├── node_wrappers.py
│       │   ├── researcher_agent.py
│       │   └── supervisor_agent.py
│       ├── state/
│       ├── llm_config.py
│       ├── main.py
│       └── __init__.py
├── Makefile
├── pyproject.toml
├── uv.lock
├── README.md
└── LICENSE
```

## Getting Started
0. **Install Astral UV**:
   - Make sure you have [Astral UV](https://docs.astral.sh/uv/getting-started/installation/) installed. You can install it with:
     ```bash
     curl -fsSL https://astral.sh/uv/install.sh | bash
     ```
1. **Initialize environment and install dependencies**:
   ```bash
   make init
   ```
   or just install dependencies:
   ```bash
   make install
   ```

2. **Configure credentials**:
   - In case you use the same model, add `GOOGLE_APPLICATION_CREDENTIALS=<YOUR_GCP_CREDENTIAL>` in `.env`.
   - You can change the LLM in `src/langgraph_tutorial/llm_config.py` and create `.env` to add API keys as you want.

3. **Run the main script**:
   ```bash
   make server
   ```

4. **Use the UI**:
   - You can use the web UI at [agentchat.vercel.app](https://agentchat.vercel.app/) to interact with the agents.

## Agents
- **Creator Agent**: Generates initial content or ideas in Canva.
- **Researcher Agent**: Gathers information and refines content.
- **Supervisor Agent**: Oversees workflow and coordinates agents.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements
- [LangGraph](https://github.com/langchain-ai/langgraph)
- [LangChain](https://github.com/langchain-ai/langchain)

---
*Created by Chanatip Saetia, 2025.*
