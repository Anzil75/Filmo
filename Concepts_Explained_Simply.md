# 🧠 FILMO Project — Key Concepts Explained Simply

*Plain-language explanations of the main technologies in your project, with everyday comparisons and examples from your own code.*

**What FILMO is, in one line:** a **talent showcase** website where performers put videos of their talent on their profile, approved film makers browse those profiles to find people for their projects, and an admin decides which film makers are allowed in.

---

## 1. Flask — the "brain" of the website

**What it is:** Flask is a **web framework** for Python. A framework is a ready-made starter kit that handles the boring, repetitive parts of building a website, so you only write your own features.

**Everyday comparison:** Building a website from zero is like building a car engine yourself. Flask hands you the engine already built — you just add the seats and steering (your features).

**Its role in your project — it's the middle-man:**
1. Listens for what the user does in the browser (clicks a link, submits a form).
2. Runs your Python code to decide what to do.
3. Talks to the database if needed.
4. Sends back the correct web page.

**Why Flask and not something else (Django, PHP, Node.js)?**
- It uses **Python**, one of the easiest languages to read — perfect for a beginner.
- It's **lightweight** — small and simple, you learn only what you need.
- Bigger frameworks (like Django) come with lots of extra features you don't need for a college project. Flask keeps things simple.

**Example from your code:** `@app.route("/login")` means *"when someone visits the /login page, run this function."* Your whole website is **19 of these routes** in one file, `app.py`.

---

## 2. Routes — the map of your website

**What a route is:** a **web address joined to a Python function**. The address is what the visitor types or clicks; the function is what actually happens.

**Everyday comparison:** Like the **door numbers in a building**. `/login` is one door, `/admin/dashboard` is another. Flask is the receptionist who reads the number and sends you to the right room.

**Your 19 routes, grouped by who they belong to:**

| Group | Routes |
|---|---|
| **Public** (anyone) | `/` home, `/register` choose type, `/register/user`, `/register/filmmaker`, `/login`, `/logout` |
| **Performer** | `/user/dashboard`, `/profile`, `/user/talents`, `/user/talents/add`, `/user/talents/<id>/delete` |
| **Film maker** | `/filmmaker/dashboard`, `/filmmaker/performers` |
| **Admin** | `/admin/dashboard`, `/admin/filmmaker-requests`, `/admin/filmmaker-requests/<email>/<action>`, `/admin/filmmakers`, `/admin/users` |
| **Shared** | `/performer/<email>` — a performer's profile and videos, opened by **film makers and the admin both** |

Plus **two error handlers** (404 and 500) that show a friendly page instead of a blank white screen when something goes wrong.

**Notice the `<email>` and `<id>` bits.** Those are **variable parts of the address**. `/performer/meera@filmo.com` and `/performer/arjun@filmo.com` are the same route running the same function — the email is handed to the function as a parameter, and the function looks up that person. One route serves every performer.

---

## 3. Bootstrap — ready-made styling

**First, clear up one thing:** **CSS** is the *language* that styles web pages (colours, sizes, spacing). **Bootstrap is NOT a separate language** — it's a big **collection of ready-made CSS** that professionals already wrote, which you just reuse.

**Everyday comparison:**
- Writing CSS by hand = **stitching your own clothes** from raw cloth.
- Using Bootstrap = **buying ready-made clothes** that already look good and fit — you just pick and wear them.

**What it does in your project:** it gives you the dark navigation bar, the cards, the tables, the forms and the coloured badges — without writing pages of styling code. You just add a *class name* and you instantly get a styled element:
```html
<button class="btn btn-warning">Login</button>   <!-- instantly a gold button -->
<span class="badge bg-success">approved</span>   <!-- instantly a green tag -->
```

**Why Bootstrap instead of writing all the CSS myself?**
- **Speed** — the site looks professional immediately.
- **Beginner-friendly** — you don't need to be a designer.
- **Responsive** — it automatically fits phones, tablets and computers.
- **Consistent** — everything matches and looks tidy.

