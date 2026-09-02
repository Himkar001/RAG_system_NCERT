import { useState } from 'react';

export default function SourceCard({ source }) {
  const [expanded, setExpanded] = useState(false);
  return (
    <div className="source-card">
      <div className="source-card-header" onClick={() => setExpanded(e => !e)}>
        <div className="source-meta">
          <span className="source-index">[{source.index}]</span>
          <span className="source-page">Page {source.page}</span>
          <span className="source-type-badge">{source.content_type || 'text'}</span>
        </div>
        <span className="source-chevron">{expanded ? '▼' : '▶'}</span>
      </div>
      {expanded && (
        <div className="source-preview">{source.preview}</div>
      )}
    </div>
  );
}
