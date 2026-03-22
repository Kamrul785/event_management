#  Eventzilla — Premium Event Management Platform

> A full-featured, production-ready event management web application built with Django. Eventzilla enables organizers to create and manage events, and participants to discover and RSVP to them — all within a clean, modern interface.

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Visit%20Site-orange?style=for-the-badge&logo=vercel)](https://event-management-six-lime.vercel.app/)
[![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)](https://python.org)
[![Django](https://img.shields.io/badge/Django-5.2-green?style=for-the-badge&logo=django)](https://djangoproject.com)
[![TailwindCSS](https://img.shields.io/badge/TailwindCSS-CDN-38bdf8?style=for-the-badge&logo=tailwindcss)](https://tailwindcss.com)

---

## 🚀 Live Demo

🔗 **[https://event-management-six-lime.vercel.app/](https://event-management-six-lime.vercel.app/)**

---

## 📸 Screenshots

> Below is a visual walkthrough of the key pages in Eventzilla.

### 🏠 Home Page — Hero Section
![Home Page](https://via.placeholder.com/900x450/f97316/ffffff?text=Eventzilla+Home+Page)
> Animated gradient hero with stats counter, CTA buttons, and advanced event search.

### 📋 Event List
![Event List](https://via.placeholder.com/900x450/3b82f6/ffffff?text=Event+List+Page)
> Filter by category, date range. Each card shows image, category badge, location, and participant count.

### 📊 Organizer Dashboard
![Organizer Dashboard](https://via.placeholder.com/900x450/8b5cf6/ffffff?text=Organizer+Dashboard)
> Stats cards for total, upcoming, and past events. Today's events table and full event management table.

### 👤 Participant Dashboard
![Participant Dashboard](https://via.placeholder.com/900x450/10b981/ffffff?text=Participant+Dashboard)
> Personal RSVP stats, quick actions, and upcoming registered events.

### 🔐 Authentication Pages
![Login Page](https://via.placeholder.com/900x450/ea580c/ffffff?text=Login+%2F+Register+Pages)
> Clean sign-in and registration forms with inline validation and password strength rules.

---

## ✨ Features

### 🎭 Role-Based Access Control
- **Admin** — Full platform access: manage users, assign roles, create groups & permissions
- **Organizer** — Create/edit/delete events, view organizer dashboard with analytics
- **Participant** — Browse events, RSVP, track upcoming/past events via personal dashboard
- **User** — Default role auto-assigned on registration; public browsing allowed

### 📅 Event Management
- Create, update, and delete events with image upload support
- Filter events by category, start date, and end date
- Event detail page with full participant list
- One-click RSVP with duplicate prevention
- Participant count displayed per event

### 📂 Category Management
- Full CRUD for event categories
- Category stats (event count per category)
- Glassmorphism card UI with live search (frontend)

### 👥 Participant (User) Management
- Admin can create, update, and delete user accounts
- Annotated with event count per user
- Responsive table + card layout for mobile

### 🔐 Authentication & Security
- Custom `CustomUser` model extending `AbstractUser`
- Email-based account activation (token link via Gmail SMTP)
- Password reset via email (custom HTML template)
- Password change with strength validation (uppercase, number, special char, min 8 chars)
- Login/logout with flash messages

### 👤 Profile Management
- View profile: name, email, phone, member since, last login
- Edit profile: update name, email, phone, profile photo
- Password change from profile
- Profile photo upload (disabled on Vercel due to ephemeral filesystem)

### 🛡️ Admin Panel
- Custom admin dashboard (separate from Django's `/admin/`)
- Assign roles to users
- Create permission groups with granular permissions
- View all groups and their assigned permissions

### 📧 Email Notifications
- Account activation email on registration
- RSVP confirmation email sent to participant (via Django signals)
- Password reset email with custom HTML template

### 🎨 UI / UX
- Fully responsive (mobile-first) with Tailwind CSS
- Animated hero section, floating elements, gradient backgrounds
- Glassmorphism card effects
- Toast notifications with auto-dismiss
- Loading spinner on page load
- Back-to-top button
- Mobile navigation with hamburger menu
- Smooth scrolling and hover transitions

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3.11, Django 5.2 |
| **Database** | PostgreSQL (Supabase) / SQLite (dev) |
| **Frontend** | HTML5, Tailwind CSS (CDN), Vanilla JS |
| **Auth** | Django Auth + Custom User Model |
| **Email** | Gmail SMTP via Django email backend |
| **Storage** | Local media (dev) / Vercel ephemeral (prod) |
| **Deployment** | Vercel (serverless WSGI) |
| **ORM** | Django ORM with `select_related`, `annotate` |
| **Forms** | Django ModelForms with custom styled mixin |
| **Templates** | Django Template Language (DTL) |
| **Extras** | django-widget-tweaks, dj-database-url, python-decouple |

---

## ⚙️ Installation — Run Locally

### Prerequisites
- Python 3.11+
- pip
- Git
- (Optional) PostgreSQL if not using SQLite

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/event-management.git
cd event-management
```

### 2. Create & Activate a Virtual Environment

```bash
python -m venv event_env

# On Windows
event_env\Scripts\activate

# On macOS/Linux
source event_env/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True

# Email (Gmail SMTP)
EMAIL_HOST_USER=your-gmail@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Database (leave blank to use SQLite in dev)
# DATABASE_URL=postgresql://user:password@host:port/dbname

FRONTEND_URL=http://localhost:8000/
```

> 💡 To generate a Django secret key:
> ```bash
> python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
> ```

### 5. Apply Migrations

```bash
python manage.py migrate
```

### 6. Create Groups & Permissions (important!)

```bash
python manage.py shell
```

Inside the shell:

```python
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from events.models import Event, Category

# Create groups
admin_group, _ = Group.objects.get_or_create(name='Admin')
organizer_group, _ = Group.objects.get_or_create(name='Organizer')
participant_group, _ = Group.objects.get_or_create(name='Participant')

# Add permissions to Organizer
event_ct = ContentType.objects.get_for_model(Event)
for codename in ['add_event', 'change_event', 'delete_event', 'view_event']:
    perm = Permission.objects.get(content_type=event_ct, codename=codename)
    organizer_group.permissions.add(perm)

# Add view permission to Participant
view_event = Permission.objects.get(content_type=event_ct, codename='view_event')
participant_group.permissions.add(view_event)

print("Groups created successfully!")
exit()
```

### 7. Create a Superuser

```bash
python manage.py createsuperuser
```

### 8. (Optional) Collect Static Files

```bash
python manage.py collectstatic
```

### 9. Run the Development Server

```bash
python manage.py runserver
```

Visit **[http://127.0.0.1:8000](http://127.0.0.1:8000)** in your browser. 🎉

---

## 🔑 Demo Credentials

> These credentials work on the **live demo** at [https://event-management-six-lime.vercel.app/](https://event-management-six-lime.vercel.app/)

| Role | Username | Password |
|---|---|---|
| **Admin** | `admin` | `Admin@1234` |
| **Organizer** | `organizer` | `Organizer@1234` |
| **Participant** | `participant` | `Participant@1234` |

> ⚠️ Demo data may be reset periodically. Please don't change credentials.

---

## 📁 Folder Structure

```
event-management/
│
├── event_management/           # Django project settings
│   ├── settings.py             # Main config (DB, email, auth, static)
│   ├── urls.py                 # Root URL configuration
│   ├── wsgi.py                 # WSGI entry point (Vercel)
│   └── asgi.py
│
├── core/                       # Core app (home, no_permission views)
│   ├── views.py
│   └── templates/
│       ├── base.html           # Master layout (nav, footer, flash messages)
│       ├── home.html           # Landing page with hero + search
│       ├── logged_nav.html     # Nav for authenticated users
│       ├── non_logged_nav.html # Nav for guests
│       └── no_permission.html  # 403-style access denied page
│
├── events/                     # Events app
│   ├── models.py               # Event, Category models
│   ├── views.py                # FBVs + CBVs for events, categories, participants
│   ├── forms.py                # EventModelForm, CategoryModelForm, EventFilterForm
│   ├── urls.py
│   ├── signals.py              # RSVP confirmation email signal
│   └── templates/
│       ├── event_list.html
│       ├── event_detail.html
│       ├── event_form.html
│       ├── category_list.html
│       ├── category_form.html
│       ├── category_confirm_delete.html
│       ├── participant_list.html
│       ├── participant_form.html
│       ├── organizer_dashboard.html
│       └── participant_dashboard.html
│
├── users/                      # Users app
│   ├── models.py               # CustomUser (AbstractUser + phone + profile_image)
│   ├── views.py                # Auth views, admin dashboard, profile, groups
│   ├── forms.py                # Registration, login, password, profile forms
│   ├── urls.py
│   ├── signals.py              # Auto-assign 'User' group + activation email
│   ├── templatetags/
│   │   └── custom_filters.py   # humanized_date filter
│   └── templates/
│       ├── registration/
│       │   ├── login.html
│       │   ├── register.html
│       │   ├── reset_password.html
│       │   └── reset_email.html
│       ├── accounts/
│       │   ├── profile.html
│       │   ├── update_profile.html
│       │   ├── change_password.html
│       │   └── change_password_done.html
│       └── admin/
│           ├── dashboard.html
│           ├── user_list.html
│           ├── assign_role.html
│           ├── create_group.html
│           └── group_list.html
│
├── static/                     # Static assets (CSS, JS, images)
├── media/                      # User-uploaded files (dev only)
├── requirements.txt
├── manage.py
├── vercel.json                 # Vercel deployment config
└── .env                        # Environment variables (not committed)
```

---

## 🔮 Future Improvements

Here's what I'd build next to make Eventzilla production-grade:

- [ ] **Ticket System** — Paid tickets with Stripe integration and QR code generation
- [ ] **Event Comments & Ratings** — Let participants leave feedback after events
- [ ] **Calendar View** — Interactive calendar with drag-and-drop event scheduling
- [ ] **Real-time Notifications** — Django Channels + WebSockets for live RSVP alerts
- [ ] **Email Reminders** — Celery + Redis background tasks to send event reminders 24h before
- [ ] **Event Analytics Dashboard** — Charts (Chart.js/Recharts) for registrations over time
- [ ] **Social Login** — Google / GitHub OAuth via `django-allauth`
- [ ] **REST API** — Django REST Framework API for a future React/Next.js frontend
- [ ] **Map Integration** — Google Maps embed on event detail pages
- [ ] **Image CDN** — Cloudinary or AWS S3 for persistent media in production
- [ ] **Multi-language Support** — Django i18n for Bengali + English
- [ ] **PWA Support** — Service worker + manifest for offline access on mobile

---

## 👨‍💻 Author

**Kamrul Khan**

- 🌐 Portfolio: [your-portfolio.com](https://your-portfolio.com)
- 💼 LinkedIn: [linkedin.com/in/yourprofile](https://linkedin.com/in/yourprofile)
- 🐙 GitHub: [github.com/yourusername](https://github.com/yourusername)
- 📧 Email: kamrulkhan526785@gmail.com

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

<div align="center">
  <sub>Built with ❤️ using Django & Tailwind CSS</sub>
</div>