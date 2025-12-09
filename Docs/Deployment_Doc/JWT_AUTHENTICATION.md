# JWT Authentication Guide - React Frontend ↔ Django Backend

## 🔐 Overview

This application uses **JWT (JSON Web Tokens)** for stateless authentication between the React frontend and Django REST API backend.

```
┌─────────────────┐                           ┌─────────────────┐
│  React Frontend │                           │ Django Backend  │
│  (Vite + TS)    │◄─────── JWT Tokens ──────►│   (REST API)    │
│                 │                           │                 │
│  - localStorage │                           │  - SimpleJWT    │
│  - Axios        │                           │  - Validation   │
└─────────────────┘                           └─────────────────┘
```

---

## 📦 Dependencies

### Backend (Django)

```toml
# Already included in pyproject.toml
djangorestframework = ">=3.16.0"
djangorestframework-simplejwt = ">=5.5.0"
django-cors-headers = ">=4.7.0"
```

### Frontend (React)

```json
{
  "dependencies": {
    "axios": "^1.6.0"  // Already configured
  }
}
```

---

## 🔧 Configuration

### Backend Configuration

**File: `Backend/config/settings/production.py`**

```python
from datetime import timedelta

# CORS Configuration
CORS_ALLOWED_ORIGINS = os.environ.get(
    'CORS_ALLOWED_ORIGINS',
    'https://d1pjttps83iyey.cloudfront.net'
).split(',')

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# JWT Settings
SIMPLE_JWT = {
    # Token lifetimes
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=int(os.environ.get('SIMPLE_JWT_ACCESS_TOKEN_LIFETIME_MINUTES', 60))),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=int(os.environ.get('SIMPLE_JWT_REFRESH_TOKEN_LIFETIME_DAYS', 7))),

    # Security
    'ROTATE_REFRESH_TOKENS': True,  # Issue new refresh token on refresh
    'BLACKLIST_AFTER_ROTATION': True,  # Blacklist old tokens
    'UPDATE_LAST_LOGIN': True,

    # Algorithm & Keys
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': os.environ.get('SIMPLE_JWT_SIGNING_KEY', SECRET_KEY),
    'VERIFYING_KEY': None,

    # Headers
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',

    # Token claims
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    # Token classes
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    # Sliding tokens (not used, but available)
    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',  # For browsable API
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
}
```

### Backend URLs

**File: `Backend/config/urls.py`**

```python
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # JWT Authentication endpoints
    path('api/v1/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/auth/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # Your app URLs
    path('api/v1/', include('your_app.urls')),
]
```

### Frontend Configuration

**File: `Frontend/src/services/api.ts`** (Already configured)

```typescript
import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor - Add JWT token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('accessToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor - Handle token expiration
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // If 401 and not already retried
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem('refreshToken');

        if (!refreshToken) {
          // No refresh token, redirect to login
          localStorage.clear();
          window.location.href = '/login';
          return Promise.reject(error);
        }

        // Try to refresh the token
        const response = await axios.post(
          `${import.meta.env.VITE_API_URL}/auth/refresh/`,
          { refresh: refreshToken }
        );

        const { access } = response.data;

        // Update stored token
        localStorage.setItem('accessToken', access);

        // Retry original request with new token
        originalRequest.headers.Authorization = `Bearer ${access}`;
        return api(originalRequest);
      } catch (refreshError) {
        // Refresh failed, logout user
        localStorage.clear();
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export default api;
```

**File: `Frontend/src/services/auth.ts`** (Already configured)

```typescript
import api from './api';

interface LoginRequest {
  email: string;
  password: string;
}

interface LoginResponse {
  access: string;
  refresh: string;
  user: {
    id: string;
    email: string;
    name: string;
  };
}

interface RegisterRequest {
  email: string;
  password: string;
  name: string;
}

export const authService = {
  login: async (credentials: LoginRequest): Promise<LoginResponse> => {
    const { data } = await api.post<LoginResponse>(
      '/auth/login/',
      credentials
    );

    // Store tokens
    localStorage.setItem('accessToken', data.access);
    localStorage.setItem('refreshToken', data.refresh);

    return data;
  },

  register: async (userData: RegisterRequest): Promise<LoginResponse> => {
    const { data } = await api.post<LoginResponse>(
      '/auth/register/',
      userData
    );

    // Store tokens
    localStorage.setItem('accessToken', data.access);
    localStorage.setItem('refreshToken', data.refresh);

    return data;
  },

  logout: async (): Promise<void> => {
    try {
      await api.post('/auth/logout/');
    } finally {
      // Clear tokens regardless of API response
      localStorage.removeItem('accessToken');
      localStorage.removeItem('refreshToken');
      localStorage.removeItem('auth-storage');
    }
  },

  verifyToken: async (): Promise<boolean> => {
    try {
      const token = localStorage.getItem('accessToken');
      if (!token) return false;

      await api.post('/auth/verify/', { token });
      return true;
    } catch {
      return false;
    }
  },

  refreshToken: async (): Promise<string> => {
    const refresh = localStorage.getItem('refreshToken');
    if (!refresh) throw new Error('No refresh token');

    const { data } = await api.post('/auth/refresh/', { refresh });
    localStorage.setItem('accessToken', data.access);

    return data.access;
  },
};
```

---

## 🔄 Authentication Flow

### 1. User Login

```typescript
// Frontend: Login Component
import { authService } from '@/services/auth';
import { useAuthStore } from '@/stores/authStore';

const handleLogin = async (email: string, password: string) => {
  try {
    const data = await authService.login({ email, password });

    // Update global state
    useAuthStore.getState().setUser(data.user);
    useAuthStore.getState().setToken(data.access);

    // Tokens already stored in localStorage by authService
    navigate('/dashboard');
  } catch (error) {
    console.error('Login failed:', error);
    // Show error message
  }
};
```

