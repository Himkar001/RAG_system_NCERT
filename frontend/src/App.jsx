import { useState, useRef, useEffect } from "react";
import ReactMarkdown from "react-markdown";
import remarkMath from "remark-math";
import rehypeKatex from "rehype-katex";
import "katex/dist/katex.min.css";
import "./App.css";

function App() {
  const [chats, setChats] = useState([
    { id: 1, name: "Chat 1", messages: [] }
  ]);

  const [activeChatId, setActiveChatId] = useState(1);
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);

  const chatEndRef = useRef(null);

  const activeChat = chats.find(c => c.id === activeChatId);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [activeChat?.messages, loading]);

  const updateMessages = (newMessages) => {
    setChats(chats.map(chat =>
      chat.id === activeChatId
        ? { ...chat, messages: newMessages }
        : chat
    ));
  };

  const createNewChat = () => {
    const newId = chats.length + 1;

    const newChat = {
      id: newId,
      name: `Chat ${newId}`,
      messages: []
    };

    setChats([...chats, newChat]);
    setActiveChatId(newId);
  };

  const handleSubmit = async () => {
    if (!query.trim()) return;

    const userMessage = { role: "user", text: query };

    updateMessages([...activeChat.messages, userMessage]);
    setQuery("");
    setLoading(true);

    try {
      const res = await fetch("http://127.0.0.1:8000/ask", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ query }),
      });

      const data = await res.json();

      let botText;

      // IMAGE
      if (data.answer?.image_path) {
        botText = `![image](http://127.0.0.1:8000/${data.answer.image_path})`;
      }

      // STRUCTURED DATA (FORMULA)
      else if (typeof data.answer !== "string") {
        botText = `
### ${data.answer.name}

**Formula:** ${data.answer.formula}

**Topic:** ${data.answer.topic}

**Description:**  
${data.answer.description}
`;
      }

      // NORMAL TEXT
      else {
        botText = data.answer;
      }

      const botMessage = { role: "bot", text: botText };

      updateMessages([...activeChat.messages, userMessage, botMessage]);

    } catch (error) {
      updateMessages([
        ...activeChat.messages,
        userMessage,
        { role: "bot", text: "⚠️ Backend error" },
      ]);
    }

    setLoading(false);
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter") handleSubmit();
  };

  return (
    <div className="main">

      {/* SIDEBAR */}
      <div className="sidebar">
        <button onClick={createNewChat}>+ New Chat</button>

        {chats.map(chat => (
          <div
            key={chat.id}
            className={`chat-item ${chat.id === activeChatId ? "active" : ""}`}
            onClick={() => setActiveChatId(chat.id)}
          >
            {chat.name}
          </div>
        ))}
      </div>

      {/* CHAT AREA */}
      <div className="chat-area">

        <div className="header">
          NCERT SMART ASSISTANT
        </div>

        <div className="chat-container">
          {activeChat.messages.map((msg, index) => (
            <div key={index} className={`message-row ${msg.role}`}>
              <div className="message">
                <ReactMarkdown>{msg.text}</ReactMarkdown>
              </div>
            </div>
          ))}

          {loading && (
            <div className="message-row bot">
              <div className="message typing">Typing...</div>
            </div>
          )}

          <div ref={chatEndRef}></div>
        </div>

        {/* INPUT */}
        <div className="input-container">
          <input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask your question..."
          />
          <button onClick={handleSubmit}>Send</button>
        </div>

      </div>
    </div>
  );
}

export default App;