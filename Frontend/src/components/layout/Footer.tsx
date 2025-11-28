import { Box, Container, Typography, Grid, Link, Divider } from '@mui/material';

export const Footer = () => {
  const currentYear = new Date().getFullYear();

  const footerLinks = {
    About: ['Mission', 'About Us', 'Team', 'Careers'],
    Standards: ['Browse Standards', 'Categories', 'Organizations', 'Recent Updates'],
    Support: ['Documentation', 'FAQ', 'Contact Us', 'Report Issue'],
    Legal: ['Privacy Policy', 'Terms of Service', 'Accessibility', 'Cookie Policy'],
  };

  return (
    <Box
      component="footer"
      sx={{
        backgroundColor: '#1a3a52',
        color: '#ffffff',
        py: 6,
        mt: 'auto',
      }}
    >
      <Container maxWidth="lg">
        <Grid container spacing={4} sx={{ mb: 4 }}>
          {Object.entries(footerLinks).map(([section, links]) => (
            <Grid item xs={12} sm={6} md={3} key={section}>
              <Typography
                variant="subtitle1"
                sx={{
                  fontWeight: 600,
                  mb: 2,
                  color: '#1e88e5',
                }}
              >
                {section}
              </Typography>
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
                {links.map((link) => (
                  <Link
                    key={link}
                    href="#"
                    sx={{
                      color: '#ffffff',
                      textDecoration: 'none',
                      fontSize: '0.9rem',
                      opacity: 0.8,
                      transition: 'opacity 0.2s',
                      '&:hover': {
                        opacity: 1,
                        color: '#1e88e5',
                      },
                    }}
                  >
                    {link}
                  </Link>
                ))}
              </Box>
            </Grid>
          ))}
        </Grid>

        <Divider sx={{ backgroundColor: 'rgba(255, 255, 255, 0.2)', my: 3 }} />

        <Box
          sx={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            flexWrap: 'wrap',
            gap: 2,
          }}
        >
          <Typography variant="body2" sx={{ opacity: 0.8 }}>
            © {currentYear} Global Standards Platform. All rights reserved.
          </Typography>
          <Box sx={{ display: 'flex', gap: 3, flexWrap: 'wrap' }}>
            <Link
              href="#"
              sx={{
                color: '#ffffff',
                textDecoration: 'none',
                fontSize: '0.85rem',
                opacity: 0.8,
                '&:hover': {
                  opacity: 1,
                },
              }}
            >
              Accessibility
            </Link>
            <Link
              href="#"
              sx={{
                color: '#ffffff',
                textDecoration: 'none',
                fontSize: '0.85rem',
                opacity: 0.8,
                '&:hover': {
                  opacity: 1,
                },
              }}
            >
              Privacy
            </Link>
            <Link
              href="#"
              sx={{
                color: '#ffffff',
                textDecoration: 'none',
                fontSize: '0.85rem',
                opacity: 0.8,
                '&:hover': {
                  opacity: 1,
                },
              }}
            >
              Terms
            </Link>
          </Box>
        </Box>
      </Container>
    </Box>
  );
};
