import {
  memo,
  useCallback,
  useEffect,
  useRef,
  useState,
  type DragEvent,
} from 'react';
import {
  Box,
  Button,
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
import DeleteIcon from '@mui/icons-material/Delete';
import EditIcon from '@mui/icons-material/Edit';
import InboxIcon from '@mui/icons-material/Inbox';
import { useTranslation } from 'react-i18next';
import type { Dayjs } from 'dayjs';
import { deletePostponed, listPostponed, updatePostponed } from '../../api/group';
import { errorMessage } from '../../api/client';
import { formatDateTime } from '../../i18n/format';
import type { PostponedItem } from '../../types';
import type { NotifyFn } from './postponed.types';
import { VIDEO_EXTENSIONS, mediaName, mediaUrl } from './postponed.media';
import { MediaThumbnail } from './postponed.media-thumbnail';
import { VideoPreview } from './postponed.video-preview';

export interface PostponedListProps {
  domain: string;
  date: Dayjs | null;
  refreshToken: number;
  onNotify: NotifyFn;
}

function byScheduledAsc(a: PostponedItem, b: PostponedItem): number {
  return Date.parse(a.scheduled) - Date.parse(b.scheduled);
}

export const PostponedList = memo(function PostponedList({
  domain,
  date,
  refreshToken,
  onNotify,
}: PostponedListProps) {
  const { t, i18n } = useTranslation();
  const [items, setItems] = useState<PostponedItem[]>([]);
  const [loading, setLoading] = useState(true);

  const [editingId, setEditingId] = useState<string | null>(null);
  const [editText, setEditText] = useState('');
  const [editFile, setEditFile] = useState<File | null>(null);
  const [editPreviewUrl, setEditPreviewUrl] = useState<string | null>(null);
  const [editRemoveMedia, setEditRemoveMedia] = useState(false);
  const [saving, setSaving] = useState(false);
  const [editDragOver, setEditDragOver] = useState(false);

  const editPreviewUrlRef = useRef<string | null>(null);

  const setEditPreview = (url: string | null) => {
    if (editPreviewUrlRef.current) {
      URL.revokeObjectURL(editPreviewUrlRef.current);
    }
    editPreviewUrlRef.current = url;
    setEditPreviewUrl(url);
  };

  useEffect(
    () => () => {
      if (editPreviewUrlRef.current) {
        URL.revokeObjectURL(editPreviewUrlRef.current);
      }
    },
    []
  );

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const data = await listPostponed(domain);
      setItems([...data].sort(byScheduledAsc));
    } catch {
      setItems([]);
    } finally {
      setLoading(false);
    }
  }, [domain]);

  useEffect(() => {
    void load();
  }, [load, refreshToken]);

  const chooseEditFile = (nextFile: File | null) => {
    setEditFile(nextFile);
    setEditRemoveMedia(false);
    setEditPreview(nextFile ? URL.createObjectURL(nextFile) : null);
  };

  const handleRemoveMedia = () => {
    if (editFile) {
      chooseEditFile(null);
      return;
    }
    setEditRemoveMedia(true);
  };

  const handleEditDrop = (event: DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    setEditDragOver(false);
    const dropped = event.dataTransfer.files?.[0] ?? null;
    if (
      dropped &&
      (dropped.type.startsWith('image/') || dropped.type.startsWith('video/'))
    ) {
      chooseEditFile(dropped);
    }
  };

  const startEditing = (item: PostponedItem) => {
    setEditingId(item.id);
    setEditText(item.text ?? '');
    setEditFile(null);
    setEditPreview(null);
    setEditRemoveMedia(false);
  };

  const cancelEditing = () => {
    setEditingId(null);
    setEditText('');
    setEditFile(null);
    setEditPreview(null);
    setEditRemoveMedia(false);
  };

  const handleSave = async (item: PostponedItem) => {
    setSaving(true);
    try {
      await updatePostponed(
        domain,
        item.id,
        editText,
        editFile,
        editRemoveMedia,
        date
      );
      // Update locally instead of a full reload. The server echo for a media
      // change is unknown here, so reconcile silently in the background only
      // when media may have changed.
      setItems((prev) =>
        prev
          .map((p) =>
            p.id === item.id
              ? {
                  ...p,
                  text: editText.trim() || null,
                  scheduled: date ? date.toISOString() : p.scheduled,
                }
              : p
          )
          .sort(byScheduledAsc)
      );
      cancelEditing();
      onNotify(t('postponed.updated'));
      if (editFile || editRemoveMedia) {
        void listPostponed(domain)
          .then((data) => setItems([...data].sort(byScheduledAsc)))
          .catch(() => undefined);
      }
    } catch (err) {
      onNotify(errorMessage(err), 'error');
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async (item: PostponedItem) => {
    if (!window.confirm(t('postponed.deleteConfirm'))) {
      return;
    }
    try {
      await deletePostponed(domain, item.id);
      setItems((prev) => prev.filter((p) => p.id !== item.id));
      onNotify(t('postponed.deleted'));
    } catch (err) {
      onNotify(errorMessage(err), 'error');
    }
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', py: 3 }}>
        <CircularProgress size={28} />
      </Box>
    );
  }

  if (items.length === 0) {
    return (
      <Box sx={{ textAlign: 'center', py: 3 }}>
        <InboxIcon sx={{ fontSize: 40, color: 'text.disabled' }} />
        <Typography color="text.secondary" variant="body2" sx={{ mt: 1 }}>
          {t('postponed.nothingYet')}
        </Typography>
      </Box>
    );
  }

  return (
    <List>
      {items.map((item) => (
        <ListItem key={item.id} divider alignItems="flex-start">
          {editingId !== item.id && <MediaThumbnail item={item} />}
          {editingId === item.id ? (
            <Stack spacing={1} sx={{ flexGrow: 1 }}>
              <TextField
                size="small"
                fullWidth
                value={editText}
                onChange={(event) => setEditText(event.target.value)}
                multiline
                minRows={2}
                maxRows={6}
                autoFocus
              />
              {((editPreviewUrl &&
                editFile &&
                (editFile.type.startsWith('image/') ||
                  editFile.type.startsWith('video/'))) ||
                (item.media_path && !editRemoveMedia)) && (
                <Stack
                  spacing={0.5}
                  alignItems="center"
                  sx={{ alignSelf: 'flex-start' }}
                >
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
                    {editFile ? (
                      editFile.type.startsWith('video/') && editPreviewUrl ? (
                        <VideoPreview
                          key={editPreviewUrl}
                          src={editPreviewUrl}
                        />
                      ) : (
                        <img
                          src={editPreviewUrl ?? undefined}
                          alt="new media"
                          style={{
                            width: '100%',
                            height: '100%',
                            objectFit: 'cover',
                          }}
                        />
                      )
                    ) : item.media_path &&
                      VIDEO_EXTENSIONS.test(item.media_path) ? (
                      <VideoPreview
                        key={item.media_path}
                        src={mediaUrl(item)}
                        crossOrigin="use-credentials"
                      />
                    ) : (
                      <img
                        src={mediaUrl(item)}
                        alt="attached media"
                        crossOrigin="use-credentials"
                        style={{
                          width: '100%',
                          height: '100%',
                          objectFit: 'cover',
                        }}
                      />
                    )}
                    <IconButton
                      size="small"
                      onClick={handleRemoveMedia}
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
                    {editFile ? editFile.name : mediaName(item)}
                  </Typography>
                </Stack>
              )}
              <Box
                onDragOver={(event) => {
                  event.preventDefault();
                  setEditDragOver(true);
                }}
                onDragLeave={() => setEditDragOver(false)}
                onDrop={handleEditDrop}
                sx={{
                  border: '2px dashed',
                  borderColor: editDragOver ? 'primary.main' : 'divider',
                  borderRadius: 2,
                  p: 2,
                  display: 'flex',
                  flexDirection: 'column',
                  alignItems: 'center',
                  gap: 1,
                  transition: 'border-color 0.2s',
                  bgcolor: editDragOver ? 'action.hover' : 'transparent',
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
                    key={editFile ? editFile.name : 'empty'}
                    type="file"
                    hidden
                    accept="image/png,image/jpeg,video/mp4"
                    onChange={(event) =>
                      chooseEditFile(event.target.files?.[0] ?? null)
                    }
                  />
                </Button>
                <Typography variant="caption" color="text.secondary">
                  {t('postponed.dropHint')}
                </Typography>
              </Box>
              <Stack direction="row" spacing={1}>
                <Button
                  variant="contained"
                  size="small"
                  onClick={() => void handleSave(item)}
                  loading={saving}
                >
                  {t('postponed.save')}
                </Button>
                <Button size="small" onClick={cancelEditing}>
                  {t('postponed.cancel')}
                </Button>
              </Stack>
            </Stack>
          ) : (
            <>
              <ListItemText
                primary={item.text ?? t('postponed.mediaOnly')}
                secondary={"На " + formatDateTime(item.scheduled, i18n.language)}
              />
              <IconButton
                size="small"
                onClick={() => startEditing(item)}
                aria-label={t('postponed.edit')}
              >
                <EditIcon fontSize="small" />
              </IconButton>
              <IconButton
                size="small"
                onClick={() => void handleDelete(item)}
                aria-label={t('postponed.delete')}
              >
                <DeleteIcon fontSize="small" />
              </IconButton>
            </>
          )}
        </ListItem>
      ))}
    </List>
  );
});
