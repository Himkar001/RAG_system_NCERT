from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.api.routes import router
from backend.api.stream_routes import stream_router

app = FastAPI(
    title="NCERT RAG Study Assistant",
    description="Stage 2 Intelligent NCERT Science Tutor",
    version="1.0"
)

# -----------------------------
# CORS Configuration
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Static Images (IMPORTANT)
# -----------------------------
app.mount(
    "/images",
    StaticFiles(directory="data/processed/rendered_pages"),
    name="images"
)

# -----------------------------
# Register API Routes
# -----------------------------
app.include_router(router)
app.include_router(stream_router)

# -----------------------------
# Root Endpoint
# -----------------------------
@app.get("/")
def root():
    return {
        "message": "NCERT RAG Backend Running",
        "status": "success"
    }

# -----------------------------
# Health Check Endpoint
# -----------------------------
@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }