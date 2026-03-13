import Layout from '../components/Layout';
import '../styles.css'; // Import global styles
import type { AppProps } from 'next/app';

function MyApp({ Component, pageProps }: AppProps) {
  return (
    
      <Component {...pageProps} />
    
  );
}

export default MyApp;