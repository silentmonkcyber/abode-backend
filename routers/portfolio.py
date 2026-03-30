from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from database import get_db
from schemas import PortfolioCreate, PortfolioUpdate, PortfolioOut

router = APIRouter()


# ── POST /api/portfolio ───────────────────────────────────────────────────────
@router.post("/", response_model=PortfolioOut, status_code=201,
             summary="Add a new portfolio project")
def create_project(payload: PortfolioCreate):
    with get_db() as conn:
        cursor = conn.execute(
            """INSERT INTO portfolio
               (title, location, category, description, image_url, is_featured)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (payload.title, payload.location, payload.category,
             payload.description, payload.image_url, int(payload.is_featured))
        )
        row = conn.execute(
            "SELECT * FROM portfolio WHERE id = ?", (cursor.lastrowid,)
        ).fetchone()
    return _format(row)


# ── GET /api/portfolio ────────────────────────────────────────────────────────
@router.get("/", response_model=List[PortfolioOut],
            summary="List portfolio projects")
def list_projects(
    category:    Optional[str] = Query(None, description="Filter by category"),
    featured:    Optional[bool]= Query(None, description="Filter featured only"),
    limit:       int           = Query(20,   ge=1, le=100),
    offset:      int           = Query(0,    ge=0),
):
    sql    = "SELECT * FROM portfolio WHERE 1=1"
    params = []
    if category:
        sql += " AND category = ?"
        params.append(category)
    if featured is not None:
        sql += " AND is_featured = ?"
        params.append(int(featured))
    sql += " ORDER BY created_at DESC LIMIT ? OFFSET ?"
    params += [limit, offset]

    with get_db() as conn:
        rows = conn.execute(sql, params).fetchall()
    return [_format(r) for r in rows]


# ── GET /api/portfolio/categories ────────────────────────────────────────────
@router.get("/categories", response_model=List[str],
            summary="Get all distinct project categories")
def get_categories():
    with get_db() as conn:
        rows = conn.execute(
            "SELECT DISTINCT category FROM portfolio WHERE category IS NOT NULL"
        ).fetchall()
    return [r["category"] for r in rows]


# ── GET /api/portfolio/{id} ───────────────────────────────────────────────────
@router.get("/{project_id}", response_model=PortfolioOut,
            summary="Get a single portfolio project")
def get_project(project_id: int):
    with get_db() as conn:
        row = conn.execute(
            "SELECT * FROM portfolio WHERE id = ?", (project_id,)
        ).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Project not found")
    return _format(row)


# ── PATCH /api/portfolio/{id} ─────────────────────────────────────────────────
@router.patch("/{project_id}", response_model=PortfolioOut,
              summary="Update a portfolio project (admin)")
def update_project(project_id: int, payload: PortfolioUpdate):
    with get_db() as conn:
        existing = conn.execute(
            "SELECT * FROM portfolio WHERE id = ?", (project_id,)
        ).fetchone()
        if not existing:
            raise HTTPException(status_code=404, detail="Project not found")

        fields = {}
        if payload.title       is not None: fields["title"]       = payload.title
        if payload.location    is not None: fields["location"]    = payload.location
        if payload.category    is not None: fields["category"]    = payload.category
        if payload.description is not None: fields["description"] = payload.description
        if payload.image_url   is not None: fields["image_url"]   = payload.image_url
        if payload.is_featured is not None: fields["is_featured"] = int(payload.is_featured)

        if fields:
            set_clause = ", ".join(f"{k} = ?" for k in fields)
            conn.execute(
                f"UPDATE portfolio SET {set_clause} WHERE id = ?",
                (*fields.values(), project_id)
            )

        updated = conn.execute(
            "SELECT * FROM portfolio WHERE id = ?", (project_id,)
        ).fetchone()
    return _format(updated)


# ── DELETE /api/portfolio/{id} ────────────────────────────────────────────────
@router.delete("/{project_id}", status_code=204,
               summary="Delete a portfolio project (admin)")
def delete_project(project_id: int):
    with get_db() as conn:
        row = conn.execute(
            "SELECT id FROM portfolio WHERE id = ?", (project_id,)
        ).fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Project not found")
        conn.execute("DELETE FROM portfolio WHERE id = ?", (project_id,))


# ── Helper ────────────────────────────────────────────────────────────────────
def _format(row) -> dict:
    d = dict(row)
    d["is_featured"] = bool(d["is_featured"])
    return d
