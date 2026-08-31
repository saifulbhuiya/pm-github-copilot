"use client";

import { useState, useRef, useEffect } from "react";

interface ChatMessage {
  role: "user" | "assistant";
  content: string;
}

export const AIChatSidebar = ({ onBoardChange }: { onBoardChange: () => void }) => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userMessage = input;
    setInput("");
    setMessages((prev) => [...prev, { role: "user", content: userMessage }]);
    setLoading(true);
    setError(null);

    try {
      const response = await fetch("/api/ai/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userMessage }),
      });

      if (!response.ok) throw new Error("Failed to get AI response");

      const data = await response.json();
      
      let assistantMessage = data.summary || (data.action && data.action !== "error" ? `I ${data.action}d ${data.cards?.length || 0} card(s).` : data.message || "I've processed your request");

      setMessages((prev) => [...prev, { role: "assistant", content: assistantMessage }]);
      onBoardChange();
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : "Failed to process request";
      setError(errorMessage);
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: `Error: ${errorMessage}` },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex h-screen w-80 flex-col border-l border-[var(--stroke)] bg-white shadow-lg">
      <div className="border-b border-[var(--stroke)] px-6 py-4">
        <h2 className="text-lg font-semibold text-[var(--navy-dark)]">AI Assistant</h2>
        <p className="mt-1 text-xs text-[var(--gray-text)]">Manage your cards with AI</p>
      </div>

      <div className="flex-1 overflow-y-auto p-4">
        <div className="space-y-4">
          {messages.length === 0 && (
            <div className="text-center text-sm text-[var(--gray-text)]">
              <p className="mb-2">Chat with AI to manage your Kanban board</p>
              <p className="text-xs">Try: "Create a bug fix card in backlog" or "Move task X to done"</p>
            </div>
          )}
          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
            >
              <div
                className={`max-w-xs rounded-lg px-4 py-2 text-sm ${
                  msg.role === "user"
                    ? "bg-[var(--primary-blue)] text-white"
                    : "bg-[var(--surface)] text-[var(--navy-dark)]"
                }`}
              >
                {msg.content}
              </div>
            </div>
          ))}
          {loading && (
            <div className="flex justify-start">
              <div className="bg-[var(--surface)] rounded-lg px-4 py-2">
                <div className="flex gap-1">
                  <div className="h-2 w-2 rounded-full bg-[var(--gray-text)] animate-bounce" />
                  <div
                    className="h-2 w-2 rounded-full bg-[var(--gray-text)] animate-bounce"
                    style={{ animationDelay: "0.2s" }}
                  />
                  <div
                    className="h-2 w-2 rounded-full bg-[var(--gray-text)] animate-bounce"
                    style={{ animationDelay: "0.4s" }}
                  />
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
      </div>

      {error && (
        <div className="border-t border-red-200 bg-red-50 px-4 py-2 text-xs text-red-700">
          {error}
        </div>
      )}

      <form
        onSubmit={handleSendMessage}
        className="border-t border-[var(--stroke)] p-4"
      >
        <div className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask me anything..."
            disabled={loading}
            className="flex-1 rounded-lg border border-[var(--stroke)] px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-[var(--primary-blue)] disabled:opacity-50"
          />
          <button
            type="submit"
            disabled={loading || !input.trim()}
            className="rounded-lg bg-[var(--secondary-purple)] px-4 py-2 text-sm font-semibold text-white hover:bg-opacity-90 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Send
          </button>
        </div>
      </form>
    </div>
  );
};
