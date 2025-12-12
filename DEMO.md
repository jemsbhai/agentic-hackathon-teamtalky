# Demo Video

## Video Walkthrough

This 3–5 minute video demonstrates the Video Conversation Agent in action, showing the complete agentic workflow from user input to multi-turn conversation.

---

## 📺 Hosted Video Link

**[Add your demo video link here]**

Please upload to: YouTube (unlisted), Loom, Google Drive, or any publicly accessible platform

**IMPORTANT**: Videos must be publicly accessible and hosted online. Raw video file submissions will not be reviewed.

---

## Expected Demo Flow & Timestamps

### **00:00–00:30 — Introduction & Setup**
- Brief overview of the problem: "YouTube videos have valuable info but are hard to engage with"
- Solution: "Chat with the video as if the creator is explaining it to you"
- Demo environment setup
- Show the `.env.example` file and how to add Gemini API key

### **00:30–01:30 — User Input → Planning Step**
- User provides a YouTube video URL (e.g., TED talk, educational video)
- User selects their native language for responses
- Show the **ReAct Planning** step:
  - Console output showing 5 sub-tasks being created
  - Logs showing: "Extract metadata", "Analyze content", "Understand intent", etc.
  - Show the plan JSON structure

### **01:30–02:30 — Tool Calls & Memory Retrieval**
- Show the **Executor** calling Gemini API
  - Display API prompts and responses
  - Show the conversation generation in progress
- Show **YouTube Handler** extracting:
  - Video ID from URL
  - Transcript from YouTube
- Show **Memory** operations:
  - Loading previous conversation (if exists)
  - Storing new conversation to `data/memory/`
  - Display the JSON memory file

### **02:30–03:30 — Final Output & Edge Cases**
- Display the **final response** from the "video creator"
- Show follow-up questions:
  - Ask a second question about the same video
  - Show how **conversation context** is used
  - Display improvement in response quality with memory
- Demo an **edge case**:
  - Invalid YouTube URL → handled gracefully with error message
  - Long transcript → shows partial processing
  - Different language → response in chosen language

---

## Key Agentic Features to Highlight

✅ **ReAct Pattern**: Show reasoning (planning) → acting (API calls)
✅ **Tool Orchestration**: YouTube API → Gemini API → Memory Storage
✅ **Memory & Context**: Previous conversations inform new responses
✅ **Logging & Observability**: Full trace of agent decisions
✅ **Error Handling**: Graceful failure recovery
✅ **Multi-turn Conversation**: Context carries across multiple exchanges

---

## Demo Script (Optional)

**Narrator**:
"This is the Video Conversation Agent. Let's demonstrate how it works.

**[00:00–00:10]**
First, we start the application. The agent is initialized with our Gemini API key.

**[00:10–00:30]**
We paste a YouTube video URL – let's use this TED talk on machine learning. We specify English as our language.

**[00:30–01:00]**
The planner immediately breaks down the task into 5 sub-steps using the ReAct pattern. You can see in the logs:
- Extract video metadata
- Analyze content
- Understand user intent
- Generate response  
- Store in memory

**[01:00–01:30]**
The executor starts calling Gemini API. Notice how it's analyzing the transcript and generating a personalized response.

**[01:30–02:00]**
Meanwhile, the memory module is retrieving and storing conversations. This is the first time we're talking about this video, so there's no history yet.

**[02:00–02:30]**
The response comes back! It's as if the video creator is explaining their TED talk directly to us.

**[02:30–03:00]**
Now we ask a follow-up question. The agent retrieves the previous conversation context and generates a more nuanced response.

**[03:00–03:30]**
Finally, we demonstrate error handling with an invalid URL, which the agent handles gracefully. That's the Video Conversation Agent – agentic AI in action!"

---

## Recording Tips

- Use a screen recorder (Loom, OBS, or QuickTime)
- Speak clearly and at a measured pace
- Show code, logs, and responses clearly
- Include cursor movement to highlight important parts
- Keep video under 5 minutes (optimal: 3–4 minutes)
- Ensure audio is clear and background noise is minimal
- Use subtitles if background noise is present

---

## Submission Checklist

- [ ] Video is 3–5 minutes long
- [ ] Video link is publicly accessible
- [ ] All timestamps match the expected demo flow
- [ ] Shows agentic planning, tool calls, and memory
- [ ] Demonstrates Gemini API usage
- [ ] Includes error handling example
- [ ] Audio is clear and instructions are understood
