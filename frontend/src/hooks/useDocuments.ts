import { useCallback, useEffect, useState } from "react";

import { fetchDocuments } from "../lib/api";
import type { DocumentItem } from "../types/api";

export function useDocuments() {
  const [documents, setDocuments] = useState<DocumentItem[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  const loadDocuments = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await fetchDocuments();
      setDocuments(response.documents);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to fetch documents");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    void loadDocuments();
  }, [loadDocuments]);

  return {
    documents,
    loading,
    error,
    reload: loadDocuments,
  };
}
