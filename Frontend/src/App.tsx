import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Container } from '@mui/material';
import { MainLayout } from '@/components/layout/MainLayout';

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<MainLayout />}>
          <Route
            index
            element={
              <Container>
                <h1>Welcome to ISO Standards Platform</h1>
              </Container>
            }
          />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}
