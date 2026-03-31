import { useCallback, useState } from 'react'
import { api } from '../lib/api'
import type { DocumentInfo, DocumentUploadResponse } from '../types'

export function useDocuments() {
  const [documents, setDocuments] = useState<DocumentInfo[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const fetchDocuments = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const docs = await api.listDocuments()
      setDocuments(docs)
    } catch (e) {
      setError((e as Error).message)
    } finally {
      setLoading(false)
    }
  }, [])

  const uploadDocument = useCallback(
    async (file: File): Promise<DocumentUploadResponse | null> => {
      setLoading(true)
      setError(null)
      try {
        const result = await api.uploadDocument(file)
        await fetchDocuments()
        return result
      } catch (e) {
        setError((e as Error).message)
        return null
      } finally {
        setLoading(false)
      }
    },
    [fetchDocuments],
  )

  return { documents, loading, error, fetchDocuments, uploadDocument }
}
