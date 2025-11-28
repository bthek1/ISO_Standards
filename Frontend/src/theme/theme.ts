import { createTheme } from '@mui/material/styles';
import { colors } from './colors';
import { typography } from './typography';

export const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: colors.primary[600],
      light: colors.primary[400],
      dark: colors.primary[800],
    },
    secondary: {
      main: colors.secondary[600],
      light: colors.secondary[400],
      dark: colors.secondary[800],
    },
    error: {
      main: colors.error[600],
    },
    warning: {
      main: colors.warning[600],
    },
    success: {
      main: colors.success[600],
    },
    background: {
      default: '#f5f5f5',
      paper: '#ffffff',
    },
  },
  typography,
  shape: {
    borderRadius: 8,
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none',
          fontWeight: 600,
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
        },
      },
    },
  },
});
