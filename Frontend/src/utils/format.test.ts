import { describe, it, expect } from 'vitest';
import {
  formatDate,
  formatDateDistance,
  truncateText,
  capitalizeFirstLetter,
  slugify,
} from '../../utils/format';

describe('Format Utilities', () => {
  describe('formatDate', () => {
    it('formats date to ISO string', () => {
      const date = new Date('2025-12-01');
      const formatted = formatDate(date);
      expect(formatted).toMatch(/2025-12-01/);
    });

    it('handles null dates', () => {
      const formatted = formatDate(null);
      expect(formatted).toBe('');
    });

    it('formats date objects correctly', () => {
      const date = new Date('2025-01-15');
      const formatted = formatDate(date);
      expect(formatted).toContain('2025');
    });
  });

  describe('formatDateDistance', () => {
    it('returns formatted distance string', () => {
      const past = new Date(Date.now() - 60000); // 1 minute ago
      const distance = formatDateDistance(past);
      expect(distance).toBeDefined();
      expect(typeof distance).toBe('string');
    });

    it('handles recent dates', () => {
      const now = new Date();
      const distance = formatDateDistance(now);
      expect(distance).toBeDefined();
    });
  });

  describe('truncateText', () => {
    it('truncates text to specified length', () => {
      const text = 'This is a long text that should be truncated';
      const truncated = truncateText(text, 10);
      expect(truncated.length).toBeLessThanOrEqual(13); // 10 + "..."
    });

    it('does not truncate short text', () => {
      const text = 'Short';
      const truncated = truncateText(text, 20);
      expect(truncated).toBe('Short');
    });

    it('adds ellipsis when truncated', () => {
      const text = 'This is a long text';
      const truncated = truncateText(text, 5);
      expect(truncated).toContain('...');
    });

    it('uses custom suffix', () => {
      const text = 'This is a long text';
      const truncated = truncateText(text, 5, '→');
      expect(truncated).toContain('→');
    });
  });

  describe('capitalizeFirstLetter', () => {
    it('capitalizes first letter', () => {
      expect(capitalizeFirstLetter('hello')).toBe('Hello');
    });

    it('handles already capitalized text', () => {
      expect(capitalizeFirstLetter('Hello')).toBe('Hello');
    });

    it('handles single character', () => {
      expect(capitalizeFirstLetter('a')).toBe('A');
    });

    it('handles empty string', () => {
      expect(capitalizeFirstLetter('')).toBe('');
    });
  });

  describe('slugify', () => {
    it('converts to lowercase', () => {
      expect(slugify('Hello World')).toBe('hello-world');
    });

    it('replaces spaces with hyphens', () => {
      expect(slugify('hello world test')).toBe('hello-world-test');
    });

    it('removes special characters', () => {
      expect(slugify('hello@world!')).toBe('helloworld');
    });

    it('handles multiple spaces', () => {
      expect(slugify('hello   world')).toBe('hello-world');
    });

    it('removes leading/trailing hyphens', () => {
      const result = slugify('  hello world  ');
      expect(result).not.toMatch(/^-|-$/);
    });
  });
});
