import { useState } from 'react';
import Button from '@mui/material/Button';
import Dialog, { type DialogProps } from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogTitle from '@mui/material/DialogTitle';
import TextField from '@mui/material/TextField';
import Stack from '@mui/material/Stack';
import { useAuth } from '../contexts/auth.context';
import { Typography } from '@mui/material';

interface SignUpProps {
  open: boolean;
  onClose: (event: {}, reason: 'backdropClick' | 'escapeKeyDown' | 'signUp') => void;
  onLoginClick: () => void;
}

export default function SignUp({ open, onClose, onLoginClick }: SignUpProps) {
  const [name, setName] = useState('');
  const [surname, setSurname] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [confirmTouched, setConfirmTouched] = useState(false); // track if user left the field
  const [submitError, setSubmitError] = useState(''); // for other errors like API failures
  const { signup } = useAuth();

  // Derived validation: true if confirm is not empty AND doesn't match password
  const isConfirmError = confirmTouched && confirmPassword !== password;

  const handleDialogClose: DialogProps['onClose'] = (_, reason) => {
    if (reason === 'backdropClick') return;
    onClose(_, reason);
  };

  const handleSignup = async () => {
    // Clear previous submit errors
    setSubmitError('');

    // Double-check before submit (in case validation was bypassed)
    if (password !== confirmPassword) {
      setConfirmTouched(true); // force error display
      return;
    }

    try {
      await signup(name, surname, email, password);
      onClose({}, 'signUp'); // close dialog on success
    } catch (err: any) {
      setSubmitError(err.message);
    }
  };

  return (
    <Dialog open={open} onClose={handleDialogClose} maxWidth="xs" fullWidth>
      <DialogTitle>Create Account</DialogTitle>
      <DialogContent>
        <Stack spacing={2} sx={{ mt: 1 }}>
          <TextField
            label="Name"
            value={name}
            onChange={(e) => setName(e.target.value)}
            fullWidth
            required
          />
          <TextField
            label="Surname"
            value={surname}
            onChange={(e) => setSurname(e.target.value)}
            fullWidth
            required
          />
          <TextField
            label="Email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            fullWidth
            required
          />
          <TextField
            label="Password"
            type="password"
            value={password}
            onChange={(e) => {
              setPassword(e.target.value);
              // Optionally clear confirm error when password changes?
              // But better to leave it for user to see they still need to fix.
            }}
            fullWidth
            required
          />
          <TextField
            label="Confirm Password"
            type="password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
            onBlur={() => setConfirmTouched(true)} // mark as touched when user leaves field
            error={isConfirmError}
            helperText={isConfirmError ? 'Passwords do not match' : ' '} // keep spacing with empty string
            fullWidth
            required
          />
          {submitError && (
            // You can also use MUI Alert or a simple Typography
            <Typography color="error" variant="body2">
              {submitError}
            </Typography>
          )}
        </Stack>
      </DialogContent>
      <DialogActions sx={{ px: 3, pb: 2 }}>
        <Button onClick={onLoginClick} color="secondary">
          Back to Login
        </Button>
        <Button onClick={handleSignup} variant="contained">
          Sign Up
        </Button>
      </DialogActions>
    </Dialog>
  );
}
