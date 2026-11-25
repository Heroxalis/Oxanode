
"use client";

import { useRouter } from "next/navigation";
import { useState, type SyntheticEvent } from "react";
import { Eye, EyeOff, LoaderCircle, LockKeyhole } from "lucide-react";
import { login } from "@/features/auth/lib/auth-api";

export default function LoginForm() {
    const router = useRouter();

    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [showPassword, setShowPassword] = useState(false);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    async function handleSubmit(event: SyntheticEvent<HTMLFormElement>) {
        event.preventDefault();

        if (loading) return;

        setError("");
        setLoading(true);

        try {
            await login({ username, password });
            router.replace("/dashboard");
        } catch (err) {
            setError(
                err instanceof Error
                    ? err.message
                    : "Unable to sign in. Please try again."
            );
        } finally {
            setLoading(false);
        }
    }

    return (
        <form onSubmit={handleSubmit} className="w-full space-y-5">
            <div className="space-y-2">
                <label
                    htmlFor="username"
                    className="block text-sm font-medium"
                >
                    Administrator username
                </label>

                <input
                    id="username"
                    name="username"
                    type="text"
                    autoComplete="username"
                    value={username}
                    onChange={(event) => setUsername(event.target.value)}
                    placeholder="Enter your username"
                    required
                    disabled={loading}
                    className="w-full rounded-xl border border-[var(--ox-border)] bg-[var(--ox-surface)] px-4 py-3 text-sm text-[var(--ox-text)] outline-none transition placeholder:text-[var(--ox-muted)] focus:border-[var(--ox-accent)] disabled:opacity-60"
                />
            </div>

            <div className="space-y-2">
                <label
                    htmlFor="password"
                    className="block text-sm font-medium"
                >
                    Password
                </label>

                <div className="relative">
                    <input
                        id="password"
                        name="password"
                        type={showPassword ? "text" : "password"}
                        autoComplete="current-password"
                        value={password}
                        onChange={(event) => setPassword(event.target.value)}
                        placeholder="Enter your password"
                        required
                        disabled={loading}
                        onKeyDown={(event) => {
                            if (event.key === "Enter") {
                                event.preventDefault();
                                event.currentTarget.form?.requestSubmit();
                            }
                        }}
                        className="w-full rounded-xl border border-[var(--ox-border)] bg-[var(--ox-surface)] px-4 py-3 pr-12 text-sm text-[var(--ox-text)] outline-none transition placeholder:text-[var(--ox-muted)] focus:border-[var(--ox-accent)] disabled:opacity-60"
                    />

                    <button
                        type="button"
                        onClick={() => setShowPassword((current) => !current)}
                        disabled={loading}
                        aria-label={showPassword ? "Hide password" : "Show password"}
                        className="absolute inset-y-0 right-0 flex items-center px-4 text-[var(--ox-muted)] transition hover:text-[var(--ox-text)]"
                    >
                        {showPassword ? (
                            <EyeOff size={18} />
                        ) : (
                            <Eye size={18} />
                        )}
                    </button>
                </div>
            </div>

            {error && (
                <div
                    role="alert"
                    className="rounded-xl border border-red-500/30 bg-red-500/10 px-4 py-3 text-sm text-red-400"
                >
                    {error}
                </div>
            )}

            <button
                type="submit"
                disabled={loading || !username.trim() || !password}
                className="flex w-full items-center justify-center gap-2 rounded-xl bg-[var(--ox-accent)] px-4 py-3 text-sm font-semibold text-white transition hover:bg-[var(--ox-accent-hover)] disabled:cursor-not-allowed disabled:opacity-60"
            >
                {loading ? (
                    <>
                        <LoaderCircle size={18} className="animate-spin" />
                        Signing in...
                    </>
                ) : (
                    <>
                        <LockKeyhole size={17} />
                        Sign in
                    </>
                )}
            </button>
        </form>
    );
}
