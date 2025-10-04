import { Link, useLocation } from 'react-router-dom'
import { 
  TrendingUp, 
  Lightbulb, 
  Calendar, 
  BarChart3, 
  FileText, 
  Settings 
} from 'lucide-react'

const navigationItems = [
  { name: 'Trends', path: '/trends', icon: TrendingUp },
  { name: 'Ideas', path: '/ideas', icon: Lightbulb },
  { name: 'Calendar', path: '/calendar', icon: Calendar },
  { name: 'Analytics', path: '/analytics', icon: BarChart3 },
  { name: 'Publish Log', path: '/publish-log', icon: FileText },
  { name: 'Settings', path: '/settings', icon: Settings },
]

export function Sidebar() {
  const location = useLocation()

  return (
    <div className="w-64 bg-slate-800 border-r border-slate-700 flex flex-col">
      {/* Logo/Title */}
      <div className="p-6 border-b border-slate-700">
        <h1 className="text-xl font-bold bg-gradient-to-r from-purple-400 to-orange-400 bg-clip-text text-transparent">
          Social Agent
        </h1>
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-4">
        <ul className="space-y-2">
          {navigationItems.map((item) => {
            const Icon = item.icon
            const isActive = location.pathname === item.path || 
                           (location.pathname === '/' && item.path === '/trends')
            
            return (
              <li key={item.name}>
                <Link
                  to={item.path}
                  className={`flex items-center gap-3 px-3 py-2 rounded-lg transition-colors ${
                    isActive 
                      ? 'sidebar-active' 
                      : 'text-slate-300 hover:text-white hover:bg-slate-700'
                  }`}
                >
                  <Icon size={20} />
                  <span className="font-medium">{item.name}</span>
                </Link>
              </li>
            )
          })}
        </ul>
      </nav>
    </div>
  )
}
