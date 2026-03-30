from pydantic import BaseModel, EmailStr, validator
from typing import Optional


# ── Bookings ──────────────────────────────────────────────────────────────────

class BookingCreate(BaseModel):
    name:    str
    email:   EmailStr
    phone:   Optional[str] = None
    service: Optional[str] = None
    message: Optional[str] = None

class BookingUpdate(BaseModel):
    status: str

class BookingOut(BookingCreate):
    id:         int
    status:     str
    created_at: str

    class Config:
        orm_mode = True


# ── Testimonials ──────────────────────────────────────────────────────────────

class TestimonialCreate(BaseModel):
    client_name: str
    location:    Optional[str] = None
    rating:      int = 5
    review:      str
    is_visible:  bool = True

class TestimonialUpdate(BaseModel):
    client_name: Optional[str] = None
    location:    Optional[str] = None
    rating:      Optional[int] = None
    review:      Optional[str] = None
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
        orm_mode = True


# ── Portfolio ─────────────────────────────────────────────────────────────────

class PortfolioCreate(BaseModel):
    title:       str
    location:    Optional[str] = None
    category:    Optional[str] = None
    description: Optional[str] = None
    image_url:   Optional[str] = None
    is_featured: bool = False

class PortfolioUpdate(BaseModel):
    title:       Optional[str] = None
    location:    Optional[str] = None
    category:    Optional[str] = None
    description: Optional[str] = None
    image_url:   Optional[str] = None
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
        orm_mode = True