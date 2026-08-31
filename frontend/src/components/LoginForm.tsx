"use client";

import { useState } from "react";
import { validateCredentials, setSession } from "@/lib/auth";

interface LoginFormProps {
  onSuccess: () => void;
}

export const LoginForm = ({ onSuccess }: LoginFormProps) => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setIsLoading(true);

    if (validateCredentials(username, password)) {
      setSession(username);
      setUsername("");
      setPassword("");
      onSuccess();
    } else {
      setError("Invalid username or password");
    }

    setIsLoading(false);
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-[var(--surface)]">
      <div className="max-w-md w-full">
        <div className="bg-white rounded-3xl border border-[var(--stroke)] shadow-[var(--shadow)] p-8">
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold text-[var(--navy-dark)] mb-2">
              Kanban Studio
            </h1>
            <p className="text-sm text-[var(--gray-text)]">Sign in to continue</p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-sm font-semibold text-[var(--navy-dark)] mb-2">
                Username
              </label>
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="user"
                className="w-full px-4 py-3 rounded-lg border border-[var(--stroke)] focus:outline-none focus:ring-2 focus:ring-[var(--primary-blue)]"
                disabled={isLoading}
              />
            </div>

            <div>
              <label className="block text-sm font-semibold text-[var(--navy-dark)] mb-2">
                Password
              </label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="password"
                className="w-full px-4 py-3 rounded-lg border border-[var(--stroke)] focus:outline-none focus:ring-2 focus:ring-[var(--primary-blue)]"
                disabled={isLoading}
              />
            </div>

            {error && (
              <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
                <p className="text-sm text-red-700">{error}</p>
              </div>
            )}

            <button
              type="submit"
              disabled={isLoading}
              className="w-full bg-[var(--secondary-purple)] text-white font-semibold py-3 rounded-lg hover:opacity-90 disabled:opacity-50 transition-opacity"
            >
              {isLoading ? "Signing in..." : "Sign In"}
            </button>
          </form>

          <div className="mt-6 pt-6 border-t border-[var(--stroke)]">
            <p className="text-xs text-[var(--gray-text)] text-center">
              Demo credentials:<br />
              Username: <code className="font-mono">user</code><br />
              Password: <code className="font-mono">password</code>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};
