from typing import Dict, List, Any, TypedDict
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
import json
import os
import asyncio

class AgentState(TypedDict):
    persona: str
    brand_rules: str
    platform_targets: List[str]
    trending_seeds: List[Dict[str, Any]]
    ideas: List[Dict[str, Any]]
    repurposed_content: Dict[str, List[Dict[str, Any]]]
    scheduled_posts: List[Dict[str, Any]]
    error: str

class SocialMediaAgent:
    def __init__(self):
        try:
            self.llm = ChatOpenAI(
                model="gpt-3.5-turbo",
                temperature=0.7,
                api_key=os.environ.get("OPENAI_API_KEY")
            )
        except Exception as e:
            print(f"Warning: OpenAI not configured: {e}")
            self.llm = None

    def collect_trends(self, state: AgentState) -> AgentState:
        """Collect trending content from various sources"""
        # Mock trending data for demo
        mock_trends = [
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
        
        state["trending_seeds"] = mock_trends
        return state

    def rank_trends(self, state: AgentState) -> AgentState:
        """Rank trends using score-based sorting"""
        trends = state["trending_seeds"]
        
        # Simple ranking by score
        ranked_trends = sorted(trends, key=lambda x: x["score"], reverse=True)
        
        state["trending_seeds"] = ranked_trends[:5]  # Top 5 trends
        return state

    def generate_ideas(self, state: AgentState) -> AgentState:
        """Generate content ideas based on trends"""
        persona = state["persona"]
        brand_rules = state["brand_rules"]
        trends = state["trending_seeds"]
        
        ideas = []
        
        # Generate ideas for each trend
        for i, trend in enumerate(trends):
            try:
                if self.llm:
                    # Use OpenAI to generate content
                    system_prompt = f"""
                    Persona: {persona}
                    Brand rules: {brand_rules}

                    Create a social media post idea based on the trending topic.
                    Make it engaging, actionable, and aligned with the brand persona.
                    """
                    
                    messages = [
                        SystemMessage(content=system_prompt),
                        HumanMessage(content=f"Create content based on this trend: {trend['text']}")
                    ]
                    
                    response = self.llm(messages)
                    generated_content = response.content
                else:
                    # Fallback mock content
                    generated_content = f"Engaging content about {trend['topic']} - {trend['text'][:50]}..."
                
                idea = {
                    "id": i + 1,
                    "trend_id": trend["id"],
                    "title": f"Content idea: {trend['topic']}",
                    "summary": generated_content[:200] + "...",
                    "hook": f"Transform your strategy with {trend['topic']}",
                    "caption": generated_content,
                    "hashtags": [trend["topic"], "#ContentCreation", "#SocialMedia", "#AI", "#CreatorEconomy"],
                    "ai_type": "text",
                    "status": "draft"
                }
                ideas.append(idea)
                
            except Exception as e:
                print(f"Error generating idea for trend {trend['id']}: {e}")
                # Create fallback idea
                idea = {
                    "id": i + 1,
                    "trend_id": trend["id"],
                    "title": f"Content idea: {trend['topic']}",
                    "summary": f"Create engaging content about {trend['topic']} based on current trends",
                    "hook": f"Discover the power of {trend['topic']}",
                    "caption": f"Here's what you need to know about {trend['topic']}: {trend['text']}",
                    "hashtags": [trend["topic"], "#ContentCreation", "#SocialMedia"],
                    "ai_type": "text",
                    "status": "draft"
                }
                ideas.append(idea)
        
        state["ideas"] = ideas
        return state

    def repurpose_content(self, state: AgentState) -> AgentState:
        """Repurpose content for different platforms"""
        ideas = state["ideas"]
        platforms = state["platform_targets"]
        
        repurposed = {}
        
        for platform in platforms:
            repurposed[platform] = []
            
            for idea in ideas:
                platform_content = self._adapt_for_platform(idea, platform)
                repurposed[platform].append(platform_content)
        
        state["repurposed_content"] = repurposed
        return state

    def _adapt_for_platform(self, idea: Dict[str, Any], platform: str) -> Dict[str, Any]:
        """Adapt content for specific platform"""
        base_content = {
            "idea_id": idea["id"],
            "platform": platform,
            "title": idea["title"],
            "hook": idea["hook"]
        }
        
        if platform == "x":
            # Twitter/X - 280 character limit
            caption = idea["caption"]
            if len(caption) > 250:
                caption = caption[:247] + "..."
            
            base_content.update({
                "caption": caption,
                "hashtags": idea["hashtags"][:3],  # Fewer hashtags for X
                "character_limit": 280
            })
        elif platform == "instagram":
            # Instagram - longer captions, more hashtags
            base_content.update({
                "caption": f"{idea['caption']}\n\n✨ What's your experience with this? Share in the comments!",
                "hashtags": idea["hashtags"] + ["#Instagram", "#Reels", "#ContentStrategy"],
                "media_type": "image_or_video"
            })
        elif platform == "linkedin":
            # LinkedIn - professional tone, longer content
            base_content.update({
                "caption": f"Professional insight: {idea['caption']}\n\nWhat are your thoughts on this trend? Let's discuss in the comments.",
                "hashtags": [tag for tag in idea["hashtags"] if tag in ["#AI", "#CreatorEconomy", "#ContentCreation"]],
                "tone": "professional"
            })
        
        return base_content

    def compliance_guard(self, state: AgentState) -> AgentState:
        """Check content against brand rules and compliance"""
        brand_rules = state["brand_rules"]
        repurposed_content = state["repurposed_content"]
        
        # Simple compliance check
        banned_terms = ["fake", "scam", "guaranteed", "instant", "get rich quick"]
        
        for platform, contents in repurposed_content.items():
            for content in contents:
                caption = content.get("caption", "").lower()
                
                # Check for banned terms
                has_banned_terms = any(term in caption for term in banned_terms)
                
                if has_banned_terms:
                    content["compliance_status"] = "failed"
                    content["compliance_issues"] = "Contains banned terms"
                else:
                    content["compliance_status"] = "passed"
        
        state["repurposed_content"] = repurposed_content
        return state

    def scheduler_suggest(self, state: AgentState) -> AgentState:
        """Suggest optimal posting times"""
        repurposed_content = state["repurposed_content"]
        
        # Optimal posting times by platform
        optimal_times = {
            "x": ["09:00", "12:00", "17:00"],
            "instagram": ["11:00", "14:00", "19:00"],
            "linkedin": ["08:00", "12:00", "17:00"]
        }
        
        scheduled_posts = []
        
        for platform, contents in repurposed_content.items():
            times = optimal_times.get(platform, ["12:00"])
            
            for i, content in enumerate(contents):
                if content.get("compliance_status") == "passed":
                    scheduled_post = {
                        "idea_id": content["idea_id"],
                        "platform": platform,
                        "content": content,
                        "suggested_time": times[i % len(times)],
                        "status": "suggested"
                    }
                    scheduled_posts.append(scheduled_post)
        
        state["scheduled_posts"] = scheduled_posts
        return state

    def run_workflow(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Run the complete workflow step by step"""
        try:
            # Initialize state
            state = AgentState(
                persona=input_data.get("persona", "AI assistant"),
                brand_rules=input_data.get("brand_rules", "Be helpful and accurate"),
                platform_targets=input_data.get("platforms", ["x", "instagram", "linkedin"]),
                trending_seeds=[],
                ideas=[],
                repurposed_content={},
                scheduled_posts=[],
                error=""
            )
            
            # Execute workflow steps
            print("🔍 Collecting trends...")
            state = self.collect_trends(state)
            
            print("📊 Ranking trends...")
            state = self.rank_trends(state)
            
            print("💡 Generating ideas...")
            state = self.generate_ideas(state)
            
            print("🔄 Repurposing content...")
            state = self.repurpose_content(state)
            
            print("✅ Checking compliance...")
            state = self.compliance_guard(state)
            
            print("📅 Suggesting schedule...")
            state = self.scheduler_suggest(state)
            
            return {
                "ideas": state["ideas"],
                "repurposed_content": state["repurposed_content"],
                "scheduled_posts": state["scheduled_posts"],
                "trending_context": state["trending_seeds"]
            }
            
        except Exception as e:
            print(f"Workflow error: {e}")
            return {
                "error": str(e),
                "ideas": [],
                "repurposed_content": {},
                "scheduled_posts": []
            }

# Global agent instance
agent = SocialMediaAgent()

def generate_content_ideas(persona: str, brand_rules: str, platforms: List[str]) -> Dict[str, Any]:
    """Main function to generate content ideas"""
    input_data = {
        "persona": persona,
        "brand_rules": brand_rules,
        "platforms": platforms
    }
    
    return agent.run_workflow(input_data)
