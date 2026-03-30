from database import init_db, get_db

def seed():
    init_db()
    with get_db() as conn:
        conn.executemany(
            "INSERT OR IGNORE INTO testimonials (id, client_name, location, rating, review, is_visible) VALUES (?, ?, ?, ?, ?, ?)",
            [
                (1, "Priya Sharma", "Mumbai", 5, "Working with Abode Renovators was a dream.", 1),
                (2, "Rahul Mehra", "Bangalore", 5, "The team was incredibly professional.", 1),
                (3, "Ananya Krishnan", "Pune", 5, "They delivered magic.", 1),
                (4, "Vikram Nair", "Delhi", 5, "Our home office makeover changed how I work.", 1),
                (5, "Kavya Reddy", "Chennai", 5, "They listened. Our home reflects us perfectly.", 1),
            ]
        )
        conn.executemany(
            "INSERT OR IGNORE INTO portfolio (id, title, location, category, description, is_featured) VALUES (?, ?, ?, ?, ?, ?)",
            [
                (1, "The Meridian Suite", "Mumbai", "Living Room", "A warm contemporary living space.", 1),
                (2, "Loft Minimal", "Pune", "Bedroom", "Clean lines for a calming urban retreat.", 0),
                (3, "Verde Living", "Bangalore", "Full Home", "Biophilic design weaving nature into every room.", 1),
                (4, "Terracotta Home", "Hyderabad", "Kitchen & Dining", "Rich terracotta hues in a family dining space.", 0),
                (5, "The Ivory Penthouse", "Delhi", "Full Home", "Luxurious ivory tones across a penthouse.", 1),
            ]
        )
    print("Seeded successfully.")

if __name__ == "__main__":
    seed()