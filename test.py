"""
Test script for Video Conversation Agent
Validates that all components work correctly
"""

import sys
import logging
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.planner import TaskPlanner
from src.executor import AgentExecutor
from src.memory import ConversationMemory
from src.utils.youtube import YouTubeHandler
from src.utils.logger import setup_logging
import os
from dotenv import load_dotenv


def test_imports():
    """Test that all modules import correctly."""
    print("✓ Testing imports...")
    assert TaskPlanner is not None
    assert AgentExecutor is not None
    assert ConversationMemory is not None
    assert YouTubeHandler is not None
    print("  ✅ All imports successful")


def test_logger():
    """Test logging setup."""
    print("\n✓ Testing logger setup...")
    setup_logging()
    logger = logging.getLogger("TestLogger")
    logger.info("Test log message")
    print("  ✅ Logging works")


def test_youtube_handler():
    """Test YouTube URL validation."""
    print("\n✓ Testing YouTube handler...")
    yt = YouTubeHandler()
    
    # Test valid URL
    valid_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    assert yt.validate_url(valid_url), "Should validate YouTube URL"
    
    video_id = yt.extract_video_id(valid_url)
    assert video_id == "dQw4w9WgXcQ", "Should extract correct video ID"
    
    # Test invalid URL
    invalid_url = "https://not-a-youtube-url.com"
    assert not yt.validate_url(invalid_url), "Should reject non-YouTube URL"
    
    print("  ✅ YouTube handler works")


def test_memory():
    """Test memory operations."""
    print("\n✓ Testing memory operations...")
    memory = ConversationMemory("test_memory")
    
    # Test saving conversation
    video_id = "test_video_123"
    conversation = [
        {"user": "What is this video about?", "assistant": "This video is about..."}
    ]
    metadata = {"title": "Test Video", "channel": "Test Channel"}
    
    filepath = memory.save_conversation(video_id, conversation, metadata)
    assert Path(filepath).exists(), "Conversation file should exist"
    
    # Test loading conversation
    loaded = memory.load_conversation(video_id)
    assert loaded is not None, "Should load conversation"
    assert loaded["video_id"] == video_id, "Video ID should match"
    
    # Cleanup
    memory.clear_memory(video_id)
    print("  ✅ Memory operations work")


def test_planner():
    """Test task planner."""
    print("\n✓ Testing task planner...")
    planner = TaskPlanner()
    
    plan = planner.plan_video_conversation(
        "What is this video about?",
        "https://youtube.com/watch?v=dQw4w9WgXcQ"
    )
    
    assert "sub_tasks" in plan, "Plan should have sub_tasks"
    assert len(plan["sub_tasks"]) == 5, "Should have 5 sub-tasks"
    
    tools = planner.identify_required_tools(plan)
    assert len(tools) > 0, "Should identify required tools"
    
    print("  ✅ Planner works")


def test_api_key():
    """Test API key configuration."""
    print("\n✓ Testing API key configuration...")
    load_dotenv()
    
    api_key = os.getenv("GOOGLE_API_KEY")
    if api_key and api_key != "your_google_gemini_api_key_here":
        print("  ✅ API key configured")
        return True
    else:
        print("  ⚠️  API key not configured")
        print("     Please set GOOGLE_API_KEY in .env file")
        return False


def main():
    """Run all tests."""
    print("=" * 50)
    print("Video Conversation Agent - Test Suite")
    print("=" * 50)
    
    try:
        test_imports()
        test_logger()
        test_youtube_handler()
        test_memory()
        test_planner()
        api_configured = test_api_key()
        
        print("\n" + "=" * 50)
        print("✅ All tests passed!")
        print("=" * 50)
        
        if api_configured:
            print("\n🚀 Ready to run: python src/main.py")
        else:
            print("\n⚠️  Configure API key before running the agent")
        
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
