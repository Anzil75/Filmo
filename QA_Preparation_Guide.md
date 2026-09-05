# 🎓 FILMO Project — Viva / QA Preparation Guide

*A mock question-and-answer sheet for your project review. Read the answers, then say them in **your own words** — don't memorise word-for-word. If you understand the idea, you can answer whatever way the question is asked.*

**Your project in one line:** *FILMO — a talent showcase platform* — a website (built with **Python + Flask + Firebase**) where **performers** put videos of their talent on their profile, **film makers** browse those profiles to find people for their projects, and an **admin** decides which film makers are allowed in.

---

## PART 1 — Project Overview

**Q1. Tell me about your project.**
> "My project is called FILMO. It's a talent showcase website that connects performers with film makers. Performers — actors, dancers, singers — make a profile and add videos of their talent to it. Film makers browse those profiles, watch the videos, and contact the people they're interested in. An admin approves the film makers and oversees the platform."

💡 *Tip: keep the first answer short and confident. They'll ask follow-ups — let them.*

**Q2. What are the modules / types of users?**
> "There are three modules:
> - **Admin** – approves or rejects film maker requests, views all approved film makers, and views every performer and their talent videos.
> - **Film Maker** – registers, waits for admin approval, then browses performer profiles and watches their talent videos.
> - **Performer** – registers, views and updates their profile, and adds or removes talent videos."

**Q3. What problem does your project solve?**
> "Talented people, especially outside the cities, have no easy way to be seen by film makers — it usually happens through personal contacts. FILMO gives them one place to put their videos where film makers are actually looking, and gives film makers one place to search instead of relying on who they happen to know."

**Q4. Why did you choose this project?**
> "It solves a real problem I found interesting, and it let me practise building a complete system — registration, login, different user roles, an approval process, and a cloud database."

**Q5. Why is it called FILMO?**
> "It's short for film, and it's easy to remember. The tagline is 'Where Talent Meets Opportunity'."

---

## PART 2 — Programming Languages & Tools

**Q6. What programming languages did you use?**
> "**Python** for the backend (the logic), and **HTML + CSS** for the frontend (what the user sees). I also used **Jinja2**, which lets me put Python data into my HTML pages."

**Q7. What framework did you use, and why?**
> "I used **Flask**, a Python web framework. I chose it because it's lightweight and beginner-friendly — it lets me build a full website with less code, and I can understand every line of it."

💡 *A "framework" = a ready-made toolbox that handles the common parts of building a website, so you focus on your own features.*

**Q8. What tools and libraries did you use?**
> "- **Flask** – the web framework
> - **firebase-admin** – connects my Python code to the Firebase database
> - **Werkzeug** – for securely hashing passwords (it comes with Flask)
> - **Bootstrap 5** – for the design and styling"

**Q9. What software did you use to write the code?**
> "**Visual Studio Code** as my editor, and I run the project with Python inside a virtual environment."

**Q10. How big is your project?**
> "The whole backend is one file, `app.py`, about 450 lines with 19 routes. There are 18 HTML templates, and two small helper files — `firebase_config.py` for the database connection and `seed_demo.py` which fills the site with sample data for a demo."

---

## PART 3 — Frontend

**Q11. What did you use for the frontend / design?**
> "**HTML** for the structure and **Bootstrap** for the styling. Bootstrap gives ready-made buttons, cards, tables and forms that already look good, and it makes the site work on mobile. I also wrote a few lines of my own CSS for the purple banner on the home page and FILMO's gold colour."

**Q12. What is Bootstrap?**
> "Bootstrap is a free **CSS framework** — a collection of pre-made design pieces like buttons, cards and navigation bars. I added it with a **CDN link**, which means I linked to it online instead of downloading it."

