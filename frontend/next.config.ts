import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  async rewrites() {
    return [
      {
        source: "/api/:path*",
        destination: process.env.NODE_ENV === "development" 
          ? "http://127.0.0.1:8000/api/:path*"
          : `${process.env.BACKEND_API_URL || 'https://kashrut-api.onrender.com'}/api/:path*`,
      },
    ];
  },
};

export default nextConfig;
