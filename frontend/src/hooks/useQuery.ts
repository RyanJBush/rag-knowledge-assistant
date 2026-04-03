import { useState } from "react";

import { queryDocuments } from "../lib/api";
import type { QueryResponse } from "../types/api";

export function useQuery() {
  const [result, setResult] = useState<QueryResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const askQuestion = async (question: string, topK = 4) => {
    try {
      setLoading(true);
      setError(null);
      const response = await queryDocuments({ question, top_k: topK });
      setResult(response);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Query failed");
      setResult(null);
    } finally {
      setLoading(false);
    }
  };

  return {
    askQuestion,
    result,
    loading,
    error,
  };
}
