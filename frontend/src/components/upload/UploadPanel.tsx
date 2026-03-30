import { useRef } from "react";

import { useUpload } from "../../hooks/useUpload";

interface UploadPanelProps {
  onUploaded: () => void;
}

function UploadPanel({ onUploaded }: UploadPanelProps) {
  const inputRef = useRef<HTMLInputElement | null>(null);
  const { upload, isUploading, uploadResult, error } = useUpload(onUploaded);

  const onSelectFile = async () => {
    const file = inputRef.current?.files?.[0];
    if (!file) {
      return;
    }
    await upload(file);
    if (inputRef.current) {
      inputRef.current.value = "";
    }
  };

  return (
    <section className="rounded-lg border border-slate-200 bg-white p-4 shadow-sm">
      <h2 className="text-lg font-semibold">Upload Documents</h2>
      <p className="mt-1 text-sm text-slate-600">Supported formats: PDF and TXT.</p>

      <input
        ref={inputRef}
        type="file"
        accept=".pdf,.txt"
        className="mt-4 block w-full text-sm file:mr-4 file:rounded-md file:border-0 file:bg-slate-900 file:px-4 file:py-2 file:text-white"
      />

      <button
        type="button"
        onClick={() => void onSelectFile()}
        disabled={isUploading}
        className="mt-4 rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white disabled:cursor-not-allowed disabled:bg-slate-400"
      >
        {isUploading ? "Uploading..." : "Upload & Index"}
      </button>

      {uploadResult && (
        <p className="mt-3 text-sm text-emerald-700">
          Uploaded <strong>{uploadResult.filename}</strong> ({uploadResult.chunks_indexed} chunks indexed)
        </p>
      )}
      {error && <p className="mt-3 text-sm text-rose-700">{error}</p>}
    </section>
  );
}

export default UploadPanel;
