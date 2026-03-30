import CitationList from "../citations/CitationList";

import type { QueryResponse } from "../../types/api";

interface AnswerCardProps {
  result: QueryResponse;
}

function AnswerCard({ result }: AnswerCardProps) {
  return (
    <article className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
      <h3 className="text-base font-semibold text-slate-900">Answer</h3>
      <p className="mt-2 whitespace-pre-wrap text-sm text-slate-700">{result.answer}</p>
      <p className="mt-2 text-xs text-slate-500">Retrieved chunks: {result.retrieved_chunks}</p>
      <CitationList citations={result.citations} />
    </article>
  );
}

export default AnswerCard;
