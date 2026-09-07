import { useEffect, useState } from 'react';
import {
  Button,
  Card,
  CardContent,
  Stack,
  TextField,
  Typography,
} from '@mui/material';
import { useTranslation } from 'react-i18next';

interface GroupPanelProps {
  currentDomain: string;
  onDomainChange: (domain: string) => void;
}

export default function GroupPanel({
  currentDomain,
  onDomainChange,
}: GroupPanelProps) {
  const { t } = useTranslation();
  const [input, setInput] = useState(currentDomain);

  useEffect(() => {
    setInput(currentDomain);
  }, [currentDomain]);

  const handleLoad = () => {
    const value = input.trim();
    if (!value) {
      return;
    }
    onDomainChange(value);
  };

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          {t('group.group')}
        </Typography>
        <Stack direction={{ xs: 'column', sm: 'row' }} spacing={2}>
          <TextField
            label={t('group.domain')}
            size="small"
            value={input}
            onChange={(event) => setInput(event.target.value)}
            onKeyDown={(event) => {
              if (event.key === 'Enter') {
                handleLoad();
              }
            }}
            fullWidth
          />
          <Button variant="outlined" onClick={handleLoad}>
            {t('group.load')}
          </Button>
        </Stack>
      </CardContent>
    </Card>
  );
}
