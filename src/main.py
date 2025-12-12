"""
Main Application - Video Conversation Agent
Orchestrates the agent workflow for YouTube video conversations.
"""

import os
import sys
import logging
from typing import Optional
from dotenv import load_dotenv

# Import agent modules
from src.planner import TaskPlanner
from src.executor import AgentExecutor
from src.memory import ConversationMemory
from src.utils.youtube import YouTubeHandler
from src.utils.logger import setup_logging


class VideoConversationAgent:
    """
    Main agent that orchestrates video understanding and conversation.
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the agent.
        
        Args:
            api_key: Google Gemini API key (if None, reads from environment)
        """
        # Setup logging
        setup_logging()
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # Initialize components
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY environment variable not set")
        
        self.planner = TaskPlanner()
        self.executor = AgentExecutor(self.api_key)
        self.memory = ConversationMemory()
        self.youtube = YouTubeHandler()
        
        self.logger.info("VideoConversationAgent initialized successfully")

    def run_conversation(
        self,
        video_url: str,
        user_query: str,
        native_language: str = "English"
    ) -> str:
        """
        Run the complete conversation workflow.
        
        Args:
            video_url: YouTube video URL
            user_query: User's question or message about the video
            native_language: Language to respond in
            
        Returns:
            Agent's response about the video
        """
        self.logger.info(f"Starting conversation for video: {video_url}")
        
        # Step 1: Validate URL
        if not self.youtube.validate_url(video_url):
            self.logger.error(f"Invalid YouTube URL: {video_url}")
            return "Error: Invalid YouTube URL. Please provide a valid YouTube link."
        
        # Step 2: Get video metadata and transcript
        video_id = self.youtube.extract_video_id(video_url)
        metadata = self.youtube.get_video_metadata(video_url)
        transcript = self.youtube.get_video_transcript(video_url)
        
        self.logger.info(f"Retrieved content for video: {video_id}")
        
        # Step 3: Plan the conversation (ReAct reasoning)
        plan = self.planner.plan_video_conversation(user_query, video_url)
        self.logger.info(f"Created plan with {len(plan['sub_tasks'])} sub-tasks")
        
        # Step 4: Load previous conversation if exists
        previous_conversation = self.memory.load_conversation(video_id)
        conversation_history = []
        
        if previous_conversation:
            conversation_history = previous_conversation.get('conversation', [])
            self.logger.info(f"Loaded {len(conversation_history)} previous messages")
        
        # Step 5: Generate response
        if conversation_history:
            # Continue existing conversation
            self.logger.info("Continuing previous conversation")
            response = self.executor.continue_conversation(
                user_query,
                conversation_history,
                transcript,
                native_language
            )
        else:
            # Start new conversation
            self.logger.info("Starting new conversation")
            response = self.executor.generate_conversational_response(
                user_query,
                transcript,
                metadata,
                native_language
            )
        
        if response.get("status") != "success":
            self.logger.error(f"Error generating response: {response.get('error')}")
            return f"Error: {response.get('error', 'Unknown error')}"
        
        # Step 6: Store in memory
        conversation_history.append({
            "user": user_query,
            "assistant": response.get("response"),
            "timestamp": None  # Added by memory module
        })
        
        self.memory.save_conversation(video_id, conversation_history, metadata)
        self.logger.info("Conversation saved to memory")
        
        return response.get("response", "")

    def interactive_mode(self):
        """
        Run the agent in interactive CLI mode.
        """
        print("\n" + "="*60)
        print("Welcome to the Video Conversation Agent!")
        print("="*60)
        print("\nThis agent allows you to have conversations about YouTube videos")
        print("as if the content creator is explaining it to you in your language.\n")
        
        while True:
            # Get video URL
            video_url = input("\nEnter YouTube video URL (or 'quit' to exit):\n> ").strip()
            if video_url.lower() == 'quit':
                print("\nThank you for using Video Conversation Agent. Goodbye!")
                break
            
            if not video_url:
                print("Please enter a valid URL.")
                continue
            
            # Get language preference
            native_language = input("\nWhat language would you like to chat in? (default: English):\n> ").strip()
            if not native_language:
                native_language = "English"
            
            print("\n" + "-"*60)
            print("Loading video... This may take a moment.\n")
            
            # Conversation loop
            while True:
                user_input = input(f"\nAsk about the video (or 'next' for a new video):\n> ").strip()
                
                if user_input.lower() == 'next':
                    break
                
                if not user_input:
                    print("Please enter a question or message.")
                    continue
                
                print("\n" + "-"*40)
                print("Video Creator: Thinking...\n")
                
                try:
                    response = self.run_conversation(
                        video_url,
                        user_input,
                        native_language
                    )
                    print(f"Video Creator: {response}\n")
                except Exception as e:
                    print(f"Error: {str(e)}\n")
                    self.logger.error(f"Conversation error: {str(e)}")
        
        print("-"*60)


def main():
    """Main entry point."""
    # Load environment variables
    load_dotenv()
    
    try:
        agent = VideoConversationAgent()
        agent.interactive_mode()
    except ValueError as e:
        print(f"Configuration Error: {e}")
        print("\nPlease set GOOGLE_API_KEY in .env file or environment variable")
        sys.exit(1)
    except Exception as e:
        print(f"Fatal Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
