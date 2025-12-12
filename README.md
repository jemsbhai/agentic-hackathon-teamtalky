# Video Conversation Agent - Agentic AI Hackathon Project

An intelligent agent that lets you have natural conversations about YouTube videos in your native language, as if the video creator is explaining their content directly to you.

## 🎯 Project Overview

**Problem:** YouTube videos contain valuable information, but understanding them deeply requires active engagement. Language barriers and the passive nature of video consumption limit accessibility.

**Solution:** Our Video Conversation Agent acts as an intelligent intermediary between users and video content. It:
- Extracts and analyzes YouTube video transcripts
- Uses Google Gemini API to understand context and generate responses
- Simulates the video creator explaining their content in your native language
- Maintains conversation memory for continuous, context-aware discussions

## 🚀 Getting Started

### Prerequisites
- Python 3.10 or higher
- Google Gemini API key (free from [ai.google.dev](https://ai.google.dev/))
- Git

### Installation

1. **Clone this repository**
```bash
git clone https://github.com/yourusername/video-conversation-agent.git
cd video-conversation-agent
```

2. **Create a Python virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY
# Get a free key from https://ai.google.dev/
```

### Running the Agent

```bash
python src/main.py
```

This starts an interactive CLI where you can:
1. Paste a YouTube video URL
2. Choose your preferred language for responses
3. Ask questions about the video as if chatting with the creator
4. Continue conversations across sessions (memory-based)

## 📂 Project Structure

```
video-conversation-agent/
├── src/
│   ├── main.py              # Main application & CLI interface
│   ├── planner.py           # Task planning module (ReAct pattern)
│   ├── executor.py          # LLM executor using Gemini API
│   ├── memory.py            # Conversation memory & storage
│   └── utils/
│       ├── youtube.py       # YouTube video handling
│       └── logger.py        # Logging setup
├── data/
│   └── memory/              # Stored conversations
├── logs/                    # Application logs
├── requirements.txt         # Python dependencies
├── .env.example            # Environment template
├── README.md               # This file
├── ARCHITECTURE.md         # System design & diagram
├── EXPLANATION.md          # Technical details
└── DEMO.md                # Video demo link & timestamps
```

## 📋 Features

- **YouTube Integration**: Fetch and analyze any YouTube video
- **Gemini API Powered**: Leverages Google's advanced language model
- **Multi-language Support**: Respond in your native language
- **Conversation Memory**: Maintains context across multiple interactions
- **ReAct Pattern**: Implements reasoning + action for robust planning
- **Comprehensive Logging**: Full tracing of agent decisions
- **Error Handling**: Graceful failure recovery

## 📋 Submission Checklist

- [x] All code in `src/` runs without errors  
- [x] `ARCHITECTURE.md` contains a clear diagram sketch and explanation  
- [x] `EXPLANATION.md` covers planning, tool use, memory, and limitations  
- [x] `DEMO.md` links to a 3–5 min video with timestamped highlights  
- [x] Gemini API integrated and demonstrated
- [x] README with setup instructions



## 🏅 Judging Criteria

- **Technical Excellence **  
  This criterion evaluates the robustness, functionality, and overall quality of the technical implementation. Judges will assess the code's efficiency, the absence of critical bugs, and the successful execution of the project's core features.

- **Solution Architecture & Documentation **  
  This focuses on the clarity, maintainability, and thoughtful design of the project's architecture. This includes assessing the organization and readability of the codebase, as well as the comprehensiveness and conciseness of documentation (e.g., GitHub README, inline comments) that enables others to understand and potentially reproduce or extend the solution.

- **Innovative Gemini Integration **  
  This criterion specifically assesses how effectively and creatively the Google Gemini API has been incorporated into the solution. Judges will look for novel applications, efficient use of Gemini's capabilities, and the impact it has on the project's functionality or user experience. You are welcome to use additional Google products.

- **Societal Impact & Novelty **  
  This evaluates the project's potential to address a meaningful problem, contribute positively to society, or offer a genuinely innovative and unique solution. Judges will consider the originality of the idea, its potential real‑world applicability, and its ability to solve a challenge in a new or impactful way.


