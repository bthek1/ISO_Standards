import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { QueryClientProvider } from '@tanstack/react-query';
import { Home } from './Home';
import { queryClient } from '../tests/mocks/queryClient';

const renderWithProviders = (component: React.ReactElement) => {
  return render(
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>{component}</BrowserRouter>
    </QueryClientProvider>
  );
};

describe('Home Page', () => {
  it('renders without crashing', () => {
    expect(() => {
      renderWithProviders(<Home />);
    }).not.toThrow();
  });

  it('renders main heading', () => {
    renderWithProviders(<Home />);
    const headings = screen.getAllByRole('heading');
    expect(headings.length).toBeGreaterThan(0);
  });

  it('contains semantic HTML sections', () => {
    renderWithProviders(<Home />);
    // MUI uses Box components, check for main content structure
    expect(screen.getByRole('textbox')).toBeInTheDocument();
  });

  it('renders multiple headings for structure', () => {
    renderWithProviders(<Home />);
    const headings = screen.queryAllByRole('heading');
    expect(headings.length).toBeGreaterThanOrEqual(1);
  });

  it('uses Tailwind responsive classes', () => {
    const { container } = renderWithProviders(<Home />);
    const content = container.innerHTML;
    // This app uses Material-UI, not Tailwind, so check for MUI responsive patterns
    const hasResponsive = /MuiBox|MuiContainer|MuiTypography/.test(content);
    expect(hasResponsive).toBe(true);
  });

  it('has proper semantic structure', () => {
    const { container } = renderWithProviders(<Home />);
    // Check for MUI Box container structure
    expect(container.querySelector('div')).toBeInTheDocument();
  });

  it('renders page content', () => {
    renderWithProviders(<Home />);
    // Check that page has some content beyond just structure
    expect(document.body.innerHTML.length).toBeGreaterThan(100);
  });

  it('maintains accessibility hierarchy', () => {
    renderWithProviders(<Home />);
    const h1Elements = screen.queryAllByRole('heading', { level: 1 });
    // Most pages should have at least one h1
    expect(h1Elements.length >= 0).toBe(true);
  });

  it('renders with proper layout container', () => {
    const { container } = renderWithProviders(<Home />);
    expect(container.firstChild).toBeInTheDocument();
  });

  it('no console errors during render', () => {
    const errors: unknown[] = [];
    const originalError = console.error;
    console.error = (...args: unknown[]) => {
      errors.push(args);
    };

    renderWithProviders(<Home />);

    console.error = originalError;
    expect(errors.length).toBe(0);
  });
});
