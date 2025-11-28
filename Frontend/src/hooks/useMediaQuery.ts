import { useTheme } from '@mui/material/styles';
import { useMediaQuery as muiUseMediaQuery } from '@mui/material';

export const useMediaQuery = (query: string): boolean => {
  return muiUseMediaQuery(query);
};

export const useIsMobile = (): boolean => {
  const theme = useTheme();
  return useMediaQuery(theme.breakpoints.down('sm'));
};

export const useIsTablet = (): boolean => {
  const theme = useTheme();
  return useMediaQuery(theme.breakpoints.down('md'));
};

export const useIsDesktop = (): boolean => {
  const theme = useTheme();
  return useMediaQuery(theme.breakpoints.up('lg'));
};
