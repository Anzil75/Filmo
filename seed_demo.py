# seed_demo.py — fills FILMO with believable sample data for your demo.
#
#   Add the demo data :   venv\Scripts\python.exe seed_demo.py
#   Remove it again   :   venv\Scripts\python.exe seed_demo.py remove
#
# Everything it creates is tagged with  demo: True  in the database, so
# "remove" can delete exactly the demo data and nothing else. Your own
# accounts (admin@filmo.com, maker@filmo.com, star@filmo.com) and anything
# you made by hand are never touched.
#
# Running it twice is safe — it clears the old demo data first, then rebuilds.

import sys
from datetime import datetime, timedelta, timezone

from werkzeug.security import generate_password_hash

from firebase_config import db

PASSWORD = "demo123"        # every demo account uses this one password


def days_ago(n):
    """A timestamp n days in the past, in the same format app.py uses."""
    return (datetime.now(timezone.utc) - timedelta(days=n)).isoformat()


# ============================ THE DEMO DATA ============================
# Film makers. status decides what the admin sees:
#   approved -> can log in;  pending -> waiting on the requests page;
#   rejected -> shows in the "previously rejected" section.
FILMMAKERS = [
    {"email": "ravi@filmo.com", "name": "Ravi Menon", "phone": "9847011001",
     "company": "Menon Motion Pictures", "experience": "14", "city": "Kochi",
     "status": "approved", "days": 40},
    {"email": "fathima@filmo.com", "name": "Fathima Basheer", "phone": "9847011002",
     "company": "Backwater Films", "experience": "6", "city": "Alappuzha",
     "status": "approved", "days": 22},
    {"email": "george@filmo.com", "name": "George Thomas", "phone": "9847011003",
     "company": "Highrange Studios", "experience": "3", "city": "Thodupuzha",
     "status": "pending", "days": 2},
    {"email": "sneha@filmo.com", "name": "Sneha Pillai", "phone": "9847011004",
     "company": "Firstcut Creations", "experience": "1", "city": "Kollam",
     "status": "pending", "days": 1},
    {"email": "vinod@filmo.com", "name": "Vinod Kumar", "phone": "9847011005",
     "company": "Unknown Productions", "experience": "0", "city": "Kannur",
     "status": "rejected", "days": 15},
]

# Performers, each with a few talent videos on their profile.
PERFORMERS = [
    {"email": "meera@filmo.com", "name": "Meera Krishnan", "phone": "9846022001",
     "age": "24", "gender": "Female", "city": "Thrissur",
     "skills": "Acting, Mohiniyattam, Carnatic singing",
     "bio": "Five years with a theatre group in Thrissur. Trained in Mohiniyattam "
            "since I was seven. Comfortable acting in Malayalam and English.",
     "days": 35,
     "talents": [
         ("Mohiniyattam solo", "Dancing", "https://www.youtube.com/watch?v=demo-meera-dance",
          "A four-minute classical piece performed at the Thrissur temple festival.", 30),
         ("Monologue from Chemmeen", "Acting", "https://www.youtube.com/watch?v=demo-meera-act",
          "The scene where Karuthamma says goodbye to the shore.", 18),
         ("Carnatic varnam", "Singing", "https://www.youtube.com/watch?v=demo-meera-sing",
          "Recorded at home with a tanpura backing.", 9),
     ]},
    {"email": "arjun@filmo.com", "name": "Arjun Nair", "phone": "9846022002",
     "age": "27", "gender": "Male", "city": "Kochi",
     "skills": "Acting, Stunts, Kalaripayattu",
     "bio": "Trained stunt performer turned actor. Six short films so far. "
            "I do my own action scenes and I swim well.",
     "days": 33,
     "talents": [
         ("Kalaripayattu demo", "Stunts / Action", "https://www.youtube.com/watch?v=demo-arjun-kalari",
          "Two minutes of stick and sword forms, shot in one take.", 28),
         ("Angry father scene", "Acting", "https://www.youtube.com/watch?v=demo-arjun-act",
          "A quiet argument that slowly turns into a shout.", 12),
     ]},
    {"email": "anjali@filmo.com", "name": "Anjali Rajan", "phone": "9846022003",
     "age": "22", "gender": "Female", "city": "Kozhikode",
     "skills": "Acting, Comedy, Mimicry",
     "bio": "College theatre lead. I write and perform my own comedy sketches "
            "and I can mimic about thirty voices.",
     "days": 20,
     "talents": [
         ("Stand-up set, five minutes", "Comedy", "https://www.youtube.com/watch?v=demo-anjali-comedy",
          "Performed at the college arts festival. Malayalam with some English.", 16),
         ("Thirty voices in two minutes", "Other", "https://www.youtube.com/watch?v=demo-anjali-mimicry",
          "Mimicry reel - actors, politicians and one very unhappy cat.", 6),
     ]},
    {"email": "hari@filmo.com", "name": "Hari Sankar", "phone": "9846022004",
     "age": "31", "gender": "Male", "city": "Thiruvananthapuram",
     "skills": "Acting, Playback singing, Guitar",
     "bio": "Radio jockey for four years. Looking for character roles. "
            "I sing and play guitar, so music videos are welcome too.",
     "days": 14,
     "talents": [
         ("Original song, acoustic", "Music", "https://www.youtube.com/watch?v=demo-hari-song",
          "My own composition, guitar and voice only.", 11),
     ]},
    {"email": "divya@filmo.com", "name": "Divya Menon", "phone": "9846022005",
     "age": "19", "gender": "Female", "city": "Palakkad",
     "skills": "Modelling, Bharatanatyam",
     "bio": "First year student. New to all this but I have modelled for two "
            "local clothing brands.",
     "days": 5,
     "talents": []},          # deliberately empty - shows the "no videos yet" page
]


