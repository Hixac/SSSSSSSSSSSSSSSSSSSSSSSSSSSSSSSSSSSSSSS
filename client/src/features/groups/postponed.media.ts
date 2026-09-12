import type { PostponedItem } from '../../types';

export const VIDEO_EXTENSIONS = /\.(mp4|webm|mov|m4v|avi)$/i;

export function mediaUrl(item: PostponedItem): string {
  return `${import.meta.env.VITE_API_BASE_URL}/group/${item.group_domain}/postponed/${item.id}/media`;
}

export function mediaName(item: PostponedItem): string {
  return item.media_path ? (item.media_path.split('/').pop() ?? '') : '';
}
