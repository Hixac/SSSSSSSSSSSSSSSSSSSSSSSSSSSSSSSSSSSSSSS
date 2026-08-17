import { Navigate, Route, Routes } from 'react-router-dom';
import { AuthProvider } from './contexts/auth.context';
import ProtectedRoute from './routes/ProtectedRoute';
import MainLayout from './layouts/MainLayout';
import LoginPage from './pages/login.page';
import SignupPage from './pages/signup.page';
import BoardPage from './pages/board.page';

export default function App() {
  return (
    <AuthProvider>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/signup" element={<SignupPage />} />
        <Route element={<ProtectedRoute />}>
          <Route element={<MainLayout />}>
            <Route path="/board" element={<BoardPage />} />
          </Route>
        </Route>
        <Route path="*" element={<Navigate to="/board" replace />} />
      </Routes>
    </AuthProvider>
  );
}
