"use client";

import { useEffect, useState } from "react";
import { isAuthenticated, clearSession } from "@/lib/auth";
import { LoginForm } from "@/components/LoginForm";
import { KanbanBoard } from "@/components/KanbanBoard";

export default function Home() {
  const [authenticated, setAuthenticated] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    setAuthenticated(isAuthenticated());
    setIsLoading(false);
  }, []);

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-[var(--surface)]">
        <div className="text-center">
          <p className="text-[var(--gray-text)]">Loading...</p>
        </div>
      </div>
    );
  }

  if (!authenticated) {
    return <LoginForm onSuccess={() => setAuthenticated(true)} />;
  }

  return (
    <div>
      <button
        onClick={() => {
          clearSession();
          setAuthenticated(false);
        }}
        className="fixed top-6 right-6 bg-[var(--secondary-purple)] text-white px-4 py-2 rounded-lg text-sm font-semibold hover:opacity-90 z-50"
      >
        Logout
      </button>
      <KanbanBoard />
    </div>
  );
}

