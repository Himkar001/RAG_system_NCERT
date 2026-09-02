import React, { useState, useEffect, useRef } from 'react';
import './App.css';
import StreamingMessage from './components/StreamingMessage';
import IntentBadge from './components/IntentBadge';
import SourceCard from './components/SourceCard';
import { DiagramGallery } from './components/DiagramCard';

const API_BASE = import.meta.env.VITE_API_URL || '';

const SUGGESTIONS = [
  // Theory (2)
  { icon: '🧠', text: "What is Newton's first law of motion?",        type: 'theory'    },
  { icon: '⚖️', text: 'What is the difference between mass and weight?', type: 'theory' },
  // Formula (2)
  { icon: '📐', text: 'What is the formula for gravitational force?', type: 'equation'  },
  { icon: '∑',  text: 'Write and explain F = ma',                     type: 'equation'  },
  // Numerical (1)
  { icon: '🔢', text: 'A car of mass 1000 kg accelerates at 2 m/s². Find the force.', type: 'numerical' },
  // Diagram (1)
  { icon: '🖼️', text: 'Show me the diagram of a plant cell',          type: 'image'     },
];

function GraduationCapIcon() {
  return (
    <svg viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg" className="grad-cap-svg">
      <rect width="64" height="64" rx="16" fill="#7c3aed" />
      <path d="M32 18L10 28L32 38L54 28L32 18Z" fill="white" />
      <path d="M18 33V44C18 44 24 50 32 50C40 50 46 44 46 44V33L32 40L18 33Z" fill="white" fillOpacity="0.85" />
      <rect x="51" y="28" width="3" height="12" rx="1.5" fill="white" fillOpacity="0.7" />
      <circle cx="52.5" cy="41.5" r="2.5" fill="white" fillOpacity="0.7" />
    </svg>
  );
}

function ChatBubbleIcon() {
  return (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
    </svg>
  );
}

function SendIcon() {
  return (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
      <line x1="22" y1="2" x2="11" y2="13" />
      <polygon points="22 2 15 22 11 13 2 9 22 2" />
    </svg>
  );
}

