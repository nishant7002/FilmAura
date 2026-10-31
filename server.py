"""
FilmAura — Backend API Server
Serves the React frontend and provides REST API endpoints
for the FilmAura recommendation engine.
"""

import os
import json
from pathlib import Path
from typing import Optional

import uvicorn
from starlette.applications import Starlette
from starlette.responses import JSONResponse, FileResponse
from starlette.routing import Route, Mount
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from recommender import FilmAuraRecommender

# Initialize recommender engine
recommender: Optional[FilmAuraRecommender] = None
init_error: Optional[str] = None

try:
    recommender = FilmAuraRecommender()
except Exception as e:
    init_error = str(e)
    print(f"⚠️ Warning loading recommender: {e}")

# API Handlers
async def api_health(request):
    """Health check endpoint."""
    return JSONResponse({
        "status": "healthy" if recommender and recommender.is_loaded else "uninitialized",
        "error": init_error
    })

async def api_metadata(request):
    """Returns available moods, genres, and movie catalog for dropdowns."""
    if not recommender or not recommender.is_loaded:
        return JSONResponse(
            {"detail": f"Model artifacts not loaded. {init_error}"},
            status_code=503
        )
    
    return JSONResponse({
        "moods": recommender.get_available_moods(),
        "genres": recommender.get_available_genres(),
        "movies": recommender.get_movie_titles()
    })

async def api_recommend(request):
    """Processes recommendation query and returns top-K ranked movies."""
    if not recommender or not recommender.is_loaded:
        return JSONResponse(
            {"detail": f"Model artifacts not loaded. {init_error}"},
            status_code=503
        )

    try:
        data = await request.json()
    except Exception:
        return JSONResponse({"detail": "Invalid JSON payload."}, status_code=400)

    mood = data.get("mood")
    genre = data.get("genre")
    favorite_movie_id = data.get("favorite_movie_id")
    top_k = int(data.get("top_k", 5))

    try:
        recommendations = recommender.recommend(
            mood=mood,
            genre=genre,
            favorite_movie_id=favorite_movie_id,
            top_k=top_k
        )
        return JSONResponse({"recommendations": recommendations})
    except Exception as e:
        return JSONResponse({"detail": str(e)}, status_code=500)

# Paths for static React frontend build
BASE_DIR = Path(__file__).resolve().parent
DIST_DIR = BASE_DIR / "frontend" / "dist"

# Setup routes
routes = [
    Route("/api/health", api_health, methods=["GET"]),
    Route("/api/metadata", api_metadata, methods=["GET"]),
    Route("/api/recommend", api_recommend, methods=["POST"]),
]

# Mount static React app if frontend/dist exists
if DIST_DIR.exists():
    routes.append(Mount("/", StaticFiles(directory=str(DIST_DIR), html=True), name="static"))
else:
    async def index_fallback(request):
        return JSONResponse({
            "message": "FilmAura API is running. Build the React frontend with 'cd frontend && npm run build' to serve the UI here.",
            "api_endpoints": ["/api/health", "/api/metadata", "/api/recommend"]
        })
    routes.append(Route("/", index_fallback))

# CORS middleware for development (allows React dev server on :5173 to call :8000)
middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )
]

app = Starlette(debug=True, routes=routes, middleware=middleware)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"\n🎬 FilmAura Server starting at: http://localhost:{port}")
    if DIST_DIR.exists():
        print(f"✨ Serving built React frontend from: {DIST_DIR}")
    else:
        print(f"ℹ️  React build not found in {DIST_DIR}. Serving API only.")
    print("Press Ctrl+C to stop.\n")
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
