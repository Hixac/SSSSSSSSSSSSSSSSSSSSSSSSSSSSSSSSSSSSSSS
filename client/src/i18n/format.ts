/**
 * Locale-aware date formatting. Locale derived from active i18n language,
 * so switching language reformats every rendered date.
 */
const formatters = new Map<string, Intl.DateTimeFormat>();

export function formatDateTime(
  value: string | number | Date,
  language: string
): string {
  const locale = language === 'ru' ? 'ru-RU' : 'en-US';
  let formatter = formatters.get(locale);
  if (!formatter) {
    formatter = new Intl.DateTimeFormat(locale, {
      day: 'numeric',
      month: 'long',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
    formatters.set(locale, formatter);
  }
  return formatter.format(new Date(value));
}
