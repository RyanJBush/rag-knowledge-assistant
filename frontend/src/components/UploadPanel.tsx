import { useCallback, useRef, useState } from 'react'

interface Props {
  onUpload: (file: File) => Promise<unknown>
  loading: boolean
}

export default function UploadPanel({ onUpload, loading }: Props) {
  const [dragging, setDragging] = useState(false)
  const [uploadStatus, setUploadStatus] = useState<string | null>(null)
  const inputRef = useRef<HTMLInputElement>(null)

  const handleFile = useCallback(
    async (file: File) => {
      setUploadStatus(null)
      const result = await onUpload(file)
      if (result) {
        setUploadStatus(`✓ Uploaded "${file.name}" successfully`)
      }
    },
    [onUpload],
  )

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault()
      setDragging(false)
      const file = e.dataTransfer.files[0]
      if (file) void handleFile(file)
    },
    [handleFile],
  )

  return (
    <div className="bg-white rounded-xl border border-gray-200 p-6 shadow-sm">
      <h2 className="text-lg font-semibold text-gray-800 mb-4">Upload Document</h2>

      <div
        onDragOver={(e) => {
          e.preventDefault()
          setDragging(true)
        }}
        onDragLeave={() => setDragging(false)}
        onDrop={handleDrop}
        onClick={() => inputRef.current?.click()}
        className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors ${
          dragging
            ? 'border-blue-400 bg-blue-50'
            : 'border-gray-300 hover:border-blue-300 hover:bg-gray-50'
        }`}
      >
        <div className="text-4xl mb-2">📄</div>
        <p className="text-gray-600 text-sm">
          Drag &amp; drop a <strong>.pdf</strong> or <strong>.txt</strong> file here
        </p>
        <p className="text-gray-400 text-xs mt-1">or click to browse</p>
        <input
          ref={inputRef}
          type="file"
          accept=".pdf,.txt"
          className="hidden"
          onChange={(e) => {
            const file = e.target.files?.[0]
            if (file) void handleFile(file)
            e.target.value = ''
          }}
        />
      </div>

      {loading && (
        <div className="mt-3 flex items-center gap-2 text-blue-600 text-sm">
          <span className="animate-spin">⟳</span> Processing document…
        </div>
      )}

      {uploadStatus && !loading && (
        <div className="mt-3 text-green-600 text-sm">{uploadStatus}</div>
      )}
    </div>
  )
}