**How you added it:** with a single **CDN link** in `base.html` — a link to Bootstrap hosted online, so you didn't even have to download it.

**Your own CSS on top:** there are about eight lines of custom CSS in `base.html` — the purple cinema-style banner on the home page (`.hero`), FILMO's gold colour (`.text-gold`), and the gentle lift when you hover over a card (`.hover-lift`). So you can honestly say you used Bootstrap **and** wrote a little CSS yourself.

---

## 4. Jinja2 — putting data into pages

**The problem it solves:** a plain HTML page is fixed text. But you need pages that show **different data for different people** — Meera's profile must show Meera's three videos, and Hari's must show his one. Plain HTML can't do that on its own.

**What it is:** Jinja2 is Flask's **templating engine**. It lets you put **placeholders** in your HTML that get filled with real data when the page loads.

**Everyday comparison:** a **fill-in-the-blanks form letter** (like mail-merge). You write "Dear ______," once, and the computer fills in each person's name.

**The three things Jinja2 does, with examples from your project:**

| What | Looks like | In your project |
|---|---|---|
| **Show a value** | `{{ ... }}` | `{{ session.get('name') }}` in the navbar → the logged-in person's real name |
| **Repeat something** | `{% for %}` | `{% for t in talents %}` in `view_performer.html` → one card per talent video |
| **Decide something** | `{% if %}` | `{% if talents %}` → show the video grid, otherwise show "no videos yet" |

**Template inheritance — the thing that saves you the most work.** `base.html` holds everything that's the same on every page: the `<head>`, the Bootstrap link, the navigation bar, the flash-message area and the footer. Every other page starts with `{% extends "base.html" %}` and then only fills in `{% block content %}`. That's why you have **18 templates but only wrote the navbar once**.

**A custom filter you wrote yourself.** The database stores dates in a long computer format like `2026-09-04T14:20:00+00:00`. Nobody wants to read that, so in `app.py` you made your own Jinja filter:
```python
@app.template_filter("nice_date")
def nice_date(value):
    return datetime.fromisoformat(value).strftime("%d %b %Y")
```
Now any page can write `{{ t.created_at | nice_date }}` and get **04 Sep 2026**. This is a nice thing to point at in a viva — it shows you didn't just use Flask's features, you added one.

---

## 5. The Cloud — where your data lives

**What "the cloud" means:** instead of storing data on your own computer, it's stored on **Google's computers (servers) on the internet**. "The cloud" simply means *"someone else's powerful computers, used over the internet."*

**Everyday comparison:** like keeping your photos on **Google Drive** instead of only on your phone — you can reach them from anywhere, and you don't lose them if your phone breaks.

