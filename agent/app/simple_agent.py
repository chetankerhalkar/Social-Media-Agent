from typing import Dict, List, Any
import json
import os

class SocialMediaAgent:
    """Simplified Social Media Agent without LangGraph dependencies"""
    
    def __init__(self):
        self.openai_api_key = os.environ.get("OPENAI_API_KEY")
        
    def generate_content_ideas(self, persona: str, brand_rules: str, platforms: List[str]) -> Dict[str, Any]:
        """Generate content ideas based on persona and brand rules"""
        
        # Mock trending data
        trending_seeds = [
            {
                "id": 1,
                "source": "linkedin",
                "topic": "#AI",
                "text": "AI agents are revolutionizing content creation workflows",
                "author": "TechInfluencer",
                "engagement": {"likes": 150, "comments": 25, "shares": 30},
                "score": 0.85
            },
            {
                "id": 2,
                "source": "x",
                "topic": "#CreatorEconomy",
                "text": "The creator economy is booming with new AI-powered tools",
                "author": "CreatorExpert",
                "engagement": {"likes": 200, "comments": 40, "shares": 50},
                "score": 0.92
            },
            {
                "id": 3,
                "source": "instagram",
                "topic": "#SocialMedia",
                "text": "Social media strategies that actually work in 2024",
                "author": "SocialMediaGuru",
                "engagement": {"likes": 300, "comments": 60, "shares": 25},
                "score": 0.78
            }
        ]
        
        # Generate ideas based on trends
        ideas = []
        for i, trend in enumerate(trending_seeds):
            idea = {
                "id": i + 1,
                "trend_id": trend["id"],
                "title": f"Content idea: {trend['topic']}",
                "summary": f"Create engaging content about {trend['topic']} based on current trends. {trend['text'][:100]}...",
                "hook": f"Transform your strategy with {trend['topic']}",
                "caption": self._generate_caption(trend, persona, brand_rules),
                "hashtags": [trend["topic"], "#ContentCreation", "#SocialMedia", "#AI", "#CreatorEconomy"],
                "ai_type": "text",
                "status": "draft",
                "platform_adaptations": self._create_platform_adaptations(trend, persona, platforms)
            }
            ideas.append(idea)
        
        return {
            "ideas": ideas,
            "trending_context": trending_seeds,
            "repurposed_content": self._repurpose_for_platforms(ideas, platforms),
            "scheduled_posts": self._suggest_schedule(ideas, platforms)
        }
    
    def _generate_caption(self, trend: Dict[str, Any], persona: str, brand_rules: str) -> str:
        """Generate a caption based on trend and brand guidelines"""
        
        if self.openai_api_key:
            # If OpenAI is available, you could make an API call here
            # For now, using template-based generation
            pass
        
        # Template-based caption generation
        topic = trend["topic"]
        text = trend["text"]
        
        if "AI" in topic:
            return f"🤖 AI is transforming how we create content!\n\n{text}\n\nAs a {persona}, I believe this trend shows us that the future of content creation is here. {brand_rules}\n\nWhat's your experience with AI tools? Share below! 👇"
        elif "CreatorEconomy" in topic:
            return f"💰 The creator economy is evolving fast!\n\n{text}\n\nThis aligns perfectly with my role as a {persona}. {brand_rules}\n\nHow are you adapting to these changes? Let's discuss! 💬"
        else:
            return f"📱 {topic} insights you need to know:\n\n{text}\n\nAs a {persona}, I'm excited about these developments. {brand_rules}\n\nWhat are your thoughts? Drop a comment! 👇"
    
    def _create_platform_adaptations(self, trend: Dict[str, Any], persona: str, platforms: List[str]) -> Dict[str, Dict[str, Any]]:
        """Create platform-specific adaptations"""
        adaptations = {}
        
        base_caption = self._generate_caption(trend, persona, "")
        
        for platform in platforms:
            if platform == "x":
                # Twitter/X - shorter, punchier
                adaptations[platform] = {
                    "caption": f"{trend['topic']} is changing the game! 🚀\n\n{trend['text'][:100]}...\n\nThoughts? 💭",
                    "hashtags": [trend["topic"], "#ContentCreation", "#SocialMedia"][:3],
                    "character_limit": 280
                }
            elif platform == "instagram":
                # Instagram - visual focus, more hashtags
                adaptations[platform] = {
                    "caption": f"{base_caption}\n\n✨ Save this post for later!\n📱 Share with a friend who needs to see this!",
                    "hashtags": [trend["topic"], "#ContentCreation", "#SocialMedia", "#AI", "#CreatorEconomy", "#Instagram", "#Reels"],
                    "media_type": "image_or_video"
                }
            elif platform == "linkedin":
                # LinkedIn - professional, longer form
                adaptations[platform] = {
                    "caption": f"Professional insight: {trend['text']}\n\nAs content creators and marketers, we're witnessing a significant shift in our industry. This trend represents more than just a passing fad—it's a fundamental change in how we approach content strategy.\n\nKey takeaways:\n• {trend['topic']} is driving innovation\n• Early adopters are seeing significant results\n• The landscape is evolving rapidly\n\nWhat's your perspective on this development? I'd love to hear your experiences in the comments.",
                    "hashtags": [tag for tag in [trend["topic"], "#ContentCreation", "#AI", "#CreatorEconomy"] if tag in ["#AI", "#CreatorEconomy", "#ContentCreation"]],
                    "tone": "professional"
                }
        
        return adaptations
    
    def _repurpose_for_platforms(self, ideas: List[Dict[str, Any]], platforms: List[str]) -> Dict[str, List[Dict[str, Any]]]:
        """Repurpose content for different platforms"""
        repurposed = {}
        
        for platform in platforms:
            repurposed[platform] = []
            for idea in ideas:
                if "platform_adaptations" in idea and platform in idea["platform_adaptations"]:
                    platform_content = {
                        "idea_id": idea["id"],
                        "platform": platform,
                        "title": idea["title"],
                        "content": idea["platform_adaptations"][platform],
                        "compliance_status": "passed"
                    }
                    repurposed[platform].append(platform_content)
        
        return repurposed
    
    def _suggest_schedule(self, ideas: List[Dict[str, Any]], platforms: List[str]) -> List[Dict[str, Any]]:
        """Suggest optimal posting schedule"""
        optimal_times = {
            "x": ["09:00", "12:00", "17:00"],
            "instagram": ["11:00", "14:00", "19:00"],
            "linkedin": ["08:00", "12:00", "17:00"]
        }
        
        scheduled_posts = []
        
        for platform in platforms:
            times = optimal_times.get(platform, ["12:00"])
            for i, idea in enumerate(ideas):
                scheduled_post = {
                    "idea_id": idea["id"],
                    "platform": platform,
                    "suggested_time": times[i % len(times)],
                    "status": "suggested",
                    "content": idea.get("platform_adaptations", {}).get(platform, {})
                }
                scheduled_posts.append(scheduled_post)
        
        return scheduled_posts

# Global agent instance
agent = SocialMediaAgent()

def generate_content_ideas(persona: str, brand_rules: str, platforms: List[str]) -> Dict[str, Any]:
    """Main function to generate content ideas"""
    return agent.generate_content_ideas(persona, brand_rules, platforms)
