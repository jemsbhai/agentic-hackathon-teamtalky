"""
Planner Module - Breaks down user goals into sub-tasks using ReAct pattern.
"""

import json
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)


class TaskPlanner:
    """
    Breaks down a user query into actionable sub-tasks using ReAct (Reasoning + Acting) pattern.
    """

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def plan_video_conversation(self, user_query: str, video_url: str) -> Dict[str, Any]:
        """
        Plan sub-tasks for analyzing and conversing about a YouTube video.
        
        Args:
            user_query: User's question or request about the video
            video_url: The YouTube video URL
            
        Returns:
            Dictionary containing planned sub-tasks
        """
        self.logger.info(f"Planning conversation for video: {video_url}")
        
        plan = {
            "main_goal": f"Have a conversation about the YouTube video in the user's native language",
            "video_url": video_url,
            "user_query": user_query,
            "sub_tasks": [
                {
                    "task_id": 1,
                    "task_name": "Extract Video Metadata",
                    "description": "Retrieve video title, duration, channel info, and transcript",
                    "tool_required": "youtube_api"
                },
                {
                    "task_id": 2,
                    "task_name": "Process Video Content",
                    "description": "Analyze transcript and extract key concepts, themes, and important points",
                    "tool_required": "gemini_api"
                },
                {
                    "task_id": 3,
                    "task_name": "Understand User Intent",
                    "description": "Analyze user query to determine what aspect of the video they want to discuss",
                    "tool_required": "gemini_api"
                },
                {
                    "task_id": 4,
                    "task_name": "Generate Conversational Response",
                    "description": "Create a response as if the video content is speaking directly to the user",
                    "tool_required": "gemini_api"
                },
                {
                    "task_id": 5,
                    "task_name": "Store Conversation Memory",
                    "description": "Save the conversation for future context and continuity",
                    "tool_required": "memory_store"
                }
            ],
            "reasoning": {
                "approach": "ReAct - We reason about the video content, then act by calling appropriate tools",
                "context_needed": ["video_url", "transcript", "user_query"],
                "language_preference": "User's native language"
            }
        }
        
        self.logger.info(f"Plan created with {len(plan['sub_tasks'])} sub-tasks")
        return plan

    def identify_required_tools(self, plan: Dict[str, Any]) -> List[str]:
        """
        Identify which tools are needed for the plan.
        
        Args:
            plan: The plan dictionary from plan_video_conversation()
            
        Returns:
            List of required tool names
        """
        tools = set()
        for task in plan.get("sub_tasks", []):
            if "tool_required" in task:
                tools.add(task["tool_required"])
        
        self.logger.info(f"Required tools: {tools}")
        return list(tools)

    def estimate_tokens(self, video_transcript: str) -> int:
        """
        Estimate the number of tokens in the transcript.
        
        Args:
            video_transcript: The full video transcript text
            
        Returns:
            Estimated token count
        """
        # Rough estimation: 1 token ≈ 4 characters
        estimated_tokens = len(video_transcript) // 4
        self.logger.info(f"Estimated tokens: {estimated_tokens}")
        return estimated_tokens
