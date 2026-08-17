import axios from 'axios';
import i18n from '../i18n';

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  timeout: 60_000,
  withCredentials: true,
});

export function errorMessage(error: unknown): string {
  if (axios.isAxiosError(error)) {
    const detail = error.response?.data?.detail;
    if (typeof detail === 'string') {
      return detail;
    }
    if (Array.isArray(detail) && detail.length > 0) {
      const first = detail[0];
      if (typeof first === 'object' && first !== null && 'msg' in first) {
        return String((first as { msg: unknown }).msg);
      }
    }
    return i18n.t('errors.requestFailed', {
      status: error.response?.status ?? 'network',
    });
  }
  return error instanceof Error ? error.message : i18n.t('errors.unexpected');
}
