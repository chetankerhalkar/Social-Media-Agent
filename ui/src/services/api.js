const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
const AGENT_BASE_URL = import.meta.env.VITE_AGENT_URL || 'http://localhost:8001';

class ApiService {
  constructor() {
    this.baseURL = API_BASE_URL;
    this.agentURL = AGENT_BASE_URL;
    // Store generated ideas locally for demo purposes
    this.generatedIdeas = [];
    this.ideasCounter = 1;
    
    // Initialize with some pre-existing ideas in different statuses
    this.initializeDemoIdeas();
  }
  
  initializeDemoIdeas() {
    // Add scheduled ideas
    this.generatedIdeas.push({
      id: this.ideasCounter++,
      title: "ChatGPT Pulse Release Analysis",
      summary: "Breaking down OpenAI's latest ChatGPT Pulse feature and its impact on real-time AI interactions. What this means for creators and businesses.",
      status: "scheduled",
      scheduledFor: "2024-01-22T10:00:00Z",
      platform_adaptations: {
        x: "🚨 BREAKING: ChatGPT Pulse is here! 🚀\n\nReal-time AI interactions just got a massive upgrade:\n✅ Instant responses\n✅ Live collaboration\n✅ Enhanced context awareness\n\nThis changes everything for content creators! Thread below 🧵\n\n#ChatGPT #AI #OpenAI #TechNews",
        instagram: "ChatGPT Pulse just dropped and it's INCREDIBLE! 🤯\n\nWhat's new:\n🔥 Real-time AI conversations\n⚡ Lightning-fast responses\n🎯 Better context understanding\n💡 Enhanced creative workflows\n\nAs a content creator, this is a game-changer! The possibilities are endless...\n\nWhat will you create with ChatGPT Pulse? Drop your ideas below! 👇\n\n#ChatGPT #AI #ContentCreation #OpenAI #TechUpdate #CreatorEconomy",
        linkedin: "ChatGPT Pulse: A Strategic Analysis for Business Leaders\n\nOpenAI's latest release introduces real-time AI interaction capabilities that will fundamentally reshape how organizations approach:\n\n• Customer service automation\n• Content creation workflows\n• Team collaboration processes\n• Decision-making support systems\n\nKey business implications:\n1. 40% reduction in response times for customer inquiries\n2. Enhanced productivity for content teams\n3. New opportunities for AI-human collaboration\n4. Competitive advantages for early adopters\n\nHow is your organization preparing for this AI evolution?\n\n#ChatGPT #AI #BusinessStrategy #DigitalTransformation #OpenAI"
      }
    });

    this.generatedIdeas.push({
      id: this.ideasCounter++,
      title: "Google Nano Banana Model Deep Dive",
      summary: "Exploring Google's revolutionary Nano Banana model - the smallest yet most efficient AI model for mobile devices. Perfect for edge computing applications.",
      status: "scheduled", 
      scheduledFor: "2024-01-23T14:30:00Z",
      platform_adaptations: {
        x: "🍌 Google's Nano Banana model is tiny but MIGHTY!\n\n• 10x smaller than competitors\n• Runs on ANY mobile device\n• Zero latency responses\n• Privacy-first design\n\nEdge AI just got bananas! 🚀\n\n#Google #AI #EdgeComputing #MobileTech #NanoBanana",
        instagram: "Google just went BANANAS with their new AI model! 🍌🤖\n\nMeet Nano Banana - the tiniest AI that packs a HUGE punch:\n\n✨ Fits on your phone\n⚡ Instant responses\n🔒 Your data stays private\n🎯 Perfect accuracy\n\nThis is the future of mobile AI! Imagine having ChatGPT-level intelligence running directly on your phone without internet...\n\nMind = blown! 🤯 What would you use this for?\n\n#Google #AI #MobileTech #EdgeComputing #TechInnovation #FutureIsNow",
        linkedin: "Google's Nano Banana Model: Revolutionizing Edge AI Computing\n\nGoogle's latest breakthrough in AI miniaturization presents significant opportunities for enterprise applications:\n\nTechnical Specifications:\n• 95% size reduction compared to traditional models\n• Sub-millisecond inference times\n• On-device processing eliminates data privacy concerns\n• Compatible with standard mobile hardware\n\nBusiness Applications:\n• Real-time customer service without cloud dependency\n• Offline AI capabilities for remote operations\n• Enhanced data security for sensitive industries\n• Reduced operational costs through edge computing\n\nThis represents a paradigm shift toward democratized AI access. Organizations can now deploy sophisticated AI capabilities without massive infrastructure investments.\n\nThoughts on how edge AI will transform your industry?\n\n#EdgeAI #Google #AIInnovation #DigitalTransformation #TechStrategy"
      }
    });

    // Add posted ideas
    this.generatedIdeas.push({
      id: this.ideasCounter++,
      title: "AI Agents Revolution in Content Creation",
      summary: "How AI agents are transforming the content creation landscape. Real examples and case studies from successful creators.",
      status: "posted",
      publishedAt: "2024-01-20T09:15:00Z",
      engagement: { likes: 234, comments: 45, shares: 28 },
      platform_adaptations: {
        x: "🤖 AI agents are revolutionizing content creation!\n\nReal results from creators using AI:\n📈 3x faster content production\n🎯 Better audience targeting\n✨ Higher engagement rates\n💡 Endless creative possibilities\n\nThe future is here! #AI #ContentCreation",
        instagram: "AI agents are changing the content game! 🚀\n\nWhat I've learned after 6 months:\n• Ideas flow faster than ever\n• Quality has improved dramatically\n• More time for strategy and engagement\n• Creativity is enhanced, not replaced\n\nAI isn't taking over - it's leveling up! 💪\n\n#AI #ContentCreation #CreatorEconomy #TechTrends #Innovation",
        linkedin: "The AI Agent Revolution: 6 Months of Real-World Results\n\nAfter implementing AI agents in our content workflow, here's what we've observed:\n\n• 300% increase in content output\n• 45% improvement in engagement rates\n• 60% reduction in ideation time\n• 25% increase in conversion rates\n\nKey insight: AI doesn't replace creativity - it amplifies it.\n\nHow are you integrating AI into your content strategy?\n\n#AI #ContentStrategy #MarketingInnovation #DigitalTransformation"
      }
    });

    this.generatedIdeas.push({
      id: this.ideasCounter++,
      title: "Social Media Trends 2024 Predictions",
      summary: "Data-driven predictions for social media trends in 2024. What platforms, features, and content types will dominate.",
      status: "posted",
      publishedAt: "2024-01-19T16:45:00Z", 
      engagement: { likes: 189, comments: 32, shares: 15 },
      platform_adaptations: {
        x: "📱 2024 Social Media Predictions:\n\n1. AI-generated content goes mainstream\n2. Vertical video dominates ALL platforms\n3. Community > Followers\n4. Authenticity beats perfection\n5. Micro-influencers rule\n\nWhat's your prediction? #SocialMedia2024",
        instagram: "My 2024 Social Media Predictions! 🔮✨\n\nBased on current data and trends:\n\n🤖 AI content creation explodes\n📱 Short-form video continues to dominate\n👥 Community building becomes #1 priority\n🎯 Niche content outperforms broad appeal\n💡 Interactive content drives engagement\n\nWhich prediction do you think will be most accurate? 🤔\n\n#SocialMedia2024 #ContentTrends #DigitalMarketing #Predictions",
        linkedin: "2024 Social Media Landscape: Strategic Predictions for Businesses\n\nBased on comprehensive data analysis and current trajectory:\n\n1. AI-assisted content creation will become standard practice\n2. Community-driven marketing will outperform traditional advertising\n3. Authenticity metrics will influence algorithm rankings\n4. Cross-platform content strategies will be essential\n5. Employee advocacy programs will drive B2B success\n\nRecommendations:\n• Invest in AI content tools now\n• Focus on community building over follower count\n• Develop authentic brand storytelling\n• Create platform-specific content strategies\n\nHow is your organization preparing for these shifts?\n\n#SocialMediaStrategy #DigitalMarketing #BusinessStrategy #2024Trends"
      }
    });

    this.generatedIdeas.push({
      id: this.ideasCounter++,
      title: "Creator Economy Monetization Strategies",
      summary: "Comprehensive guide to monetizing your content in 2024. Multiple revenue streams and practical implementation tips.",
      status: "posted",
      publishedAt: "2024-01-18T11:30:00Z",
      engagement: { likes: 312, comments: 67, shares: 41 },
      platform_adaptations: {
        x: "💰 Creator Economy Revenue Streams 2024:\n\n1. Content subscriptions\n2. Digital products\n3. Coaching/consulting\n4. Brand partnerships\n5. Community memberships\n6. Course creation\n\nDiversify your income! Thread below 🧵 #CreatorEconomy",
        instagram: "How I built multiple revenue streams as a creator! 💪💰\n\nMy income sources:\n📚 Digital courses (40%)\n🤝 Brand partnerships (25%)\n💎 Premium community (20%)\n📱 Content subscriptions (10%)\n🎯 Consulting (5%)\n\nKey lesson: Don't rely on just one platform or revenue source!\n\nWhat's your main income stream? Share below! 👇\n\n#CreatorEconomy #ContentMonetization #DigitalEntrepreneur #OnlineBusiness",
        linkedin: "Creator Economy Monetization: A Strategic Framework for 2024\n\nAfter analyzing 500+ successful creators, here are the most effective monetization strategies:\n\nTier 1 (Foundation):\n• Content subscriptions and memberships\n• Digital product sales\n• Email list monetization\n\nTier 2 (Growth):\n• Brand partnerships and sponsorships\n• Coaching and consulting services\n• Online course creation\n\nTier 3 (Scale):\n• Community platforms\n• Software/tool development\n• Investment and equity opportunities\n\nKey insight: Successful creators typically have 3-5 active revenue streams, reducing platform dependency and increasing stability.\n\nWhat monetization strategies are you exploring?\n\n#CreatorEconomy #ContentMonetization #DigitalBusiness #EntrepreneurshipStrategy"
      }
    });
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('API request failed:', error);
      // Return mock data for demo purposes
      return this.getMockResponse(endpoint, options.method);
    }
  }

  async agentRequest(endpoint, options = {}) {
    const url = `${this.agentURL}${endpoint}`;
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return await response.json();
    } catch (error) {
      console.error('Agent request failed:', error);
      // Return mock data for demo purposes
      return this.getMockAgentResponse(endpoint, options.method);
    }
  }

  getMockResponse(endpoint, method) {
    // Mock responses for when backend is not available
    if (endpoint.includes('/config/brand')) {
      if (method === 'PUT') {
        return { message: "Brand configuration updated successfully" };
      }
      return {
        persona: "Playful AI coach for creators",
        brand_rules: "Be optimistic, include actionable advice, keep it concise.",
        default_hashtags: "#AI #ContentCreation #SocialMedia"
      };
    }

    if (endpoint.includes('/trends/list')) {
      return {
        trends: [
          {
            id: 1,
            source: "linkedin",
            topic: "#AI",
            text: "AI agents are revolutionizing content creation workflows",
            author: "TechInfluencer",
            url: "https://linkedin.com/posts/tech-influencer-ai-agents",
            engagement: { likes: 150, comments: 25, shares: 30 },
            score: 0.85,
            captured_at: "2024-01-01T12:00:00Z"
          },
          {
            id: 2,
            source: "x",
            topic: "#CreatorEconomy",
            text: "The creator economy is booming with new AI-powered tools",
            author: "CreatorExpert",
            url: "https://x.com/creatorexpert/status/1234567890",
            engagement: { likes: 200, comments: 40, shares: 50 },
            score: 0.92,
            captured_at: "2024-01-01T11:30:00Z"
          },
          {
            id: 3,
            source: "instagram",
            topic: "#SocialMedia",
            text: "Social media strategies that actually work in 2024",
            author: "SocialMediaGuru",
            url: "https://instagram.com/p/socialmediaguru123",
            engagement: { likes: 300, comments: 60, shares: 25 },
            score: 0.78,
            captured_at: "2024-01-01T10:15:00Z"
          }
        ]
      };
    }

    if (endpoint.includes('/ideas/list')) {
      return {
        ideas: [
          {
            id: 1,
            title: "AI Content Creation Revolution",
            summary: "Explore how AI is transforming content creation workflows...",
            status: "draft",
            platform_adaptations: {
              x: "🤖 AI is changing content creation! Here's what you need to know... #AI #ContentCreation",
              instagram: "AI tools are revolutionizing how we create content! ✨ What's your experience? #AI #ContentCreation #CreatorEconomy",
              linkedin: "Professional insight: AI agents are transforming content workflows. Key takeaways for marketers..."
            }
          },
          {
            id: 2,
            title: "Creator Economy Trends 2024",
            summary: "Latest trends in the creator economy and how to leverage them...",
            status: "approved",
            platform_adaptations: {
              x: "💰 Creator economy is booming! New opportunities everywhere... #CreatorEconomy",
              instagram: "The creator economy is evolving! 🚀 Share your creator journey below! #CreatorEconomy #ContentStrategy",
              linkedin: "The creator economy presents unprecedented opportunities for professionals. Here's my analysis..."
            }
          }
        ]
      };
    }

    if (endpoint.includes('/auth/accounts')) {
      return {
        accounts: [
          { id: 1, platform: "x", username: "demo_user", status: "connected" },
          { id: 2, platform: "instagram", username: "demo_user", status: "disconnected" },
          { id: 3, platform: "linkedin", username: "demo_user", status: "disconnected" }
        ]
      };
    }

    return { message: "Mock response", data: [] };
  }

  getMockAgentResponse(endpoint, method) {
    if (endpoint.includes('/generate_ideas')) {
      return {
        ideas: [
          {
            id: 1,
            title: "AI Content Creation Revolution",
            summary: "Explore how AI is transforming content creation workflows for modern creators...",
            hook: "Transform your content strategy with AI",
            caption: "🤖 AI is revolutionizing content creation! Here's what every creator needs to know about leveraging AI tools for better, faster content production.",
            hashtags: ["#AI", "#ContentCreation", "#SocialMedia", "#CreatorEconomy"],
            ai_type: "text",
            status: "draft"
          },
          {
            id: 2,
            title: "Creator Economy Insights",
            summary: "Latest trends and opportunities in the creator economy landscape...",
            hook: "Unlock creator economy opportunities",
            caption: "💰 The creator economy is booming! New tools and platforms are creating unprecedented opportunities for content creators.",
            hashtags: ["#CreatorEconomy", "#ContentStrategy", "#SocialMedia"],
            ai_type: "text",
            status: "draft"
          }
        ],
        repurposed_content: {
          x: [
            { idea_id: 1, platform: "x", caption: "🤖 AI is changing content creation! Here's what you need to know... #AI #ContentCreation" },
            { idea_id: 2, platform: "x", caption: "💰 Creator economy is booming! New opportunities everywhere... #CreatorEconomy" }
          ],
          instagram: [
            { idea_id: 1, platform: "instagram", caption: "AI tools are revolutionizing how we create content! ✨ What's your experience? #AI #ContentCreation #CreatorEconomy" },
            { idea_id: 2, platform: "instagram", caption: "The creator economy is evolving! 🚀 Share your creator journey below! #CreatorEconomy #ContentStrategy" }
          ],
          linkedin: [
            { idea_id: 1, platform: "linkedin", caption: "Professional insight: AI agents are transforming content workflows. Key takeaways for marketers..." },
            { idea_id: 2, platform: "linkedin", caption: "The creator economy presents unprecedented opportunities for professionals. Here's my analysis..." }
          ]
        },
        scheduled_posts: [
          { idea_id: 1, platform: "x", suggested_time: "09:00", status: "suggested" },
          { idea_id: 1, platform: "instagram", suggested_time: "11:00", status: "suggested" },
          { idea_id: 1, platform: "linkedin", suggested_time: "08:00", status: "suggested" }
        ],
        count: 2
      };
    }

    if (endpoint.includes('/refresh_trends')) {
      return {
        trends: [
          {
            id: 1,
            source: "linkedin",
            topic: "#AI",
            text: "AI agents are revolutionizing content creation workflows",
            author: "TechInfluencer",
            url: "https://linkedin.com/posts/tech-influencer-ai-agents",
            engagement: { likes: 150, comments: 25, shares: 30 },
            score: 0.85,
            captured_at: "2024-01-01T12:00:00Z"
          },
          {
            id: 2,
            source: "x",
            topic: "#CreatorEconomy",
            text: "The creator economy is booming with new AI-powered tools",
            author: "CreatorExpert",
            url: "https://x.com/creatorexpert/status/1234567890",
            engagement: { likes: 200, comments: 40, shares: 50 },
            score: 0.92,
            captured_at: "2024-01-01T11:30:00Z"
          },
          {
            id: 3,
            source: "instagram",
            topic: "#SocialMedia",
            text: "Social media strategies that actually work in 2024",
            author: "SocialMediaGuru",
            url: "https://instagram.com/p/socialmediaguru123",
            engagement: { likes: 300, comments: 60, shares: 25 },
            score: 0.78,
            captured_at: "2024-01-01T10:15:00Z"
          }
        ]
      };
    }

    return { message: "Mock agent response", data: [] };
  }

  // Health check
  async healthCheck() {
    return this.request('/health');
  }

  // Brand configuration
  async getBrandConfig() {
    return this.request('/config/brand');
  }

  async updateBrandConfig(config) {
    return this.request('/config/brand', {
      method: 'PUT',
      body: JSON.stringify(config),
    });
  }

  // Trends
  async refreshTrends() {
    return this.agentRequest('/refresh_trends', {
      method: 'POST',
    });
  }

  async getTrends() {
    return this.request('/trends/list');
  }

  // Ideas
  async generateIdeas(data) {
    try {
      const result = await this.agentRequest('/generate_ideas', {
        method: 'POST',
        body: JSON.stringify(data),
      });
      
      // Store generated ideas locally for the Ideas page to display
      if (result.ideas) {
        result.ideas.forEach(idea => {
          const newIdea = {
            ...idea,
            id: this.ideasCounter++,
            status: 'draft',
            platform_adaptations: {}
          };
          
          // Add platform adaptations from repurposed content
          if (result.repurposed_content) {
            Object.keys(result.repurposed_content).forEach(platform => {
              const platformContent = result.repurposed_content[platform].find(
                content => content.idea_id === idea.id
              );
              if (platformContent) {
                newIdea.platform_adaptations[platform] = platformContent.caption;
              }
            });
          }
          
          this.generatedIdeas.push(newIdea);
        });
      }
      
      return result;
    } catch (error) {
      // Generate mock ideas even on error
      const mockIdeas = [
        {
          id: this.ideasCounter++,
          title: "AI Content Creation Revolution",
          summary: "Explore how AI is transforming content creation workflows for modern creators. Learn about the latest tools and techniques.",
          status: "draft",
          platform_adaptations: {
            x: "🤖 AI is changing the game! 🚀 \n\nAI agents are revolutionizing how we create content:\n✅ Faster ideation\n✅ Better optimization\n✅ Consistent quality\n\nWhat's your experience with AI tools? #AI #ContentCreation",
            instagram: "AI tools are revolutionizing how we create content! ✨\n\nFrom idea generation to optimization, AI is changing everything. What's your favorite AI tool for content creation?\n\n#AI #ContentCreation #CreatorEconomy #SocialMedia #TechTrends",
            linkedin: "Professional insight: AI agents are transforming content workflows across industries.\n\nKey benefits I've observed:\n• 60% faster content production\n• Improved consistency and quality\n• Better audience targeting\n• Enhanced creative possibilities\n\nHow is your organization leveraging AI for content? #AI #ContentStrategy #DigitalTransformation"
          }
        },
        {
          id: this.ideasCounter++,
          title: "Creator Economy Insights 2024",
          summary: "Latest trends and opportunities in the creator economy landscape. Understand how creators are monetizing their content.",
          status: "draft",
          platform_adaptations: {
            x: "💰 Creator economy update!\n\nThe numbers are incredible:\n📈 $104B market size\n🚀 50M+ creators worldwide\n💡 New monetization models emerging daily\n\nAre you part of the creator economy? #CreatorEconomy #ContentCreator",
            instagram: "The creator economy is evolving! 🚀\n\nNew opportunities everywhere:\n• Brand partnerships\n• Digital products\n• Community building\n• Course creation\n\nShare your creator journey below! 👇\n\n#CreatorEconomy #ContentStrategy #Entrepreneurship #DigitalNomad",
            linkedin: "The creator economy presents unprecedented opportunities for professionals.\n\nMy analysis of current trends:\n• B2B creators seeing 40% higher engagement\n• LinkedIn becoming the go-to platform for thought leadership\n• Personal branding driving career advancement\n• Content creation skills now essential for most roles\n\nThoughts on the professionalization of content creation? #CreatorEconomy #PersonalBranding #ProfessionalDevelopment"
          }
        },
        {
          id: this.ideasCounter++,
          title: "Social Media Strategy 2024",
          summary: "Effective social media strategies that actually work in 2024. Focus on authentic engagement and community building.",
          status: "draft",
          platform_adaptations: {
            x: "📱 Social media strategy that works:\n\n1. Authenticity > Perfection\n2. Community > Followers\n3. Value > Vanity metrics\n4. Consistency > Viral moments\n\nWhat's your #1 social media tip? #SocialMedia #Strategy",
            instagram: "Social media strategies that actually work in 2024! 📱✨\n\nStop chasing algorithms, start building relationships:\n• Be authentic, not perfect\n• Engage genuinely with your community\n• Share valuable insights consistently\n• Focus on quality over quantity\n\nWhat strategy works best for you? 💭\n\n#SocialMedia #Strategy #ContentTips #Community #Authenticity",
            linkedin: "Effective social media strategies for professionals in 2024.\n\nAfter analyzing 1000+ successful profiles, here's what works:\n\n1. Thought leadership content performs 3x better than promotional posts\n2. Personal stories drive 5x more engagement than generic advice\n3. Consistent posting schedule builds 40% stronger audience relationships\n4. Cross-platform content adaptation increases reach by 60%\n\nKey takeaway: Authenticity and value creation remain the foundation of successful social media presence.\n\n#SocialMediaStrategy #DigitalMarketing #ThoughtLeadership"
          }
        }
      ];
      
      this.generatedIdeas.push(...mockIdeas);
      
      return {
        ideas: mockIdeas,
        count: mockIdeas.length
      };
    }
  }

  async getIdeas() {
    try {
      const result = await this.request('/ideas/list');
      // Combine API results with locally generated ideas
      const allIdeas = [...this.generatedIdeas, ...(result.ideas || [])];
      return { ideas: allIdeas };
    } catch (error) {
      // Return locally stored ideas if API fails
      return { ideas: this.generatedIdeas };
    }
  }

  async approveIdea(ideaId) {
    try {
      const result = await this.request(`/agent/approve_idea/${ideaId}`, {
        method: 'POST',
      });
      
      // Update local idea status
      const ideaIndex = this.generatedIdeas.findIndex(idea => idea.id === ideaId);
      if (ideaIndex !== -1) {
        this.generatedIdeas[ideaIndex].status = 'approved';
      }
      
      return result;
    } catch (error) {
      // Update local idea status even if API fails
      const ideaIndex = this.generatedIdeas.findIndex(idea => idea.id === ideaId);
      if (ideaIndex !== -1) {
        this.generatedIdeas[ideaIndex].status = 'approved';
      }
      return { message: 'Idea approved successfully' };
    }
  }

  // OAuth
  async getXAuthUrl() {
    return this.request('/auth/x/login');
  }

  async getInstagramAuthUrl() {
    return this.request('/auth/instagram/login');
  }

  async getLinkedInAuthUrl() {
    return this.request('/auth/linkedin/login');
  }

  async getConnectedAccounts() {
    return this.request('/auth/accounts');
  }

  async disconnectAccount(accountId) {
    return this.request(`/auth/accounts/${accountId}`, {
      method: 'DELETE',
    });
  }

  // Analytics
  async refreshAnalytics() {
    return this.request('/analytics/refresh', {
      method: 'POST',
    });
  }

  // Publishing
  async runPublisher() {
    return this.request('/publish/run', {
      method: 'POST',
    });
  }

  // Scheduling
  async createSchedule(data) {
    return this.request('/schedule/create', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }
}

export const apiService = new ApiService();
export default apiService;
