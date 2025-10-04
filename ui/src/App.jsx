import { useState } from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { Sidebar } from './components/layout/Sidebar'
import { Header } from './components/layout/Header'
import { TrendsPage } from './pages/TrendsPage'
import { IdeasPage } from './pages/IdeasPage'
import { CalendarPage } from './pages/CalendarPage'
import { AnalyticsPage } from './pages/AnalyticsPage'
import { PublishLogPage } from './pages/PublishLogPage'
import { SettingsPage } from './pages/SettingsPage'
import './App.css'

function App() {
  const [currentUser] = useState('demo-user')

  return (
    <Router>
      <div className="min-h-screen bg-slate-900 text-white flex">
        <Sidebar />
        <div className="flex-1 flex flex-col">
          <Header currentUser={currentUser} />
          <main className="flex-1 p-6">
            <Routes>
              <Route path="/" element={<TrendsPage />} />
              <Route path="/trends" element={<TrendsPage />} />
              <Route path="/ideas" element={<IdeasPage />} />
              <Route path="/calendar" element={<CalendarPage />} />
              <Route path="/analytics" element={<AnalyticsPage />} />
              <Route path="/publish-log" element={<PublishLogPage />} />
              <Route path="/settings" element={<SettingsPage />} />
            </Routes>
          </main>
        </div>
      </div>
    </Router>
  )
}

export default App
