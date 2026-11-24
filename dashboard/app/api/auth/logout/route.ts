import { proxyAuthRequest } from "@/features/auth/lib/server-api";

export const dynamic = "force-dynamic";

export async function POST(request: Request) {
  return proxyAuthRequest("/api/auth/logout", {
    method: "POST",
    cookie: request.headers.get("cookie") ?? undefined,
  });
}