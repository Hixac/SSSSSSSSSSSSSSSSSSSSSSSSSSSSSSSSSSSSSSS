import { memo } from 'react';
import { DateTimePicker, LocalizationProvider } from '@mui/x-date-pickers';
import type { Dayjs } from 'dayjs';
import 'dayjs/locale/ru';
import 'dayjs/locale/en-gb';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs';
import { useTranslation } from 'react-i18next';

/**
 * The DateTimePicker is the single most expensive subtree (rebuilds the clock
 * view on every render). Memoized with a stable onChange, so typing elsewhere
 * in the form doesn't re-render the picker.
 */
export const SchedulePicker = memo(function SchedulePicker({
  value,
  onChange,
  label,
}: {
  value: Dayjs | null;
  onChange: (date: Dayjs | null) => void;
  label?: string;
}) {
  const { i18n } = useTranslation();
  return (
    <LocalizationProvider
      dateAdapter={AdapterDayjs}
      adapterLocale={i18n.language === 'ru' ? 'ru' : 'en-gb'}
    >
      <DateTimePicker
        value={value}
        onChange={onChange}
        label={label}
        sx={{ width: '100%' }}
      />
    </LocalizationProvider>
  );
});
