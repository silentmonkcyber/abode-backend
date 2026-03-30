from fastapi import APIRouter, HTTPException
from typing import List, Optional
from database import get_db
from schemas import TestimonialCreate, TestimonialUpdate, TestimonialOut

router = APIRouter()

@router.post("/", response_model=TestimonialOut, status_code=201)
def create_testimonial(payload: TestimonialCreate):
    with get_db() as conn:
        cursor = conn.execute(
            "INSERT INTO testimonials (client_name, location, rating, review, is_visible) VALUES (?, ?, ?, ?, ?)",
            (payload.client_name, payload.location, payload.rating, payload.review, int(payload.is_visible))
        )
        row = conn.execute("SELECT * FROM testimonials WHERE id = ?", (cursor.lastrowid,)).fetchone()
    return _fmt(row)

@router.get("/", response_model=List[TestimonialOut])
def list_testimonials(visible_only: bool = True):
    sql = "SELECT * FROM testimonials"
    if visible_only:
        sql += " WHERE is_visible = 1"
    sql += " ORDER BY created_at DESC"
    with get_db() as conn:
        rows = conn.execute(sql).fetchall()
    return [_fmt(r) for r in rows]

@router.get("/{tid}", response_model=TestimonialOut)
def get_testimonial(tid: int):
    with get_db() as conn:
        row = conn.execute("SELECT * FROM testimonials WHERE id = ?", (tid,)).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Not found")
    return _fmt(row)

@router.patch("/{tid}", response_model=TestimonialOut)
def update_testimonial(tid: int, payload: TestimonialUpdate):
    with get_db() as conn:
        existing = conn.execute("SELECT * FROM testimonials WHERE id = ?", (tid,)).fetchone()
        if not existing:
            raise HTTPException(status_code=404, detail="Not found")
        fields = {}
        if payload.client_name is not None: fields["client_name"] = payload.client_name
        if payload.location    is not None: fields["location"]    = payload.location
        if payload.rating      is not None: fields["rating"]      = payload.rating
        if payload.review      is not None: fields["review"]      = payload.review
        if payload.is_visible  is not None: fields["is_visible"]  = int(payload.is_visible)
        if fields:
            set_clause = ", ".join(f"{k} = ?" for k in fields)
            conn.execute(f"UPDATE testimonials SET {set_clause} WHERE id = ?", (*fields.values(), tid))
        updated = conn.execute("SELECT * FROM testimonials WHERE id = ?", (tid,)).fetchone()
    return _fmt(updated)

@router.delete("/{tid}", status_code=204)
def delete_testimonial(tid: int):
    with get_db() as conn:
        row = conn.execute("SELECT id FROM testimonials WHERE id = ?", (tid,)).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Not found")
        conn.execute("DELETE FROM testimonials WHERE id = ?", (tid,))

def _fmt(row):
    d = dict(row)
    d["is_visible"] = bool(d["is_visible"])
    return d
