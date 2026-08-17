import { useState, type FormEvent } from 'react';
import {
  Alert,
  Box,
  Button,
  Link,
  Paper,
  Stack,
  TextField,
  Typography,
} from '@mui/material';
import { Link as RouterLink, Navigate, useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { errorMessage } from '../api/client';
import { useAuth } from '../contexts/auth.context';
import LanguageSwitcher from '../components/language.switcher';

export default function LoginPage() {
  const { status, login } = useAuth();
  const { t } = useTranslation();
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  if (status === 'authenticated') {
    return <Navigate to="/board" replace />;
  }

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError(null);
    if (!email.trim() || !password) {
      setError(t('auth.fillAllFields'));
      return;
    }
    setSubmitting(true);
    try {
      await login(email.trim(), password);
      navigate('/board', { replace: true });
    } catch (err) {
      setError(errorMessage(err));
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <Box
      sx={{
        minHeight: '100vh',
        position: 'relative',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        bgcolor: 'background.default',
        p: 2,
      }}
    >
      <Box sx={{ position: 'absolute', top: 16, right: 16 }}>
        <LanguageSwitcher color="primary" />
      </Box>
      <Paper elevation={2} sx={{ p: 4, width: '100%', maxWidth: 400 }}>
        <Typography variant="h5" fontWeight={700} gutterBottom>
          {t('auth.signIn')}
        </Typography>
        <Typography variant="body2" color="text.secondary" sx={{ mb: 3 }}>
          {t('auth.signInSubtitle')}
        </Typography>
        <Box component="form" onSubmit={(event) => void handleSubmit(event)} noValidate>
          <Stack spacing={2}>
            <TextField
              label={t('auth.email')}
              type="email"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              fullWidth
              required
              autoComplete="email"
              autoFocus
            />
            <TextField
              label={t('auth.password')}
              type="password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              fullWidth
              required
              autoComplete="current-password"
            />
            {error && <Alert severity="error">{error}</Alert>}
            <Button type="submit" variant="contained" size="large" loading={submitting}>
              {t('auth.signIn')}
            </Button>
            <Typography variant="body2" align="center">
              {t('auth.noAccount')}{' '}
              <Link component={RouterLink} to="/signup">
                {t('auth.signUp')}
              </Link>
            </Typography>
          </Stack>
        </Box>
      </Paper>
    </Box>
  );
}
