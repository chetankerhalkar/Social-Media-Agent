import { Card, CardContent } from '@/components/ui/card'

export function PublishLogPage() {
  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-white">Publish Log</h1>
      
      <Card className="bg-slate-800 border-slate-700">
        <CardContent className="p-6">
          <div className="text-center py-12">
            <p className="text-slate-400">No publish history yet</p>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
