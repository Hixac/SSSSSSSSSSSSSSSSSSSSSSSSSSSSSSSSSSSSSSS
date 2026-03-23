import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  timeout: 1000 * 60,
  withCredentials: true,
  headers: { 'Content-Type': 'application/json' },
});

export default api;

export async function vkGetPosts(count: number = 1, offset: number = 0) {
  try {
    const response = await api.get("/vk/wall", {
      params: {
        count: count,
        offset: offset
      }
    });
    return response.data
  } catch (error) {
    if (axios.isAxiosError(error) && error.response) {
      throw new Error(error.response.data.detail || 'Failed to get posts from vk');
    }
    throw new Error('Network error');
  }
}

