import { memo } from 'react';
import { Box } from '@mui/material';
import type { PostponedItem } from '../../types';
import { VIDEO_EXTENSIONS, mediaUrl } from './postponed.media';
import { VideoPreview } from './postponed.video-preview';

/**
 * 72x72 thumbnail for a postponed item's attached media. Memoized so a list
 * re-render only re-renders the row whose item actually changed.
 */
export const MediaThumbnail = memo(function MediaThumbnail({
  item,
}: {
  item: PostponedItem;
}) {
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
          loading="lazy"
          style={{ width: '100%', height: '100%', objectFit: 'cover' }}
        />
      )}
    </Box>
  );
});
