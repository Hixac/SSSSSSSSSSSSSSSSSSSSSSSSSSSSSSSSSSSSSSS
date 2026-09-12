import { api } from './client';
import type { PostponedItem } from '../types';
import type { Dayjs } from 'dayjs';

export async function listPostponed(domain: string): Promise<PostponedItem[]> {
  const response = await api.get<PostponedItem[]>(
    `/group/${domain}/postponed/`
  );
  return response.data;
}

export async function createPostponed(
  domain: string,
  text: string,
  file: File | null,
  date: Dayjs | null
): Promise<void> {
  const form = new FormData();
  if (text.trim()) {
    form.append('text', text.trim());
  }
  if (file) {
    form.append('media', file);
  }
  if (date) {
    form.append('scheduled', date.toISOString());
  }
  await api.post(`/group/${domain}/postponed/`, form);
}

export async function updatePostponed(
  domain: string,
  id: string,
  text: string,
  file: File | null,
  deleteMedia = false,
  date: Dayjs | null
): Promise<void> {
  const form = new FormData();
  form.append('text', text.trim());
  if (file) {
    form.append('media', file);
  }
  if (deleteMedia) {
    form.append('delete_media', 'true');
  }
  if (date) {
    form.append('scheduled', date.toISOString());
  }
  await api.put(`/group/${domain}/postponed/${id}`, form);
}

export async function deletePostponed(
  domain: string,
  id: string
): Promise<void> {
  await api.delete(`/group/${domain}/postponed/${id}`);
}
