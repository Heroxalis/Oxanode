import { Network, ShieldCheck } from "lucide-react";
import LoginForm from "./components/login-form";

export default function LoginPage() {
    return (
        <main className="ox-root flex min-h-screen items-center justify-center px-5 py-12">
            <div className="w-full max-w-md">
                <div className="mb-10 flex flex-col items-center text-center">
                    <div className="mb-5 flex h-14 w-14 items-center justify-center rounded-2xl border border-[var(--ox-accent-border)] bg-[var(--ox-accent-soft)] text-[var(--ox-accent)]">
                        <Network size={28} strokeWidth={1.8} />
                    </div>

                    <h1 className="text-2xl font-bold tracking-[0.18em] text-[var(--ox-text)]">
                        OXANODE
                    </h1>

                    <p className="mt-2 text-xs font-medium tracking-[0.2em] text-[var(--ox-muted)]">
                        BY HEROXALIS
                    </p>
                </div>

                <section className="rounded-2xl border border-[var(--ox-border)] bg-[var(--ox-surface)] p-7 shadow-2xl sm:p-9">
                    <div className="mb-7">
                        <h2 className="text-xl font-semibold text-[var(--ox-text)]">
                            Welcome back
                        </h2>

                        <p className="mt-2 text-sm leading-relaxed text-[var(--ox-secondary)]">
                            Sign in to access your private infrastructure dashboard.
                        </p>
                    </div>

                    <LoginForm />

                    <div className="mt-7 flex items-center justify-center gap-2 border-t border-[var(--ox-border)] pt-5 text-xs text-[var(--ox-muted)]">
                        <ShieldCheck size={15} />
                        <span>Private infrastructure management</span>
                    </div>
                </section>

                <p className="mt-6 text-center text-xs text-[var(--ox-muted)]">
                    One node. All your applications.
                </p>
            </div>
        </main>
    );
}