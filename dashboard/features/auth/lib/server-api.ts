const API_BASE_URL = process.env.OXANODE_API_URL;

interface ProxyOptions {
    method: "GET" | "POST";
    body?: string;
    cookie?: string;
}

export async function proxyAuthRequest(
    endpoint: string,
    options: ProxyOptions,
): Promise<Response> {
    if (!API_BASE_URL) {
        return Response.json(
            { detail: "Management API is not configured." },
            { status: 503 },
        );
    }

    try {
        const headers = new Headers()

        if (options.body) {
            headers.set("Content-Type", "application/json");
        }

        if (options.cookie) {
            headers.set("Cookie", options.cookie);
        }

        const upstream = await fetch(
            `${API_BASE_URL}${endpoint}`,
            {
                method: options.method,
                headers,
                body: options.body,
                cache: "no-store",
                signal: AbortSignal.timeout(10_000),
            }
        );

        const responseHeaders = new Headers();
        const contentType = upstream.headers.get("content-type");
        const retryAfter = upstream.headers.get("retry-after");

        if (contentType) {
            responseHeaders.set("Content-Type", contentType);
        }

        if (retryAfter) {
            responseHeaders.set("Retry-After", retryAfter);
        }

        for (const cookie of upstream.headers.getSetCookie()) {
            responseHeaders.append("Set-Cookie", cookie);
        }

        return new Response(upstream.body, {
            status: upstream.status,
            headers: responseHeaders,
        });
    } catch {
        return Response.json(
            { detail: "Unable to reach the Management API"},
            { status: 503 },
        );
    }
}