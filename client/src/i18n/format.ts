/**
 * Locale-aware date formatting. Locale derived from active i18n language,
 * so switching language reformats every rendered date.
 */
export function formatDateTime(
  value: string | number | Date,
  language: string
): string {
  const locale = language === 'ru' ? 'ru-RU' : 'en-US';
  return new Intl.DateTimeFormat(locale, {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  }).format(new Date(value));
}
