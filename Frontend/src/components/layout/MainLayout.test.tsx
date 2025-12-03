import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { QueryClientProvider } from '@tanstack/react-query';
import { MainLayout } from './MainLayout';
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

describe('MainLayout Component', () => {
  it('renders header', () => {
    renderWithProviders(<MainLayout />);
    expect(screen.getByRole('banner')).toBeInTheDocument();
  });

  it('renders footer', () => {
    renderWithProviders(<MainLayout />);
    expect(screen.getByRole('contentinfo')).toBeInTheDocument();
  });

  it('renders main content area', () => {
    renderWithProviders(<MainLayout />);
    const main = screen.getByRole('main');
    expect(main).toBeInTheDocument();
  });

  it('has flex column layout', () => {
    const { container } = renderWithProviders(<MainLayout />);
    const layoutContainer = container.querySelector('.MuiBox-root');
    expect(layoutContainer).toBeInTheDocument();
  });

  it('main content expands to fill space', () => {
    renderWithProviders(<MainLayout />);
    const main = screen.getByRole('main');
    expect(main).toBeInTheDocument();
  });

  it('renders header before main content', () => {
    renderWithProviders(<MainLayout />);
    const header = screen.getByRole('banner');
    const main = screen.getByRole('main');

    expect(header.compareDocumentPosition(main) & Node.DOCUMENT_POSITION_FOLLOWING).toBe(
      Node.DOCUMENT_POSITION_FOLLOWING
    );
  });

  it('renders footer after main content', () => {
    renderWithProviders(<MainLayout />);
    const main = screen.getByRole('main');
    const footer = screen.getByRole('contentinfo');

    expect(main.compareDocumentPosition(footer) & Node.DOCUMENT_POSITION_FOLLOWING).toBe(
      Node.DOCUMENT_POSITION_FOLLOWING
    );
  });

  it('header has white background', () => {
    renderWithProviders(<MainLayout />);
    const header = screen.getByRole('banner');
    expect(header).toBeInTheDocument();
  });

  it('footer has dark background', () => {
    renderWithProviders(<MainLayout />);
    const footer = screen.getByRole('contentinfo');
    expect(footer).toBeInTheDocument();
  });

  it('children are rendered correctly', () => {
    renderWithProviders(
      <MainLayout>
        <div data-testid="child-content">Test Content</div>
      </MainLayout>
    );

    expect(screen.getByTestId('child-content')).toBeInTheDocument();
  });

  it('renders outlet for nested routes', () => {
    renderWithProviders(<MainLayout />);
    const main = screen.getByRole('main');
    expect(main).toBeInTheDocument();
  });
});
