import { describe, it, expect } from 'vitest';
import { loginSchema, registerSchema, searchSchema } from './validation';
import type { LoginFormData, RegisterFormData, SearchFormData } from './validation';

describe('Validation Schemas', () => {
  describe('loginSchema', () => {
    it('validates correct login data', () => {
      const data: LoginFormData = {
        email: 'user@example.com',
        password: 'SecurePass123',
      };
      expect(() => loginSchema.parse(data)).not.toThrow();
    });

    it('rejects invalid email', () => {
      const data = {
        email: 'invalid-email',
        password: 'SecurePass123',
      };
      expect(() => loginSchema.parse(data)).toThrow();
    });

    it('rejects short password', () => {
      const data = {
        email: 'user@example.com',
        password: 'short',
      };
      expect(() => loginSchema.parse(data)).toThrow();
    });

    it('rejects empty email', () => {
      const data = {
        email: '',
        password: 'SecurePass123',
      };
      expect(() => loginSchema.parse(data)).toThrow();
    });

    it('accepts valid 8-character password', () => {
      const data: LoginFormData = {
        email: 'user@example.com',
        password: '12345678',
      };
      expect(() => loginSchema.parse(data)).not.toThrow();
    });
  });

  describe('registerSchema', () => {
    it('validates correct registration data', () => {
      const data: RegisterFormData = {
        name: 'John Doe',
        email: 'john@example.com',
        password: 'SecurePass123',
        confirmPassword: 'SecurePass123',
      };
      expect(() => registerSchema.parse(data)).not.toThrow();
    });

    it('rejects mismatched passwords', () => {
      const data = {
        name: 'John Doe',
        email: 'john@example.com',
        password: 'SecurePass123',
        confirmPassword: 'DifferentPass456',
      };
      expect(() => registerSchema.parse(data)).toThrow();
    });

    it('rejects short name', () => {
      const data = {
        name: 'J',
        email: 'john@example.com',
        password: 'SecurePass123',
        confirmPassword: 'SecurePass123',
      };
      expect(() => registerSchema.parse(data)).toThrow();
    });

    it('rejects invalid email', () => {
      const data = {
        name: 'John Doe',
        email: 'invalid',
        password: 'SecurePass123',
        confirmPassword: 'SecurePass123',
      };
      expect(() => registerSchema.parse(data)).toThrow();
    });

    it('rejects empty name', () => {
      const data = {
        name: '',
        email: 'john@example.com',
        password: 'SecurePass123',
        confirmPassword: 'SecurePass123',
      };
      expect(() => registerSchema.parse(data)).toThrow();
    });
  });

  describe('searchSchema', () => {
    it('validates correct search query', () => {
      const data: SearchFormData = {
        query: 'ISO-9001',
      };
      expect(() => searchSchema.parse(data)).not.toThrow();
    });

    it('rejects empty query', () => {
      const data = {
        query: '',
      };
      expect(() => searchSchema.parse(data)).toThrow();
    });

    it('rejects query exceeding max length', () => {
      const data = {
        query: 'A'.repeat(201),
      };
      expect(() => searchSchema.parse(data)).toThrow();
    });

    it('accepts query at max length', () => {
      const data: SearchFormData = {
        query: 'A'.repeat(200),
      };
      expect(() => searchSchema.parse(data)).not.toThrow();
    });

    it('accepts single character query', () => {
      const data: SearchFormData = {
        query: 'Q',
      };
      expect(() => searchSchema.parse(data)).not.toThrow();
    });
  });
});
