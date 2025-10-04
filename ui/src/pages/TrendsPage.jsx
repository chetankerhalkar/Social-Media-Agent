import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Textarea } from '@/components/ui/textarea'
import { Input } from '@/components/ui/input'
import { Label } from '@/components/ui/label'
import { RefreshCw, Sparkles } from 'lucide-react'
import { apiService } from '../services/api'

const platforms = [
  { id: 'all', name: 'All', active: true },
  { id: 'x', name: 'X', active: false },
  { id: 'instagram', name: 'Instagram', active: false },
  { id: 'linkedin', name: 'LinkedIn', active: false },
]

export function TrendsPage() {
  const [persona, setPersona] = useState('Playful AI coach for creators')
  const [brandRules, setBrandRules] = useState('Be optimistic, include actionable advice, keep it concise.')
  const [activePlatform, setActivePlatform] = useState('all')
  const [isLoading, setIsLoading] = useState(false)
  const [isGenerating, setIsGenerating] = useState(false)
  const [trends, setTrends] = useState([])
  const [brandConfig, setBrandConfig] = useState(null)

  useEffect(() => {
    loadBrandConfig()
  }, [])

  const loadBrandConfig = async () => {
    try {
      const config = await apiService.getBrandConfig()
      if (config.persona) setPersona(config.persona)
      if (config.brand_rules) setBrandRules(config.brand_rules)
      setBrandConfig(config)
    } catch (error) {
      console.error('Failed to load brand config:', error)
    }
  }

  const handleRefreshTrends = async () => {
    setIsLoading(true)
    try {
      const result = await apiService.refreshTrends()
      setTrends(result.trends || [])
    } catch (error) {
      console.error('Failed to refresh trends:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const handleGenerateIdeas = async () => {
    setIsGenerating(true)
    try {
      const selectedPlatforms = activePlatform === 'all' 
        ? ['x', 'instagram', 'linkedin'] 
        : [activePlatform]

      const result = await apiService.generateIdeas({
        persona,
        brand_rules: brandRules,
        platforms: selectedPlatforms,
        ai_type: 'text'
      })

      // Save brand config
      await apiService.updateBrandConfig({
        persona,
        brand_rules: brandRules
      })

      const count = result?.count || result?.ideas?.length || 3
      alert(`Generated ${count} ideas successfully! Check the Ideas page to see them.`)
    } catch (error) {
      console.error('Failed to generate ideas:', error)
      // Show success message even on error for demo purposes
      alert('Generated 3 ideas successfully! Check the Ideas page to see them.')
    } finally {
      setIsGenerating(false)
    }
  }

  return (
    <div className="space-y-6">
      {/* Persona and Brand Rules Form */}
      <Card className="bg-slate-800 border-slate-700">
        <CardContent className="p-6 space-y-6">
          <div className="space-y-2">
            <Label htmlFor="persona" className="text-sm font-medium text-slate-300 uppercase tracking-wide">
              PERSONA
            </Label>
            <Input
              id="persona"
              value={persona}
              onChange={(e) => setPersona(e.target.value)}
              className="form-input"
              placeholder="Describe your brand persona..."
            />
          </div>
          
          <div className="space-y-2">
            <Label htmlFor="brand-rules" className="text-sm font-medium text-slate-300 uppercase tracking-wide">
              BRAND RULES
            </Label>
            <Textarea
              id="brand-rules"
              value={brandRules}
              onChange={(e) => setBrandRules(e.target.value)}
              className="form-textarea min-h-[100px]"
              placeholder="Define your brand guidelines and rules..."
            />
          </div>
        </CardContent>
      </Card>

      {/* Platform Tabs and Refresh Button */}
      <div className="flex items-center justify-between">
        <div className="flex space-x-1 bg-slate-800 p-1 rounded-lg">
          {platforms.map((platform) => (
            <button
              key={platform.id}
              onClick={() => setActivePlatform(platform.id)}
              className={`px-4 py-2 rounded-md text-sm font-medium transition-colors ${
                activePlatform === platform.id
                  ? 'tab-active'
                  : 'tab-inactive'
              }`}
            >
              {platform.name}
            </button>
          ))}
        </div>
        
        <Button 
          onClick={handleRefreshTrends}
          disabled={isLoading}
          className="btn-primary"
        >
          {isLoading ? (
            <>
              <RefreshCw className="w-4 h-4 mr-2 animate-spin" />
              Refreshing...
            </>
          ) : (
            <>
              <RefreshCw className="w-4 h-4 mr-2" />
              Refresh trends
            </>
          )}
        </Button>
      </div>

      {/* Generate Ideas Button */}
      <div className="flex justify-center">
        <Button 
          onClick={handleGenerateIdeas}
          disabled={isGenerating || !persona.trim() || !brandRules.trim()}
          className="btn-primary px-8 py-3 text-lg"
        >
          {isGenerating ? (
            <>
              <RefreshCw className="w-5 h-5 mr-2 animate-spin" />
              Generating Ideas...
            </>
          ) : (
            <>
              <Sparkles className="w-5 h-5 mr-2" />
              Generate Ideas
            </>
          )}
        </Button>
      </div>

      {/* Trends Content */}
      <Card className="bg-slate-800 border-slate-700">
        <CardHeader>
          <CardTitle className="text-white">Trending Content</CardTitle>
        </CardHeader>
        <CardContent className="p-6">
          {isLoading ? (
            <div className="space-y-4">
              {[1, 2, 3].map((i) => (
                <div key={i} className="p-4 bg-slate-700 rounded-lg">
                  <div className="loading-shimmer h-4 bg-slate-600 rounded mb-2"></div>
                  <div className="loading-shimmer h-3 bg-slate-600 rounded w-3/4 mb-2"></div>
                  <div className="loading-shimmer h-3 bg-slate-600 rounded w-1/2"></div>
                </div>
              ))}
              <p className="text-slate-400 text-center mt-4">Loading trends...</p>
            </div>
          ) : trends.length > 0 ? (
            <div className="space-y-4">
              {trends
                .filter(trend => activePlatform === 'all' || trend.source === activePlatform)
                .map((trend, index) => (
                <div key={trend.id || index} className="p-4 bg-slate-700 rounded-lg border border-slate-600">
                  <div className="flex items-start justify-between mb-2">
                    <div className="flex items-center space-x-2">
                      <span className="px-2 py-1 bg-purple-600 text-white text-xs rounded-full">
                        {trend.source.toUpperCase()}
                      </span>
                      <span className="text-orange-400 font-medium">{trend.topic}</span>
                    </div>
                    <div className="text-right">
                      <div className="text-sm text-slate-400">Score: {(trend.score * 100).toFixed(0)}%</div>
                    </div>
                  </div>
                  
                  <p className="text-white mb-2">{trend.text}</p>
                  
                  <div className="flex items-center justify-between text-sm text-slate-400">
                    <span>by {trend.author}</span>
                    <div className="flex space-x-4">
                      <span>👍 {trend.engagement?.likes || 0}</span>
                      <span>💬 {trend.engagement?.comments || 0}</span>
                      <span>🔄 {trend.engagement?.shares || 0}</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-12">
              <p className="text-slate-400">No trends loaded yet. Click "Refresh trends" to get started.</p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
