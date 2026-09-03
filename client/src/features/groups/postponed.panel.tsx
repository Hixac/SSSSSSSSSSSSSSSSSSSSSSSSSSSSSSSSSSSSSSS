import { useEffect, useRef, useState, type DragEvent } from 'react';
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
import DeleteIcon from '@mui/icons-material/Delete';
import EditIcon from '@mui/icons-material/Edit';
import ScheduleIcon from '@mui/icons-material/Schedule';
import InboxIcon from '@mui/icons-material/Inbox';
import VideocamIcon from '@mui/icons-material/Videocam';
import { useTranslation } from 'react-i18next';
import {
  createPostponed,
  deletePostponed,
  listPostponed,
  updatePostponed,
} from '../../api/group';
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

function mediaName(item: PostponedItem): string {
  return item.media_path ? item.media_path.split('/').pop() ?? '' : '';
}

function VideoPreview({ src, crossOrigin }: { src: string; crossOrigin?: 'use-credentials' }) {
  const videoRef = useRef<HTMLVideoElement | null>(null);
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const [frame, setFrame] = useState<string | null>(null);

  useEffect(() => {
    const video = videoRef.current;
    const canvas = canvasRef.current;
    if (!video || !canvas) return;

    const drawFrame = () => {
      const ctx = canvas.getContext('2d');
      if (!ctx || video.videoWidth === 0) return;
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
      try {
        setFrame(canvas.toDataURL('image/jpeg', 0.7));
      } catch {
        setFrame(null);
      }
    };

    const seeked = () => drawFrame();
    video.addEventListener('loadeddata', seeked);
    video.addEventListener('seeked', seeked);
    video.currentTime = 0.1;

    return () => {
      video.removeEventListener('loadeddata', seeked);
      video.removeEventListener('seeked', seeked);
    };
  }, [src]);

  return (
    <>
      <video
        ref={videoRef}
        src={src}
        crossOrigin={crossOrigin}
        preload="metadata"
        muted
        playsInline
        style={{ display: 'none' }}
      />
      <canvas ref={canvasRef} style={{ display: 'none' }} />
      {frame ? (
        <img
          src={frame}
          alt="video preview"
          style={{ width: '100%', height: '100%', objectFit: 'cover' }}
        />
      ) : (
        <Box
          sx={{
            width: '100%',
            height: '100%',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
          }}
        >
          <VideocamIcon fontSize="small" color="disabled" />
        </Box>
      )}
    </>
  );
}

function MediaThumbnail({ item }: { item: PostponedItem }) {
  if (!item.media_path) {
    return null;
  }
  return (
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
        <VideoPreview key={item.media_path} src={mediaUrl(item)} crossOrigin="use-credentials" />
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
  );
}

