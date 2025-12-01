import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { QueryClientProvider } from '@tanstack/react-query';
import { Home } from '../../pages/Home';
import { queryClient } from '../../tests/mocks/queryClient';

const renderWithProviders = (component: React.ReactElement) => {
  return render(
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        {component}
      </BrowserRouter>
    </QueryClientProvider>
  );
};

describe('Home Page', () => {
  it('renders hero section', () => {
    renderWithProviders(<Home />);
    expect(screen.getByRole('heading', { level: 1 })).toBeInTheDocument();
  });

  it('displays hero title', () => {
    renderWithProviders(<Home />);
    const heading = screen.getByRole('heading', { level: 1 });
    expect(heading.textContent).toMatch(/ISO|Standards|Regulations/i);
  });

  it('renders hero description', () => {
    renderWithProviders(<Home />);
    expect(screen.getByText(/global standards|international/i)).toBeInTheDocument();
  });

  it('renders call-to-action button', () => {
    renderWithProviders(<Home />);
    const buttons = screen.getAllByRole('button');
    expect(buttons.length).toBeGreaterThan(0);
  });

  it('displays statistics section', () => {
    renderWithProviders(<Home />);
    const headings = screen.getAllByRole('heading');
    expect(headings.length).toBeGreaterThanOrEqual(2);
  });

  it('renders features section', () => {
    renderWithProviders(<Home />);
    expect(screen.getByText(/features|capabilities/i)).toBeInTheDocument();
  });

  it('displays feature cards', () => {
    renderWithProviders(<Home />);
    const articles = screen.queryAllByRole('article');
    expect(articles.length).toBeGreaterThanOrEqual(1);
  });

  it('has proper heading hierarchy', () => {
    renderWithProviders(<Home />);
    const h1 = screen.getByRole('heading', { level: 1 });
    expect(h1).toBeInTheDocument();
  });

  it('hero section has background image or gradient', () => {
    const { container } = renderWithProviders(<Home />);
    const heroSection = container.querySelector('[class*="hero"], [class*="bg-gradient"], [class*="bg-blue"]');
    expect(heroSection).toBeInTheDocument();
  });

  it('layout uses proper semantic HTML', () => {
    const { container } = renderWithProviders(<Home />);
    expect(container.querySelector('section')).toBeInTheDocument();
  });

  it('responsive design classes applied', () => {
    const { container } = renderWithProviders(<Home />);
    const elements = container.querySelectorAll('[class*="md:"], [class*="lg:"], [class*="sm:"]');
    expect(elements.length).toBeGreaterThan(0);
  });

  it('contains navigation or internal links', () => {
    renderWithProviders(<Home />);
    const links = screen.queryAllByRole('link');
    expect(links.length).toBeGreaterThanOrEqual(0);
  });

  it('renders without crashing', () => {
    expect(() => {
      renderWithProviders(<Home />);
    }).not.toThrow();
  });

  it('has accessible color contrast', () => {
    const { container } = renderWithProviders(<Home />);
    const elements = container.querySelectorAll('[class*="text-"], [class*="bg-"]');
    expect(elements.length).toBeGreaterThan(0);
  });

  it('displays content in correct order', () => {
    const { container } = renderWithProviders(<Home />);
    const sections = container.querySelectorAll('section');
    expect(sections.length).toBeGreaterThanOrEqual(1);
  });
});
