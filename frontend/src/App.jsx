import { useState, useRef, useEffect, useCallback } from "react";
import ReactMarkdown from "react-markdown";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";
import "katex/dist/katex.min.css";
import "./App.css";

/* ─────────────────────────────────────────
   Helpers
───────────────────────────────────────── */
function formatTime(date) {
  return date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
}

function deriveTitle(text) {
  const clean = text.replace(/[*_#`]/g, "").trim();
  return clean.length > 34 ? clean.slice(0, 34).trimEnd() + "…" : clean;
}

const SUBJECT_CHIPS = [
  { icon: "⚡", label: "What is Newton's Second Law?", subject: "Physics" },
  { icon: "🧪", label: "Explain atomic structure", subject: "Chemistry" },
  { icon: "📐", label: "Derive the quadratic formula", subject: "Maths" },
  { icon: "🧬", label: "What is cell division (mitosis)?", subject: "Biology" },
  { icon: "🌍", label: "Explain the water cycle", subject: "Geography" },
  { icon: "⚗️", label: "What are periodic trends?", subject: "Chemistry" },
];

/* ─────────────────────────────────────────
   Icons
───────────────────────────────────────── */
const IconPlus = () => (
  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
    <line x1="12" y1="5" x2="12" y2="19" /><line x1="5" y1="12" x2="19" y2="12" />
  </svg>
);

const IconTrash = () => (
  <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <polyline points="3 6 5 6 21 6" /><path d="M19 6l-1 14H6L5 6" /><path d="M10 11v6" /><path d="M14 11v6" /><path d="M9 6V4h6v2" />
  </svg>
);

const IconMenu = () => (
  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <line x1="3" y1="6" x2="21" y2="6" /><line x1="3" y1="12" x2="21" y2="12" /><line x1="3" y1="18" x2="21" y2="18" />
  </svg>
);

const IconSend = () => (
  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
    <line x1="22" y1="2" x2="11" y2="13" /><polygon points="22 2 15 22 11 13 2 9 22 2" />
  </svg>
);

const IconCopy = () => (
  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <rect x="9" y="9" width="13" height="13" rx="2" /><path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1" />
  </svg>
);

const IconCheck = () => (
  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
    <polyline points="20 6 9 17 4 12" />
  </svg>
);

const IconChat = () => (
  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
    <path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z" />
  </svg>
);

/* ─────────────────────────────────────────
   CopyButton
───────────────────────────────────────── */
function CopyButton({ text }) {
  const [copied, setCopied] = useState(false);

  const handleCopy = async (e) => {
    e.stopPropagation();
    await navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <button
      className={`copy-btn ${copied ? "copied" : ""}`}
      onClick={handleCopy}
      title="Copy to clipboard"
    >
      {copied ? <IconCheck /> : <IconCopy />}
      {copied ? "Copied!" : "Copy"}
    </button>
  );
}

/* ─────────────────────────────────────────
   Main App
───────────────────────────────────────── */
function App() {
  const [chats, setChats] = useState([
    { id: 1, name: "New Chat", messages: [] },
  ]);
  const [activeChatId, setActiveChatId] = useState(1);
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [isMobile, setIsMobile] = useState(false);

  const chatEndRef = useRef(null);
  const textareaRef = useRef(null);
  const nextId = useRef(2);

  /* Detect mobile */
  useEffect(() => {
    const check = () => {
      const mobile = window.innerWidth < 640;
      setIsMobile(mobile);
      if (mobile) setSidebarOpen(false);
    };
    check();
    window.addEventListener("resize", check);
    return () => window.removeEventListener("resize", check);
  }, []);

  /* Scroll to bottom */
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [chats, loading]);

  /* Auto-grow textarea */
  useEffect(() => {
    const ta = textareaRef.current;
    if (!ta) return;
    ta.style.height = "auto";
    ta.style.height = Math.min(ta.scrollHeight, 160) + "px";
  }, [query]);

  const activeChat = chats.find((c) => c.id === activeChatId);

  const updateMessages = useCallback(
    (newMessages) => {
      setChats((prev) =>
        prev.map((chat) =>
          chat.id === activeChatId
            ? {
                ...chat,
                messages: newMessages,
                // Auto-title from first user message
                name:
                  chat.name === "New Chat" && newMessages.length > 0
                    ? deriveTitle(newMessages[0].text)
                    : chat.name,
              }
            : chat
        )
      );
    },
    [activeChatId]
  );

  const createNewChat = () => {
    const id = nextId.current++;
    setChats((prev) => [...prev, { id, name: "New Chat", messages: [] }]);
    setActiveChatId(id);
    if (isMobile) setSidebarOpen(false);
  };

  const deleteChat = (e, id) => {
    e.stopPropagation();
    setChats((prev) => {
      const filtered = prev.filter((c) => c.id !== id);
      if (filtered.length === 0) {
        const fresh = { id: nextId.current++, name: "New Chat", messages: [] };
        setActiveChatId(fresh.id);
        return [fresh];
      }
      if (id === activeChatId) {
        setActiveChatId(filtered[filtered.length - 1].id);
      }
      return filtered;
    });
  };

  const handleSubmit = async () => {
    if (!query.trim() || loading) return;

    const now = new Date();
    const userMessage = { role: "user", text: query.trim(), time: formatTime(now) };
    const currentMessages = activeChat.messages;

    updateMessages([...currentMessages, userMessage]);
    setQuery("");
    setLoading(true);

    try {
      const res = await fetch("http://127.0.0.1:8000/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: userMessage.text }),
      });

      const data = await res.json();
      let botText;

      if (data.answer?.image_path) {
        botText = `![image](http://127.0.0.1:8000/${data.answer.image_path})`;
      } else if (typeof data.answer !== "string") {
        botText = `### ${data.answer.name}\n\n**Formula:** $${data.answer.formula}$\n\n**Topic:** ${data.answer.topic}\n\n**Description:**\n${data.answer.description}`;
      } else {
        botText = data.answer;
      }

      const botMessage = {
        role: "bot",
        text: botText,
        time: formatTime(new Date()),
      };
      updateMessages([...currentMessages, userMessage, botMessage]);
    } catch {
      updateMessages([
        ...currentMessages,
        userMessage,
        {
          role: "bot",
          text: "⚠️ **Could not reach the backend.** Please make sure the API server is running on `http://127.0.0.1:8000`.",
          time: formatTime(new Date()),
        },
      ]);
    }

    setLoading(false);
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  const handleChipClick = (chip) => {
    setQuery(chip.label);
    textareaRef.current?.focus();
    if (isMobile) setSidebarOpen(false);
  };

  /* ── Render ── */
  return (
    <div className="app-shell">
      {/* ── Mobile overlay ── */}
      {isMobile && sidebarOpen && (
        <div className="sidebar-overlay" onClick={() => setSidebarOpen(false)} />
      )}

      {/* ══════════ SIDEBAR ══════════ */}
      <aside className={`sidebar ${!sidebarOpen ? "collapsed" : ""} ${isMobile && sidebarOpen ? "open" : ""}`}>
        {/* Brand */}
        <div className="sidebar-brand">
          <div className="sidebar-brand-icon">🎓</div>
          <span className="sidebar-brand-name">Parishiksha</span>
        </div>

        {/* New Chat */}
        <button className="new-chat-btn" onClick={createNewChat} id="new-chat-btn">
          <IconPlus />
          New Chat
        </button>

        {/* Chat list */}
        <div className="chat-list-label">Conversations</div>
        <div className="chat-list" role="list">
          {chats.map((chat) => (
            <div
              key={chat.id}
              className={`chat-item ${chat.id === activeChatId ? "active" : ""}`}
              onClick={() => {
                setActiveChatId(chat.id);
                if (isMobile) setSidebarOpen(false);
              }}
              role="listitem"
              title={chat.name}
            >
              <span className="chat-item-icon"><IconChat /></span>
              <span className="chat-item-name">{chat.name}</span>
              <button
                className="chat-delete-btn"
                onClick={(e) => deleteChat(e, chat.id)}
                title="Delete chat"
                aria-label={`Delete ${chat.name}`}
              >
                <IconTrash />
              </button>
            </div>
          ))}
        </div>

        {/* Footer */}
        <div className="sidebar-footer">
          <div className="sidebar-footer-avatar">👤</div>
          <div className="sidebar-footer-info">
            <div className="sidebar-footer-name">Student</div>
            <div className="sidebar-footer-status">
              <span className="status-dot" />
              Connected to API
            </div>
          </div>
        </div>
      </aside>

      {/* ══════════ MAIN CHAT ══════════ */}
      <main className="chat-area">
        {/* Header */}
        <header className="chat-header">
          <button
            className="header-toggle-btn"
            onClick={() => setSidebarOpen((v) => !v)}
            aria-label="Toggle sidebar"
            id="sidebar-toggle-btn"
          >
            <IconMenu />
          </button>

          <div className="header-title">
            <div className="header-chat-name">{activeChat?.name ?? "Chat"}</div>
            <div className="header-subtitle">NCERT AI Assistant</div>
          </div>

          <div className="header-badge">
            <span className="status-dot" />
            Online
          </div>
        </header>

        {/* Messages */}
        <div className="messages-area">
          <div className="messages-inner">
            {activeChat?.messages.length === 0 && !loading ? (
              /* ── Welcome state ── */
              <div className="welcome-state">
                <div className="welcome-logo">🎓</div>
                <h1 className="welcome-heading">Ask Parishiksha</h1>
                <p className="welcome-sub">
                  Your intelligent NCERT study companion. Ask any question from
                  Physics, Chemistry, Maths, Biology, and more.
                </p>
                <div className="welcome-chips-label">Try asking about</div>
                <div className="welcome-chips">
                  {SUBJECT_CHIPS.map((chip, i) => (
                    <button
                      key={i}
                      className="welcome-chip"
                      onClick={() => handleChipClick(chip)}
                      id={`chip-${chip.subject.toLowerCase()}-${i}`}
                    >
                      <span className="welcome-chip-icon">{chip.icon}</span>
                      {chip.label}
                    </button>
                  ))}
                </div>
              </div>
            ) : (
              /* ── Message list ── */
              <>
                {activeChat?.messages.map((msg, index) => (
                  <div
                    key={index}
                    className={`message-row ${msg.role}`}
                    id={`msg-${index}`}
                  >
                    {/* Avatar */}
                    <div className={`msg-avatar ${msg.role}`}>
                      {msg.role === "bot" ? "🎓" : "👤"}
                    </div>

                    {/* Bubble + meta */}
                    <div className="msg-bubble-wrap">
                      <div className="msg-bubble">
                        <ReactMarkdown
                          remarkPlugins={[remarkMath]}
                          rehypePlugins={[rehypeKatex]}
                        >
                          {msg.text}
                        </ReactMarkdown>
                      </div>
                      <div className="msg-meta">
                        <span className="msg-time">{msg.time}</span>
                        {msg.role === "bot" && <CopyButton text={msg.text} />}
                      </div>
                    </div>
                  </div>
                ))}

                {/* Typing indicator */}
                {loading && (
                  <div className="message-row bot" id="typing-indicator">
                    <div className="msg-avatar bot">🎓</div>
                    <div className="typing-bubble">
                      <div className="typing-dot" />
                      <div className="typing-dot" />
                      <div className="typing-dot" />
                    </div>
                  </div>
                )}
              </>
            )}

            <div ref={chatEndRef} />
          </div>
        </div>

        {/* Input */}
        <div className="input-area">
          <div className="input-inner">
            <div className="input-box">
              <textarea
                ref={textareaRef}
                className="input-textarea"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Ask anything from your NCERT syllabus…"
                rows={1}
                id="chat-input"
                aria-label="Chat input"
                disabled={loading}
              />
              <button
                className="send-btn"
                onClick={handleSubmit}
                disabled={!query.trim() || loading}
                id="send-btn"
                aria-label="Send message"
              >
                <IconSend />
              </button>
            </div>
            <p className="input-hint">
              Press <kbd>Enter</kbd> to send · <kbd>Shift+Enter</kbd> for new line
            </p>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;