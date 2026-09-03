import { useState } from 'react';
import { Alert, Snackbar, Stack, Tab, Tabs } from '@mui/material';
import { useTranslation } from 'react-i18next';
import GroupPanel from '../features/groups/group.panel';
import Feed from '../features/feed/feed.component';
import PostponedPanel from '../features/groups/postponed.panel';

const DOMAIN_STORAGE_KEY = 'manyS.groupDomain';
const TAB_STORAGE_KEY = 'manyS.boardTab';

interface SnackbarState {
  message: string;
  severity: 'success' | 'error';
}

export default function BoardPage() {
  const { t } = useTranslation();
  const [domain, setDomain] = useState<string>(() => {
    return localStorage.getItem(DOMAIN_STORAGE_KEY) ?? '';
  });
  const [tab, setTab] = useState<number>(() => {
    const saved = Number(localStorage.getItem(TAB_STORAGE_KEY));
    return saved === 1 ? 1 : 0;
  });
  const [snackbar, setSnackbar] = useState<SnackbarState | null>(null);

  const notify = (message: string, severity: 'success' | 'error' = 'success') => {
    setSnackbar({ message, severity });
  };

  const handleDomainChange = (nextDomain: string) => {
    setDomain(nextDomain);
    localStorage.setItem(DOMAIN_STORAGE_KEY, nextDomain);
  };

  const handleTabChange = (_event: unknown, value: number) => {
    setTab(value);
    localStorage.setItem(TAB_STORAGE_KEY, String(value));
  };

  return (
    <Stack spacing={3}>
      <GroupPanel currentDomain={domain} onDomainChange={handleDomainChange} />
      {!domain ? (
        <Alert severity="info" sx={{ borderRadius: 2 }}>
          {t('group.enterDomainHint')}
        </Alert>
      ) : (
        <>
          <Tabs
            value={tab}
            onChange={handleTabChange}
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
