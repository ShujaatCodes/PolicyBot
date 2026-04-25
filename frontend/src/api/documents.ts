import client from './client';

export interface UploadResponse {
  success: boolean;
  message: string;
  chunks_created: number;
}

export interface DocumentStatus {
  has_document: boolean;
  filename?: string;
  chunk_count?: number;
  uploaded_at?: string;
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

export const deleteDocument = () =>
  client.delete('/documents/');
