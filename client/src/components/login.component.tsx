import Button from '@mui/material/Button';
import Dialog from '@mui/material/Dialog';
import { type DialogProps } from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogTitle from '@mui/material/DialogTitle';
import TextField from '@mui/material/TextField';
import Stack from '@mui/material/Stack';

import { useAuth } from '../contexts/auth.context';
import { useState } from 'react';

interface LoginProps {
  open: boolean;
  onClose: (event: {}, reason: 'backdropClick' | 'escapeKeyDown' | 'signUp') => void;
}

export default function Login({ open, onClose }: LoginProps) {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const { login } = useAuth();

  const handleSubmit = async () => {
    setError('')
    try {
      await login(email, password)
    } catch (error) {
      console.error(error)
      setError('Invalid email or password')
    }
  }

  const handleDialogClose: DialogProps['onClose'] = (_, reason) => {
    if (reason === 'backdropClick') return; // Prevent closing on backdrop click
    onClose(_, reason);
  };

  const handleSignUp = () => {
    onClose({}, 'signUp'); // custom reason to indicate sign-up action
  };

  return (
    <Dialog open={open} onClose={handleDialogClose} maxWidth="xs" fullWidth>
      <DialogTitle>Welcome Back</DialogTitle>
      <DialogContent>
        <Stack spacing={2} sx={{ mt: 1 }}>
          <TextField
            id="email"
            label="Email"
            variant="outlined"
            type="email"
            value={email}
            onChange={(event: React.ChangeEvent<HTMLInputElement>) => {
              setEmail(event.target.value)
            }}
            fullWidth required
          />
          <TextField
            id="password"
            label="Password"
            variant="outlined"
            type="password"
            value={password}
            onChange={(event: React.ChangeEvent<HTMLInputElement>) => {
              setPassword(event.target.value)
            }}
            fullWidth required
          />
        </Stack>
      </DialogContent>
      <DialogActions sx={{ px: 3, pb: 2 }}>
        <Button onClick={handleSignUp} color="secondary">
          Sign Up
        </Button>
        <Button onClick={() => handleSubmit()} variant="contained">
          Login
        </Button>
      </DialogActions>
    </Dialog>
  );
}
