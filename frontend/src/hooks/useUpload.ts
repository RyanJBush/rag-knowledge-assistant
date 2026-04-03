import { useState } from "react";

import { uploadDocument } from "../lib/api";
import type { DocumentIngestResponse } from "../types/api";

export function useUpload(onUploadSuccess: () => void) {
  const [isUploading, setIsUploading] = useState<boolean>(false);
  const [uploadResult, setUploadResult] = useState<DocumentIngestResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const upload = async (file: File) => {
    try {
      setIsUploading(true);
      setError(null);
      const result = await uploadDocument(file);
      setUploadResult(result);
      onUploadSuccess();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Upload failed");
      setUploadResult(null);
    } finally {
      setIsUploading(false);
    }
  };

  return {
    upload,
    isUploading,
    uploadResult,
    error,
  };
}
