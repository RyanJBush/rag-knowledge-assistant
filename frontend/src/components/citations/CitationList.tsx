import type { Citation } from "../../types/api";

interface CitationListProps {
  citations: Citation[];
}

function CitationList({ citations }: CitationListProps) {
  if (!citations.length) {
    return null;
  }

  return (
    <div className="mt-4 rounded-md border border-slate-200 bg-slate-50 p-3">
      <h3 className="text-sm font-semibold text-slate-800">Citations</h3>
      <ul className="mt-2 space-y-2">
        {citations.map((citation) => (
          <li key={`${citation.document_id}-${citation.chunk_id}`} className="rounded border border-slate-200 bg-white p-2">
            <p className="text-xs font-medium text-slate-800">
              {citation.source} • {citation.chunk_id} • score {citation.score}
              {citation.page ? ` • page ${citation.page}` : ""}
            </p>
            <p className="mt-1 text-xs text-slate-600">{citation.snippet}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default CitationList;
