import client from './client';

export interface Source {
  text: string;
  chunk_index: number;
}

export interface ChatResponse {
  answer: string;
  sources: Source[];
}

export const sendMessage = (question: string) =>
  client.post<ChatResponse>('/chat/', { question });
