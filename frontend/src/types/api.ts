export interface HealthResponse {
  status: string;
  service: string;
  environment: string;
}

export interface DocumentIngestResponse {
  document_id: string;
  filename: string;
  chunks_indexed: number;
  status: string;
}

export interface DocumentItem {
  document_id: string;
  filename: string;
  content_type: string;
  created_at: string;
  chunks_indexed: number;
}

export interface DocumentListResponse {
  documents: DocumentItem[];
}

export interface QueryRequest {
  question: string;
  top_k: number;
}

export interface Citation {
  document_id: string;
  source: string;
  chunk_id: string;
  snippet: string;
  score: number;
  page: number | null;
}

export interface QueryResponse {
  answer: string;
  citations: Citation[];
  retrieved_chunks: number;
}

export interface ApiError {
  code: string;
  message: string;
  details?: Record<string, unknown>;
}
