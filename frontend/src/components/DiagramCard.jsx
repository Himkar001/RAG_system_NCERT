import { useState } from 'react';

const API_BASE = import.meta.env.VITE_API_URL || '';

/**
 * DiagramCard — renders a single NCERT page image with metadata.
 * Props:
 *   image: { image_url, page, chapter, pdf_name, has_diagram, score, ocr_preview }
 *   isExpanded: bool (controls whether image is shown full size)
 */
function DiagramCard({ image, isExpanded: defaultExpanded = true }) {
  const [expanded, setExpanded] = useState(defaultExpanded);
  const [imgError, setImgError] = useState(false);

  const cleanUrl = image.image_url.startsWith('/') ? image.image_url.slice(1) : image.image_url;
  const fullUrl = API_BASE ? `${API_BASE}/${cleanUrl}` : `/${cleanUrl}`;
  const chapterLabel = image.chapter
    .replace(/_/g, ' ')
    .replace(/\b\w/g, c => c.toUpperCase());

  return (
    <div className="diagram-card">
      <div className="diagram-card-header" onClick={() => setExpanded(!expanded)}>
        <div className="diagram-card-meta">
          <span className="diagram-icon">🖼️</span>
          <span className="diagram-chapter">{chapterLabel}</span>
          <span className="diagram-page-badge">Page {image.page}</span>
          {image.has_diagram && (
            <span className="diagram-confirmed-badge">Contains Diagram</span>
          )}
        </div>
        <span className="diagram-toggle">{expanded ? '▲' : '▼'}</span>
      </div>

      {expanded && (
        <div className="diagram-card-body">
          {imgError ? (
            <div className="diagram-error">
              Image could not be loaded. Make sure the backend is running.
            </div>
          ) : (
            <img
              src={fullUrl}
              alt={`NCERT diagram from ${chapterLabel} page ${image.page}`}
              className="diagram-image"
              onError={() => setImgError(true)}
              loading="lazy"
            />
          )}
          {image.ocr_preview && (
            <p className="diagram-ocr-preview">{image.ocr_preview}</p>
          )}
        </div>
      )}
    </div>
  );
}

/**
 * DiagramGallery — shows multiple diagram results.
 * Props:
 *   images: array of image objects
 */
export function DiagramGallery({ images }) {
  if (!images || images.length === 0) return null;

  return (
    <div className="diagram-gallery">
      <div className="diagram-gallery-label">
        📚 Relevant NCERT Pages ({images.length})
      </div>
      {images.map((img, idx) => (
        <DiagramCard
          key={`${img.chapter}-${img.page}-${idx}`}
          image={img}
          isExpanded={idx === 0}   // auto-expand first result only
        />
      ))}
    </div>
  );
}

export default DiagramCard;
