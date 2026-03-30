import type {
  DocumentIngestResponse,
  DocumentListResponse,
  QueryRequest,
  QueryResponse,
} from "../types/api";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000/api";

async function parseResponse<T>(response: Response): Promise<T> {
  const payload = await response.json();
  if (!response.ok) {
    throw new Error(payload?.message ?? "Request failed");
  }
  return payload as T;
}

export async function uploadDocument(file: File): Promise<DocumentIngestResponse> {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${API_BASE_URL}/documents/upload`, {
    method: "POST",
    body: formData,
  });

  return parseResponse<DocumentIngestResponse>(response);
}

export async function fetchDocuments(): Promise<DocumentListResponse> {
  const response = await fetch(`${API_BASE_URL}/documents`);
  return parseResponse<DocumentListResponse>(response);
}

export async function queryDocuments(payload: QueryRequest): Promise<QueryResponse> {
  const response = await fetch(`${API_BASE_URL}/query`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  return parseResponse<QueryResponse>(response);
}
