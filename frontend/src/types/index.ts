export interface DocumentInfo {
  id: string
  filename: string
  original_filename: string
  file_type: string
  uploaded_at: string
  chunk_count: number
  status: string
}

export interface DocumentUploadResponse {
  document_id: string
  filename: string
  chunk_count: number
  status: string
}

export interface Citation {
  document_id: string
  source_filename: string
  chunk_index: number
  snippet: string
  score: number
}

export interface QueryResponse {
  answer: string
  citations: Citation[]
  query: string
}

export interface ChatMessage {
  id: string
  role: 'user' | 'assistant'
  content: string
  citations?: Citation[]
  timestamp: Date
}
