export type NotifyFn = (
  message: string,
  severity?: 'success' | 'error'
) => void;
