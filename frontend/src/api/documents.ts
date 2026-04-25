import client from './client';

export interface UploadResponse {
  success: boolean;
  message: string;
  chunks_created: number;
  document_id: string;
}

export interface DocumentInfo {
  document_id: string;
  filename: string;
  chunk_count: number;
  file_size: number;
  uploaded_at: string;
}

export interface DocumentStatus {
  has_documents: boolean;
  documents: DocumentInfo[];
}

export const uploadDocument = (file: File) => {
  const formData = new FormData();
  formData.append('file', file);
  return client.post<UploadResponse>('/documents/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
};

export const getDocumentStatus = () =>
  client.get<DocumentStatus>('/documents/status');

export const deleteDocumentById = (documentId: string) =>
  client.delete(`/documents/${documentId}`);
