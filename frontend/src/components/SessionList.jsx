import React from 'react';

const SessionList = ({ sessions, activeSession, onSelectSession, onNewSession, onDeleteSession }) => {
  return (
    <div className="session-list-container">
      <button className="new-chat-btn" onClick={onNewSession}>
        + New Chat
      </button>
      <div className="session-list">
        {sessions.map((session) => (
          <div 
            key={session.id} 
            className={`session-item ${activeSession === session.id ? 'active' : ''}`}
            onClick={() => onSelectSession(session.id)}
          >
            <div className="session-info">
              <span className="session-title">
                {session.title || 'New Conversation'}
              </span>
              <span className="session-meta">
                {new Date(session.timestamp).toLocaleDateString()} • {session.messageCount} msgs
              </span>
            </div>
            <button 
              className="delete-session-btn"
              onClick={(e) => {
                e.stopPropagation();
                onDeleteSession(session.id);
              }}
              title="Delete chat"
            >
              🗑️
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default SessionList;
