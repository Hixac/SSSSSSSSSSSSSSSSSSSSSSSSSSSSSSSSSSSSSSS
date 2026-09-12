import { memo, useEffect, useRef, useState } from 'react';
import { Box } from '@mui/material';
import VideocamIcon from '@mui/icons-material/Videocam';

/**
 * Extracts a single frame from a hidden <video> and paints it as a preview.
 * Memoized so parent re-renders don't re-run the frame-extraction effect.
 */
export const VideoPreview = memo(function VideoPreview({
  src,
  crossOrigin,
}: {
  src: string;
  crossOrigin?: 'use-credentials';
}) {
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
});
