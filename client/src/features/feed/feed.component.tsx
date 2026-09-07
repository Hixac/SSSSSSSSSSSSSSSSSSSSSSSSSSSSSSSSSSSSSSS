import { useCallback, useEffect, useRef, useState } from 'react';
import {
  Alert,
  Box,
  Card,
  CardContent,
  CircularProgress,
  Skeleton,
  Stack,
  Typography,
} from '@mui/material';
import InboxIcon from '@mui/icons-material/Inbox';
import { useTranslation } from 'react-i18next';
import PostCard from './post.card';
import { getGroupInfo, getWallPosts } from '../../api/vk';
import { errorMessage } from '../../api/client';
import type { VKGroup, VKPost } from '../../types';

const PAGE_SIZE = 10;
const SCROLL_TRIGGER_PX = 600;

function FeedSkeleton() {
  return (
    <Card>
      <CardContent>
        <Skeleton variant="circular" width={40} height={40} />
        <Skeleton variant="text" width="30%" sx={{ mt: 1 }} />
        <Skeleton
          variant="rectangular"
          height={200}
          sx={{ my: 1, borderRadius: 2 }}
        />
        <Skeleton variant="text" width="50%" />
      </CardContent>
    </Card>
  );
}

export default function Feed({ domain }: { domain: string }) {
  const { t } = useTranslation();
  const [posts, setPosts] = useState<VKPost[]>([]);
  const [group, setGroup] = useState<VKGroup | null>(null);
  const [loading, setLoading] = useState(true);
  const [loadingMore, setLoadingMore] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [finished, setFinished] = useState(false);

  // Mutable pagination state — avoids re-render churn
  const pageRef = useRef({ offset: 0, finished: false, inFlight: false });

  // Initial load. BoardPage renders <Feed key={domain}> so a domain change
  // remounts this component with fresh state — no reset here, no stale appends.
  useEffect(() => {
    let cancelled = false;

    getGroupInfo(domain)
      .then((info) => {
        if (!cancelled) setGroup(info);
      })
      .catch(() => {
        if (!cancelled) setGroup(null);
      });

    getWallPosts(domain, PAGE_SIZE, 0)
      .then((data) => {
        if (cancelled) return;
        setPosts(data);
        pageRef.current.offset = data.length;
        pageRef.current.finished = data.length < PAGE_SIZE;
        setFinished(pageRef.current.finished);
      })
      .catch((err: unknown) => {
        if (!cancelled) setError(errorMessage(err));
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });

    return () => {
      cancelled = true;
    };
  }, [domain]);

  const loadMore = useCallback(() => {
    const page = pageRef.current;
    if (page.inFlight || page.finished) return;
    page.inFlight = true;
    setLoadingMore(true);

    getWallPosts(domain, PAGE_SIZE, page.offset)
      .then((data) => {
        setPosts((prev) => [...prev, ...data]);
        page.offset += data.length;
        page.finished = data.length < PAGE_SIZE;
        setFinished(page.finished);
      })
      .catch(() => {
        // Silent — next scroll retries
      })
      .finally(() => {
        page.inFlight = false;
        setLoadingMore(false);
      });
  }, [domain]);

  useEffect(() => {
    const handleScroll = () => {
      const nearBottom =
        window.innerHeight + window.scrollY >=
        document.documentElement.scrollHeight - SCROLL_TRIGGER_PX;
      if (nearBottom) {
        loadMore();
      }
    };
    window.addEventListener('scroll', handleScroll, { passive: true });
    window.addEventListener('resize', handleScroll);
    return () => {
      window.removeEventListener('scroll', handleScroll);
      window.removeEventListener('resize', handleScroll);
    };
  }, [loadMore]);

  if (loading) {
    return (
      <Stack spacing={2}>
        <FeedSkeleton />
        <FeedSkeleton />
      </Stack>
    );
  }

  if (error) {
    return (
      <Alert severity="error" sx={{ borderRadius: 2 }}>
        {error}
      </Alert>
    );
  }

  if (posts.length === 0) {
    return (
      <Box sx={{ textAlign: 'center', py: 6 }}>
        <InboxIcon sx={{ fontSize: 48, color: 'text.disabled' }} />
        <Typography color="text.secondary" sx={{ mt: 1 }}>
          {t('feed.noPosts')}
        </Typography>
      </Box>
    );
  }

  return (
    <Stack spacing={2}>
      {posts.map((post, index) => (
        <PostCard
          key={`${post.timestamp}-${index}`}
          post={post}
          group={group}
        />
      ))}
      <Box sx={{ display: 'flex', justifyContent: 'center', py: 2 }}>
        {loadingMore ? (
          <CircularProgress size={24} />
        ) : finished ? (
          <Typography variant="body2" color="text.disabled">
            {t('feed.all')}
          </Typography>
        ) : (
          <Typography variant="body2" color="text.secondary">
            {t('feed.scrollMore')}
          </Typography>
        )}
      </Box>
    </Stack>
  );
}
