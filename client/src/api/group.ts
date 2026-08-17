import { api } from './client';
import type { PostponedItem } from '../types';

export async function listPostponed(domain: string): Promise<PostponedItem[]> {
  const response = await api.get<PostponedItem[]>(`/group/${domain}/postponed/`);
  return response.data;
}

export async function createPostponed(
  domain: string,
  text: string,
  file: File | null,
): Promise<void> {
  const form = new FormData();
  if (text.trim()) {
    form.append('text', text.trim());
  }
  if (file) {
    form.append('media', file);
  }
  await api.post(`/group/${domain}/postponed/`, form);
}
