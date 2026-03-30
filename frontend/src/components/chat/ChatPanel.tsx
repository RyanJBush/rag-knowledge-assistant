import { useState } from "react";

import { useQuery } from "../../hooks/useQuery";
import AnswerCard from "./AnswerCard";

function ChatPanel() {
  const [question, setQuestion] = useState<string>("");
  const { askQuestion, result, loading, error } = useQuery();

  const onSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!question.trim()) {
      return;
    }
    await askQuestion(question.trim());
  };

  return (
    <section className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
      <h2 className="text-lg font-semibold">Ask Your Knowledge Base</h2>
      <form onSubmit={(event) => void onSubmit(event)} className="mt-3 flex gap-2">
        <input
          value={question}
          onChange={(event) => setQuestion(event.target.value)}
          placeholder="Ask a question about uploaded documents..."
          className="flex-1 rounded-md border border-slate-300 px-3 py-2 text-sm outline-none focus:border-blue-500"
        />
        <button
          type="submit"
          disabled={loading}
          className="rounded-md bg-slate-900 px-4 py-2 text-sm font-medium text-white disabled:cursor-not-allowed disabled:bg-slate-400"
        >
          {loading ? "Asking..." : "Ask"}
        </button>
      </form>

      {error && <p className="mt-3 text-sm text-rose-700">{error}</p>}

      {!loading && !error && !result && (
        <p className="mt-3 text-sm text-slate-600">Upload documents and ask your first question.</p>
      )}

      {result && <div className="mt-4"><AnswerCard result={result} /></div>}
    </section>
  );
}

export default ChatPanel;
