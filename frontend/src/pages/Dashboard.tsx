import { useEffect } from 'react'
import ChatInterface from '../components/ChatInterface'
import DocumentLibrary from '../components/DocumentLibrary'
import UploadPanel from '../components/UploadPanel'
import { useChat } from '../hooks/useChat'
import { useDocuments } from '../hooks/useDocuments'

export default function Dashboard() {
  const { documents, loading: docLoading, error: docError, fetchDocuments, uploadDocument } =
    useDocuments()
  const { messages, loading: chatLoading, error: chatError, sendMessage, clearChat } = useChat()

  useEffect(() => {
    void fetchDocuments()
  }, [fetchDocuments])

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 px-6 py-4 shadow-sm">
        <div className="max-w-7xl mx-auto flex items-center gap-3">
          <span className="text-2xl">🔍</span>
          <div>
            <h1 className="text-xl font-bold text-gray-900">RAG Knowledge Assistant</h1>
            <p className="text-xs text-gray-500">AI-powered document Q&amp;A</p>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-6 py-6 grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left sidebar */}
        <div className="lg:col-span-1 space-y-6">
          <UploadPanel onUpload={uploadDocument} loading={docLoading} />

          {docError && (
            <div className="bg-red-50 border border-red-200 text-red-700 text-sm rounded-lg px-4 py-3">
              ⚠ {docError}
            </div>
          )}

          <DocumentLibrary
            documents={documents}
            loading={docLoading}
            onRefresh={fetchDocuments}
          />
        </div>

        {/* Main chat area */}
        <div className="lg:col-span-2">
          <ChatInterface
            messages={messages}
            loading={chatLoading}
            error={chatError}
            onSend={sendMessage}
            onClear={clearChat}
          />
        </div>
      </main>
    </div>
  )
}
