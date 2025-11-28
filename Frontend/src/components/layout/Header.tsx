import {
  AppBar,
  Toolbar,
  Typography,
  Button,
  Box,
  IconButton,
  Menu,
  MenuItem,
} from '@mui/material';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import SearchIcon from '@mui/icons-material/Search';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '@/hooks/useAuth';
import { useState } from 'react';

export const Header = () => {
  const navigate = useNavigate();
  const { isAuthenticated, user, logout } = useAuth();
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);

  const handleMenuOpen = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  const handleLogout = async () => {
    handleMenuClose();
    await logout();
    navigate('/login');
  };

  return (
    <AppBar
      position="static"
      sx={{
        backgroundColor: '#ffffff',
        color: '#1a3a52',
        boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)',
        borderBottom: '1px solid #e0e0e0',
      }}
    >
      <Toolbar sx={{ justifyContent: 'space-between', py: 1 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          <Typography
            variant="h6"
            sx={{
              cursor: 'pointer',
              fontWeight: 700,
              color: '#1e88e5',
              fontSize: '1.3rem',
              '&:hover': { color: '#1565c0' },
            }}
            onClick={() => navigate('/')}
          >
            ISO Standards
          </Typography>
          <Typography
            variant="caption"
            sx={{
              color: '#666',
              fontSize: '0.85rem',
              borderLeft: '1px solid #e0e0e0',
              pl: 2,
            }}
          >
            Global Standards Platform
          </Typography>
        </Box>

        <Box sx={{ display: 'flex', gap: 1, alignItems: 'center' }}>
          <Button
            color="inherit"
            onClick={() => navigate('/search')}
            startIcon={<SearchIcon />}
            sx={{
              textTransform: 'none',
              fontSize: '0.95rem',
              '&:hover': { backgroundColor: 'rgba(30, 136, 229, 0.08)' },
            }}
          >
            Search
          </Button>

          {isAuthenticated ? (
            <>
              <Button
                color="inherit"
                onClick={() => navigate('/dashboard')}
                sx={{
                  textTransform: 'none',
                  fontSize: '0.95rem',
                  '&:hover': { backgroundColor: 'rgba(30, 136, 229, 0.08)' },
                }}
              >
                Dashboard
              </Button>

              <IconButton
                onClick={handleMenuOpen}
                sx={{
                  color: '#1e88e5',
                  '&:hover': { backgroundColor: 'rgba(30, 136, 229, 0.08)' },
                }}
              >
                <AccountCircleIcon />
              </IconButton>

              <Menu
                anchorEl={anchorEl}
                open={Boolean(anchorEl)}
                onClose={handleMenuClose}
              >
                <MenuItem disabled>{user?.email}</MenuItem>
                <MenuItem onClick={() => navigate('/profile')}>
                  Profile
                </MenuItem>
                <MenuItem onClick={handleLogout}>Logout</MenuItem>
              </Menu>
            </>
          ) : (
            <>
              <Button
                color="inherit"
                onClick={() => navigate('/login')}
                sx={{
                  textTransform: 'none',
                  fontSize: '0.95rem',
                  '&:hover': { backgroundColor: 'rgba(30, 136, 229, 0.08)' },
                }}
              >
                Sign In
              </Button>
              <Button
                variant="contained"
                onClick={() => navigate('/register')}
                sx={{
                  backgroundColor: '#1e88e5',
                  color: 'white',
                  textTransform: 'none',
                  fontSize: '0.95rem',
                  '&:hover': { backgroundColor: '#1565c0' },
                }}
              >
                Register
              </Button>
            </>
          )}
        </Box>
      </Toolbar>
    </AppBar>
  );
};
