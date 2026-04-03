import ChatPanel from "../components/chat/ChatPanel";
import DocumentLibrary from "../components/documents/DocumentLibrary";
import UploadPanel from "../components/upload/UploadPanel";
import { useDocuments } from "../hooks/useDocuments";

function DashboardPage() {
  const { documents, loading, error, reload } = useDocuments();

  return (
    <main className="min-h-screen bg-slate-100 p-6 text-slate-900">
      <div className="mx-auto grid max-w-7xl gap-6 lg:grid-cols-[360px,1fr]">
        <aside className="space-y-6">
          <UploadPanel onUploaded={reload} />
          <DocumentLibrary documents={documents} loading={loading} error={error} />
        </aside>
        <section>
          <ChatPanel />
        </section>
      </div>
    </main>
  );
}

export default DashboardPage;
