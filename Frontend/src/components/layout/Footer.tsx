import { Box, Container, Typography } from '@mui/material';

export const Footer = () => {
  const currentYear = new Date().getFullYear();

  return (
    <Box component="footer" sx={{ py: 4, mt: 8, backgroundColor: '#f5f5f5' }}>
      <Container>
        <Typography variant="body2" color="textSecondary" align="center">
          © {currentYear} ISO Standards Platform. All rights reserved.
        </Typography>
        <Box
          sx={{
            display: 'flex',
            justifyContent: 'center',
            gap: 3,
            mt: 2,
            flexWrap: 'wrap',
          }}
        >
          <Typography
            variant="body2"
            color="primary"
            sx={{ cursor: 'pointer', '&:hover': { textDecoration: 'underline' } }}
          >
            Privacy Policy
          </Typography>
          <Typography
            variant="body2"
            color="primary"
            sx={{ cursor: 'pointer', '&:hover': { textDecoration: 'underline' } }}
          >
            Terms of Service
          </Typography>
          <Typography
            variant="body2"
            color="primary"
            sx={{ cursor: 'pointer', '&:hover': { textDecoration: 'underline' } }}
          >
            Contact Us
          </Typography>
        </Box>
      </Container>
    </Box>
  );
};
