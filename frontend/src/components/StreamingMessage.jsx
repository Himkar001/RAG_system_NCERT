import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import MathBlock from './MathBlock';

export default function StreamingMessage({ content, isStreaming }) {
  return (
    <div className="streaming-message">
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={{
          code({ node, inline, className, children, ...props }) {
            if (className === 'language-math') {
              return <MathBlock math={String(children).replace(/\n$/, '')} display={true} />;
            }
            return !inline ? (
              <pre><code className={className} {...props}>{children}</code></pre>
            ) : (
              <code className={className} {...props}>{children}</code>
            );
          }
        }}
      >
        {content}
      </ReactMarkdown>
      {isStreaming && <span className="streaming-cursor" />}
    </div>
  );
}
