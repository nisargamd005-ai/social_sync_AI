"""
social_posting/ai_agent.py

AI Agent mock implementation for processing commands and preparing content.
"""

def analyze_command(command_text: str) -> dict:
    """
    Parse the user command to determine target platforms and instructions.
    In a production app, this would use an LLM API (e.g., OpenAI).
    """
    platforms = []
    text_lower = command_text.lower()
    
    # Simple keyword-based intent detection
    if "instagram" in text_lower:
        platforms.append("instagram")
    if "linkedin" in text_lower:
        platforms.append("linkedin")
    if "twitter" in text_lower or " x " in text_lower:
        platforms.append("twitter")
        
    # Default to all if none explicitly mentioned
    if not platforms:
        platforms = ["linkedin", "instagram", "twitter"]
        
    return {
        "platforms": platforms,
        "base_content": command_text
    }

def prepare_content(base_content: str, platform: str) -> str:
    """
    Format the content specifically for the given platform.
    """
    # In a production app, this would use an LLM to rewrite the content for the platform.
    if platform == "twitter":
        return f"{base_content[:260]}\n\n#SocialSync"
    elif platform == "linkedin":
        return f"{base_content}\n\nShared via #SocialSync AI 🚀 #Professional"
    elif platform == "instagram":
        return f"{base_content}\n\n✨ #SocialSync #InstaDaily"
    
    return base_content
