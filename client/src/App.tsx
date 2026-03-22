import { useState } from 'react';
import Login from './components/login.component';
import SignUp from './components/signup.component';
import { AuthProvider } from './contexts/auth.context';

function App() {
  const [loginOpen, setLoginOpen] = useState(true); // or false initially
  const [signUpOpen, setSignUpOpen] = useState(false);

  const handleLoginClose = (_: {}, reason: string) => {
    if (reason === 'signUp') {
      setLoginOpen(false);
      setSignUpOpen(true);
    } else if (reason === 'escapeKeyDown') {
      setLoginOpen(false); // just close login
    }
    // ignore backdrop click
  };

  const handleSignUpClose = () => {
    setSignUpOpen(false);
  };

  const handleBackToLogin = () => {
    setSignUpOpen(false);
    setLoginOpen(true);
  };

  return (
    <>
     <AuthProvider>
      {/* You might have a button to open login dialog initially */}
      <Login open={loginOpen} onClose={handleLoginClose} />
      <SignUp open={signUpOpen} onClose={handleSignUpClose} onLoginClick={handleBackToLogin} />
     </AuthProvider>
    </>
  );
}

export default App;
