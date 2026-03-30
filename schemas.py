from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


# ── Bookings ─────────────────────────────────────────────────────────────────

class BookingCreate(BaseModel):
    name:    str            = Field(..., min_length=2, max_length=100, example="Priya Sharma")
    email:   EmailStr       = Field(..., example="priya@example.com")
    phone:   Optional[str]  = Field(None, max_length=20, example="+91 98765 43210")
    service: Optional[str]  = Field(None, example="Living Room Design")
    message: Optional[str]  = Field(None, max_length=1000)

class BookingUpdate(BaseModel):
    status: str = Field(..., pattern="^(pending|confirmed|completed|cancelled)$")

class BookingOut(BookingCreate):
    id:         int
    status:     str
    created_at: str

    class Config:
        from_attributes = True


# ── Testimonials ──────────────────────────────────────────────────────────────

class TestimonialCreate(BaseModel):
    client_name: str            = Field(..., min_length=2, max_length=100)
    location:    Optional[str]  = Field(None, max_length=100)
    rating:      int            = Field(5, ge=1, le=5)
    review:      str            = Field(..., min_length=10, max_length=1000)
    is_visible:  bool           = True

class TestimonialUpdate(BaseModel):
    client_name: Optional[str]  = None
    location:    Optional[str]  = None
    rating:      Optional[int]  = Field(None, ge=1, le=5)
    review:      Optional[str]  = None
    is_visible:  Optional[bool] = None

class TestimonialOut(BaseModel):
    id:          int
    client_name: str
    location:    Optional[str]
    rating:      int
    review:      str
    is_visible:  bool
    created_at:  str

    class Config:
        from_attributes = True


# ── Portfolio ─────────────────────────────────────────────────────────────────

class PortfolioCreate(BaseModel):
    title:       str            = Field(..., min_length=2, max_length=200)
    location:    Optional[str]  = Field(None, max_length=100)
    category:    Optional[str]  = Field(None, max_length=100, example="Living Room")
    description: Optional[str]  = Field(None, max_length=2000)
    image_url:   Optional[str]  = Field(None, max_length=500)
    is_featured: bool           = False

class PortfolioUpdate(BaseModel):
    title:       Optional[str]  = None
    location:    Optional[str]  = None
    category:    Optional[str]  = None
    description: Optional[str]  = None
    image_url:   Optional[str]  = None
    is_featured: Optional[bool] = None

class PortfolioOut(BaseModel):
    id:          int
    title:       str
    location:    Optional[str]
    category:    Optional[str]
    description: Optional[str]
    image_url:   Optional[str]
    is_featured: bool
    created_at:  str

    class Config:
        from_attributes = True
