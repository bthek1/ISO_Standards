import { describe, it, expect } from 'vitest';
import { renderHook, waitFor } from '@testing-library/react';
import { useDebounce } from './useDebounce';

describe('useDebounce Hook', () => {
  it('returns initial value immediately', () => {
    const { result } = renderHook(() => useDebounce('initial', 500));
    expect(result.current).toBe('initial');
  });

  it('debounces value updates', async () => {
    const { result, rerender } = renderHook(
      ({ value, delay }: { value: string; delay: number }) => useDebounce(value, delay),
      {
        initialProps: { value: 'initial', delay: 500 },
      }
    );

    expect(result.current).toBe('initial');

    // Update value
    rerender({ value: 'updated', delay: 500 });

    // Value should still be old after a short delay
    expect(result.current).toBe('initial');

    // Wait for debounce to complete
    await waitFor(() => {
      expect(result.current).toBe('updated');
    }, { timeout: 1000 });
  });

  it('uses custom delay', async () => {
    const { result, rerender } = renderHook(
      ({ value, delay }: { value: string; delay: number }) => useDebounce(value, delay),
      {
        initialProps: { value: 'initial', delay: 100 },
      }
    );

    rerender({ value: 'updated', delay: 100 });

    // Should debounce faster with shorter delay
    await waitFor(() => {
      expect(result.current).toBe('updated');
    }, { timeout: 300 });
  });

  it('cancels previous debounce on rapid updates', async () => {
    const { result, rerender } = renderHook(
      ({ value, delay }: { value: string; delay: number }) => useDebounce(value, delay),
      {
        initialProps: { value: 'first', delay: 500 },
      }
    );

    // Rapid updates
    rerender({ value: 'second', delay: 500 });
    rerender({ value: 'third', delay: 500 });
    rerender({ value: 'final', delay: 500 });

    // Should only use final value
    await waitFor(() => {
      expect(result.current).toBe('final');
    }, { timeout: 1000 });
  });

  it('works with different data types', () => {
    const { result, rerender } = renderHook(
      ({ value, delay }: { value: number; delay: number }) => useDebounce(value, delay),
      {
        initialProps: { value: 123, delay: 500 },
      }
    );

    expect(result.current).toBe(123);

    rerender({ value: 456, delay: 500 });
    expect(result.current).toBe(123);
  });
});
