import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

// Runtime proxy for /api/* → the FastAPI backend. Reads API_URL at request
// time so it works with Railway's runtime environment variables (the config-
// file rewrite is evaluated at build time and can't see runtime secrets).
export function middleware(request: NextRequest) {
  const apiUrl = process.env.API_URL || "http://localhost:8000";
  const url = request.nextUrl.clone();
  const target = `${apiUrl}${url.pathname}${url.search}`;
  return NextResponse.rewrite(new URL(target));
}

export const config = {
  matcher: "/api/:path*",
};
