/** @type {import('next').NextConfig} */
const nextConfig = {
  // Disable CSS processing to avoid PostCSS issues
  experimental: {
    cssChunking: false,
  },
};

export default nextConfig;
