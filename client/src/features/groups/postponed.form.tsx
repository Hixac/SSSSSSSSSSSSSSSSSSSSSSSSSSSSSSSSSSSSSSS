import { memo, useEffect, useRef, useState, type DragEvent } from 'react';
import {
  Box,
  Button,
  IconButton,
  Stack,
  TextField,
  Typography,
} from '@mui/material';
import AttachFileIcon from '@mui/icons-material/AttachFile';
import CloseIcon from '@mui/icons-material/Close';
import ScheduleIcon from '@mui/icons-material/Schedule';
import { useTranslation } from 'react-i18next';
import type { Dayjs } from 'dayjs';
import { createPostponed } from '../../api/group';
import { errorMessage } from '../../api/client';
import type { NotifyFn } from './postponed.types';
import { SchedulePicker } from './postponed.schedule-picker';
import { VideoPreview } from './postponed.video-preview';

export interface PostponedFormProps {
  domain: string;
  date: Dayjs | null;
  onDateChange: (date: Dayjs | null) => void;
  onCreated: () => void;
  onNotify: NotifyFn;
}

export const PostponedForm = memo(function PostponedForm({
  domain,
  date,
  onDateChange,
  onCreated,
  onNotify,
}: PostponedFormProps) {
  const { t } = useTranslation();
  const [text, setText] = useState('');
  const [file, setFile] = useState<File | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [createPreviewUrl, setCreatePreviewUrl] = useState<string | null>(null);
  const [createDragOver, setCreateDragOver] = useState(false);

  const createPreviewUrlRef = useRef<string | null>(null);

  const setCreatePreview = (url: string | null) => {
    if (createPreviewUrlRef.current) {
      URL.revokeObjectURL(createPreviewUrlRef.current);
    }
    createPreviewUrlRef.current = url;
    setCreatePreviewUrl(url);
  };

  useEffect(
    () => () => {
      if (createPreviewUrlRef.current) {
        URL.revokeObjectURL(createPreviewUrlRef.current);
      }
    },
    []
  );

  const chooseCreateFile = (nextFile: File | null) => {
    setFile(nextFile);
    setCreatePreview(nextFile ? URL.createObjectURL(nextFile) : null);
  };

  const handleCreateDrop = (event: DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    setCreateDragOver(false);
    const dropped = event.dataTransfer.files?.[0] ?? null;
    if (
      dropped &&
      (dropped.type.startsWith('image/') || dropped.type.startsWith('video/'))
    ) {
      chooseCreateFile(dropped);
    }
  };

  const handleSubmit = async () => {
    setError(null);
    if (!text.trim() && !file) {
      setError(t('postponed.enterTextOrFile'));
      return;
    }
    setSubmitting(true);
    try {
      await createPostponed(domain, text, file, date);
      setText('');
      setFile(null);
      setCreatePreview(null);
      onDateChange(null);
      onNotify(t('postponed.created'));
      onCreated();
    } catch (err) {
      setError(errorMessage(err));
    } finally {
      setSubmitting(false);
    }
  };

  return (
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
      <SchedulePicker
        value={date}
        onChange={onDateChange}
        label={t('postponed.scheduleFor')}
      />
      <Box
        onDragOver={(event) => {
          event.preventDefault();
          setCreateDragOver(true);
        }}
        onDragLeave={() => setCreateDragOver(false)}
        onDrop={handleCreateDrop}
        sx={{
          border: '2px dashed',
          borderColor: createDragOver ? 'primary.main' : 'divider',
          borderRadius: 2,
          p: 2,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          gap: 1,
          transition: 'border-color 0.2s',
          bgcolor: createDragOver ? 'action.hover' : 'transparent',
        }}
      >
        <Button
          component="label"
          variant="outlined"
          size="small"
          startIcon={<AttachFileIcon />}
        >
          {t('postponed.attachMedia')}
          <input
            key={file ? file.name : 'empty'}
            type="file"
            hidden
            accept="image/png,image/jpeg,video/mp4"
            onChange={(event) =>
              chooseCreateFile(event.target.files?.[0] ?? null)
            }
          />
        </Button>
        <Typography variant="caption" color="text.secondary">
          {t('postponed.dropHint')}
        </Typography>
      </Box>
      <Stack direction="row" spacing={1} alignItems="center">
        {createPreviewUrl &&
          file &&
          (file.type.startsWith('image/') ||
            file.type.startsWith('video/')) && (
            <Stack spacing={0.5} alignItems="center" sx={{ flexShrink: 0 }}>
              <Box
                sx={{
                  position: 'relative',
                  width: 72,
                  height: 72,
                  borderRadius: 2,
                  overflow: 'hidden',
                  bgcolor: '#eef0f4',
                }}
              >
                {file.type.startsWith('video/') ? (
                  <VideoPreview key={createPreviewUrl} src={createPreviewUrl} />
                ) : (
                  <img
                    src={createPreviewUrl}
                    alt="new media"
                    style={{
                      width: '100%',
                      height: '100%',
                      objectFit: 'cover',
                    }}
                  />
                )}
                <IconButton
                  size="small"
                  onClick={() => chooseCreateFile(null)}
                  aria-label={t('postponed.removeMedia')}
                  sx={{
                    position: 'absolute',
                    top: 2,
                    right: 2,
                    bgcolor: 'rgba(0,0,0,0.55)',
                    color: '#fff',
                    '&:hover': { bgcolor: 'rgba(0,0,0,0.75)' },
                  }}
                >
                  <CloseIcon sx={{ fontSize: 16 }} />
                </IconButton>
              </Box>
              <Typography variant="caption" noWrap sx={{ maxWidth: 72 }}>
                {file.name}
              </Typography>
            </Stack>
          )}
      </Stack>
      {error && (
        <Typography color="error" variant="body2">
          {error}
        </Typography>
      )}
      <Button
        variant="contained"
        startIcon={<ScheduleIcon />}
        onClick={() => void handleSubmit()}
        loading={submitting}
      >
        {t('postponed.schedule')}
      </Button>
    </Stack>
  );
});
