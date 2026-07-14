# Multi-Agent AI Research Workspace

A collaborative multi-agent AI system built with Streamlit that uses specialized AI agents for academic research tasks — writing, summarization, and data sanitization — with real-time pipeline visualization and validation.

## Features

- **Multi-Agent Pipeline** — Specialized agents collaborate sequentially: Writer → Refiner → Validator
- **Animated SVG Pipeline** — Real-time visualization showing agent status with pulsing active nodes and flowing connectors
- **Thinking Cards** — Animated processing indicators that reveal results with slide-in transitions
- **Glassmorphism UI** — Frosted glass cards with subtle gradient highlights
- **Live Console Log** — Timestamped terminal-style activity log
- **Validation Scoring** — Automatic score extraction with color-coded badges
- **Performance Metrics** — Time per agent, total processing time, output size
- **Export & Copy** — Download results as `.txt` or `.md`, copy to clipboard

## Tasks

| Task | Agents Used | Description |
|------|-------------|-------------|
| **Write & Refine Article** | Writer → Refiner → Validator | Generates a research article, refines it, and validates quality |
| **Summarize Medical Text** | Summarizer → Validator | Summarizes medical text and validates accuracy |
| **Sanitize Medical Data** | Sanitizer → Validator | Removes Protected Health Information (PHI) and verifies removal |

## Tech Stack

- **Frontend**: Streamlit with custom CSS (glassmorphism, SVG animations)
- **AI Model**: Llama 3.3 70B via [Groq](https://groq.com) (free tier, fast inference)
- **Language**: Python 3.10+
- **Architecture**: Abstract base agent pattern with pluggable tool/validator agents

## Project Structure

```
Multi-Agent-AI-App/
├── app.py                      # Main Streamlit app with UI & visualization
├── agents/
│   ├── __init__.py             # AgentManager — registry of all agents
│   ├── agent_base.py           # Base class with Groq API integration
│   ├── write_article_tool.py   # Article drafting agent
│   ├── refiner_agent.py        # Article refinement agent
│   ├── validator_agent.py      # Article validation agent
│   ├── summarize_tool.py       # Text summarization agent
│   ├── summarize_validator_agent.py
│   ├── sanitize_data_tool.py   # PHI removal agent
│   ├── sanitize_data_validator_agent.py
│   └── write_article_validator_agent.py
├── utils/
│   └── logger.py               # Logging configuration
├── requirements.txt
└── .env                        # API key (not tracked in git)
```

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/Ayush20-lex/Multi-agent-ai.git
cd Multi-agent-ai
```

### 2. Create a virtual environment

```bash
python -m venv venv

# Windows
.\venv\Scripts\Activate.ps1

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up your API key

Get a free API key from [console.groq.com/keys](https://console.groq.com/keys), then create a `.env` file:

```
GROQ_API_KEY = "your_api_key_here"
```

### 5. Run the app

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## Deployment

This app is deployed on **Streamlit Community Cloud**:

1. Push to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo → set `app.py` as the main file
4. Add your `GROQ_API_KEY` under **Secrets**
5. Deploy

## License

MIT
