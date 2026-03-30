from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from database import get_db
from schemas import BookingCreate, BookingUpdate, BookingOut

router = APIRouter()


# ── POST /api/bookings ────────────────────────────────────────────────────────
@router.post("/", response_model=BookingOut, status_code=201,
             summary="Submit a booking / contact request")
def create_booking(payload: BookingCreate):
    with get_db() as conn:
        cursor = conn.execute(
            """INSERT INTO bookings (name, email, phone, service, message)
               VALUES (?, ?, ?, ?, ?)""",
            (payload.name, payload.email, payload.phone,
             payload.service, payload.message)
        )
        row = conn.execute(
            "SELECT * FROM bookings WHERE id = ?", (cursor.lastrowid,)
        ).fetchone()
    return dict(row)


# ── GET /api/bookings ─────────────────────────────────────────────────────────
@router.get("/", response_model=List[BookingOut],
            summary="List all bookings (admin)")
def list_bookings(
    status: Optional[str] = Query(None, description="Filter by status"),
    limit:  int           = Query(50, ge=1, le=200),
    offset: int           = Query(0, ge=0),
):
    sql    = "SELECT * FROM bookings"
    params = []
    if status:
        sql += " WHERE status = ?"
        params.append(status)
    sql += " ORDER BY created_at DESC LIMIT ? OFFSET ?"
    params += [limit, offset]

    with get_db() as conn:
        rows = conn.execute(sql, params).fetchall()
    return [dict(r) for r in rows]


# ── GET /api/bookings/{id} ────────────────────────────────────────────────────
@router.get("/{booking_id}", response_model=BookingOut,
            summary="Get a single booking")
def get_booking(booking_id: int):
    with get_db() as conn:
        row = conn.execute(
            "SELECT * FROM bookings WHERE id = ?", (booking_id,)
        ).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Booking not found")
    return dict(row)


# ── PATCH /api/bookings/{id} ──────────────────────────────────────────────────
@router.patch("/{booking_id}", response_model=BookingOut,
              summary="Update booking status (admin)")
def update_booking_status(booking_id: int, payload: BookingUpdate):
    with get_db() as conn:
        row = conn.execute(
            "SELECT id FROM bookings WHERE id = ?", (booking_id,)
        ).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Booking not found")
        conn.execute(
            "UPDATE bookings SET status = ? WHERE id = ?",
            (payload.status, booking_id)
        )
        updated = conn.execute(
            "SELECT * FROM bookings WHERE id = ?", (booking_id,)
        ).fetchone()
    return dict(updated)


# ── DELETE /api/bookings/{id} ─────────────────────────────────────────────────
@router.delete("/{booking_id}", status_code=204,
               summary="Delete a booking (admin)")
def delete_booking(booking_id: int):
    with get_db() as conn:
        row = conn.execute(
            "SELECT id FROM bookings WHERE id = ?", (booking_id,)
        ).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Booking not found")
        conn.execute("DELETE FROM bookings WHERE id = ?", (booking_id,))
