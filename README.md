# Event_ticket_system

A Django-based web application for managing college events with separate workflows for students and organizers. Students can browse events, register for available seats, and join a waitlist when an event is full. Organizers can create and manage events, feature important listings, and track attendees from a dedicated dashboard.

## Features

- Role-based authentication for `student` and `organizer` accounts
- Student dashboard with registered events overview
- Organizer dashboard with event stats and management tools
- Event creation, editing, and deletion
- Event categories: Music, Technology, Sports, Cultural, and Workshop
- Search and category filtering on the event listing page
- Featured events section
- Seat tracking with automatic waitlist support
- Auto-promotion from waitlist when a registration is cancelled
- Profile page for each logged-in user
- Image uploads for events and user avatars

## Tech Stack

- Python 
- Django  
- SQLite
- HTML, CSS, and Django Templates

## Project Structure

```text
Event_ticket_system/
|-- README.md
|-- event_organizer/
|   |-- manage.py
|   |-- db.sqlite3
|   |-- event_organizer/     # Django project settings and root URLs
|   |-- events/            # Main application: models, views, routes
|   |-- templates/         # Shared templates
|   |-- static/            # CSS and frontend assets
|   \-- media/             # Uploaded event images
\-- venv/                  # Local virtual environment
```

## Core Workflows

### Student

- Sign up and log in
- Browse all events
- Search by title and filter by category
- Open an event detail page
- Register for available events
- Join the waitlist when an event is full
- Cancel a registration from `My Events`
- View a personal dashboard and profile

### Organizer

- Sign up and log in as an organizer
- Create events with title, description, date, venue, category, image, capacity, and featured status
- View an organizer dashboard with total events and total registrations
- Edit or delete events they created
- View attendee and waitlist details for each event

## Data Model Overview

The application centers around four main models:

- `Event`: stores event details, category, capacity, creator, image, and featured status
- `Registration`: links students to events they have joined
- `Waitlist`: stores students waiting for a seat when an event is full
- `Profile`: extends Django's built-in `User` model with role, bio, and avatar

Profiles are created automatically whenever a new user account is created.

## Getting Started

### 1. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install Django==6.0.2 Pillow==12.1.1
```

### 3. Move into the Django project directory

```bash
cd event_organizer
```

### 4. Apply migrations

```bash
python manage.py migrate
```

### 5. Create an admin account (optional)

```bash
python manage.py createsuperuser
```

### 6. Start the development server

```bash
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in your browser.

## Main Routes

- `/` -> redirects to login
- `/login/` -> login page
- `/signup/` -> account creation page
- `/events/` -> event listing page
- `/dashboard/student/` -> student dashboard
- `/organizer-dashboard/` -> organizer dashboard
- `/create-event/` -> create a new event
- `/profile/` -> profile page
- `/admin/` -> Django admin panel

## Media and Static Files

- Uploaded event and profile images are stored in `event_organizer/media/`
- Static assets are stored in `event_organizer/static/`
- In development, Django is configured to serve both static and media files

## Useful Commands

Run system checks:

```bash
python manage.py check
```

Run tests:

```bash
python manage.py test
```

Note: the current automated test suite is minimal and can be expanded.

## Current Highlights

- Role-aware dashboards keep the student and organizer experience separate
- Waitlist handling improves registration flow for full events
- Organizer tools make it easy to manage capacity and attendees

## Future Improvements

- Add stronger form validation and friendlier error handling
- Add email notifications for registrations and waitlist promotion
- Expand automated test coverage
- Add richer analytics for organizers
- Improve profile editing from the UI

## License

This project is currently unlicensed. Add a license if you plan to publish or share it publicly.
