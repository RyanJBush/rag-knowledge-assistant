import type { DocumentInfo } from '../types'

interface Props {
  documents: DocumentInfo[]
  loading: boolean
  onRefresh: () => void
}

function formatDate(iso: string) {
  return new Date(iso).toLocaleString()
}

function FileTypeIcon({ type }: { type: string }) {
  return (
    <span className="inline-block text-xs font-mono bg-gray-100 text-gray-600 px-1.5 py-0.5 rounded">
      {type}
    </span>
  )
}

export default function DocumentLibrary({ documents, loading, onRefresh }: Props) {
  return (
    <div className="bg-white rounded-xl border border-gray-200 p-6 shadow-sm">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold text-gray-800">Document Library</h2>
        <button
          onClick={onRefresh}
          disabled={loading}
          className="text-sm text-blue-500 hover:text-blue-700 disabled:opacity-50"
        >
          {loading ? 'Loading…' : '↺ Refresh'}
        </button>
      </div>

      {documents.length === 0 && !loading && (
        <div className="text-center py-8 text-gray-400">
          <div className="text-3xl mb-2">📂</div>
          <p className="text-sm">No documents uploaded yet.</p>
        </div>
      )}

      {loading && (
        <div className="text-center py-6 text-gray-400 text-sm">Loading…</div>
      )}

      <ul className="divide-y divide-gray-100">
        {documents.map((doc) => (
          <li key={doc.id} className="py-3 flex items-start gap-3">
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-gray-800 truncate">
                {doc.original_filename}
              </p>
              <p className="text-xs text-gray-400 mt-0.5">
                {doc.chunk_count} chunks · {formatDate(doc.uploaded_at)}
              </p>
            </div>
            <div className="flex items-center gap-2 shrink-0">
              <FileTypeIcon type={doc.file_type} />
              <span
                className={`text-xs px-2 py-0.5 rounded-full ${
                  doc.status === 'processed'
                    ? 'bg-green-100 text-green-700'
                    : 'bg-yellow-100 text-yellow-700'
                }`}
              >
                {doc.status}
              </span>
            </div>
          </li>
        ))}
      </ul>
    </div>
  )
}
