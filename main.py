from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import init_db
from routers import bookings, testimonials, portfolio

app = FastAPI(
    title="Abode Renovators API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    init_db()

app.include_router(bookings.router,     prefix="/api/bookings",     tags=["Bookings"])
app.include_router(testimonials.router, prefix="/api/testimonials", tags=["Testimonials"])
app.include_router(portfolio.router,    prefix="/api/portfolio",    tags=["Portfolio"])

@app.get("/")
def root():
    return {"status": "ok", "message": "Abode Renovators API is running"}