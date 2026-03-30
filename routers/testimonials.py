from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from database import get_db
from schemas import TestimonialCreate, TestimonialUpdate, TestimonialOut

router = APIRouter()


# ── POST /api/testimonials ────────────────────────────────────────────────────
@router.post("/", response_model=TestimonialOut, status_code=201,
             summary="Submit a new testimonial")
def create_testimonial(payload: TestimonialCreate):
    with get_db() as conn:
        cursor = conn.execute(
            """INSERT INTO testimonials
               (client_name, location, rating, review, is_visible)
               VALUES (?, ?, ?, ?, ?)""",
            (payload.client_name, payload.location, payload.rating,
             payload.review, int(payload.is_visible))
        )
        row = conn.execute(
            "SELECT * FROM testimonials WHERE id = ?", (cursor.lastrowid,)
        ).fetchone()
    return _format(row)


# ── GET /api/testimonials ─────────────────────────────────────────────────────
@router.get("/", response_model=List[TestimonialOut],
            summary="List testimonials")
def list_testimonials(
    visible_only: bool = Query(True,  description="Show only visible reviews"),
    limit:        int  = Query(20,    ge=1, le=100),
    offset:       int  = Query(0,     ge=0),
):
    sql    = "SELECT * FROM testimonials"
    params = []
    if visible_only:
        sql += " WHERE is_visible = 1"
    sql += " ORDER BY created_at DESC LIMIT ? OFFSET ?"
    params += [limit, offset]

    with get_db() as conn:
        rows = conn.execute(sql, params).fetchall()
    return [_format(r) for r in rows]


# ── GET /api/testimonials/{id} ────────────────────────────────────────────────
@router.get("/{testimonial_id}", response_model=TestimonialOut,
            summary="Get a single testimonial")
def get_testimonial(testimonial_id: int):
    with get_db() as conn:
        row = conn.execute(
            "SELECT * FROM testimonials WHERE id = ?", (testimonial_id,)
        ).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Testimonial not found")
    return _format(row)


# ── PATCH /api/testimonials/{id} ──────────────────────────────────────────────
@router.patch("/{testimonial_id}", response_model=TestimonialOut,
              summary="Update a testimonial (admin)")
def update_testimonial(testimonial_id: int, payload: TestimonialUpdate):
    with get_db() as conn:
        existing = conn.execute(
            "SELECT * FROM testimonials WHERE id = ?", (testimonial_id,)
        ).fetchone()
        if not existing:
            raise HTTPException(status_code=404, detail="Testimonial not found")

        fields = {}
        if payload.client_name is not None: fields["client_name"] = payload.client_name
        if payload.location    is not None: fields["location"]    = payload.location
        if payload.rating      is not None: fields["rating"]      = payload.rating
        if payload.review      is not None: fields["review"]      = payload.review
        if payload.is_visible  is not None: fields["is_visible"]  = int(payload.is_visible)

        if fields:
            set_clause = ", ".join(f"{k} = ?" for k in fields)
            conn.execute(
                f"UPDATE testimonials SET {set_clause} WHERE id = ?",
                (*fields.values(), testimonial_id)
            )

        updated = conn.execute(
            "SELECT * FROM testimonials WHERE id = ?", (testimonial_id,)
        ).fetchone()
    return _format(updated)


# ── DELETE /api/testimonials/{id} ─────────────────────────────────────────────
@router.delete("/{testimonial_id}", status_code=204,
               summary="Delete a testimonial (admin)")
def delete_testimonial(testimonial_id: int):
    with get_db() as conn:
        row = conn.execute(
            "SELECT id FROM testimonials WHERE id = ?", (testimonial_id,)
        ).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Testimonial not found")
        conn.execute("DELETE FROM testimonials WHERE id = ?", (testimonial_id,))


# ── Helper ────────────────────────────────────────────────────────────────────
def _format(row) -> dict:
    d = dict(row)
    d["is_visible"] = bool(d["is_visible"])
    return d