export default function App() {
  const [sessions, setSessions] = useState([]);
  const [activeSessionId, setActiveSessionId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isStreaming, setIsStreaming] = useState(false);
  const [streamingContent, setStreamingContent] = useState('');
  const [streamingIntent, setStreamingIntent] = useState('');
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [isConnected, setIsConnected] = useState(false);

  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  // Check backend connection (initial + polling every 4s)
  useEffect(() => {
    const checkHealth = () => {
      fetch(`${API_BASE}/health`)
        .then(r => r.ok ? setIsConnected(true) : setIsConnected(false))
        .catch(() => setIsConnected(false));
    };

    checkHealth();
    const interval = setInterval(checkHealth, 4000);
    return () => clearInterval(interval);
  }, []);

  // Load sessions on mount
  useEffect(() => {
    const saved = JSON.parse(localStorage.getItem('ncert_sessions') || '[]');
    setSessions(saved);
    if (saved.length > 0) {
      loadSession(saved[0].id);
    } else {
      createNewSession();
    }
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, streamingContent]);

  const saveSessions = (list) => {
    setSessions(list);
    localStorage.setItem('ncert_sessions', JSON.stringify(list));
  };

  const saveMessages = (sid, msgs) => {
    localStorage.setItem(`ncert_session_${sid}_messages`, JSON.stringify(msgs));
  };

  const loadSession = (sid) => {
    const msgs = JSON.parse(localStorage.getItem(`ncert_session_${sid}_messages`) || '[]');
    setActiveSessionId(sid);
    setMessages(msgs);
  };

  const createNewSession = () => {
    const id = crypto.randomUUID ? crypto.randomUUID() : Math.random().toString(36).slice(2);
    const session = { id, title: 'New Chat', timestamp: Date.now(), messageCount: 0 };
    const updated = [session, ...sessions];
    saveSessions(updated);
    setActiveSessionId(id);
    setMessages([]);
  };

  const deleteSession = (sid, e) => {
    e.stopPropagation();
    const updated = sessions.filter(s => s.id !== sid);
    saveSessions(updated);
    localStorage.removeItem(`ncert_session_${sid}_messages`);
    if (activeSessionId === sid) {
      if (updated.length > 0) loadSession(updated[0].id);
      else createNewSession();
    }
  };

  const updateSessionTitle = (sid, firstMsg, count) => {
    setSessions(prev => {
      const updated = prev.map(s =>
        s.id === sid
          ? { ...s, title: firstMsg.slice(0, 32) || 'New Chat', messageCount: count }
          : s
      );
      localStorage.setItem('ncert_sessions', JSON.stringify(updated));
      return updated;
    });
  };

  const finalizeMessage = (content, sources, intent, imageResults, prevMessages) => {
    const msg = {
      role: 'assistant', content, sources, intent,
      image_results: imageResults || [], timestamp: Date.now()
    };
    const updated = [...prevMessages, msg];
    setMessages(updated);
    saveMessages(activeSessionId, updated);
    const firstUser = updated.find(m => m.role === 'user');
    updateSessionTitle(activeSessionId, firstUser?.content || 'New Chat', updated.length);
    setIsStreaming(false);
    setStreamingContent('');
    setStreamingIntent('');
  };

  const handleSubmit = async (e, overrideQuery) => {
    e?.preventDefault();
    const query = overrideQuery || inputValue.trim();
    if (!query || isStreaming) return;
    setInputValue('');

    const userMsg = { role: 'user', content: query, timestamp: Date.now() };
    const prev = [...messages, userMsg];
    setMessages(prev);
    saveMessages(activeSessionId, prev);

    setIsStreaming(true);
    setStreamingContent('');
    setStreamingIntent('');

    try {
      const res = await fetch(`${API_BASE}/ask/stream`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query, session_id: activeSessionId }),
      });
      if (!res.ok) throw new Error('stream failed');

      const reader = res.body.getReader();
      const dec = new TextDecoder();
      let full = '', sources = [], intent = '', imgs = [];

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;
        const chunk = dec.decode(value, { stream: true });
        for (const line of chunk.split('\n')) {
          if (!line.startsWith('data: ')) continue;
          const raw = line.slice(6).trim();
          if (!raw) continue;
          try {
            const d = JSON.parse(raw);
            if (d.token) { full += d.token; setStreamingContent(full); }
            if (d.done) {
              sources = d.sources || [];
              intent = d.intent || '';
              imgs = d.image_results || [];
              setStreamingIntent(intent);
            }
          } catch { /* ignore */ }
        }
      }
      finalizeMessage(full, sources, intent, imgs, prev);

    } catch {
      // Fallback to batch
      try {
        const res = await fetch(`${API_BASE}/ask`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ query, session_id: activeSessionId }),
        });
        const d = await res.json();
        finalizeMessage(d.answer, d.sources || [], d.intent || '', d.image_results || [], prev);
      } catch {
        finalizeMessage('Could not connect to the backend. Please make sure the server is running.', [], 'error', [], prev);
      }
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const handleSuggestion = (text) => {
    handleSubmit(null, text);
  };

  const showWelcome = messages.length === 0 && !isStreaming;

  return (
    <div className="app">
      {/* ── Sidebar ── */}
      <aside className={`sidebar ${sidebarOpen ? '' : 'collapsed'}`}>
        <div className="sidebar-brand">
          <div className="brand-icon"><GraduationCapIcon /></div>
          <span className="brand-name">Parishiksha</span>
        </div>

        <button className="new-chat-btn" onClick={createNewSession}>
          <span className="new-chat-plus">+</span> New Chat
        </button>

        <div className="conversations-label">Conversations</div>

        <nav className="conversations-list">
          {sessions.map(s => (
            <div
              key={s.id}
              className={`conv-item ${s.id === activeSessionId ? 'active' : ''}`}
              onClick={() => loadSession(s.id)}
            >
              <span className="conv-icon"><ChatBubbleIcon /></span>
              <span className="conv-title">{s.title}</span>
              <button
                className="conv-delete"
                onClick={(e) => deleteSession(s.id, e)}
                title="Delete"
              >×</button>
            </div>
          ))}
        </nav>

        <div className="sidebar-footer">
          <div className="user-avatar">S</div>
          <div className="user-info">
            <span className="user-name">Student</span>
            <span className={`user-status ${isConnected ? 'connected' : 'disconnected'}`}>
              <span className="status-dot" />
              {isConnected ? 'Connected to API' : 'Not connected'}
            </span>
          </div>
        </div>
      </aside>

      {/* ── Main ── */}
      <main className="main">
        {/* Header */}
        <header className="chat-header">
          <div className="header-left">
            <button className="hamburger" onClick={() => setSidebarOpen(o => !o)}>
              <span /><span /><span />
            </button>
            <div className="header-titles">
              <span className="header-chat-name">
                {sessions.find(s => s.id === activeSessionId)?.title || 'New Chat'}
              </span>
              <span className="header-subtitle">NCERT AI Assistant</span>
            </div>
          </div>
          <div className={`online-badge ${isConnected ? 'online' : 'offline'}`}>
            <span className="online-dot" />
            {isConnected ? 'Online' : 'Offline'}
          </div>
        </header>

        {/* Messages / Welcome */}
        <div className="messages-area">
          {showWelcome ? (
            <div className="welcome-screen">
              <div className="welcome-logo"><GraduationCapIcon /></div>
              <h1 className="welcome-title">Ask Parishiksha</h1>
              <p className="welcome-subtitle">
                Your intelligent NCERT study companion. Ask any<br />
                question from Physics, Chemistry, Maths, Biology, and more.
              </p>
              <div className="suggestions-label">TRY ASKING ABOUT</div>
              <div className="suggestions-grid">
                {SUGGESTIONS.map((s, i) => (
                  <button
                    key={i}
                    className="suggestion-chip"
                    onClick={() => handleSuggestion(s.text)}
                  >
                    <span className="chip-icon">{s.icon}</span>
                    <span className="chip-text">{s.text}</span>
                  </button>
                ))}
              </div>
            </div>
          ) : (
            <div className="messages-list">
              {messages.map((msg, idx) => (
                <div key={idx} className={`message-row ${msg.role}`}>
                  {msg.role === 'assistant' && (
                    <div className="assistant-avatar"><GraduationCapIcon /></div>
                  )}
                  <div className="message-bubble">
                    {msg.role === 'assistant' && msg.intent && (
                      <IntentBadge intent={msg.intent} />
                    )}
                    {msg.role === 'assistant' ? (
                      <StreamingMessage content={msg.content} isStreaming={false} />
                    ) : (
                      <span className="user-text">{msg.content}</span>
                    )}
                    {msg.role === 'assistant' && msg.sources?.length > 0 && (
                      <div className="sources-block">
                        <div className="sources-label">Sources</div>
                        {msg.sources.map((src, i) => (
                          <SourceCard key={i} source={src} />
                        ))}
                      </div>
                    )}
                    {msg.role === 'assistant' && msg.image_results?.length > 0 && (
                      <DiagramGallery images={msg.image_results} />
                    )}
                    <span className="msg-time">
                      {new Date(msg.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </span>
                  </div>
                </div>
              ))}

              {isStreaming && (
                <div className="message-row assistant streaming-row">
                  <div className="assistant-avatar"><GraduationCapIcon /></div>
                  <div className="message-bubble">
                    {streamingIntent && <IntentBadge intent={streamingIntent} />}
                    <StreamingMessage content={streamingContent} isStreaming={true} />
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>
          )}
        </div>

        {/* Input */}
        <div className="input-area">
          <form className="input-form" onSubmit={handleSubmit}>
            <textarea
              ref={inputRef}
              className="input-box"
              value={inputValue}
              onChange={e => setInputValue(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask anything from your NCERT syllabus..."
              disabled={isStreaming}
              rows={1}
            />
            <button
              type="submit"
              className="send-btn"
              disabled={!inputValue.trim() || isStreaming}
            >
              <SendIcon />
            </button>
          </form>
          <div className="input-hint">
            Press <kbd>Enter</kbd> to send · <kbd>Shift+Enter</kbd> for new line
          </div>
        </div>
      </main>
    </div>
  );
}