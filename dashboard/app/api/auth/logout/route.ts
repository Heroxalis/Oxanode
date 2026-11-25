import { proxyAuthRequest } from "@/features/auth/lib/server-api";

export async function POST(request: Request) {
  return proxyAuthRequest("/api/auth/logout", {
    method: "POST",
    cookie: request.headers.get("cookie") ?? undefined,
  });
}