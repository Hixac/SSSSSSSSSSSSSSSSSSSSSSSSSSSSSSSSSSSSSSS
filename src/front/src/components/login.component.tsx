import { useState } from 'react';
import Button from '@mui/material/Button';
import Dialog from '@mui/material/Dialog';
import { type DialogProps } from '@mui/material/Dialog';
import DialogActions from '@mui/material/DialogActions';
import DialogContent from '@mui/material/DialogContent';
import DialogTitle from '@mui/material/DialogTitle';
import TextField from '@mui/material/TextField';
import Stack from '@mui/material/Stack';

export default function Login() {
  const [open, setOpen] = useState(true);

  const handleClose: DialogProps['onClose'] = (_, reason) => {
    if (reason === 'backdropClick') return;
    setOpen(false);
  };

  return (
    <Dialog open={open} onClose={handleClose} maxWidth="xs" fullWidth>
      <DialogTitle>Welcome Back</DialogTitle>
      <DialogContent>
        <Stack spacing={2} sx={{ mt: 1 }}>
          <TextField
            id="email"
            label="Email"
            variant="outlined"
            type="email"
            fullWidth
          />
          <TextField
            id="password"
            label="Password"
            variant="outlined"
            type="password"
            fullWidth
          />
        </Stack>
      </DialogContent>
      <DialogActions sx={{ px: 3, pb: 2 }}>
        <Button onClick={handleClose} color="secondary">
          Sign Up
        </Button>
        <Button onClick={handleClose} variant="contained">
          Login
        </Button>
      </DialogActions>
    </Dialog>
  );
}
