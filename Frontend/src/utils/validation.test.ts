import { describe, it, expect } from 'vitest';
import {
  validateEmail,
  validatePassword,
  validateStandard,
} from '../../utils/validation';

describe('Validation Utilities', () => {
  describe('validateEmail', () => {
    it('returns no errors for valid email', () => {
      const result = validateEmail('user@example.com');
      expect(result).toEqual([]);
    });

    it('returns error for empty email', () => {
      const result = validateEmail('');
      expect(result).toContain(expect.stringMatching(/required|email/i));
    });

    it('returns error for invalid format', () => {
      const result = validateEmail('invalid-email');
      expect(result.length).toBeGreaterThan(0);
    });

    it('returns error for email with spaces', () => {
      const result = validateEmail('user @example.com');
      expect(result.length).toBeGreaterThan(0);
    });

    it('accepts emails with plus addressing', () => {
      const result = validateEmail('user+filter@example.com');
      expect(result).toEqual([]);
    });
  });

  describe('validatePassword', () => {
    it('returns no errors for strong password', () => {
      const result = validatePassword('SecurePass123!');
      expect(result).toEqual([]);
    });

    it('returns error for password less than 8 characters', () => {
      const result = validatePassword('Short1!');
      expect(result).toContain(expect.stringMatching(/8.*characters|too short|minimum/i));
    });

    it('returns error for password without uppercase', () => {
      const result = validatePassword('lowercase123!');
      expect(result.length).toBeGreaterThan(0);
    });

    it('returns error for password without lowercase', () => {
      const result = validatePassword('UPPERCASE123!');
      expect(result.length).toBeGreaterThan(0);
    });

    it('returns error for password without number', () => {
      const result = validatePassword('NoNumbers!');
      expect(result.length).toBeGreaterThan(0);
    });

    it('returns error for password without special character', () => {
      const result = validatePassword('NoSpecial123');
      expect(result.length).toBeGreaterThan(0);
    });

    it('returns no errors for very strong password', () => {
      const result = validatePassword('VeryStr0ng@Password#2024');
      expect(result).toEqual([]);
    });
  });

  describe('validateStandard', () => {
    it('returns no errors for valid standard object', () => {
      const standard = {
        code: 'ISO-9001',
        title: 'Quality Management',
        description: 'International standard for quality management',
      };
      const result = validateStandard(standard);
      expect(result).toEqual([]);
    });

    it('returns error for missing code', () => {
      const standard = {
        title: 'Quality Management',
        description: 'Description',
      };
      const result = validateStandard(standard);
      expect(result).toContain(expect.stringMatching(/code|required/i));
    });

    it('returns error for missing title', () => {
      const standard = {
        code: 'ISO-9001',
        description: 'Description',
      };
      const result = validateStandard(standard);
      expect(result).toContain(expect.stringMatching(/title|required/i));
    });

    it('returns error for empty code', () => {
      const standard = {
        code: '',
        title: 'Quality Management',
        description: 'Description',
      };
      const result = validateStandard(standard);
      expect(result.length).toBeGreaterThan(0);
    });

    it('returns error for code not matching ISO format', () => {
      const standard = {
        code: 'INVALID-CODE',
        title: 'Quality Management',
        description: 'Description',
      };
      const result = validateStandard(standard);
      expect(result.length).toBeGreaterThan(0);
    });

    it('returns error for very long title', () => {
      const standard = {
        code: 'ISO-9001',
        title: 'A'.repeat(300),
        description: 'Description',
      };
      const result = validateStandard(standard);
      expect(result.length).toBeGreaterThan(0);
    });
  });
});
