"""
seed.py — Populate the database with sample data for development.
Run once:  python seed.py
"""

from database import init_db, get_db

def seed():
    init_db()

    with get_db() as conn:
        # ── Sample bookings ───────────────────────────────────────────────
        conn.executemany(
            """INSERT OR IGNORE INTO bookings
               (id, name, email, phone, service, message, status)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            [
                (1, "Priya Sharma",  "priya@example.com",  "+91 98765 11111",
                 "Living Room Design",  "Looking to redesign my 2BHK in Bandra.", "pending"),
                (2, "Rahul Mehra",   "rahul@example.com",  "+91 98765 22222",
                 "Full Home Makeover",  "New apartment, need complete interior work.", "confirmed"),
                (3, "Ananya Krishnan","ananya@example.com", "+91 98765 33333",
                 "Kitchen & Dining",   "Want a modern modular kitchen.", "completed"),
            ]
        )

        # ── Sample testimonials ───────────────────────────────────────────
        conn.executemany(
            """INSERT OR IGNORE INTO testimonials
               (id, client_name, location, rating, review, is_visible)
               VALUES (?, ?, ?, ?, ?, ?)""",
            [
                (1, "Priya Sharma", "Mumbai", 5,
                 "Working with Abode Renovators was a dream. They completely understood our vision and delivered something far beyond what we imagined.", 1),
                (2, "Rahul & Nidhi Mehra", "Bangalore", 5,
                 "The team was incredibly professional, punctual, and detail-oriented. They transformed our outdated apartment into a modern, functional space.", 1),
                (3, "Ananya Krishnan", "Pune", 5,
                 "I gave them complete creative freedom and they delivered magic. Every corner of my home now has a story and a purpose.", 1),
                (4, "Vikram Nair", "Delhi", 5,
                 "Our home office makeover has genuinely changed how I work. The space is so calming yet energizing — I am more productive than ever.", 1),
                (5, "Kavya Reddy", "Chennai", 5,
                 "They listened. That's what set them apart. Every suggestion came from a place of understanding our lifestyle. Our home reflects us perfectly.", 1),
            ]
        )

        # ── Sample portfolio projects ─────────────────────────────────────
        conn.executemany(
            """INSERT OR IGNORE INTO portfolio
               (id, title, location, category, description, image_url, is_featured)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            [
                (1, "The Meridian Suite", "Mumbai", "Living Room",
                 "A warm, contemporary living space blending earthy tones with modern furniture.",
                 "/images/meridian.jpg", 1),
                (2, "Loft Minimal", "Pune", "Bedroom",
                 "Clean lines and muted neutrals for a calming urban retreat.",
                 "/images/loft.jpg", 0),
                (3, "Verde Living", "Bangalore", "Full Home",
                 "A biophilic design concept weaving nature into every room.",
                 "/images/verde.jpg", 1),
                (4, "Terracotta Home", "Hyderabad", "Kitchen & Dining",
                 "Rich terracotta hues and handcrafted tiles in a family dining space.",
                 "/images/terracotta.jpg", 0),
                (5, "The Ivory Penthouse", "Delhi", "Full Home",
                 "Luxurious ivory and gold tones across a sprawling penthouse apartment.",
                 "/images/ivory.jpg", 1),
            ]
        )

    print("🌱 Database seeded with sample data.")

if __name__ == "__main__":
    seed()
