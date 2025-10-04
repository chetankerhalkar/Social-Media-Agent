import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { RefreshCw, CheckCircle, Calendar, Send } from 'lucide-react'
import { apiService } from '../services/api'

const statusColumns = [
  { id: 'draft', title: 'Draft', color: 'bg-slate-600' },
  { id: 'approved', title: 'Approved', color: 'bg-green-600' },
  { id: 'scheduled', title: 'Scheduled', color: 'bg-blue-600' },
  { id: 'posted', title: 'Posted', color: 'bg-purple-600' },
]

export function IdeasPage() {
  const [ideas, setIdeas] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const [isRefreshing, setIsRefreshing] = useState(false)

  useEffect(() => {
    loadIdeas()
  }, [])

  const loadIdeas = async () => {
    setIsLoading(true)
    try {
      const result = await apiService.getIdeas()
      setIdeas(result.ideas || [])
    } catch (error) {
      console.error('Failed to load ideas:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const handleRefresh = async () => {
    setIsRefreshing(true)
    try {
      await loadIdeas()
    } finally {
      setIsRefreshing(false)
    }
  }

  const handleApproveIdea = async (ideaId) => {
    try {
      await apiService.approveIdea(ideaId)
      // Update the idea status locally
      setIdeas(prevIdeas => 
        prevIdeas.map(idea => 
          idea.id === ideaId ? { ...idea, status: 'approved' } : idea
        )
      )
    } catch (error) {
      console.error('Failed to approve idea:', error)
    }
  }

  const handleScheduleIdea = async (ideaId) => {
    try {
      // Update the idea status locally
      setIdeas(prevIdeas => 
        prevIdeas.map(idea => 
          idea.id === ideaId ? { 
            ...idea, 
            status: 'scheduled',
            scheduledFor: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString() // Tomorrow
          } : idea
        )
      )
    } catch (error) {
      console.error('Failed to schedule idea:', error)
    }
  }

  const handlePublishIdea = async (ideaId) => {
    try {
      // Update the idea status locally
      setIdeas(prevIdeas => 
        prevIdeas.map(idea => 
          idea.id === ideaId ? { 
            ...idea, 
            status: 'posted',
            publishedAt: new Date().toISOString(),
            engagement: { likes: Math.floor(Math.random() * 200) + 50, comments: Math.floor(Math.random() * 30) + 10, shares: Math.floor(Math.random() * 20) + 5 }
          } : idea
        )
      )
    } catch (error) {
      console.error('Failed to publish idea:', error)
    }
  }

  const getIdeasByStatus = (status) => {
    return ideas.filter(idea => idea.status === status)
  }

  const renderIdeaCard = (idea) => (
    <Card key={idea.id} className="bg-slate-700 border-slate-600 mb-4">
      <CardHeader className="pb-3">
        <CardTitle className="text-white text-sm font-medium">
          {idea.title}
        </CardTitle>
      </CardHeader>
      <CardContent className="pt-0">
        <p className="text-slate-300 text-sm mb-3 line-clamp-3">
          {idea.summary}
        </p>
        
        {/* Platform Adaptations */}
        {idea.platform_adaptations && (
          <div className="space-y-2 mb-3">
            <p className="text-xs text-slate-400 font-medium">Platform Adaptations:</p>
            {Object.entries(idea.platform_adaptations).map(([platform, content]) => (
              <div key={platform} className="bg-slate-800 p-2 rounded text-xs">
                <div className="flex items-center mb-1">
                  <span className="px-2 py-1 bg-purple-600 text-white text-xs rounded-full mr-2">
                    {platform.toUpperCase()}
                  </span>
                </div>
                <p className="text-slate-300 line-clamp-2">{content}</p>
              </div>
            ))}
          </div>
        )}

        {/* Engagement Metrics for Posted Ideas */}
        {idea.status === 'posted' && idea.engagement && (
          <div className="bg-slate-800 p-2 rounded mb-3">
            <p className="text-xs text-slate-400 font-medium mb-1">Engagement:</p>
            <div className="flex space-x-4 text-xs text-slate-300">
              <span>👍 {idea.engagement.likes}</span>
              <span>💬 {idea.engagement.comments}</span>
              <span>🔄 {idea.engagement.shares}</span>
            </div>
            <p className="text-xs text-slate-400 mt-1">
              Published: {new Date(idea.publishedAt).toLocaleDateString()}
            </p>
          </div>
        )}

        {/* Scheduled Info */}
        {idea.status === 'scheduled' && idea.scheduledFor && (
          <div className="bg-blue-900/30 p-2 rounded mb-3">
            <p className="text-xs text-blue-300">
              📅 Scheduled for: {new Date(idea.scheduledFor).toLocaleString()}
            </p>
          </div>
        )}

        {/* Action Buttons */}
        <div className="flex space-x-2">
          {idea.status === 'draft' && (
            <Button
              size="sm"
              onClick={() => handleApproveIdea(idea.id)}
              className="btn-primary text-xs"
            >
              <CheckCircle className="w-3 h-3 mr-1" />
              Approve
            </Button>
          )}
          {idea.status === 'approved' && (
            <Button
              size="sm"
              onClick={() => handleScheduleIdea(idea.id)}
              className="bg-blue-600 hover:bg-blue-700 text-white text-xs"
            >
              <Calendar className="w-3 h-3 mr-1" />
              Schedule
            </Button>
          )}
          {idea.status === 'scheduled' && (
            <Button
              size="sm"
              onClick={() => handlePublishIdea(idea.id)}
              className="bg-green-600 hover:bg-green-700 text-white text-xs"
            >
              <Send className="w-3 h-3 mr-1" />
              Publish
            </Button>
          )}
        </div>
      </CardContent>
    </Card>
  )

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-white">Content pipeline</h1>
        <Button 
          onClick={handleRefresh}
          disabled={isRefreshing}
          className="btn-primary"
        >
          {isRefreshing ? (
            <>
              <RefreshCw className="w-4 h-4 mr-2 animate-spin" />
              Refreshing...
            </>
          ) : (
            <>
              <RefreshCw className="w-4 h-4 mr-2" />
              Refresh
            </>
          )}
        </Button>
      </div>

      {/* Kanban Board */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {statusColumns.map((column) => {
          const columnIdeas = getIdeasByStatus(column.id)
          
          return (
            <div key={column.id} className="space-y-4">
              {/* Column Header */}
              <div className="flex items-center space-x-2">
                <div className={`w-3 h-3 rounded-full ${column.color}`}></div>
                <h3 className="font-medium text-white">{column.title}</h3>
                <span className="text-sm text-slate-400">({columnIdeas.length})</span>
              </div>

              {/* Column Content */}
              <div className="space-y-3">
                {isLoading ? (
                  // Loading skeleton
                  <div className="space-y-3">
                    {[1, 2].map((i) => (
                      <Card key={i} className="bg-slate-700 border-slate-600">
                        <CardContent className="p-4">
                          <div className="loading-shimmer h-4 bg-slate-600 rounded mb-2"></div>
                          <div className="loading-shimmer h-3 bg-slate-600 rounded w-3/4 mb-2"></div>
                          <div className="loading-shimmer h-3 bg-slate-600 rounded w-1/2"></div>
                        </CardContent>
                      </Card>
                    ))}
                  </div>
                ) : columnIdeas.length > 0 ? (
                  columnIdeas.map(renderIdeaCard)
                ) : (
                  <Card className="bg-slate-800 border-slate-700 border-dashed">
                    <CardContent className="p-6 text-center">
                      <p className="text-slate-400 text-sm">
                        {column.id === 'draft' 
                          ? 'No draft ideas yet. Generate some ideas from the Trends page!'
                          : `No ${column.title.toLowerCase()} ideas`
                        }
                      </p>
                    </CardContent>
                  </Card>
                )}
              </div>
            </div>
          )
        })}
      </div>

      {/* Empty State */}
      {!isLoading && ideas.length === 0 && (
        <Card className="bg-slate-800 border-slate-700">
          <CardContent className="p-12 text-center">
            <div className="text-slate-400 mb-4">
              <div className="w-16 h-16 bg-slate-700 rounded-full flex items-center justify-center mx-auto mb-4">
                💡
              </div>
              <h3 className="text-lg font-medium text-white mb-2">No ideas yet</h3>
              <p className="text-sm">
                Generate your first content ideas by going to the Trends page and clicking "Generate Ideas".
              </p>
            </div>
            <Button 
              onClick={() => window.location.href = '/trends'} 
              className="btn-primary"
            >
              Go to Trends
            </Button>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
