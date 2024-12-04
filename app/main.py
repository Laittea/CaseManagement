from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.clients.router import router as clients_router


app = FastAPI()

# Root route
@app.get("/")
def read_root():
    return {
        "message": "Welcome to the application!",
        "status": "healthy",
        "version": "1.0.0",
        "docs_url": "/docs"
    }
@app.get("/health")
def health_check():
    return {"status": "healthy"}
    
# Set API endpoints on router
app.include_router(clients_router)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_methods=["*"],  # Allows all methods, including OPTIONS
    allow_headers=["*"],  # Allows all headers
)


