import { proxyAuthRequest } from "@/features/auth/lib/server-api";

export async function GET(request: Request) {
    return proxyAuthRequest("/api/metrics/latest", {
        method: "GET",
        cookie: request.headers.get("cookie") ?? undefined,
    });
}