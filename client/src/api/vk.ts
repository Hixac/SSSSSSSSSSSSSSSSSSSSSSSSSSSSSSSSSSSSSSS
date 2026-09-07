import { api } from './client';
import type { VKGroup, VKPost } from '../types';

export async function getGroupInfo(domain: string): Promise<VKGroup> {
  const response = await api.get<VKGroup>('/vk/group', {
    params: { domain },
  });
  return response.data;
}

export async function getWallPosts(
  domain: string,
  count: number = 20,
  offset: number = 0
): Promise<VKPost[]> {
  const response = await api.get<VKPost[]>('/vk/wall', {
    params: { domain, count, offset },
  });
  return response.data;
}
