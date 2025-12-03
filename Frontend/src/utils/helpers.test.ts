import { describe, it, expect } from 'vitest';
import { isValidEmail, isEmpty } from './helpers';

describe('Helper Utilities', () => {
  describe('isValidEmail', () => {
    it('validates correct email format', () => {
      expect(isValidEmail('test@example.com')).toBe(true);
    });

    it('validates email with subdomain', () => {
      expect(isValidEmail('user@mail.example.com')).toBe(true);
    });

    it('rejects email without @', () => {
      expect(isValidEmail('testexample.com')).toBe(false);
    });

    it('rejects email without domain', () => {
      expect(isValidEmail('test@')).toBe(false);
    });

    it('rejects email with only @', () => {
      expect(isValidEmail('@')).toBe(false);
    });

    it('rejects empty string', () => {
      expect(isValidEmail('')).toBe(false);
    });

    it('rejects email with spaces', () => {
      expect(isValidEmail('test @example.com')).toBe(false);
    });

    it('accepts email with plus sign', () => {
      expect(isValidEmail('user+tag@example.com')).toBe(true);
    });
  });

  describe('isEmpty', () => {
    it('returns true for empty string', () => {
      expect(isEmpty('')).toBe(true);
    });

    it('returns true for null', () => {
      expect(isEmpty(null)).toBe(true);
    });

    it('returns true for undefined', () => {
      expect(isEmpty(undefined)).toBe(true);
    });

    it('returns true for empty array', () => {
      expect(isEmpty([])).toBe(true);
    });

    it('returns true for empty object', () => {
      expect(isEmpty({})).toBe(true);
    });

    it('returns false for non-empty string', () => {
      expect(isEmpty('hello')).toBe(false);
    });

    it('returns false for non-empty array', () => {
      expect(isEmpty([1, 2, 3])).toBe(false);
    });

    it('returns false for non-empty object', () => {
      expect(isEmpty({ key: 'value' })).toBe(false);
    });

    it('returns true for whitespace-only string', () => {
      expect(isEmpty('   ')).toBe(true);
    });

    it('returns false for number zero', () => {
      expect(isEmpty(0)).toBe(false);
    });

    it('returns false for boolean false', () => {
      expect(isEmpty(false)).toBe(false);
    });
  });
});
