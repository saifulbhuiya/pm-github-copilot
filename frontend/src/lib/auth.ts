export function validateCredentials(username: string, password: string): boolean {
  return username === "user" && password === "password";
}

export function setSession(username: string): void {
  const session = {
    username,
    token: "demo-token-" + Date.now(),
    timestamp: new Date().toISOString(),
  };
  localStorage.setItem("user-session", JSON.stringify(session));
}

export function getSession() {
  const stored = localStorage.getItem("user-session");
  if (!stored) return null;
  try {
    return JSON.parse(stored);
  } catch {
    return null;
  }
}

export function clearSession(): void {
  localStorage.removeItem("user-session");
}

export function isAuthenticated(): boolean {
  return getSession() !== null;
}
