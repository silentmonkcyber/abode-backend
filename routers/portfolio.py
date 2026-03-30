from fastapi import APIRouter, HTTPException
from typing import List, Optional
from database import get_db
from schemas import PortfolioCreate, PortfolioUpdate, PortfolioOut

router = APIRouter()

@router.post("/", response_model=PortfolioOut, status_code=201)
def create_project(payload: PortfolioCreate):
    with get_db() as conn:
        cursor = conn.execute(
            "INSERT INTO portfolio (title, location, category, description, image_url, is_featured) VALUES (?, ?, ?, ?, ?, ?)",
            (payload.title, payload.location, payload.category, payload.description, payload.image_url, int(payload.is_featured))
        )
        row = conn.execute("SELECT * FROM portfolio WHERE id = ?", (cursor.lastrowid,)).fetchone()
    return _fmt(row)

@router.get("/", response_model=List[PortfolioOut])
def list_projects(category: Optional[str] = None, featured: Optional[bool] = None):
    sql = "SELECT * FROM portfolio WHERE 1=1"
    params = []
    if category:
        sql += " AND category = ?"
        params.append(category)
    if featured is not None:
        sql += " AND is_featured = ?"
        params.append(int(featured))
    sql += " ORDER BY created_at DESC"
    with get_db() as conn:
        rows = conn.execute(sql, params).fetchall()
    return [_fmt(r) for r in rows]

@router.get("/categories", response_model=List[str])
def get_categories():
    with get_db() as conn:
        rows = conn.execute("SELECT DISTINCT category FROM portfolio WHERE category IS NOT NULL").fetchall()
    return [r["category"] for r in rows]

@router.get("/{pid}", response_model=PortfolioOut)
def get_project(pid: int):
    with get_db() as conn:
        row = conn.execute("SELECT * FROM portfolio WHERE id = ?", (pid,)).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Not found")
    return _fmt(row)

@router.patch("/{pid}", response_model=PortfolioOut)
def update_project(pid: int, payload: PortfolioUpdate):
    with get_db() as conn:
        existing = conn.execute("SELECT * FROM portfolio WHERE id = ?", (pid,)).fetchone()
        if not existing:
            raise HTTPException(status_code=404, detail="Not found")
        fields = {}
        if payload.title       is not None: fields["title"]       = payload.title
        if payload.location    is not None: fields["location"]    = payload.location
        if payload.category    is not None: fields["category"]    = payload.category
        if payload.description is not None: fields["description"] = payload.description
        if payload.image_url   is not None: fields["image_url"]   = payload.image_url
        if payload.is_featured is not None: fields["is_featured"] = int(payload.is_featured)
        if fields:
            set_clause = ", ".join(f"{k} = ?" for k in fields)
            conn.execute(f"UPDATE portfolio SET {set_clause} WHERE id = ?", (*fields.values(), pid))
        updated = conn.execute("SELECT * FROM portfolio WHERE id = ?", (pid,)).fetchone()
    return _fmt(updated)

@router.delete("/{pid}", status_code=204)
def delete_project(pid: int):
    with get_db() as conn:
        row = conn.execute("SELECT id FROM portfolio WHERE id = ?", (pid,)).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Not found")
        conn.execute("DELETE FROM portfolio WHERE id = ?", (pid,))

def _fmt(row):
    d = dict(row)
    d["is_featured"] = bool(d["is_featured"])
    return d
