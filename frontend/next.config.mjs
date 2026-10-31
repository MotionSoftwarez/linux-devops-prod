const API_BASE_URL = process.env.API_PROXY_TARGET || "http://127.0.0.1:8000";

/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  async rewrites() {
    // Dev convenience: same-origin proxy to the FastAPI backend.
    // In production the frontend calls NEXT_PUBLIC_API_BASE directly.
    return [
      {
        source: "/api/:path*",
        destination: `${API_BASE_URL}/api/:path*`,
      },
    ];
  },
};

export default nextConfig;
