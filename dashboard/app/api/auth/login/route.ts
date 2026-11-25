import { proxyAuthRequest } from "@/features/auth/lib/server-api";

export async function POST(request: Request) {
    let payload: unknown;

    try {
        payload = await request.json();
    } catch {
        return Response.json(
            { detail: "Invalid request body." },
            { status: 400 },
        );
    }

    if (
        typeof payload !== "object" ||
        payload === null ||
        !("username" in payload) ||
        !("password" in payload) ||
        typeof payload.username !== "string" ||
        typeof payload.password !== "string"
    ) {
        return Response.json(
            { detail: "Username and password are required." },
            { status: 400 },
        );
    }

    return proxyAuthRequest("/api/auth/login", {
        method: "POST",
        body: JSON.stringify(payload),
    });
}