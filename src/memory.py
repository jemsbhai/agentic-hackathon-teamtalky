"""
Memory Module - Stores and retrieves conversation history and video context.
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)


class ConversationMemory:
    """
    Manages conversation history and video context for continuity and learning.
    """

    def __init__(self, memory_dir: str = "data/memory"):
        """
        Initialize the memory store.
        
        Args:
            memory_dir: Directory to store conversation files
        """
        self.memory_dir = Path(memory_dir)
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info(f"Memory store initialized at {memory_dir}")

    def save_conversation(
        self,
        video_id: str,
        conversation: List[Dict[str, str]],
        video_metadata: Dict[str, Any]
    ) -> str:
        """
        Save a conversation session to disk.
        
        Args:
            video_id: Unique identifier for the video
            conversation: List of user/assistant message pairs
            video_metadata: Metadata about the video
            
        Returns:
            Path to saved conversation file
        """
        timestamp = datetime.now().isoformat()
        filename = f"{video_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = self.memory_dir / filename
        
        memory_data = {
            "video_id": video_id,
            "video_metadata": video_metadata,
            "created_at": timestamp,
            "conversation": conversation
        }
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(memory_data, f, indent=2, ensure_ascii=False)
            self.logger.info(f"Conversation saved to {filepath}")
            return str(filepath)
        except Exception as e:
            self.logger.error(f"Error saving conversation: {str(e)}")
            raise

    def load_conversation(self, video_id: str) -> Optional[Dict[str, Any]]:
        """
        Load the most recent conversation for a video.
        
        Args:
            video_id: The video identifier
            
        Returns:
            Dictionary with conversation history or None
        """
        try:
            files = sorted(self.memory_dir.glob(f"{video_id}_*.json"), reverse=True)
            if not files:
                self.logger.info(f"No conversation found for video {video_id}")
                return None
            
            with open(files[0], 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.logger.info(f"Loaded conversation from {files[0]}")
            return data
        except Exception as e:
            self.logger.error(f"Error loading conversation: {str(e)}")
            return None

    def add_message(
        self,
        video_id: str,
        user_message: str,
        assistant_response: str
    ) -> Dict[str, str]:
        """
        Add a new message pair to memory.
        
        Args:
            video_id: The video identifier
            user_message: User's input
            assistant_response: Assistant's response
            
        Returns:
            Dictionary with the message pair and metadata
        """
        message = {
            "timestamp": datetime.now().isoformat(),
            "user": user_message,
            "assistant": assistant_response
        }
        self.logger.info(f"Message added to memory for {video_id}")
        return message

    def get_conversation_context(self, video_id: str, limit: int = 5) -> str:
        """
        Get recent conversation context for the video.
        
        Args:
            video_id: The video identifier
            limit: Number of recent messages to retrieve
            
        Returns:
            Formatted conversation context
        """
        conversation_data = self.load_conversation(video_id)
        if not conversation_data:
            return "No previous conversation context"
        
        messages = conversation_data.get('conversation', [])[-limit:]
        context = "\n".join([
            f"User: {msg.get('user', '')}\n"
            f"Assistant: {msg.get('assistant', '')}"
            for msg in messages
        ])
        
        return context if context else "No conversation history"

    def clear_memory(self, video_id: Optional[str] = None) -> int:
        """
        Clear memory for a specific video or all videos.
        
        Args:
            video_id: Optional video ID. If None, clears all memory.
            
        Returns:
            Number of files deleted
        """
        try:
            if video_id:
                files = list(self.memory_dir.glob(f"{video_id}_*.json"))
            else:
                files = list(self.memory_dir.glob("*.json"))
            
            for f in files:
                f.unlink()
            
            self.logger.info(f"Cleared {len(files)} memory files")
            return len(files)
        except Exception as e:
            self.logger.error(f"Error clearing memory: {str(e)}")
            return 0

    def list_conversations(self) -> List[Dict[str, Any]]:
        """
        List all stored conversations.
        
        Returns:
            List of conversation metadata
        """
        conversations = []
        try:
            for filepath in sorted(self.memory_dir.glob("*.json"), reverse=True):
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                conversations.append({
                    "video_id": data.get("video_id"),
                    "video_title": data.get("video_metadata", {}).get("title"),
                    "created_at": data.get("created_at"),
                    "message_count": len(data.get("conversation", []))
                })
            self.logger.info(f"Listed {len(conversations)} conversations")
        except Exception as e:
            self.logger.error(f"Error listing conversations: {str(e)}")
        
        return conversations
