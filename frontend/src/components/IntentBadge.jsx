import React from 'react';

const INTENT_CONFIG = {
  conceptual:       { icon: '🧠', label: 'Conceptual' },
  numerical:        { icon: '🔢', label: 'Numerical' },
  equation:         { icon: '∑',  label: 'Equation' },
  image:            { icon: '🖼️', label: 'Diagram' },
  definition:       { icon: '📖', label: 'Definition' },
  comparison:       { icon: '⚖️', label: 'Comparison' },
  out_of_scope:     { icon: '🚫', label: 'Out of Scope' },
  fallback_hybrid:  { icon: '🔍', label: 'Search' },
  error:            { icon: '⚠️', label: 'Error' },
};

export default function IntentBadge({ intent }) {
  if (!intent) return null;
  const key = intent.toLowerCase();
  const { icon, label } = INTENT_CONFIG[key] || { icon: 'ℹ️', label: intent };
  return (
    <div className={`intent-badge intent-${key}`}>
      <span>{icon}</span>
      <span>{label}</span>
    </div>
  );
}
