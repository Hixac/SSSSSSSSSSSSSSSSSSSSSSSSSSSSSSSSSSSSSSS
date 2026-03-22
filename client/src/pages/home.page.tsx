import { Button, Container, Typography } from '@mui/material';
import { useAuthModal } from '../contexts/AuthModalContext'; // we'll create this

export default function Home() {
  const { openLogin, openSignup } = useAuthModal();
  return (
    <Container>
      <Typography variant="h2">Welcome</Typography>
      <Button onClick={openLogin}>Login</Button>
      <Button onClick={openSignup}>Sign Up</Button>
    </Container>
  );
}
