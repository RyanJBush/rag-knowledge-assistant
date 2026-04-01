import type { DocumentInfo, DocumentUploadResponse, QueryResponse } from '../types'

const BASE_URL = '/api/v1'

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, options)
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }))
    throw new Error(err.detail ?? `Request failed: ${res.status}`)
  }
  return res.json() as Promise<T>
}

export const api = {
  health: () => request<{ status: string; version: string }>('/health'),

  uploadDocument: (file: File): Promise<DocumentUploadResponse> => {
    const form = new FormData()
    form.append('file', file)
    return request<DocumentUploadResponse>('/documents/upload', {
      method: 'POST',
      body: form,
    })
  },

  listDocuments: () => request<DocumentInfo[]>('/documents'),

  query: (question: string, top_k = 5): Promise<QueryResponse> =>
    request<QueryResponse>('/query', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question, top_k }),
    }),
}
