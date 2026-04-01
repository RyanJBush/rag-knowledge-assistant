import type { Citation } from '../types'

interface Props {
  citations: Citation[]
}

export default function CitationPanel({ citations }: Props) {
  if (citations.length === 0) return null

  return (
    <div className="mt-3 border-t border-gray-100 pt-3">
      <p className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">
        Sources
      </p>
      <div className="space-y-2">
        {citations.map((c, i) => (
          <div
            key={`${c.document_id}-${c.chunk_index}`}
            className="bg-gray-50 rounded-lg p-3 text-xs border border-gray-100"
          >
            <div className="flex items-center justify-between mb-1">
              <span className="font-medium text-gray-700">
                [{i + 1}] {c.source_filename}
              </span>
              <span className="text-gray-400">chunk {c.chunk_index}</span>
            </div>
            <p className="text-gray-600 line-clamp-3 italic">"{c.snippet}"</p>
          </div>
        ))}
      </div>
    </div>
  )
}
