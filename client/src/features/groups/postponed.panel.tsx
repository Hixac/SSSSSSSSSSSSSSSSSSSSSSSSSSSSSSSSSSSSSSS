import { useEffect, useState } from 'react';
import {
  Box,
  Button,
  Card,
  CardContent,
  CircularProgress,
  IconButton,
  List,
  ListItem,
  ListItemText,
  Stack,
  TextField,
  Typography,
} from '@mui/material';
import AttachFileIcon from '@mui/icons-material/AttachFile';
import CloseIcon from '@mui/icons-material/Close';
import ScheduleIcon from '@mui/icons-material/Schedule';
import InboxIcon from '@mui/icons-material/Inbox';
import { useTranslation } from 'react-i18next';
import { createPostponed, listPostponed } from '../../api/group';
import { errorMessage } from '../../api/client';
import { formatDateTime } from '../../i18n/format';
import type { PostponedItem } from '../../types';

interface PostponedPanelProps {
  domain: string;
  onNotify: (message: string, severity?: 'success' | 'error') => void;
}

const VIDEO_EXTENSIONS = /\.(mp4|webm|mov|m4v|avi)$/i;

function mediaUrl(item: PostponedItem): string {
  return `${import.meta.env.VITE_API_BASE_URL}/group/${item.group_domain}/postponed/${item.id}/media`;
}

export default function PostponedPanel({ domain, onNotify }: PostponedPanelProps) {
  const { t, i18n } = useTranslation();
  const [items, setItems] = useState<PostponedItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [text, setText] = useState('');
  const [file, setFile] = useState<File | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const load = async () => {
    setLoading(true);
    try {
      setItems(await listPostponed(domain));
    } catch {
      setItems([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    void load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [domain]);

  const handleSubmit = async () => {
    setError(null);
    if (!text.trim() && !file) {
      setError(t('postponed.enterTextOrFile'));
      return;
    }
    setSubmitting(true);
    try {
      await createPostponed(domain, text, file);
      setText('');
      setFile(null);
      onNotify(t('postponed.created'));
      await load();
    } catch (err) {
      setError(errorMessage(err));
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          {t('postponed.title')}
        </Typography>
        <Stack spacing={2}>
          <TextField
            label={t('postponed.text')}
            size="small"
            value={text}
            onChange={(event) => setText(event.target.value)}
            fullWidth
            multiline
            minRows={2}
            maxRows={6}
          />
          <Stack direction="row" spacing={1} alignItems="center">
            <Button
              component="label"
              variant="outlined"
              size="small"
              startIcon={<AttachFileIcon />}
            >
              {file ? file.name : t('postponed.attachMedia')}
              <input
                type="file"
                hidden
                onChange={(event) => setFile(event.target.files?.[0] ?? null)}
              />
            </Button>
            {file && (
              <IconButton size="small" onClick={() => setFile(null)} aria-label={t('postponed.removeFile')}>
                <CloseIcon />
              </IconButton>
            )}
          </Stack>
          {error && <Typography color="error" variant="body2">{error}</Typography>}
          <Button
            variant="contained"
            startIcon={<ScheduleIcon />}
            onClick={() => void handleSubmit()}
            loading={submitting}
          >
            {t('postponed.schedule')}
          </Button>
        </Stack>

        {loading ? (
          <Box sx={{ display: 'flex', justifyContent: 'center', py: 3 }}>
            <CircularProgress size={28} />
          </Box>
        ) : items.length === 0 ? (
          <Box sx={{ textAlign: 'center', py: 3 }}>
            <InboxIcon sx={{ fontSize: 40, color: 'text.disabled' }} />
            <Typography color="text.secondary" variant="body2" sx={{ mt: 1 }}>
              {t('postponed.nothingYet')}
            </Typography>
          </Box>
        ) : (
          <List>
            {items.map((item) => (
              <ListItem key={item.id} divider alignItems="flex-start">
                {item.media_path && (
                  <Box
                    sx={{
                      width: 72,
                      height: 72,
                      mr: 2,
                      borderRadius: 2,
                      overflow: 'hidden',
                      bgcolor: '#eef0f4',
                      flexShrink: 0,
                    }}
                  >
                    {VIDEO_EXTENSIONS.test(item.media_path) ? (
                      <video
                        src={mediaUrl(item)}
                        crossOrigin="use-credentials"
                        style={{ width: '100%', height: '100%', objectFit: 'cover' }}
                      />
                    ) : (
                      <img
                        src={mediaUrl(item)}
                        alt="attached media"
                        crossOrigin="use-credentials"
                        loading="lazy"
                        style={{ width: '100%', height: '100%', objectFit: 'cover' }}
                      />
                    )}
                  </Box>
                )}
                <ListItemText
                  primary={item.text ?? t('postponed.mediaOnly')}
                  secondary={formatDateTime(item.created_at, i18n.language)}
                />
              </ListItem>
            ))}
          </List>
        )}
      </CardContent>
    </Card>
  );
}
