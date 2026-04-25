import client from './client';

export interface Source {
  text: string;
  chunk_index: number;
  filename: string;
  page_number: number | null;
}

export interface ChatResponse {
  answer: string;
  sources: Source[];
}

export const sendMessage = (question: string) =>
  client.post<ChatResponse>('/chat/', { question });

export async function sendMessageStream(
  question: string,
  onToken: (token: string) => void,
  onDone: (sources: Source[]) => void,
  onError: (message: string) => void,
): Promise<void> {
  const token = localStorage.getItem('access_token');
  const baseUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';

  let response: Response;
  try {
    response = await fetch(`${baseUrl}/chat/stream`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ question }),
    });
  } catch {
    onError('Connection failed. Please try again.');
    return;
  }

  if (!response.ok) {
    onError('Failed to get a response. Please try again.');
    return;
  }

  const reader = response.body!.getReader();
  const decoder = new TextDecoder();
  let buffer = '';

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });
    const lines = buffer.split('\n');
    buffer = lines.pop() ?? '';

    for (const line of lines) {
      if (!line.startsWith('data: ')) continue;
      try {
        const data = JSON.parse(line.slice(6));
        if (data.done) {
          onDone(data.sources ?? []);
        } else if (data.token) {
          onToken(data.token as string);
        }
      } catch {
        // skip malformed SSE line
      }
    }
  }
}
