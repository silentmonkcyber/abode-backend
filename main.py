from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import init_db
from routers import bookings, testimonials, portfolio

app = FastAPI(
    title="Abode Renovators API",
    description="Backend API for Abode Renovators interior design website",
    version="1.0.0"
)

# Allow requests from the frontend (update origin in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database tables on startup
@app.on_event("startup")
async def startup():
    init_db()

# Include routers
app.include_router(bookings.router,      prefix="/api/bookings",      tags=["Bookings"])
app.include_router(testimonials.router,  prefix="/api/testimonials",  tags=["Testimonials"])
app.include_router(portfolio.router,     prefix="/api/portfolio",     tags=["Portfolio"])


@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "message": "Abode Renovators API is running 🏠"}
