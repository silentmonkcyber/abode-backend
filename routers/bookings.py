from fastapi import APIRouter, HTTPException
from typing import List, Optional
from database import get_db
from schemas import BookingCreate, BookingUpdate, BookingOut

router = APIRouter()

@router.post("/", response_model=BookingOut, status_code=201)
def create_booking(payload: BookingCreate):
    with get_db() as conn:
        cursor = conn.execute(
            "INSERT INTO bookings (name, email, phone, service, message) VALUES (?, ?, ?, ?, ?)",
            (payload.name, payload.email, payload.phone, payload.service, payload.message)
        )
        row = conn.execute("SELECT * FROM bookings WHERE id = ?", (cursor.lastrowid,)).fetchone()
    return dict(row)

@router.get("/", response_model=List[BookingOut])
def list_bookings(status: Optional[str] = None):
    sql = "SELECT * FROM bookings"
    params = []
    if status:
        sql += " WHERE status = ?"
        params.append(status)
    sql += " ORDER BY created_at DESC"
    with get_db() as conn:
        rows = conn.execute(sql, params).fetchall()
    return [dict(r) for r in rows]

@router.get("/{booking_id}", response_model=BookingOut)
def get_booking(booking_id: int):
    with get_db() as conn:
        row = conn.execute("SELECT * FROM bookings WHERE id = ?", (booking_id,)).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Booking not found")
    return dict(row)

@router.patch("/{booking_id}", response_model=BookingOut)
def update_booking(booking_id: int, payload: BookingUpdate):
    with get_db() as conn:
        row = conn.execute("SELECT id FROM bookings WHERE id = ?", (booking_id,)).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Booking not found")
        conn.execute("UPDATE bookings SET status = ? WHERE id = ?", (payload.status, booking_id))
        updated = conn.execute("SELECT * FROM bookings WHERE id = ?", (booking_id,)).fetchone()
    return dict(updated)

@router.delete("/{booking_id}", status_code=204)
def delete_booking(booking_id: int):
    with get_db() as conn:
        row = conn.execute("SELECT id FROM bookings WHERE id = ?", (booking_id,)).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Booking not found")
        conn.execute("DELETE FROM bookings WHERE id = ?", (booking_id,))
