import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Box } from '@mui/material';
import { MainLayout } from '@/components/layout/MainLayout';
import { Home } from '@/pages/Home';

export default function App() {
  return (
    <Box sx={{ width: '100%', display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<MainLayout />}>
            <Route index element={<Home />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </Box>
  );
}
