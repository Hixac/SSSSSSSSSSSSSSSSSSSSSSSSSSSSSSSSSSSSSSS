import type { ReactNode } from 'react';
import {
  Avatar,
  Card,
  CardContent,
  CardHeader,
  CardMedia,
  Chip,
  Stack,
  Typography,
} from '@mui/material';
import { FavoriteBorder, PushPin, Repeat, Visibility } from '@mui/icons-material';
import { useTranslation } from 'react-i18next';
import { formatDateTime } from '../../i18n/format';
import type { VKGroup, VKPost } from '../../types';

function Stat({ icon, value }: { icon: ReactNode; value: number }) {
  return (
    <Stack direction="row" spacing={0.5} alignItems="center">
      {icon}
      <Typography variant="body2" color="text.secondary">
        {value.toLocaleString()}
      </Typography>
    </Stack>
  );
}

export default function PostCard({
  post,
  group,
}: {
  post: VKPost;
  group: VKGroup | null;
}) {
  const { t, i18n } = useTranslation();
  const groupName = group?.name ?? t('post.fallback');
  const fallback = groupName.slice(0, 1).toUpperCase();

  return (
    <Card>
      <CardHeader
        avatar={
          <Avatar src={group?.photo_url ?? undefined} alt={groupName}>
            {fallback}
          </Avatar>
        }
        title={
          <Stack direction="row" spacing={1} alignItems="center">
            <Typography variant="subtitle1">{groupName}</Typography>
            {post.is_pinned && (
              <Chip
                icon={<PushPin />}
                label={t('post.pinned')}
                size="small"
                color="primary"
                variant="outlined"
              />
            )}
          </Stack>
        }
        subheader={formatDateTime(post.timestamp * 1000, i18n.language)}
      />
      {post.text && (
        <CardContent sx={{ pt: 0 }}>
          <Typography variant="body1" sx={{ whiteSpace: 'pre-wrap' }}>
            {post.text}
          </Typography>
        </CardContent>
      )}
      {post.photos_url && post.photos_url.length > 0 && (
        <CardMedia
          component="img"
          image={post.photos_url[0]}
          alt="post attachment"
          sx={{
            maxHeight: 480,
            objectFit: 'contain',
            bgcolor: '#eef0f4',
          }}
        />
      )}
      <CardContent>
        <Stack direction="row" spacing={3}>
          <Stat icon={<FavoriteBorder fontSize="small" />} value={post.likes} />
          <Stat icon={<Repeat fontSize="small" />} value={post.reposts} />
          <Stat icon={<Visibility fontSize="small" />} value={post.views} />
        </Stack>
      </CardContent>
    </Card>
  );
}
