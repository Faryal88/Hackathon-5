/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://localhost:8000/api/:path*', // Proxy to backend
      },
      {
        source: '/health',
        destination: 'http://localhost:8000/health',
      },
      {
        source: '/webhooks/:path*',
        destination: 'http://localhost:8000/webhooks/:path*',
      },
    ]
  },
}

module.exports = nextConfig