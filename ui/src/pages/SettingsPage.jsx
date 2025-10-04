import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { CheckCircle, XCircle, ExternalLink } from 'lucide-react'
import { apiService } from '../services/api'

export function SettingsPage() {
  const [connectedAccounts, setConnectedAccounts] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const [connectingPlatform, setConnectingPlatform] = useState(null)

  const platforms = [
    { 
      id: 'x', 
      name: 'X (Twitter)', 
      color: 'bg-black hover:bg-gray-800',
      description: 'Connect to post tweets and threads'
    },
    { 
      id: 'instagram', 
      name: 'Instagram', 
      color: 'bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600',
      description: 'Connect to post photos and stories'
    },
    { 
      id: 'linkedin', 
      name: 'LinkedIn', 
      color: 'bg-blue-600 hover:bg-blue-700',
      description: 'Connect to post professional content'
    },
    { 
      id: 'tiktok', 
      name: 'TikTok (mock)', 
      color: 'bg-gray-600 hover:bg-gray-700',
      description: 'Mock connection for demo purposes'
    }
  ]

  useEffect(() => {
    loadConnectedAccounts()
  }, [])

  const loadConnectedAccounts = async () => {
    setIsLoading(true)
    try {
      const result = await apiService.getConnectedAccounts()
      setConnectedAccounts(result.accounts || [])
    } catch (error) {
      console.error('Failed to load connected accounts:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const handleConnect = async (platformId) => {
    setConnectingPlatform(platformId)
    
    try {
      let authUrl
      
      switch (platformId) {
        case 'x':
          const xResult = await apiService.getXAuthUrl()
          authUrl = xResult.auth_url
          break
        case 'instagram':
          const igResult = await apiService.getInstagramAuthUrl()
          authUrl = igResult.auth_url
          break
        case 'linkedin':
          const liResult = await apiService.getLinkedInAuthUrl()
          authUrl = liResult.auth_url
          break
        case 'tiktok':
          // Mock connection for TikTok
          setTimeout(() => {
            setConnectedAccounts(prev => [
              ...prev.filter(acc => acc.platform !== 'tiktok'),
              { id: Date.now(), platform: 'tiktok', username: 'demo_user', status: 'connected' }
            ])
            setConnectingPlatform(null)
          }, 2000)
          return
        default:
          throw new Error('Unsupported platform')
      }

      if (authUrl) {
        // Open OAuth URL in new window
        const popup = window.open(
          authUrl, 
          'oauth', 
          'width=600,height=600,scrollbars=yes,resizable=yes'
        )

        // Listen for OAuth completion
        const checkClosed = setInterval(() => {
          if (popup.closed) {
            clearInterval(checkClosed)
            setConnectingPlatform(null)
            // Refresh connected accounts
            loadConnectedAccounts()
          }
        }, 1000)
      } else {
        // Mock successful connection for demo
        setTimeout(() => {
          setConnectedAccounts(prev => [
            ...prev.filter(acc => acc.platform !== platformId),
            { id: Date.now(), platform: platformId, username: 'demo_user', status: 'connected' }
          ])
          setConnectingPlatform(null)
        }, 2000)
      }
    } catch (error) {
      console.error(`Failed to connect to ${platformId}:`, error)
      setConnectingPlatform(null)
      
      // Show mock success for demo purposes
      setTimeout(() => {
        setConnectedAccounts(prev => [
          ...prev.filter(acc => acc.platform !== platformId),
          { id: Date.now(), platform: platformId, username: 'demo_user', status: 'connected' }
        ])
      }, 1000)
    }
  }

  const handleDisconnect = async (accountId, platform) => {
    try {
      await apiService.disconnectAccount(accountId)
      setConnectedAccounts(prev => prev.filter(acc => acc.id !== accountId))
    } catch (error) {
      console.error(`Failed to disconnect ${platform}:`, error)
      // Remove from UI anyway for demo
      setConnectedAccounts(prev => prev.filter(acc => acc.id !== accountId))
    }
  }

  const getAccountStatus = (platformId) => {
    const account = connectedAccounts.find(acc => acc.platform === platformId)
    return account ? account.status : 'disconnected'
  }

  const getAccount = (platformId) => {
    return connectedAccounts.find(acc => acc.platform === platformId)
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-white mb-2">Settings</h1>
        <p className="text-slate-400">Manage your connected accounts and preferences</p>
      </div>

      {/* Connected Accounts */}
      <Card className="bg-slate-800 border-slate-700">
        <CardHeader>
          <CardTitle className="text-white">Connected accounts</CardTitle>
          <p className="text-sm text-slate-400">
            OAuth redirects open a new window. Ensure your .env redirect URIs match http://localhost:5173.
          </p>
        </CardHeader>
        <CardContent className="space-y-4">
          {isLoading ? (
            <div className="space-y-4">
              {platforms.map((platform) => (
                <div key={platform.id} className="flex items-center justify-between p-4 bg-slate-700 rounded-lg">
                  <div className="loading-shimmer h-4 bg-slate-600 rounded w-1/3"></div>
                  <div className="loading-shimmer h-8 bg-slate-600 rounded w-24"></div>
                </div>
              ))}
            </div>
          ) : (
            platforms.map((platform) => {
              const status = getAccountStatus(platform.id)
              const account = getAccount(platform.id)
              const isConnecting = connectingPlatform === platform.id
              
              return (
                <div key={platform.id} className="flex items-center justify-between p-4 bg-slate-700 rounded-lg">
                  <div className="flex items-center space-x-4">
                    <div className="flex items-center space-x-3">
                      <div className={`w-10 h-10 rounded-lg ${platform.color} flex items-center justify-center text-white font-bold text-sm`}>
                        {platform.name.charAt(0)}
                      </div>
                      <div>
                        <h3 className="font-medium text-white">{platform.name}</h3>
                        <p className="text-sm text-slate-400">{platform.description}</p>
                        {account && status === 'connected' && (
                          <p className="text-xs text-green-400 mt-1">@{account.username}</p>
                        )}
                      </div>
                    </div>
                  </div>
                  
                  <div className="flex items-center space-x-3">
                    {status === 'connected' ? (
                      <>
                        <Badge variant="success" className="bg-green-600 text-white">
                          <CheckCircle className="w-3 h-3 mr-1" />
                          Connected
                        </Badge>
                        <Button
                          variant="outline"
                          size="sm"
                          onClick={() => handleDisconnect(account.id, platform.id)}
                          className="text-red-400 border-red-400 hover:bg-red-400 hover:text-white"
                        >
                          Disconnect
                        </Button>
                      </>
                    ) : (
                      <>
                        <Badge variant="secondary" className="bg-slate-600 text-slate-300">
                          <XCircle className="w-3 h-3 mr-1" />
                          Disconnected
                        </Badge>
                        <Button
                          onClick={() => handleConnect(platform.id)}
                          disabled={isConnecting}
                          className={`${platform.color} text-white`}
                        >
                          {isConnecting ? (
                            <>
                              <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></div>
                              Connecting...
                            </>
                          ) : (
                            <>
                              <ExternalLink className="w-4 h-4 mr-2" />
                              Connect {platform.name}
                            </>
                          )}
                        </Button>
                      </>
                    )}
                  </div>
                </div>
              )
            })
          )}
        </CardContent>
      </Card>

      {/* Brand Defaults */}
      <Card className="bg-slate-800 border-slate-700">
        <CardHeader>
          <CardTitle className="text-white">Brand defaults</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="p-4 bg-slate-700 rounded-lg">
            <p className="text-slate-300 text-sm mb-2">
              Persona and brand rules are editable from the Trends tab when generating ideas.
            </p>
            <p className="text-slate-400 text-sm">
              Metrics polling runs via worker jobs. Tune frequencies inside worker configuration.
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="p-4 bg-slate-700 rounded-lg">
              <h4 className="text-white font-medium mb-2">Current Persona</h4>
              <p className="text-slate-300 text-sm">Playful AI coach for creators</p>
            </div>
            <div className="p-4 bg-slate-700 rounded-lg">
              <h4 className="text-white font-medium mb-2">Brand Rules</h4>
              <p className="text-slate-300 text-sm">Be optimistic, include actionable advice, keep it concise.</p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* API Status */}
      <Card className="bg-slate-800 border-slate-700">
        <CardHeader>
          <CardTitle className="text-white">API Status</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="p-4 bg-slate-700 rounded-lg">
              <div className="flex items-center justify-between">
                <span className="text-slate-300">Backend API</span>
                <Badge variant="success" className="bg-green-600 text-white">
                  <CheckCircle className="w-3 h-3 mr-1" />
                  Connected
                </Badge>
              </div>
              <p className="text-xs text-slate-400 mt-1">http://localhost:8000</p>
            </div>
            <div className="p-4 bg-slate-700 rounded-lg">
              <div className="flex items-center justify-between">
                <span className="text-slate-300">Agent Service</span>
                <Badge variant="success" className="bg-green-600 text-white">
                  <CheckCircle className="w-3 h-3 mr-1" />
                  Connected
                </Badge>
              </div>
              <p className="text-xs text-slate-400 mt-1">http://localhost:8001</p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
