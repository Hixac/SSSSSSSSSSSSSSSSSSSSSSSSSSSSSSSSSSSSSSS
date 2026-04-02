import React, { useState } from 'react';
import { Box, Typography, Collapse } from '@mui/material';

interface ExpandableTextProps {
  text: string;
  maxLength?: number; // максимальная длина до усечения (по умолчанию 100)
}

const ExpandableText: React.FC<ExpandableTextProps> = ({ text, maxLength = 100 }) => {
  const [expanded, setExpanded] = useState(false);
  const needTruncate = text.length > maxLength;

  const truncatedText = `${text.slice(0, maxLength)}...`;

  const handleTextClick = () => {
    setExpanded(!expanded);
  };

  return (
    <Box sx={{ display: 'flex', alignItems: 'flex-start', gap: 1 }}>
      <Box sx={{ flex: 1 }}>
        {/* Кликабельный текст */}
        <Typography
          variant="body1"
          sx={{
            wordBreak: 'break-word',
            cursor: needTruncate ? 'pointer' : 'default',
          }}
          onClick={handleTextClick}
        >
          {needTruncate && !expanded ? truncatedText : text}
        </Typography>
        {/* Полный текст с анимацией */}
        {needTruncate && (
          <Collapse in={expanded} timeout="auto" unmountOnExit>
            <Typography 
              variant="body1"
              sx={{
                wordBreak: 'break-word',
                cursor: needTruncate ? 'pointer' : 'default'
              }}
              onClick={handleTextClick}
              >
              {text}
            </Typography>
          </Collapse>
        )}
      </Box>
    </Box>
  );
};

export default ExpandableText;
