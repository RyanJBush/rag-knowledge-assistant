import type { DocumentItem } from "../../types/api";

interface DocumentLibraryProps {
  documents: DocumentItem[];
  loading: boolean;
  error: string | null;
}

function DocumentLibrary({ documents, loading, error }: DocumentLibraryProps) {
  return (
    <section className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-semibold">Document Library</h2>
        <span className="text-xs text-slate-500">{documents.length} documents</span>
      </div>

      {loading && <p className="mt-3 text-sm text-slate-600">Loading documents...</p>}
      {error && <p className="mt-3 text-sm text-rose-700">{error}</p>}

      {!loading && !error && documents.length === 0 && (
        <p className="mt-3 text-sm text-slate-600">No documents uploaded yet.</p>
      )}

      <ul className="mt-3 space-y-2">
        {documents.map((doc) => (
          <li key={doc.document_id} className="rounded-md border border-slate-200 p-3">
            <p className="text-sm font-medium text-slate-900">{doc.filename}</p>
            <p className="text-xs text-slate-500">
              {doc.content_type} • {doc.chunks_indexed} chunks
            </p>
          </li>
        ))}
      </ul>
    </section>
  );
}

export default DocumentLibrary;