**In your project the cloud is Firebase Firestore** (Google's cloud database). Its role:
- It **stores all your project's data online**, safely, not tied to one computer.
- Your Flask app talks to it over the internet to save and fetch data.

**Collections and documents.** Firestore doesn't use tables, rows and columns. It uses:
- a **collection** = a category (like a drawer in a filing cabinet)
- a **document** = one record inside it (like one file in that drawer)
- **fields** = the details inside that document (name, email, city…)

**FILMO uses just two collections:**

| Collection | What one document is | The fields it holds |
|---|---|---|
| **users** | one person | `name`, `email`, `password` (hashed), `phone`, `city`, `role`, `created_at` — **plus** `age`, `gender`, `skills`, `bio` for performers, or `company`, `experience`, `status` for film makers |
| **talents** | one talent video | `user_email` (whose it is), `user_name`, `title`, `category`, `description`, `video_url`, `created_at` |

**Why all three roles live in one `users` collection.** Admin, film maker and performer are all *people who log in*, so they share one collection and are told apart by a **`role` field** (`"admin"`, `"filmmaker"` or `"user"`). That means one login function handles everybody — the alternative would be three separate collections and three copies of the same login code.

**How `talents` is joined to `users`.** Each talent video stores the **email of the performer who owns it** in `user_email`. To show one performer's videos you fetch the talents and keep the ones whose `user_email` matches. In a SQL database this would be called a *foreign key*; here it's just a field you match on.

**Benefit of the cloud:** your data is **online, safe and always available** — no need to install or manage a database on your laptop.

---

## 6. Database Connection — how your app reaches the cloud

This is how your Python code connects and gets **permission** to use the cloud database.

**Everyday comparison:** to enter a locked building you need a **key / ID card**. Your app needs a key to reach Firebase. That key is the **`serviceAccountKey.json`** file you downloaded from Firebase.

**How it works, in the file `firebase_config.py` (19 lines, the shortest file in the project):**
1. It finds your secret key file sitting next to it (`serviceAccountKey.json`).
2. It uses that key to **log your app in** to Firebase (`initialize_app`).
3. It creates a `db` object — your **live connection** to the database.
4. Every other file just writes `from firebase_config import db` and can then read and write data.

So `db` is your **doorway to the cloud database**. Once connected you use `db.collection("users")…` to work with data.

**Why the key is secret:** it gives full access to your database — like a master password. That's why it's kept private and never uploaded online (it's listed in `.gitignore`).

**The four database commands you actually use:**

| Command | What it does | Where in FILMO |
|---|---|---|
| `.document(email).set({...})` | create/overwrite one document **with an id you choose** | registering a user |
| `.collection("talents").add({...})` | create a document and **let Firestore invent the id** | adding a talent video |
| `.document(email).get()` | fetch **one** document | login, opening a profile |
| `.collection("users").stream()` | loop through **all** documents | listing performers, counting for a dashboard |
| `.document(email).update({...})` | change some fields, leave the rest | editing a profile, approving a film maker |
| `.document(id).delete()` | remove a document | removing a talent video |

**Why two different ways of creating?** A user's document id is their **email**, because an email is unique and you always know it when you need to look someone up (`db.collection("users").document(email).get()` — one instant lookup, no searching). A talent video has no natural unique name — two performers could both call a video "Monologue" — so `.add()` lets Firestore generate a random id, and the page keeps that id so its Delete button knows which video to remove.

---

## 7. Login & Security — four parts

### (a) Checking who you are (login)
1. You type your email and password.
2. The app looks that email up in the **users** collection. Not there → *"No account found with that email."*
3. It checks the password against the stored hash. Wrong → *"Incorrect password."*
4. If you're a **film maker**, it also checks your `status` (see section 8).
5. All clear → your details go into the **session** and you're sent to the dashboard for your **role**.

**One neat line worth knowing.** Instead of three `if` statements deciding where to send each role, the login function does:
```python
return redirect(url_for(user["role"] + "_dashboard"))
```
The role is the text `"admin"`, `"filmmaker"` or `"user"`, so adding `"_dashboard"` builds the name of the right route — `admin_dashboard`, `filmmaker_dashboard`, `user_dashboard`. One line covers all three.

### (b) Keeping passwords safe — *hashing*
- Passwords are **never stored as real text**. When you register, the app runs your password through `generate_password_hash`, turning it into a long scrambled code (a **hash**).
- **Everyday comparison:** like putting fruit in a **blender** — you can turn fruit into juice, but you can't turn the juice back into fruit. Hashing is **one-way**.
- At login the app hashes what you typed and checks whether it matches the stored hash (`check_password_hash`). It never needs your real password back.
- **Benefit:** even if someone stole your database, they still couldn't read anyone's password.

### (c) Staying logged in — *sessions*
- After login the app saves three things in a **session**: your `email`, your `name` and your `role`.
- **Everyday comparison:** like a **wristband at an event** — you show it to move around freely instead of buying a ticket again at every door.
- This is how the site remembers you as you move between pages, and how the navbar knows to greet you by name. **Logout** removes the wristband (`session.clear()`).
- **The secret key.** `app.secret_key` in `app.py` is a long random string Flask uses to **sign** that wristband. Without it, someone could edit the cookie in their browser and change their role to `admin`. With it, any tampering breaks the signature and Flask rejects the session.

### (d) Role protection
- Some pages are only for certain roles. Before showing an admin page the app checks `session["role"]`, and if you're not an admin it redirects you away with a warning.
- Your helper function does exactly this check, and every protected page starts with the same two lines:
```python
guard = require_role("admin")   # returns a redirect if they're not allowed, else None
if guard:
    return guard
```
- **Why this matters:** hiding a link is not security. Even if the navbar never shows the admin pages to a performer, they could still *type* `/admin/users` into the address bar. The guard is what actually stops them — the page checks for itself, every single time, and never trusts that you arrived by clicking an approved link.
- **The shared profile page is the one exception.** `/performer/<email>` is allowed for **two** roles, so instead of `require_role` it checks `if session.get("role") not in ("filmmaker", "admin")`. Its Back button also changes depending on who's looking — the admin goes back to Performers, the film maker back to Browse performers.

---

## 8. The approval workflow — the most interesting idea in FILMO

**The problem:** performers put personal details on FILMO — their age, their city, their phone number. You can't let *anybody* who signs up browse all of that. But an admin can't be awake at 2am to hand-approve people either.

**The solution: a `status` field with three possible values.** A film maker's document carries `status`, and it decides what happens at login:

| `status` | Set when | What happens at login |
|---|---|---|
| `pending` | automatically, the moment they register | Blocked — *"Your film maker account is still waiting for admin approval."* |
| `approved` | the admin presses **Accept** | Let in normally |
| `rejected` | the admin presses **Reject** | Blocked — *"Sorry — your film maker request was rejected by the admin."* |

**Everyday comparison:** joining a members-only club. You fill in the form straight away, but you can't walk in until the committee says yes.

**Why the check lives in the login function.** It would be easy to think "just don't show the browse page to unapproved film makers." But the strongest place to stop someone is at the **front door** — if they never get a session at all, there is no page anywhere on the site they can reach, including any page you add in future. One check protects everything.

**Performers don't have a `status` field at all.** They get in immediately, because a performer joining is exactly what the platform wants. Only the people who *look at* others need vetting. That asymmetry is a deliberate design decision, and it's a good thing to say out loud if you're asked why the two registration forms are different.

---

## 9. CRUD — the four database actions, all four present

CRUD means **Create, Read, Update, Delete** — the four things any database application does.

| Letter | In FILMO |
|---|---|
| **Create** | registering a performer or film maker; adding a talent video |
| **Read** | the login lookup; browsing performers; opening a profile; every dashboard count |
| **Update** | a performer editing their profile; the admin changing a film maker's `status` to approved or rejected |
| **Delete** | a performer removing one of their own talent videos |

**The Delete is worth a closer look**, because it's the one place where the app has to be careful. Deleting is done by document id, and the id is sitting right there in the web address — so what stops a performer from deleting *someone else's* video by changing the id in the URL? This does:

```python
elif talent_doc.to_dict().get("user_email") != session["email"]:
    flash("You can only remove your own videos.", "danger")
```

Before deleting, the app checks that the video's owner is **the person currently logged in**. Being logged in as a performer isn't enough — you have to own that particular video. If a teacher asks "how do you know a user can't tamper with someone else's data?", this is the line to show them.

---

## 🔗 Putting it all together (the big picture)

> A visitor clicks something in the browser →
> **Flask** (Python) matches the address to one of your 19 **routes** and runs that function →
> the function checks the **session** (are you logged in? what role? are you allowed here?) →
> it reads or writes data in the **Firebase Firestore** cloud database (through the `db` connection) →
> it hands that data to a template, where **Jinja2** fills in the blanks and **Bootstrap** makes it look good →
> and the finished page goes back to the browser.

If you can say that flow out loud, you understand your whole project. 💪