**Q13. How do you show data (like a user's name) on a web page?**
> "I use **Jinja2**, Flask's templating engine. In the HTML I write a placeholder like `{{ performer.name }}`, and Flask fills in the real value from the database when the page loads."

**Q14. What is `base.html` / template inheritance?**
> "I made one base template holding everything that's the same on every page — the navigation bar, the message area and the footer. All the other pages **extend** it and only fill in their own content block. So I wrote the navbar once instead of 18 times, and if I change it, it changes everywhere."

**Q15. How do you show success and error messages?**
> "I use Flask's **flash messages**. In Python I write `flash("Talent video added!", "success")`, and `base.html` displays any waiting messages at the top of the page as a coloured Bootstrap alert — green for success, red for errors. The category I pass becomes the Bootstrap colour class."

**Q16. Is your website responsive (does it work on phones)?**
> "Yes. Because I used Bootstrap's grid system, the layout automatically adjusts to phones, tablets and computers."

**Q17. Did you use JavaScript?**
> "Barely any of my own. Bootstrap's JavaScript file handles the little ✕ that closes a message. Everything else — every form and every button — works with plain HTML forms and Python, because I wanted to be sure I understood the whole flow myself."

💡 *This is a good, honest answer. Don't claim JavaScript you didn't write.*

---

## PART 4 — Backend

**Q18. Explain the backend of your project.**
> "The backend is written in **Python using Flask** — it's the brain of the website. When a user does something, like submitting the login form, the browser sends a request to my Flask app. The app runs the matching function, checks whether that person is allowed, talks to the database if needed, and sends back a finished web page."

**Q19. What is a route?**
> "A **route** is a URL path connected to a Python function. For example `/login` is a route — when someone visits it, Flask runs my login function. I create routes with the `@app.route()` decorator. My project has 19 of them."

**Q20. What is the difference between GET and POST?**
> "**GET** is for viewing a page — opening the login form. **POST** is for sending data to the server — submitting that form. My forms use POST, and inside the function I check `if request.method == "POST"` to know which one happened. That's why one function can both show a form and save it."

**Q21. How does the login system work?**
> "When someone enters their email and password, my app looks that email up in the users collection. If there's no account, it says so. If there is, it checks the password against the stored hash. If it's a film maker, it also checks whether the admin has approved them. If everything's fine, I save their email, name and role in a **session** and send them to the dashboard for their role."

**Q22. What is a session?**
> "A session is how the website **remembers who is logged in** as you move from page to page. After login, Flask stores my details in it so I don't have to log in again on every page, and the navbar can greet me by name. Logging out clears it."

**Q23. What is the secret key for?**
> "Flask stores the session in a cookie in the browser, and it uses the secret key to **sign** that cookie. Without it, somebody could edit the cookie and change their own role to admin. With it, any tampering breaks the signature and Flask throws the session away."

**Q24. How do you handle the three different roles?**
> "When someone registers I save a **role** field — `admin`, `filmmaker` or `user`. At login I put that role in the session. Every protected page checks it before showing anything. I wrote a helper function called `require_role` so that check is one line at the top of each page."

**Q25. What stops a performer from just typing `/admin/users` in the address bar?**
> "The `require_role` check. Hiding a link isn't security — the page itself checks the session role every time it's opened, and if the role is wrong it redirects them to login with a warning. It doesn't matter how they got to the address."

💡 *This is a favourite question. The point to make: **every page checks for itself.***

**Q26. How does data flow from a form to the database?**
> "The user fills in a form and submits it as a POST. Flask hands me the values through `request.form`, my Python code checks them and tidies them up, and then I save them to Firebase with the firebase-admin library. To show the data again, I read it back from Firebase and pass it into a template."

**Q27. Do you validate the data people type in?**
> "Yes, in two layers. In the HTML I use `required` and `type="email"` so the browser catches empty and malformed fields straight away. Then in Python I check again — a video needs a title, a profile name can't be blank, a video link has to start with http:// or https://, and a registration email must not already exist. Browser checks can be bypassed, so the Python checks are the ones that really count."

**Q28. What are those `<email>` and `<talent_id>` parts in your URLs?**
> "They're **variable parts of the address**. `/performer/<email>` is one route that works for every performer — Flask pulls the email out of the address and passes it into my function as a parameter, and the function looks up that person. So I didn't need a separate page per performer."

**Q29. What happens if someone visits a page that doesn't exist?**
> "I wrote **error handlers** for 404 and 500 using `@app.errorhandler`. Instead of Flask's blank white error page, the visitor gets a proper FILMO page with the navigation bar and a friendly explanation."

---

## PART 5 — Database

**Q30. What database did you use?**
> "**Firebase Firestore**, a cloud database from Google. It's a **NoSQL** database — it stores data as *documents* with fields, instead of tables with rows and columns."

**Q31. What is Firebase / Firestore?**
> "Firebase is a platform by Google for building apps, and Firestore is its database. It stores the data **in the cloud**, so I don't have to install or run a database on my own computer. My Python code connects to it with the **firebase-admin** library."

**Q32. What is the difference between SQL and NoSQL? Why did you choose NoSQL?**
> "**SQL** databases like MySQL store data in **tables** with fixed columns — every row must have the same shape. **NoSQL** databases like Firestore store **documents**, and documents in the same collection can have different fields. I chose Firestore because it's quick to set up, keeps my data online, and the flexible shape suited my project — my performers and film makers are both users but they store different details."

**Q33. How is your data organised? (Data model)**
> "Firestore uses **collections** (categories) and **documents** (individual records). I have just two collections:
> - **users** – every admin, film maker and performer, told apart by a `role` field
> - **talents** – the talent videos, each one storing the email of the performer it belongs to"

**Q34. Why are all three roles in one collection?**
> "Because they're all people who log in. Keeping them together means one login function handles everybody — I just read the `role` field to know who they are. If I'd made three collections I'd have written the same login code three times."

**Q35. How are the two collections linked?**
> "Each talent video stores the performer's email in a `user_email` field. To show one performer's videos I fetch the talents and keep the ones whose `user_email` matches that person. In SQL that would be a **foreign key** — here it's just a field I match on."

**Q36. How do you save and read data from the database?**
> "With the firebase-admin library. To save I use `db.collection('users').document(email).set({...})`. To read one record I use `.get()`, and to loop through all of them I use `.stream()`. To change some fields I use `.update()`, and to remove a record `.delete()`."

**Q37. Why is a user's document id their email, but a talent video's id is random?**
> "An email is already unique, and it's the thing I always know when I need to look someone up — so making it the document id means login is one direct lookup instead of searching through everyone. A talent video has no unique natural name — two performers could both call one 'Monologue' — so I use `.add()` and let Firestore generate the id. The page remembers that id so the Delete button knows which video to remove."

💡 *This is a strong answer because it shows you made a **decision**, not just followed a tutorial.*

**Q38. What is CRUD? Did you use it?**
> "CRUD means **Create, Read, Update, Delete** — the four basic database actions. All four are in FILMO:
> - **Create** – registering an account, adding a talent video
> - **Read** – login, browsing performers, opening a profile, the dashboard counts
> - **Update** – a performer editing their profile, the admin approving or rejecting a film maker
> - **Delete** – a performer removing one of their own talent videos"

---

## PART 6 — Security

**Q39. How do you store passwords? Are they safe?**
> "I **never store passwords as plain text**. I use `generate_password_hash`, which turns the password into a long scrambled code called a **hash**. When someone logs in, I hash what they typed and compare the two hashes. So even if someone got into my database, they couldn't read anyone's password."

**Q40. What is password hashing?**
> "Hashing turns a password into a fixed scrambled string that **can't be reversed** back into the original. It's like blending fruit into juice — you can't get the fruit back. At login the system hashes what you typed and checks whether it matches the stored hash."

**Q41. Why do film makers need approval but performers don't?**
> "Because film makers are the ones **looking at** other people's personal details — a performer's age, city and phone number are on their profile. So film makers get checked by the admin first. A performer joining is exactly what the platform wants, so they get in straight away. Only the people who view others need vetting."

💡 *This is the most distinctive idea in your project. Be ready for it — and notice it's a design decision you can defend, not just a feature.*

**Q42. How exactly is an unapproved film maker blocked?**
> "When a film maker registers, their document is saved with `status: 'pending'`. In the login function, after the password is checked, I check the status — pending or rejected and they're sent back to the login page with a message explaining why. Only `approved` gets a session. Blocking them at the front door means there's no page anywhere on the site they can reach, including pages I add later."

**Q43. How do you stop a user from deleting someone else's video?**
> "The delete route checks ownership. Before deleting, it reads the video and compares its `user_email` with the email in the session — if they don't match, it refuses and says 'You can only remove your own videos.' Being logged in as a performer isn't enough; you have to own that particular video."

💡 *Have this one ready. It's the question that separates "I made pages" from "I thought about security."*

**Q44. How do you protect the admin pages?**
> "Every admin route starts with `require_role('admin')`, which checks the session role and redirects anyone else to the login page with a warning."

**Q45. What is the serviceAccountKey file?**
> "It's a **secret key file** from Firebase that lets my Python app connect to my database — like a password for the app itself. I keep it private and never upload it. It's listed in my `.gitignore` so it can't be committed by accident."

---

## PART 7 — "How does it work?" (Flow questions)

**Q46. Walk me through what happens when a performer adds a talent video.**
> "They open **Add talent video** and fill in a title, pick a category from the dropdown, write a short description and paste the video link. When they submit, my app checks they're logged in as a performer, checks the title isn't empty and that the link starts with http:// or https://. Then it saves a new document in the **talents** collection with their email and name, the details, and the current date and time. It flashes 'Talent video added!' and shows them their updated list of videos."

**Q47. Walk me through what a film maker does.**
> "They register, and their account sits as pending until the admin approves it. Once approved they log in and land on their dashboard, which shows how many performers and how many videos are on the platform. They click **Browse performers** and get a table of everyone — name, age, gender, city and skills. They press **View profile** on somebody, and they see that performer's full details, their phone number, and every talent video they've uploaded, with a link to watch each one."

**Q48. Walk me through what the admin does.**
> "The admin logs in and sees four counts on the dashboard — film maker requests waiting, approved film makers, performers, and total talent videos. On **Film maker requests** they see everyone waiting, with their company and years of experience, and an Accept and a Reject button on each. Pressing Accept sets that person's status to approved so they can log in; Reject sets it to rejected and they're told so at login. The admin can also see all approved film makers, and all performers — and open any performer's profile to see their videos."

**Q49. Does the admin see the same profile page as the film maker?**
> "Yes — it's one route, `/performer/<email>`, shared by both. Rather than build two nearly identical pages, I let the one page allow both roles, and only the Back button changes depending on who's looking. Less code and no risk of the two versions drifting apart."

**Q50. How is the admin account created? Can anyone register as an admin?**
> "No — there's no admin option on the registration page at all, so nobody can make themselves an admin through the website. I created the single admin account by running a small script called `seed_admin.py` once, which writes that one document with the role set to admin."

**Q51. What are the dashboard numbers, and where do they come from?**
> "They're counted live from the database each time the page loads. For the admin dashboard I read the users collection once and then count the different kinds — pending film makers, approved film makers, performers — and count the talents collection for the total videos. Reading once and counting in Python is faster than asking the database a separate question for each number."

---

## PART 8 — Reflective Questions

**Q52. What challenges did you face?**
> "I'm new to coding, so at first I couldn't see how the frontend, the backend and the database fitted together. Setting up Firebase and getting the login and the roles right took the longest. What helped was building it in small steps and testing each piece before moving on."

**Q53. How are the talent videos stored? Are they uploaded to your server?**
> "They're **links**, not uploaded files — a performer pastes a YouTube or Google Drive link and I store that address in a `video_url` field. I did it that way because video files are very large, and storing and streaming them properly needs paid cloud storage. Since it's the address that's stored, upgrading to real uploads later would only mean changing the one part of the code that handles that field."

💡 *Answer this confidently. It's a sensible engineering decision with a real reason, not a shortcut — say the reason.*

**Q54. What are the limitations of your project?**
> "It's a basic system. Videos are links rather than uploaded files. There are no email or SMS notifications, so a film maker has to be told by phone that they've been approved. There's no search or filter on the performers list yet — a film maker sees everyone and scrolls. The admin account is created by a script rather than through the site. And there's no messaging inside FILMO; a film maker contacts a performer using the phone number on their profile."

💡 *Knowing your own limitations makes you look more competent, not less. Say them calmly.*

**Q55. What future improvements would you make?**
> "Search and filters on the performers list — by city, age or skill, which is the first thing a real film maker would want. Real video uploads. Email notifications when a film maker is approved. A messaging feature so film makers and performers can talk inside the site. And hosting it online so it isn't only on my laptop."

**Q56. Is your project hosted online?**
> "Not yet — it runs locally with Flask's development server on port 5001. It could be deployed later on something like PythonAnywhere, Render or Heroku. The database is already in the cloud, so only the Flask part would need hosting."

**Q57. Why port 5001 and not 5000?**
> "5000 is Flask's default, but my other project is already using it. Running FILMO on 5001 means both can run at the same time without clashing. It's set in the last line of `app.py`."

**Q58. If you built it again, what would you do differently?**
> "I'd add the search and filters from the start, because a browse list only works while there are a few dozen performers. And I'd split `app.py` into a few smaller files by module, since one 450-line file is fine now but would get hard to navigate as it grows."

---

## PART 9 — Rapid-fire one-liners (short, confident answers)

- **Backend language?** → Python
- **Framework?** → Flask
- **Database?** → Firebase Firestore (NoSQL, cloud)
- **Frontend?** → HTML + Bootstrap 5 (CSS)
- **How data gets into pages?** → Jinja2 templates (`{{ }}`)
- **How many routes?** → 19, plus two error handlers
- **How many collections?** → Two — `users` and `talents`
- **How many modules?** → Three — admin, film maker, performer
- **How users stay logged in?** → Sessions
- **How passwords are kept safe?** → Hashing with Werkzeug
- **How Python talks to the database?** → the firebase-admin library
- **What tells the three roles apart?** → a `role` field on each user document
- **What blocks an unapproved film maker?** → a `status` field checked during login
- **How you run it?** → `python app.py`, then open `127.0.0.1:5001` in the browser
- **What is a virtual environment (venv)?** → a separate space for this project's Python libraries so they don't mix with other projects
- **What is localhost / a port?** → the site running on my own computer; the port is the "door number" it answers on

---

## PART 10 — Tips for the QA session

1. **Answer in your own words.** Understanding beats memorising — you'll handle any wording of the question.
2. **Keep the first answer short**, then let them ask follow-ups. Don't recite everything at once.
3. **If you don't know something, be honest:** "I'm not sure, but I think it works like… / I'd find out by…" — far better than guessing wildly. Nobody expects you to know everything.
4. **Have the project running before you start**, with the demo data loaded, so you can show a flow instead of describing it.
5. **Know your data flow cold:** Browser → Flask (Python) → Firebase database → back to an HTML page. If you can explain that, you can explain the whole project.
6. **Lead with the approval workflow if you get the chance.** It's the most thoughtful part of FILMO — a film maker can't get in until the admin lets them, because film makers see other people's personal details. It shows you thought about *why*, not just *how*.

### Demo accounts to use

| Role | Email | Password |
|---|---|---|
| Admin | `admin@filmo.com` | `admin123` |
| Film maker (approved) | `ravi@filmo.com` | `demo123` |
| Film maker (still pending) | `george@filmo.com` | `demo123` |
| Performer (3 videos) | `meera@filmo.com` | `demo123` |
| Performer (no videos yet) | `divya@filmo.com` | `demo123` |

*(Full list, including your own permanent accounts, is in `LOGINS.txt`.)*

### A five-step demo that shows everything

1. **Home page** — walk through the four steps of how FILMO works.
2. **Log in as a performer** (`star@filmo.com` / `star123`, which starts empty) — add a talent video and show it appear on "My talent videos".
3. **Log in as Ravi**, an approved film maker — Browse performers → View profile on Meera → her details, her three videos, her phone number.
4. **Log in as the admin** — Film maker requests → accept George. Then Performers → open the same profile the film maker saw.
5. **Try to log in as George** *before* accepting him — the site blocks him and explains why. This is the moment to explain the approval workflow.

---

## 📌 Tech Stack Cheat Sheet (memorise this table)

| Part | What I used |
|------|-------------|
| Backend language | Python |
| Web framework | Flask |
| Frontend | HTML, Bootstrap 5 (CSS) |
| Templating | Jinja2 |
| Database | Firebase Firestore (NoSQL, cloud) |
| DB connection | firebase-admin library |
| Login / security | Flask sessions + password hashing (Werkzeug) |
| Editor | VS Code |
| Runs on | `127.0.0.1:5001` |

**You've got this. 💪 Read it through a couple of times, then do one practice run-out-loud with the site open in front of you, and you'll be ready.**
