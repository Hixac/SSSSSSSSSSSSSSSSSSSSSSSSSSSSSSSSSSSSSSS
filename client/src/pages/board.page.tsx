import { useState } from 'react';
import { Alert, Snackbar, Stack, Tab, Tabs } from '@mui/material';
import { useTranslation } from 'react-i18next';
import GroupPanel from '../features/groups/group.panel';
import Feed from '../features/feed/feed.component';
import PostponedPanel from '../features/groups/postponed.panel';

interface SnackbarState {
  message: string;
  severity: 'success' | 'error';
}

export default function BoardPage() {
  const { t } = useTranslation();
  const [domain, setDomain] = useState('');
  const [tab, setTab] = useState(0);
  const [snackbar, setSnackbar] = useState<SnackbarState | null>(null);

  const notify = (message: string, severity: 'success' | 'error' = 'success') => {
    setSnackbar({ message, severity });
  };

  return (
    <Stack spacing={3}>
      <GroupPanel currentDomain={domain} onDomainChange={setDomain} />
      {!domain ? (
        <Alert severity="info" sx={{ borderRadius: 2 }}>
          {t('group.enterDomainHint')}
        </Alert>
      ) : (
        <>
          <Tabs
            value={tab}
            onChange={(_event, value: number) => setTab(value)}
            variant="fullWidth"
            sx={{ bgcolor: 'background.paper', borderRadius: 2 }}
          >
            <Tab label={t('board.wallPosts')} />
            <Tab label={t('board.postponed')} />
          </Tabs>
          {tab === 0 ? (
            <Feed key={domain} domain={domain} />
          ) : (
            <PostponedPanel domain={domain} onNotify={notify} />
          )}
        </>
      )}
      <Snackbar
        open={snackbar !== null}
        autoHideDuration={4000}
        onClose={() => setSnackbar(null)}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
      >
        {snackbar ? (
          <Alert severity={snackbar.severity} onClose={() => setSnackbar(null)}>
            {snackbar.message}
          </Alert>
        ) : undefined}
      </Snackbar>
    </Stack>
  );
}
