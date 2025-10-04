export function Header({ currentUser }) {
  return (
    <header className="bg-slate-800 border-b border-slate-700 px-6 py-4">
      <div className="flex items-center justify-between">
        <div className="text-sm text-slate-400">
          Connected as <span className="text-white font-medium">{currentUser}</span>
        </div>
      </div>
    </header>
  )
}
