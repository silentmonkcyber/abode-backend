from database import init_db, get_db

def seed():
    init_db()
    with get_db() as conn:
        conn.executemany(
            "INSERT OR IGNORE INTO testimonials (id, client_name, location, rating, review, is_visible) VALUES (?, ?, ?, ?, ?, ?)",
            [
                (1, "Priya Sharma", "Mumbai", 5, "Working with Abode Renovators was a dream. They completely understood our vision and delivered something far beyond what we imagined.", 1),
                (2, "Rahul & Nidhi Mehra", "Bangalore", 5, "The team was incredibly professional, punctual, and detail-oriented. They transformed our outdated apartment into a modern, functional space.", 1),
                (3, "Ananya Krishnan", "Pune", 5, "I gave them complete creative freedom and they delivered magic. Every corner of my home now has a story and a purpose.", 1),
                (4, "Vikram Nair", "Delhi", 5, "Our home office makeover has genuinely changed how I work. The space is so calming yet energizing.", 1),
                (5, "Kavya Reddy", "Chennai", 5, "They listened. Every suggestion came from a place of understanding our lifestyle. Our home reflects us perfectly.", 1),
            ]
        )
        conn.executemany(
            "INSERT OR IGNORE INTO portfolio (id, title, location, category, description, is_featured) VALUES (?, ?, ?, ?, ?, ?)",
            [
                (1, "The Meridian Suite", "Mumbai", "Living Room", "A warm, contemporary living space blending earthy tones with modern furniture.", 1),
                (2, "Loft Minimal", "Pune", "Bedroom", "Clean lines and muted neutrals for a calming urban retreat.", 0),
                (3, "Verde Living", "Bangalore", "Full Home", "A biophilic design concept weaving nature into every room.", 1),
                (4, "Terracotta Home", "Hyderabad", "Kitchen & Dining", "Rich terracotta hues and handcrafted tiles in a family dining space.", 0),
                (5, "The Ivory Penthouse", "Delhi", "Full Home", "Luxurious ivory and gold tones across a sprawling penthouse apartment.", 1),
            ]
        )
    print("Seeded successfully.")

if __name__ == "__main__":
    seed()
