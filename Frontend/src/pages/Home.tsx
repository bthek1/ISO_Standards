import {
  Box,
  Container,
  Typography,
  Button,
  Grid,
  Card,
  CardContent,
  TextField,
  InputAdornment,
} from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';
import PublicIcon from '@mui/icons-material/Public';
import SecurityIcon from '@mui/icons-material/Security';
import StorageIcon from '@mui/icons-material/Storage';
import { useNavigate } from 'react-router-dom';
import { useState } from 'react';

export const Home = () => {
  const navigate = useNavigate();
  const [searchQuery, setSearchQuery] = useState('');

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      navigate(`/search?q=${encodeURIComponent(searchQuery)}`);
    }
  };

  const features = [
    {
      icon: <PublicIcon sx={{ fontSize: 40, color: '#1e88e5' }} />,
      title: 'Global Standards',
      description: 'Access thousands of international standards from recognized organizations worldwide.',
    },
    {
      icon: <SecurityIcon sx={{ fontSize: 40, color: '#1e88e5' }} />,
      title: 'Secure & Reliable',
      description: 'Official standards database with verified information and compliance certifications.',
    },
    {
      icon: <StorageIcon sx={{ fontSize: 40, color: '#1e88e5' }} />,
      title: 'Comprehensive Database',
      description: 'Searchable repository with detailed standards, specifications, and documentation.',
    },
  ];

  const stats = [
    { value: '10,000+', label: 'Standards' },
    { value: '150+', label: 'Organizations' },
    { value: '50+', label: 'Countries' },
    { value: '24/7', label: 'Availability' },
  ];

  return (
    <Box>
      {/* Hero Section */}
      <Box
        sx={{
          background: 'linear-gradient(135deg, #1e88e5 0%, #1565c0 100%)',
          color: '#ffffff',
          py: { xs: 6, md: 10 },
          textAlign: 'center',
        }}
      >
        <Container maxWidth="lg">
          <Typography
            variant="h3"
            component="h1"
            sx={{
              fontWeight: 700,
              mb: 2,
              fontSize: { xs: '2rem', md: '3rem' },
            }}
          >
            Global Standards Authority
          </Typography>
          <Typography
            variant="h6"
            sx={{
              fontWeight: 300,
              mb: 4,
              opacity: 0.95,
              fontSize: { xs: '1rem', md: '1.25rem' },
            }}
          >
            Your trusted source for international standards and best practices
          </Typography>

          {/* Search Bar */}
          <Box component="form" onSubmit={handleSearch} sx={{ maxWidth: 600, mx: 'auto' }}>
            <TextField
              fullWidth
              placeholder="Search standards, organizations, or categories..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <SearchIcon sx={{ color: '#ffffff', mr: 1 }} />
                  </InputAdornment>
                ),
              }}
              sx={{
                '& .MuiOutlinedInput-root': {
                  backgroundColor: '#ffffff',
                  borderRadius: '8px',
                  '& fieldset': {
                    borderColor: '#ffffff',
                  },
                  '&:hover fieldset': {
                    borderColor: '#ffffff',
                  },
                },
                '& .MuiOutlinedInput-input': {
                  color: '#1a3a52',
                  '&::placeholder': {
                    color: '#999999',
                    opacity: 1,
                  },
                },
              }}
            />
          </Box>
        </Container>
      </Box>

      {/* Statistics Section */}
      <Box sx={{ backgroundColor: '#f8f9fa', py: 4 }}>
        <Container maxWidth="lg">
          <Grid container spacing={4}>
            {stats.map((stat) => (
              <Grid item xs={6} md={3} key={stat.label}>
                <Box sx={{ textAlign: 'center' }}>
                  <Typography
                    variant="h4"
                    sx={{
                      fontWeight: 700,
                      color: '#1e88e5',
                      mb: 1,
                    }}
                  >
                    {stat.value}
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    {stat.label}
                  </Typography>
                </Box>
              </Grid>
            ))}
          </Grid>
        </Container>
      </Box>

      {/* Features Section */}
      <Container maxWidth="lg" sx={{ py: 8 }}>
        <Typography
          variant="h4"
          sx={{
            fontWeight: 700,
            mb: 6,
            textAlign: 'center',
            color: '#1a3a52',
          }}
        >
          Why Choose Our Platform
        </Typography>

        <Grid container spacing={4}>
          {features.map((feature, index) => (
            <Grid item xs={12} md={4} key={index}>
              <Card
                sx={{
                  height: '100%',
                  display: 'flex',
                  flexDirection: 'column',
                  boxShadow: '0 2px 8px rgba(0, 0, 0, 0.08)',
                  border: '1px solid #e0e0e0',
                  transition: 'all 0.3s ease',
                  '&:hover': {
                    boxShadow: '0 8px 24px rgba(30, 136, 229, 0.15)',
                    transform: 'translateY(-4px)',
                    borderColor: '#1e88e5',
                  },
                }}
              >
                <CardContent sx={{ textAlign: 'center', py: 4 }}>
                  <Box sx={{ mb: 2 }}>{feature.icon}</Box>
                  <Typography
                    variant="h6"
                    sx={{
                      fontWeight: 600,
                      mb: 1,
                      color: '#1a3a52',
                    }}
                  >
                    {feature.title}
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    {feature.description}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Container>

      {/* CTA Section */}
      <Box
        sx={{
          backgroundColor: '#f8f9fa',
          py: 8,
          textAlign: 'center',
        }}
      >
        <Container maxWidth="md">
          <Typography
            variant="h5"
            sx={{
              fontWeight: 600,
              mb: 4,
              color: '#1a3a52',
            }}
          >
            Ready to Explore Global Standards?
          </Typography>
          <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center', flexWrap: 'wrap' }}>
            <Button
              variant="contained"
              size="large"
              onClick={() => navigate('/search')}
              sx={{
                backgroundColor: '#1e88e5',
                color: '#ffffff',
                textTransform: 'none',
                fontSize: '1rem',
                px: 4,
                '&:hover': {
                  backgroundColor: '#1565c0',
                },
              }}
            >
              Browse Standards
            </Button>
            <Button
              variant="outlined"
              size="large"
              onClick={() => navigate('/register')}
              sx={{
                borderColor: '#1e88e5',
                color: '#1e88e5',
                textTransform: 'none',
                fontSize: '1rem',
                px: 4,
                '&:hover': {
                  borderColor: '#1565c0',
                  backgroundColor: 'rgba(30, 136, 229, 0.05)',
                },
              }}
            >
              Create Account
            </Button>
          </Box>
        </Container>
      </Box>
    </Box>
  );
};
