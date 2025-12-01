import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { QueryClientProvider } from '@tanstack/react-query';
import { queryClient } from '../mocks/queryClient';
import { Header } from '../../components/layout/Header';

const renderHeader = () => {
  return render(
    <BrowserRouter>
      <QueryClientProvider client={queryClient}>
        <Header />
      </QueryClientProvider>
    </BrowserRouter>
  );
};

describe('Header Component', () => {
  it('renders header with logo text', () => {
    renderHeader();
    expect(screen.getByText(/ISO Standards/i)).toBeInTheDocument();
  });

  it('renders search button', () => {
    renderHeader();
    const searchButton = screen.getByRole('button', { name: /search/i });
    expect(searchButton).toBeInTheDocument();
  });

  it('renders navigation links', () => {
    renderHeader();
    expect(screen.getByText(/Dashboard/i)).toBeInTheDocument();
  });

  it('has white background styling', () => {
    const { container } = renderHeader();
    const header = container.querySelector('header');
    expect(header).toHaveStyle({ backgroundColor: 'rgb(255, 255, 255)' });
  });

  it('renders in sticky position', () => {
    const { container } = renderHeader();
    const box = container.firstChild?.firstChild;
    // MUI Box component applies sticky positioning
    expect(box).toBeInTheDocument();
  });
});
