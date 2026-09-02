import React from 'react';
import { InlineMath, BlockMath } from 'react-katex';
import 'katex/dist/katex.min.css';

const MathBlock = ({ math, display }) => {
  try {
    if (display) {
      return <BlockMath math={math} />;
    }
    return <InlineMath math={math} />;
  } catch (error) {
    console.error("KaTeX rendering error:", error);
    // Fallback to plain text
    return <span>{display ? `$$${math}$$` : `$${math}$`}</span>;
  }
};

export default MathBlock;
