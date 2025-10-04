import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Calendar, Clock, Plus } from 'lucide-react'

export function CalendarPage() {
  const [scheduledPosts, setScheduledPosts] = useState([])
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    loadScheduledPosts()
  }, [])

  const loadScheduledPosts = async () => {
    setIsLoading(true)
    try {
      // Simulate API call with timeout
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      // Mock scheduled posts data
      const mockScheduledPosts = [
        {
          id: 1,
          title: "AI Content Creation Tips",
          platform: "linkedin",
          scheduledFor: "2024-01-20T09:00:00Z",
          status: "scheduled",
          content: "🤖 AI is revolutionizing content creation! Here's what every creator needs to know..."
        },
        {
          id: 2,
          title: "Creator Economy Insights",
          platform: "x",
          scheduledFor: "2024-01-20T12:00:00Z",
          status: "scheduled",
          content: "💰 The creator economy is booming! New opportunities everywhere..."
        },
        {
          id: 3,
          title: "Social Media Strategy",
          platform: "instagram",
          scheduledFor: "2024-01-20T19:00:00Z",
          status: "scheduled",
          content: "📱 Social media strategies that actually work in 2024..."
        }
      ]
      
      setScheduledPosts(mockScheduledPosts)
    } catch (error) {
      console.error('Failed to load scheduled posts:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const formatDate = (dateString) => {
    const date = new Date(dateString)
    return date.toLocaleDateString('en-US', {
      weekday: 'short',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  const getPlatformColor = (platform) => {
    const colors = {
      x: 'bg-black',
      instagram: 'bg-gradient-to-r from-purple-500 to-pink-500',
      linkedin: 'bg-blue-600',
      tiktok: 'bg-gray-600'
    }
    return colors[platform] || 'bg-gray-600'
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Calendar</h1>
          <p className="text-slate-400">Manage your scheduled content</p>
        </div>
        <Button className="btn-primary">
          <Plus className="w-4 h-4 mr-2" />
          Schedule Post
        </Button>
      </div>

      {/* Calendar View */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Calendar Widget */}
        <div className="lg:col-span-2">
          <Card className="bg-slate-800 border-slate-700">
            <CardHeader>
              <CardTitle className="text-white flex items-center">
                <Calendar className="w-5 h-5 mr-2" />
                January 2024
              </CardTitle>
            </CardHeader>
            <CardContent>
              {isLoading ? (
                <div className="grid grid-cols-7 gap-2">
                  {Array.from({ length: 35 }).map((_, i) => (
                    <div key={i} className="loading-shimmer h-10 bg-slate-700 rounded"></div>
                  ))}
                </div>
              ) : (
                <div className="grid grid-cols-7 gap-2 text-center">
                  {/* Days of week */}
                  {['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].map((day) => (
                    <div key={day} className="p-2 text-sm font-medium text-slate-400">
                      {day}
                    </div>
                  ))}
                  
                  {/* Calendar days */}
                  {Array.from({ length: 35 }).map((_, i) => {
                    const dayNumber = i - 6 // Start from previous month
                    const isCurrentMonth = dayNumber > 0 && dayNumber <= 31
                    const hasScheduledPost = isCurrentMonth && [15, 20, 25].includes(dayNumber)
                    
                    return (
                      <div
                        key={i}
                        className={`
                          p-2 h-10 flex items-center justify-center text-sm rounded
                          ${isCurrentMonth 
                            ? 'text-white hover:bg-slate-700 cursor-pointer' 
                            : 'text-slate-600'
                          }
                          ${hasScheduledPost ? 'bg-purple-600 text-white' : ''}
                        `}
                      >
                        {isCurrentMonth ? dayNumber : ''}
                        {hasScheduledPost && (
                          <div className="w-1 h-1 bg-white rounded-full ml-1"></div>
                        )}
                      </div>
                    )
                  })}
                </div>
              )}
            </CardContent>
          </Card>
        </div>

        {/* Scheduled Posts */}
        <div>
          <Card className="bg-slate-800 border-slate-700">
            <CardHeader>
              <CardTitle className="text-white flex items-center">
                <Clock className="w-5 h-5 mr-2" />
                Upcoming Posts
              </CardTitle>
            </CardHeader>
            <CardContent>
              {isLoading ? (
                <div className="space-y-4">
                  {[1, 2, 3].map((i) => (
                    <div key={i} className="p-3 bg-slate-700 rounded-lg">
                      <div className="loading-shimmer h-4 bg-slate-600 rounded mb-2"></div>
                      <div className="loading-shimmer h-3 bg-slate-600 rounded w-2/3"></div>
                    </div>
                  ))}
                </div>
              ) : scheduledPosts.length > 0 ? (
                <div className="space-y-4">
                  {scheduledPosts.map((post) => (
                    <div key={post.id} className="p-3 bg-slate-700 rounded-lg">
                      <div className="flex items-center justify-between mb-2">
                        <h4 className="font-medium text-white text-sm">{post.title}</h4>
                        <div className={`w-6 h-6 rounded ${getPlatformColor(post.platform)} flex items-center justify-center text-white text-xs font-bold`}>
                          {post.platform.charAt(0).toUpperCase()}
                        </div>
                      </div>
                      <p className="text-xs text-slate-400 mb-2">
                        {formatDate(post.scheduledFor)}
                      </p>
                      <p className="text-xs text-slate-300 line-clamp-2">
                        {post.content}
                      </p>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-8">
                  <Calendar className="w-12 h-12 text-slate-600 mx-auto mb-3" />
                  <p className="text-slate-400 text-sm">No scheduled posts</p>
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Quick Stats */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card className="bg-slate-800 border-slate-700">
          <CardContent className="p-6 text-center">
            <div className="text-2xl font-bold text-white mb-1">
              {scheduledPosts.length}
            </div>
            <div className="text-sm text-slate-400">Scheduled Posts</div>
          </CardContent>
        </Card>
        
        <Card className="bg-slate-800 border-slate-700">
          <CardContent className="p-6 text-center">
            <div className="text-2xl font-bold text-white mb-1">3</div>
            <div className="text-sm text-slate-400">Platforms</div>
          </CardContent>
        </Card>
        
        <Card className="bg-slate-800 border-slate-700">
          <CardContent className="p-6 text-center">
            <div className="text-2xl font-bold text-white mb-1">7</div>
            <div className="text-sm text-slate-400">Days Ahead</div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
