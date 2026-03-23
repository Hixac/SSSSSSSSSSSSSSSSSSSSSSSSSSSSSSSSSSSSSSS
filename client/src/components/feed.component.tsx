import { Box, Container } from '@mui/material';
import Post from './post.component';
import { vkGetPosts } from '../api';
import { useEffect, useState } from 'react';

interface VKPost {
  likes: number;
  reposts: number;
  views: number;

  timestamp: number;
  is_pinned: boolean;
  text: string;

  photos_url: string[] | null;
}

const Feed: React.FC = () => {

  const [posts, setPosts] = useState<VKPost[]>([])

  useEffect(() => {
    vkGetPosts(100).then(setPosts).catch(console.error)
  }, [])

  return (
    <Box
      component="section"
      sx={{
        display: 'flex',
        flexDirection: "column",
        alignItems: 'center',
      }}
    >
      <Container maxWidth="md" sx={{ py: 2, bgcolor: "#FFFFFF" }}>
        {posts.map((post) => (
          <Post
            key={post.timestamp}  // Consider using a proper unique ID instead of timestamp
            timestamp={post.timestamp}
            content={post.text}
            image={post.photos_url?.[0]}
          />
        ))}
      </Container>
    </Box>
  );
};

export default Feed;
