"""
Executor Module - Executes LLM calls and tool invocations using Google Gemini API.
"""

import logging
from typing import Dict, Any, Optional
import google.generativeai as genai

logger = logging.getLogger(__name__)


class AgentExecutor:
    """
    Executes planned tasks by calling Gemini API and managing tool interactions.
    """

    def __init__(self, api_key: str):
        """
        Initialize the executor with Gemini API.
        
        Args:
            api_key: Google Gemini API key
        """
        self.api_key = api_key
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-1.5-pro")
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info("AgentExecutor initialized with Gemini API")

    def analyze_video_content(self, transcript: str) -> Dict[str, Any]:
        """
        Use Gemini to analyze video content and extract key insights.
        
        Args:
            transcript: The video transcript text
            
        Returns:
            Dictionary with analysis results
        """
        self.logger.info("Starting video content analysis with Gemini")
        
        prompt = f"""Analyze the following video transcript and provide:
1. Main topic/theme
2. Key concepts and ideas
3. Important takeaways
4. Target audience
5. Speaker's tone and style

Transcript:
{transcript}

Provide the analysis in a structured JSON format."""

        try:
            response = self.model.generate_content(prompt)
            analysis = {
                "status": "success",
                "content": response.text,
                "analysis_type": "video_content"
            }
            self.logger.info("Video analysis completed successfully")
            return analysis
        except Exception as e:
            self.logger.error(f"Error in video analysis: {str(e)}")
            return {"status": "error", "error": str(e)}

    def understand_user_intent(self, user_query: str, video_context: str) -> Dict[str, Any]:
        """
        Analyze user query in context of video content.
        
        Args:
            user_query: The user's question or request
            video_context: Summary of video content
            
        Returns:
            Dictionary with intent analysis
        """
        self.logger.info("Analyzing user intent")
        
        prompt = f"""Given this user query about a video:
Query: {user_query}

Video Summary:
{video_context}

Determine:
1. What aspect of the video is the user interested in?
2. What is the user really asking?
3. What tone should the response have?
4. Should the response be from the video creator's perspective?

Respond in a concise, structured format."""

        try:
            response = self.model.generate_content(prompt)
            intent = {
                "status": "success",
                "analysis": response.text,
                "intent_type": "video_discussion"
            }
            self.logger.info("Intent analysis completed")
            return intent
        except Exception as e:
            self.logger.error(f"Error in intent analysis: {str(e)}")
            return {"status": "error", "error": str(e)}

    def generate_conversational_response(
        self,
        user_query: str,
        video_transcript: str,
        video_metadata: Dict[str, str],
        native_language: str = "English"
    ) -> Dict[str, Any]:
        """
        Generate a conversational response from the video's perspective.
        
        Args:
            user_query: User's question about the video
            video_transcript: The video's transcript
            video_metadata: Video title, channel, duration, etc.
            native_language: Language to respond in
            
        Returns:
            Dictionary with the generated response
        """
        self.logger.info(f"Generating conversational response in {native_language}")
        
        prompt = f"""You are having a conversation about a YouTube video.
The video is titled: "{video_metadata.get('title', 'Untitled')}"
Channel: {video_metadata.get('channel', 'Unknown')}

Here's what the video is about:
{video_transcript}

The user is asking:
"{user_query}"

Respond as if YOU are the creator/subject of the video explaining your content.
Speak naturally and conversationally.
Respond in {native_language}.
Be engaging and helpful.
Reference specific parts of the video content when relevant."""

        try:
            response = self.model.generate_content(prompt)
            result = {
                "status": "success",
                "response": response.text,
                "language": native_language,
                "response_type": "conversational"
            }
            self.logger.info("Conversational response generated successfully")
            return result
        except Exception as e:
            self.logger.error(f"Error generating response: {str(e)}")
            return {"status": "error", "error": str(e)}

    def continue_conversation(
        self,
        user_query: str,
        conversation_history: list,
        video_context: str,
        native_language: str = "English"
    ) -> Dict[str, Any]:
        """
        Continue an ongoing conversation with context from previous messages.
        
        Args:
            user_query: New user message
            conversation_history: List of previous exchanges
            video_context: The original video content
            native_language: Language to respond in
            
        Returns:
            Dictionary with the continuation response
        """
        self.logger.info("Continuing conversation")
        
        history_text = "\n".join([
            f"User: {msg.get('user', '')}\nVideo (Assistant): {msg.get('assistant', '')}"
            for msg in conversation_history[-5:]  # Last 5 exchanges for context
        ])
        
        prompt = f"""Continue this conversation about a YouTube video.

Video Content Summary:
{video_context}

Previous Conversation:
{history_text}

New User Message:
{user_query}

Continue as the video creator/subject, maintaining context and continuity.
Respond in {native_language}.
Keep the conversation natural and engaging."""

        try:
            response = self.model.generate_content(prompt)
            result = {
                "status": "success",
                "response": response.text,
                "language": native_language,
                "response_type": "conversation_continuation"
            }
            self.logger.info("Conversation continued successfully")
            return result
        except Exception as e:
            self.logger.error(f"Error continuing conversation: {str(e)}")
            return {"status": "error", "error": str(e)}
