
"use client";

import { useState } from "react";
import {
    Activity,
    AppWindow,
    Bell,
    ChevronRight,
    Command,
    Cpu,
    Database,
    FolderOpen,
    HardDrive,
    LayoutDashboard,
    Menu,
    Moon,
    Network,
    PanelLeftClose,
    PanelLeftOpen,
    Plus,
    Server,
    Settings,
    ShieldCheck,
    Sun,
    Terminal,
    X,
    Zap,
} from "lucide-react";

type Theme = "dark" | "light";

const navigation = [
    { label: "Overview", icon: LayoutDashboard, section: "GENERAL" },
    { label: "Applications", icon: AppWindow, section: "GENERAL" },
    { label: "Terminal", icon: Terminal, section: "TOOLS" },
    { label: "Logs", icon: FolderOpen, section: "TOOLS" },
    { label: "Monitoring", icon: Activity, section: "TOOLS" },
    { label: "Storage", icon: Database, section: "TOOLS" },
    { label: "Settings", icon: Settings, section: "SYSTEM" },
];

const stats = [
    { label: "CPU Usage", value: "—", unit: "Waiting for runner", icon: Cpu },
    { label: "Memory", value: "—", unit: "Waiting for runner", icon: Activity },
    { label: "Storage", value: "—", unit: "Waiting for runner", icon: HardDrive },
    { label: "Applications", value: "0", unit: "No applications registered", icon: AppWindow },
];

