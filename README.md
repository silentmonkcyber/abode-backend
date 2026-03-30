# 🏠 Abode Renovators — Backend API

FastAPI + SQLite backend for the Abode Renovators interior design website.

---

## 📁 Project Structure

```
abode-backend/
├── main.py            # App entry point, CORS, router registration
├── database.py        # SQLite connection & table initialisation
├── schemas.py         # Pydantic request/response models
├── seed.py            # One-time sample data loader
├── requirements.txt
└── routers/
    ├── bookings.py        # Contact / booking form endpoints
    ├── testimonials.py    # Testimonials CRUD
    └── portfolio.py       # Portfolio projects CRUD
```

---

## 🚀 Quick Start

### 1 · Install dependencies
```bash
pip install -r requirements.txt
```

### 2 · (Optional) Seed sample data
```bash
python seed.py
```

### 3 · Run the server
```bash
uvicorn main:app --reload
```

The API will be live at **http://localhost:8000**  
Interactive docs at **http://localhost:8000/docs**

---

## 📡 API Endpoints

### Bookings  `/api/bookings`

| Method | Path              | Description                    |
|--------|-------------------|--------------------------------|
| POST   | `/`               | Submit a booking / contact form |
| GET    | `/`               | List all bookings (admin)       |
| GET    | `/{id}`           | Get single booking              |
| PATCH  | `/{id}`           | Update booking status           |
| DELETE | `/{id}`           | Delete a booking                |

**Booking status values:** `pending` · `confirmed` · `completed` · `cancelled`

**Example — Submit booking:**
```bash
curl -X POST http://localhost:8000/api/bookings \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Priya Sharma",
    "email": "priya@example.com",
    "phone": "+91 98765 43210",
    "service": "Living Room Design",
    "message": "Looking to redesign my 2BHK apartment."
  }'
```

---

### Testimonials  `/api/testimonials`

| Method | Path   | Description                          |
|--------|--------|--------------------------------------|
| POST   | `/`    | Submit a new testimonial             |
| GET    | `/`    | List testimonials (`?visible_only=true`) |
| GET    | `/{id}`| Get single testimonial               |
| PATCH  | `/{id}`| Update testimonial (admin)           |
| DELETE | `/{id}`| Delete testimonial (admin)           |

**Example — Add testimonial:**
```bash
curl -X POST http://localhost:8000/api/testimonials \
  -H "Content-Type: application/json" \
  -d '{
    "client_name": "Vikram Nair",
    "location": "Delhi",
    "rating": 5,
    "review": "Truly outstanding work. Every detail was perfect."
  }'
```

---

### Portfolio  `/api/portfolio`

| Method | Path              | Description                         |
|--------|-------------------|-------------------------------------|
| POST   | `/`               | Add a new project (admin)            |
| GET    | `/`               | List projects (`?category=&featured=`) |
| GET    | `/categories`     | List all distinct categories         |
| GET    | `/{id}`           | Get single project                   |
| PATCH  | `/{id}`           | Update project (admin)               |
| DELETE | `/{id}`           | Delete project (admin)               |

**Example — Add project:**
```bash
curl -X POST http://localhost:8000/api/portfolio \
  -H "Content-Type: application/json" \
  -d '{
    "title": "The Meridian Suite",
    "location": "Mumbai",
    "category": "Living Room",
    "description": "A warm, contemporary living space.",
    "image_url": "/images/meridian.jpg",
    "is_featured": true
  }'
```

---

## 🔧 Connecting the Frontend

Update the frontend HTML to fetch from the API. Example:

```js
// Load visible testimonials
const res = await fetch("http://localhost:8000/api/testimonials?visible_only=true");
const data = await res.json();

// Submit booking form
await fetch("http://localhost:8000/api/bookings", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ name, email, phone, service, message })
});
```

---

## 🛠 Switching to PostgreSQL / MySQL

Replace `database.py` with SQLAlchemy + your chosen driver.  
All routers are database-agnostic — only `database.py` needs changing.

---

## 📦 Production Notes

- Set `allow_origins` in `main.py` to your actual frontend domain
- Add API key / JWT auth middleware before exposing admin endpoints publicly
- Use environment variables for any secrets via `python-dotenv`
