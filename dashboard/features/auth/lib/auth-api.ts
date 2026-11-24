
export interface LoginCredentials {
  username: string;
  password: string;
}

export interface AuthResponse {
  authenticated: boolean;
  message: string;
}

export interface AdminResponse {
  username: string;
  authenticated: boolean;
}

async function request<T>(
  endpoint: string,
  options: RequestInit = {},
): Promise<T> {
  const response = await fetch(endpoint, {
    ...options,
    credentials: "same-origin",
    cache: "no-store",
    headers: {
      "Content-Type": "application/json",
      ...options.headers,
    },
  });

  const data = await response.json().catch(() => null);

  if (!response.ok) {
    throw new Error(
      data?.detail || data?.message || "An unexpected error occurred.",
    );
  }

  return data as T;
}

export function login(
  credentials: LoginCredentials,
): Promise<AuthResponse> {
  return request<AuthResponse>("/api/auth/login", {
    method: "POST",
    body: JSON.stringify(credentials),
  });
}

export function logout(): Promise<AuthResponse> {
  return request<AuthResponse>("/api/auth/logout", {
    method: "POST",
  });
}

export function getCurrentAdmin(): Promise<AdminResponse> {
  return request<AdminResponse>("/api/auth/me", {
    method: "GET",
  });
}
