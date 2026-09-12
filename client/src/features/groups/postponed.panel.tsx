import { useCallback, useState } from 'react';
import { Card, CardContent, Typography } from '@mui/material';
import dayjs from 'dayjs';
import type { Dayjs } from 'dayjs';
import { useTranslation } from 'react-i18next';
import type { NotifyFn } from './postponed.types';
import { PostponedForm } from './postponed.form';
import { PostponedList } from './postponed.list';

interface PostponedPanelProps {
  domain: string;
  onNotify: NotifyFn;
}

export default function PostponedPanel({
  domain,
  onNotify,
}: PostponedPanelProps) {
  const { t } = useTranslation();
  // `date` is shared between the create form and the edit flow (handleSave
  // reuses it), so it lives here in the thin shell.
  const [date, setDate] = useState<Dayjs | null>(dayjs());
  const [refreshToken, setRefreshToken] = useState(0);

  const handleCreated = useCallback(() => {
    setRefreshToken((n) => n + 1);
  }, []);

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          {t('postponed.title')}
        </Typography>
        <PostponedForm
          domain={domain}
          date={date}
          onDateChange={setDate}
          onCreated={handleCreated}
          onNotify={onNotify}
        />
        <PostponedList
          domain={domain}
          date={date}
          refreshToken={refreshToken}
          onNotify={onNotify}
        />
      </CardContent>
    </Card>
  );
}