**Backend receives:**

```json
POST /api/v1/auth/login/
{
  "email": "user@example.com",
  "password": "securepassword"
}
```

**Backend responds:**

```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": "123",
    "email": "user@example.com",
    "name": "John Doe"
  }
}
```

### 2. Authenticated API Request

```typescript
// Frontend: Any API call
import api from '@/services/api';

const fetchStandards = async () => {
  const { data } = await api.get('/standards/');
  return data;
};
```

**Request sent:**

```
GET /api/v1/standards/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

**Backend validates JWT and responds with data**

### 3. Token Refresh (Automatic)

When access token expires (after 60 minutes):

1. Frontend makes API request
2. Backend returns 401 Unauthorized
3. Axios interceptor catches 401
4. Automatically calls `/auth/refresh/` with refresh token
5. Gets new access token
6. Retries original request with new token
7. User experiences no interruption

### 4. Logout

```typescript
// Frontend: Logout
const handleLogout = async () => {
  await authService.logout();
  navigate('/login');
};
```

---

## 🛡️ Security Best Practices

### ✅ Implemented

1. **Short-lived access tokens** (60 minutes)
2. **Long-lived refresh tokens** (7 days)
3. **Token rotation** - New refresh token on refresh
4. **Token blacklisting** - Old tokens invalidated
5. **HTTPS only** - Secure transmission
6. **CORS restrictions** - Only allowed origins
7. **Secure cookies** - For session data (production)

### 📝 Recommendations

1. **Use httpOnly cookies for tokens** (more secure than localStorage)
2. **Implement rate limiting** on authentication endpoints
3. **Add CAPTCHA** for login after failed attempts
4. **Use refresh token rotation** with blacklisting
5. **Monitor for token theft** - Check IP, user agent changes
6. **Implement device tracking** - Alert on new devices
7. **Add 2FA** - Multi-factor authentication

---

## 🧪 Testing Authentication

### Test Login

```bash
curl -X POST https://api.yourdomain.com/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123"
  }'
```

Expected response:

```json
{
  "access": "eyJ0eXAiOiJKV1...",
  "refresh": "eyJ0eXAiOiJKV1..."
}
```

### Test Protected Endpoint

```bash
curl https://api.yourdomain.com/api/v1/standards/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1..."
```

### Test Token Refresh

```bash
curl -X POST https://api.yourdomain.com/api/v1/auth/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "eyJ0eXAiOiJKV1..."
  }'
```

### Test Token Verification

```bash
curl -X POST https://api.yourdomain.com/api/v1/auth/verify/ \
  -H "Content-Type: application/json" \
  -d '{
    "token": "eyJ0eXAiOiJKV1..."
  }'
```

---

## 🐛 Troubleshooting

### Issue: CORS errors on login

**Symptoms:**

```
Access to XMLHttpRequest blocked by CORS policy
```

**Solution:**

1. Check `CORS_ALLOWED_ORIGINS` includes frontend URL
2. Ensure `CORS_ALLOW_CREDENTIALS=True`
3. Verify frontend sends credentials in requests

### Issue: Token not being sent

**Symptoms:**

```
401 Unauthorized on API requests
```

**Solution:**

1. Check token is in localStorage: `localStorage.getItem('accessToken')`
2. Verify Axios interceptor is configured
3. Check Authorization header format: `Bearer <token>`

### Issue: Token refresh fails

**Symptoms:**

```
User logged out unexpectedly
```

**Solution:**

1. Check refresh token exists in localStorage
2. Verify refresh token hasn't expired (7 days)
3. Check backend `/auth/refresh/` endpoint works
4. Ensure token blacklisting isn't blocking valid tokens

### Issue: Token decode error

**Symptoms:**

```
Token backend failed to decode
```

**Solution:**

1. Verify `SIGNING_KEY` matches between token creation and validation
2. Check token hasn't been tampered with
3. Ensure `ALGORITHM` is consistent (HS256)

---

## 📊 Token Structure

### Access Token (JWT)

**Header:**

```json
{
  "typ": "JWT",
  "alg": "HS256"
}
```

**Payload:**

```json
{
  "token_type": "access",
  "exp": 1701792000,
  "iat": 1701788400,
  "jti": "abc123...",
  "user_id": 123
}
```

**Signature:**

```
HMACSHA256(
  base64UrlEncode(header) + "." +
  base64UrlEncode(payload),
  SECRET_KEY
)
```

### Refresh Token

Similar structure but:

- `token_type`: "refresh"
- Longer expiration (7 days)
- Used only for getting new access tokens

---

## 🔗 Environment Variables

### Backend (.env.production)

```bash
SIMPLE_JWT_SIGNING_KEY=your-unique-signing-key-here
SIMPLE_JWT_ACCESS_TOKEN_LIFETIME_MINUTES=60
SIMPLE_JWT_REFRESH_TOKEN_LIFETIME_DAYS=7
CORS_ALLOWED_ORIGINS=https://d1pjttps83iyey.cloudfront.net,https://yourdomain.com
```

### Frontend (.env.production)

```bash
VITE_API_URL=https://api.yourdomain.com/api/v1
```

---

## 📚 References

- [Django REST Framework SimpleJWT](https://django-rest-framework-simplejwt.readthedocs.io/)
- [JWT.io - Debugger](https://jwt.io/)
- [OWASP JWT Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html)

---

**Last Updated:** December 3, 2025
