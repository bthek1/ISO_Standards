import { describe, it, expect, afterEach } from 'vitest';
import { renderHook, act } from '@testing-library/react';
import { useLocalStorage } from '../../hooks/useLocalStorage';

describe('useLocalStorage Hook', () => {
  afterEach(() => {
    localStorage.clear();
  });

  it('returns initial value', () => {
    const { result } = renderHook(() => useLocalStorage('key', 'initial'));
    expect(result.current[0]).toBe('initial');
  });

  it('updates local storage when value changes', () => {
    const { result } = renderHook(() => useLocalStorage('key', 'initial'));

    act(() => {
      result.current[1]('updated');
    });

    expect(result.current[0]).toBe('updated');
    expect(localStorage.getItem('key')).toBe('"updated"');
  });

  it('retrieves value from local storage on mount', () => {
    localStorage.setItem('key', JSON.stringify('stored'));
    const { result } = renderHook(() => useLocalStorage('key', 'initial'));

    expect(result.current[0]).toBe('stored');
  });

  it('handles null values', () => {
    const { result } = renderHook(() => useLocalStorage('key', 'initial'));

    act(() => {
      result.current[1](null);
    });

    expect(result.current[0]).toBeNull();
  });

  it('handles complex objects', () => {
    const obj = { name: 'Test', value: 123 };
    const { result } = renderHook(() => useLocalStorage('key', obj));

    act(() => {
      result.current[1]({ ...obj, value: 456 });
    });

    expect(result.current[0]).toEqual({ name: 'Test', value: 456 });
  });

  it('handles arrays', () => {
    const arr = [1, 2, 3];
    const { result } = renderHook(() => useLocalStorage('key', arr));

    act(() => {
      result.current[1]([...arr, 4]);
    });

    expect(result.current[0]).toEqual([1, 2, 3, 4]);
  });

  it('persists across multiple hook instances with same key', () => {
    const { result: result1 } = renderHook(() => useLocalStorage('key', 'initial'));

    act(() => {
      result1.current[1]('updated');
    });

    const { result: result2 } = renderHook(() => useLocalStorage('key', 'initial'));
    expect(result2.current[0]).toBe('updated');
  });

  it('removes value when set to undefined', () => {
    localStorage.setItem('key', JSON.stringify('value'));
    const { result } = renderHook(() => useLocalStorage('key', 'initial'));

    act(() => {
      result.current[1](undefined);
    });

    expect(result.current[0]).toBeUndefined();
    expect(localStorage.getItem('key')).toBeNull();
  });

  it('handles localStorage errors gracefully', () => {
    const { result } = renderHook(() => useLocalStorage('key', 'initial'));

    // Simulate localStorage error by mocking
    const originalSetItem = Storage.prototype.setItem;
    Storage.prototype.setItem = () => {
      throw new Error('QuotaExceededError');
    };

    act(() => {
      expect(() => result.current[1]('new')).not.toThrow();
    });

    Storage.prototype.setItem = originalSetItem;
  });

  it('handles boolean values', () => {
    const { result } = renderHook(() => useLocalStorage('key', true));

    act(() => {
      result.current[1](false);
    });

    expect(result.current[0]).toBe(false);
  });
});