# ============================ REMOVING ============================
def remove_demo():
    """Delete every document that was tagged demo: True."""
    removed = {}
    for name in ("talents", "users"):
        count = 0
        for doc in db.collection(name).stream():
            if doc.to_dict().get("demo") is True:
                db.collection(name).document(doc.id).delete()
                count += 1
        removed[name] = count
    return removed


# ============================ CREATING ============================
def add_demo():
    hashed = generate_password_hash(PASSWORD)   # hash once, reuse for every account

    for m in FILMMAKERS:
        db.collection("users").document(m["email"]).set({
            "name": m["name"], "email": m["email"], "password": hashed,
            "phone": m["phone"], "company": m["company"],
            "experience": m["experience"], "city": m["city"],
            "role": "filmmaker", "status": m["status"],
            "created_at": days_ago(m["days"]), "demo": True,
        })

    for p in PERFORMERS:
        db.collection("users").document(p["email"]).set({
            "name": p["name"], "email": p["email"], "password": hashed,
            "phone": p["phone"], "age": p["age"], "gender": p["gender"],
            "skills": p["skills"], "city": p["city"], "bio": p["bio"],
            "role": "user", "created_at": days_ago(p["days"]), "demo": True,
        })
        for title, category, url, description, days in p["talents"]:
            db.collection("talents").add({
                "user_email": p["email"], "user_name": p["name"],
                "title": title, "category": category, "description": description,
                "video_url": url, "created_at": days_ago(days), "demo": True,
            })

    return (len(FILMMAKERS) + len(PERFORMERS),
            sum(len(p["talents"]) for p in PERFORMERS))


# ============================ RUN IT ============================
if __name__ == "__main__":
    wants_removal = len(sys.argv) > 1 and sys.argv[1].lower() in ("remove", "clear", "delete")

    print()
    print("Clearing any previous demo data...")
    gone = remove_demo()
    print("  removed: {users} accounts, {talents} talent videos".format(**gone))

    if wants_removal:
        print()
        print("Demo data removed. Your own accounts and data are untouched.")
        print()
        raise SystemExit

    print()
    print("Adding fresh demo data...")
    people, talents = add_demo()
    print("  added: {} accounts, {} talent videos".format(people, talents))

    print()
    print("=" * 62)
    print("  FILMO is ready to demo.  Every demo password is:  " + PASSWORD)
    print("=" * 62)
    print("  Admin        admin@filmo.com / admin123")
    print("  Film maker   ravi@filmo.com      (approved, can browse performers)")
    print("  Film maker   fathima@filmo.com   (approved)")
    print("  Performer    meera@filmo.com     (3 talent videos)")
    print("  Performer    arjun@filmo.com     (2 talent videos)")
    print("  Performer    divya@filmo.com     (no videos yet - shows the empty page)")
    print()
    print("  Nice things to show off:")
    print("   - Admin has 2 film maker requests waiting, and 1 rejected earlier.")
    print("   - Log in as Ravi, press Browse performers, then View profile on")
    print("     Meera to see her details and all three of her videos.")
    print("   - The admin can open the same profiles from the Performers page.")
    print("   - Divya has no videos, to show the empty state.")
    print()
    print("  To take all of this back out again:")
    print("   venv\\Scripts\\python.exe seed_demo.py remove")
    print()
