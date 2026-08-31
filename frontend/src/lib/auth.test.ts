import { describe, it, expect, beforeEach, afterEach } from "vitest";
import {
  validateCredentials,
  setSession,
  getSession,
  clearSession,
  isAuthenticated,
} from "@/lib/auth";

describe("auth utilities", () => {
  afterEach(() => {
    clearSession();
  });

  it("validateCredentials accepts correct credentials", () => {
    expect(validateCredentials("user", "password")).toBe(true);
  });

  it("validateCredentials rejects wrong username", () => {
    expect(validateCredentials("admin", "password")).toBe(false);
  });

  it("validateCredentials rejects wrong password", () => {
    expect(validateCredentials("user", "wrong")).toBe(false);
  });

  it("setSession stores session in localStorage", () => {
    setSession("user");
    const session = getSession();
    expect(session).not.toBeNull();
    expect(session?.username).toBe("user");
  });

  it("isAuthenticated returns true after setSession", () => {
    setSession("user");
    expect(isAuthenticated()).toBe(true);
  });

  it("isAuthenticated returns false after clearSession", () => {
    setSession("user");
    clearSession();
    expect(isAuthenticated()).toBe(false);
  });

  it("isAuthenticated returns false with no session", () => {
    expect(isAuthenticated()).toBe(false);
  });
});
