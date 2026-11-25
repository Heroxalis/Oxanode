
import { Suspense } from "react";
import { cookies } from "next/headers";
import { redirect } from "next/navigation";
import DashboardShell from "@/components/dashboard-shell";
import { proxyAuthRequest } from "@/features/auth/lib/server-api";

function DashboardLoading() {
    return (
        <main className="flex min-h-screen items-center justify-center">
            <p className="text-sm text-[var(--ox-secondary)]">
                Verifying your session...
            </p>
        </main>
    );
}

async function AuthenticatedDashboard() {
    const cookieStore = await cookies();

    const response = await proxyAuthRequest("/api/auth/me", {
        method: "GET",
        cookie: cookieStore.toString(),
    });

    if (response.status === 401) {
        redirect("/");
    }

    if (!response.ok) {
        return (
            <main className="flex min-h-screen items-center justify-center p-6">
                <div className="max-w-md text-center">
                    <h1 className="text-xl font-semibold">
                        Unable to verify your session
                    </h1>
                    <p className="mt-3 text-sm text-[var(--ox-secondary)]">
                        The Management API is currently unavailable. Please try again.
                    </p>
                </div>
            </main>
        );
    }

    return <DashboardShell />;
}

export default function DashboardPage() {
    return (
        <Suspense fallback={<DashboardLoading />}>
            <AuthenticatedDashboard />
        </Suspense>
    );
}