export default function DashboardShell() {
    const [theme, setTheme] = useState<Theme>("dark");
    const [collapsed, setCollapsed] = useState(false);
    const [mobileOpen, setMobileOpen] = useState(false);
    const [activePage, setActivePage] = useState("Overview");

    const isDark = theme === "dark";

    function changePage(label: string) {
        setActivePage(label);
        setMobileOpen(false);
    }

    return (
        <div className="ox-root" data-theme={theme}>
            <aside
                className={`ox-sidebar ${collapsed ? "is-collapsed" : ""} ${mobileOpen ? "mobile-open" : ""
                    }`}
            >
                <div className="ox-brand">
                    <div className="ox-brand-mark">
                        <Network size={23} strokeWidth={2.1} />
                    </div>

                    {!collapsed && (
                        <div className="ox-brand-name">
                            <span>OXANODE</span>
                        </div>
                    )}

                    <button
                        className="icon-button mobile-close"
                        onClick={() => setMobileOpen(false)}
                        aria-label="Close navigation"
                    >
                        <X size={19} />
                    </button>
                </div>

                <div className="ox-sidebar-content">
                    {["GENERAL", "TOOLS", "SYSTEM"].map((section) => (
                        <div className="ox-nav-section" key={section}>
                            {!collapsed && (
                                <div className="ox-nav-heading">{section}</div>
                            )}

                            {navigation
                                .filter((item) => item.section === section)
                                .map(({ label, icon: Icon }) => (
                                    <button
                                        key={label}
                                        onClick={() => changePage(label)}
                                        className={`ox-nav-item ${activePage === label ? "active" : ""
                                            }`}
                                        title={collapsed ? label : undefined}
                                    >
                                        <Icon size={19} strokeWidth={1.9} />
                                        {!collapsed && <span>{label}</span>}
                                        {activePage === label && (
                                            <span className="ox-active-indicator" />
                                        )}
                                    </button>
                                ))}
                        </div>
                    ))}
                </div>

                <div className="ox-sidebar-bottom">
                    <div className="ox-host-card">
                        <div className="ox-host-icon">
                            <Server size={19} />
                        </div>

                        {!collapsed && (
                            <div className="ox-host-info">
                                <strong>Local Host</strong>
                                <span>Runner not connected</span>
                            </div>
                        )}

                        {!collapsed && (
                            <span className="ox-status-dot offline" />
                        )}
                    </div>

                    <button
                        className="ox-nav-item collapse-button"
                        onClick={() => setCollapsed(!collapsed)}
                        aria-label={collapsed ? "Expand sidebar" : "Collapse sidebar"}
                    >
                        {collapsed ? (
                            <PanelLeftOpen size={19} />
                        ) : (
                            <PanelLeftClose size={19} />
                        )}
                        {!collapsed && <span>Collapse sidebar</span>}
                    </button>
                </div>
            </aside>

            {mobileOpen && (
                <button
                    className="ox-mobile-overlay"
                    onClick={() => setMobileOpen(false)}
                    aria-label="Close navigation overlay"
                />
            )}

            <main className="ox-main">
                <header className="ox-topbar">
                    <div className="ox-topbar-left">
                        <button
                            className="icon-button mobile-menu"
                            onClick={() => setMobileOpen(true)}
                            aria-label="Open navigation"
                        >
                            <Menu size={21} />
                        </button>

                        <div className="ox-breadcrumb">
                            <span>Oxanode</span>
                            <ChevronRight size={15} />
                            <strong>{activePage}</strong>
                        </div>
                    </div>

                    <div className="ox-topbar-actions">
                        <div className="ox-connection">
                            <span className="ox-status-dot offline" />
                            <span>Disconnected</span>
                        </div>

                        <button
                            className="icon-button"
                            onClick={() => setTheme(isDark ? "light" : "dark")}
                            title={`Switch to ${isDark ? "light" : "dark"} theme`}
                            aria-label="Toggle color theme"
                        >
                            {isDark ? <Sun size={19} /> : <Moon size={19} />}
                        </button>

                        <button
                            className="icon-button notification-button"
                            aria-label="Notifications"
                        >
                            <Bell size={19} />
                        </button>
                    </div>
                </header>

                <div className="ox-page-content">
                    {activePage === "Overview" ? (
                        <>
                            <div className="ox-page-heading">
                                <div>
                                    <div className="ox-eyebrow">
                                        <Zap size={13} />
                                        INFRASTRUCTURE
                                    </div>
                                    <h1>Overview</h1>
                                    <p>
                                        Monitor and manage your applications and host system.
                                    </p>
                                </div>

                                <button
                                    className="ox-primary-button"
                                    onClick={() => changePage("Applications")}
                                >
                                    <Plus size={17} />
                                    Register application
                                </button>
                            </div>

                            <div className="ox-notice">
                                <div className="ox-notice-icon">
                                    <ShieldCheck size={20} />
                                </div>
                                <div className="ox-notice-content">
                                    <strong>Waiting for Oxanode Runner</strong>
                                    <p>
                                        The dashboard is ready, but no host runner is connected.
                                        System metrics and application information will appear
                                        once a runner is configured.
                                    </p>
                                </div>
                                <span className="ox-notice-badge">NOT CONNECTED</span>
                            </div>

                            <section className="ox-section">
                                <div className="ox-section-heading">
                                    <div>
                                        <h2>System resources</h2>
                                        <p>
                                            Live resource utilization from your host machine.
                                        </p>
                                    </div>
                                    <span className="ox-muted-label">NO DATA</span>
                                </div>

                                <div className="ox-stats-grid">
                                    {stats.map(({ label, value, unit, icon: Icon }) => (
                                        <article className="ox-stat-card" key={label}>
                                            <div className="ox-stat-top">
                                                <div className="ox-stat-icon">
                                                    <Icon size={19} />
                                                </div>
                                                <span className="ox-stat-indicator" />
                                            </div>
                                            <div className="ox-stat-value">{value}</div>
                                            <div className="ox-stat-label">{label}</div>
                                            <div className="ox-stat-description">{unit}</div>
                                        </article>
                                    ))}
                                </div>
                            </section>

                            <div className="ox-content-grid">
                                <section className="ox-panel">
                                    <div className="ox-panel-heading">
                                        <div>
                                            <h2>Registered applications</h2>
                                            <p>
                                                Applications managed by this Oxanode instance.
                                            </p>
                                        </div>
                                        <button
                                            className="ox-text-button"
                                            onClick={() => changePage("Applications")}
                                        >
                                            View all <ChevronRight size={15} />
                                        </button>
                                    </div>

                                    <div className="ox-empty-state">
                                        <div className="ox-empty-icon">
                                            <AppWindow size={25} />
                                        </div>
                                        <strong>No applications yet</strong>
                                        <p>
                                            Register a project directory to start managing
                                            applications with Oxanode.
                                        </p>
                                        <button
                                            className="ox-secondary-button"
                                            onClick={() => changePage("Applications")}
                                        >
                                            <Plus size={16} />
                                            Add your first application
                                        </button>
                                    </div>
                                </section>

                                <section className="ox-panel ox-activity-panel">
                                    <div className="ox-panel-heading">
                                        <div>
                                            <h2>System status</h2>
                                            <p>
                                                Current infrastructure connection status.
                                            </p>
                                        </div>
                                    </div>

                                    <div className="ox-status-list">
                                        <div className="ox-status-row">
                                            <div className="ox-status-row-icon">
                                                <Server size={17} />
                                            </div>
                                            <div className="ox-status-row-info">
                                                <strong>Host runner</strong>
                                                <span>Not connected</span>
                                            </div>
                                            <span className="ox-status-dot offline" />
                                        </div>

                                        <div className="ox-status-row">
                                            <div className="ox-status-row-icon">
                                                <Database size={17} />
                                            </div>
                                            <div className="ox-status-row-info">
                                                <strong>Local database</strong>
                                                <span>Not initialized</span>
                                            </div>
                                            <span className="ox-status-dot pending" />
                                        </div>

                                        <div className="ox-status-row">
                                            <div className="ox-status-row-icon">
                                                <Network size={17} />
                                            </div>
                                            <div className="ox-status-row-info">
                                                <strong>Management API</strong>
                                                <span>Not configured</span>
                                            </div>
                                            <span className="ox-status-dot pending" />
                                        </div>
                                    </div>
                                </section>
                            </div>

                            <footer className="ox-footer">
                                <span>
                                    OXANODE{" "}
                                    <span className="ox-footer-version">v0.1.0-dev</span>
                                </span>
                                <span>Developed by Heroxalis</span>
                            </footer>
                        </>
                    ) : (
                        <section className="ox-placeholder-page">
                            <div className="ox-placeholder-icon">
                                <Command size={28} />
                            </div>
                            <h1>{activePage}</h1>
                            <p>
                                This section is part of the Oxanode roadmap. We're building it
                                one component at a time.
                            </p>
                            <span className="ox-placeholder-badge">
                                UNDER DEVELOPMENT
                            </span>
                        </section>
                    )}
                </div>
            </main>
        </div>
    );
}