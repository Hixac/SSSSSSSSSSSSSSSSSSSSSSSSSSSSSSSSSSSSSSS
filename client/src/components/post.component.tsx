import React from 'react';
import {
  Card,
  CardHeader,
  CardMedia,
  CardContent,
  Avatar,
  Typography,
  IconButton,
} from '@mui/material';
import {
  MoreVert,
} from '@mui/icons-material';

interface PostData {
  timestamp: number;
  content: string;
  image: string;
}

const Post: React.FC<PostData> = ({timestamp, content, image}) => {

  return (
    <Card sx={{ maxWidth: 600, mb: 2 }}>
      {/* Header with avatar, name, and menu */}
      <CardHeader
        avatar={
          <Avatar src="https://sun9-34.userapi.com/s/v1/ig2/nh287q44-sGhbuGg6QO5uivUiU7Gyw7jmEByy4LiAdEbaJN533sXYBACrg0nvQpfv5l3UwDF03uoVD4O5-O8XeOH.jpg?quality=95&as=32x32,48x48,72x72,108x108,160x160,240x240,360x360,480x480,540x540,640x640,720x720,1080x1080,1280x1280,1440x1440,2000x2000&from=bu&cs=1280x0" alt="123">
            "123"
          </Avatar>
        }
        action={
          <IconButton aria-label="settings">
            <MoreVert />
          </IconButton>
        }
        title="assless"
        subheader={timestamp}
        slotProps={{ variant: 'subtitle1', fontWeight: 'bold' }}
      />

      {/* content text */}
      <CardContent>
        <Typography variant="body1" color="text.primary">
          {content}
        </Typography>
      </CardContent>

      {/* Optional image */}
      {image && (
        <CardMedia
          component="img"
          height="300"
          image={image}
          alt="image"
          sx={{ 
            width: '100%',
            height: 'auto',
            objectFit: 'contain',
          }}
        />
      )}

    </Card>
  );
};

export default Post;
