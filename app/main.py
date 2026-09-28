from __future__ import annotations

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

try:
    from app.config import get_settings
    from app.routers.support import router as support_router
except ImportError:  # pragma: no cover
    from config import get_settings
    from routers.support import router as support_router

logging.basicConfig(level=logging.INFO)
settings = get_settings()

app = FastAPI(
    title="EPAM DIAL Multi-Model Orchestrator",
    description="OpenAI-compatible support routing API backed by DIAL Core and local Ollama models.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(support_router)


@app.get("/healthz")
async def healthz() -> dict[str, str]:
    return {"status": "ok", "service": settings.app_name}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=settings.app_port, reload=False)
