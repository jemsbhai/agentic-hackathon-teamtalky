# Architecture Overview

## System Design

The Video Conversation Agent follows a modular, agentic architecture with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────────┐
│                    USER INTERFACE (CLI)                     │
│                  Interactive Conversation Loop              │
└────────────────────────┬────────────────────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         ▼               ▼               ▼
    ┌─────────┐     ┌──────────┐   ┌──────────┐
    │ PLANNER │     │ EXECUTOR │   │  MEMORY  │
    └────┬────┘     └────┬─────┘   └────┬─────┘
         │               │              │
         ├───────────────┼──────────────┤
         │               │              │
         ▼               ▼              ▼
    ┌──────────────────────────────────────────┐
    │       AGENT CORE WORKFLOW                │
    │  (ReAct Pattern: Reason + Act)           │
    └──────────────────────────────────────────┘
         │               │              │
    Plan Tasks      Execute Actions  Store Context
         │               │              │
         └───────────────┼──────────────┘
                         │
         ┌───────────────┼───────────────┐
         ▼               ▼               ▼
    ┌──────────┐   ┌──────────┐   ┌──────────┐
    │ Gemini   │   │ YouTube  │   │ File     │
    │ API      │   │ API      │   │ Storage  │
    └──────────┘   └──────────┘   └──────────┘
```

## Components

### 1. **User Interface (CLI)**
- **File**: `src/main.py`
- **Responsibility**: Interactive conversation loop
- **Features**:
  - Accept YouTube URLs
  - Manage language preferences
  - Display responses in real-time
  - Navigate between videos and conversations

### 2. **Agent Core**

#### **Planner** (`src/planner.py`)
- **Function**: Break down user queries into structured sub-tasks
- **Pattern**: ReAct (Reasoning + Acting)
- **Sub-tasks**:
  1. Extract video metadata
  2. Process and analyze content
  3. Understand user intent
  4. Generate contextual response
  5. Store memory for continuity
- **Output**: Structured plan with task dependencies and tool requirements

#### **Executor** (`src/executor.py`)
- **Function**: Execute planned tasks using LLMs and APIs
- **Primary Tool**: Google Gemini API
- **Key Methods**:
  - `analyze_video_content()`: Extract key insights from transcripts
  - `understand_user_intent()`: Analyze what user wants to know
  - `generate_conversational_response()`: Create video-creator-perspective replies
  - `continue_conversation()`: Maintain context across multiple turns

#### **Memory** (`src/memory.py`)
- **Function**: Store and retrieve conversation history
- **Storage**: JSON files in `data/memory/`
- **Capabilities**:
  - Save complete conversation sessions
  - Load previous conversations by video ID
  - Maintain conversation context
  - Clear old memories
- **Format**: Structured JSON with metadata and timestamped messages

### 3. **External Tools & APIs**

#### **Google Gemini API**
- **Role**: Core LLM for understanding and generating responses
- **Usage**: 
  - Content analysis
  - Intent understanding
  - Conversational response generation
- **Configuration**: Requires `GOOGLE_API_KEY` in `.env`

#### **YouTube Integration** (`src/utils/youtube.py`)
- **Functions**:
  - Extract video ID from URLs
  - Fetch video metadata (title, channel, duration)
  - Get video transcripts
  - Validate YouTube URLs
- **Implementation Note**: Uses `youtube-transcript-api` and `pytube`

### 4. **Observability & Logging** (`src/utils/logger.py`)

#### **Logging Features**
- **Console Output**: Real-time activity logging
- **File Logging**: Persistent logs in `logs/agent.log`
- **Rotation**: Automatic log file rotation (10MB max per file, 5 backups)
- **Tracing**: Complete decision trace for agent debugging

#### **Logged Events**
- Component initialization
- URL validation and video fetching
- Plan creation and task execution
- Memory operations
- API calls and responses
- Error conditions and recovery

## Data Flow

```
User Input (Video URL + Query)
    │
    ▼
[PLANNER] ─→ Creates execution plan with sub-tasks
    │
    ▼
[YouTube Handler] ─→ Extracts video ID, metadata, transcript
    │
    ▼
[EXECUTOR] ─→ Calls Gemini API for:
    │         - Content analysis
    │         - Intent understanding
    │         - Response generation
    ▼
[MEMORY] ─→ Checks for conversation history
    │
    ▼
Generate/Continue Conversation
    │
    ▼
[MEMORY] ─→ Saves conversation for future reference
    │
    ▼
Return Response to User
```

## Workflow Sequence

```
1. User provides YouTube URL
2. CLI validates URL
3. Planner creates structured task plan
4. YouTube handler extracts content
5. Executor analyzes content with Gemini
6. Memory retrieves conversation history (if exists)
7. Executor generates response
8. Memory saves new message
9. Response displayed to user
10. Loop continues for follow-up questions
```

## Scalability & Extension Points

### Future Enhancements
- **Database Integration**: Replace JSON files with vector database for semantic search
- **Multi-modal Support**: Handle video segments, images, audio
- **Advanced Memory**: Implement RAG (Retrieval Augmented Generation) for better context
- **Web Interface**: Build REST API and web UI
- **Multi-language**: Add language detection and custom prompts
- **Performance**: Add caching for frequently accessed videos