export default function PostponedPanel({ domain, onNotify }: PostponedPanelProps) {
  const { t, i18n } = useTranslation();
  const [items, setItems] = useState<PostponedItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [text, setText] = useState('');
  const [file, setFile] = useState<File | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [editingId, setEditingId] = useState<string | null>(null);
  const [editText, setEditText] = useState('');
  const [editFile, setEditFile] = useState<File | null>(null);
  const [editPreviewUrl, setEditPreviewUrl] = useState<string | null>(null);
  const [editRemoveMedia, setEditRemoveMedia] = useState(false);
  const [saving, setSaving] = useState(false);

  const [createPreviewUrl, setCreatePreviewUrl] = useState<string | null>(null);
  const [createDragOver, setCreateDragOver] = useState(false);
  const [editDragOver, setEditDragOver] = useState(false);

  const editPreviewUrlRef = useRef<string | null>(null);
  const createPreviewUrlRef = useRef<string | null>(null);

  const setEditPreview = (url: string | null) => {
    if (editPreviewUrlRef.current) {
      URL.revokeObjectURL(editPreviewUrlRef.current);
    }
    editPreviewUrlRef.current = url;
    setEditPreviewUrl(url);
  };

  const setCreatePreview = (url: string | null) => {
    if (createPreviewUrlRef.current) {
      URL.revokeObjectURL(createPreviewUrlRef.current);
    }
    createPreviewUrlRef.current = url;
    setCreatePreviewUrl(url);
  };

  useEffect(() => () => {
    if (editPreviewUrlRef.current) {
      URL.revokeObjectURL(editPreviewUrlRef.current);
    }
    if (createPreviewUrlRef.current) {
      URL.revokeObjectURL(createPreviewUrlRef.current);
    }
  }, []);

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
      setCreatePreview(null);
      onNotify(t('postponed.created'));
      await load();
    } catch (err) {
      setError(errorMessage(err));
    } finally {
      setSubmitting(false);
    }
  };

  const chooseEditFile = (nextFile: File | null) => {
    setEditFile(nextFile);
    setEditRemoveMedia(false);
    setEditPreview(nextFile ? URL.createObjectURL(nextFile) : null);
  };

  const chooseCreateFile = (nextFile: File | null) => {
    setFile(nextFile);
    setCreatePreview(nextFile ? URL.createObjectURL(nextFile) : null);
  };

  const handleRemoveMedia = () => {
    if (editFile) {
      chooseEditFile(null);
      return;
    }
    setEditRemoveMedia(true);
  };

  const handleCreateDrop = (event: DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    setCreateDragOver(false);
    const dropped = event.dataTransfer.files?.[0] ?? null;
    if (dropped && (dropped.type.startsWith('image/') || dropped.type.startsWith('video/'))) {
      chooseCreateFile(dropped);
    }
  };

  const handleEditDrop = (event: DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    setEditDragOver(false);
    const dropped = event.dataTransfer.files?.[0] ?? null;
    if (dropped && (dropped.type.startsWith('image/') || dropped.type.startsWith('video/'))) {
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
      await updatePostponed(domain, item.id, editText, editFile, editRemoveMedia);
      cancelEditing();
      onNotify(t('postponed.updated'));
      await load();
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
      onNotify(t('postponed.deleted'));
      await load();
    } catch (err) {
      onNotify(errorMessage(err), 'error');
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
              p: 1,
              transition: 'border-color 0.2s',
            }}
          >
            <Stack direction="row" spacing={1} alignItems="center">
              {createPreviewUrl && file && (file.type.startsWith('image/') || file.type.startsWith('video/')) && (
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
                        style={{ width: '100%', height: '100%', objectFit: 'cover' }}
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
                  onChange={(event) => chooseCreateFile(event.target.files?.[0] ?? null)}
                />
              </Button>
            </Stack>
          </Box>
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
                        p: 1,
                        transition: 'border-color 0.2s',
                      }}
                    >
                      <Stack direction="row" spacing={1} alignItems="center">
                      {((editPreviewUrl && editFile && (editFile.type.startsWith('image/') || editFile.type.startsWith('video/'))) ||
                        (item.media_path && !editRemoveMedia)) && (
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
                            {editFile ? (
                              editFile.type.startsWith('video/') && editPreviewUrl ? (
                                <VideoPreview key={editPreviewUrl} src={editPreviewUrl} />
                              ) : (
                                <img
                                  src={editPreviewUrl ?? undefined}
                                  alt="new media"
                                  style={{ width: '100%', height: '100%', objectFit: 'cover' }}
                                />
                              )
                            ) : item.media_path && VIDEO_EXTENSIONS.test(item.media_path) ? (
                              <VideoPreview key={item.media_path} src={mediaUrl(item)} crossOrigin="use-credentials" />
                            ) : (
                              <img
                                src={mediaUrl(item)}
                                alt="attached media"
                                crossOrigin="use-credentials"
                                style={{ width: '100%', height: '100%', objectFit: 'cover' }}
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
                          onChange={(event) => chooseEditFile(event.target.files?.[0] ?? null)}
                        />
                      </Button>
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
                    </Box>
                  </Stack>
                ) : (
                  <>
                    <ListItemText
                      primary={item.text ?? t('postponed.mediaOnly')}
                      secondary={formatDateTime(item.created_at, i18n.language)}
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
        )}
      </CardContent>
    </Card>
  );
}
