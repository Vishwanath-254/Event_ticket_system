from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from .models import Event, Profile, Registration, Waitlist


def _organizer_required(request):
    return request.user.profile.role == "organizer"


def _student_required(request):
    return request.user.profile.role == "student"


def _set_event_percent(event):
    if event.max_participants > 0:
        event.percent = int((event.registration_set.count() / event.max_participants) * 100)
    else:
        event.percent = 0


def _promote_waitlisted_student(event):
    next_in_line = Waitlist.objects.filter(event=event).select_related("user").first()
    if next_in_line and event.seats_left() > 0:
        Registration.objects.get_or_create(user=next_in_line.user, event=event)
        next_in_line.delete()


def signup_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        role = request.POST["role"]

        if User.objects.filter(username=username).exists():
            return render(request, "signup.html", {"error": "Username already taken"})

        user = User.objects.create_user(username=username, password=password)
        profile = Profile.objects.get(user=user)
        profile.role = role
        profile.save()

        login(request, user)

        if role == "organizer":
            return redirect("organizer_dashboard")
        return redirect("student_dashboard")

    return render(request, "signup.html")


def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    registrations = event.registration_set.count()
    seats_left = event.max_participants - registrations

    if event.max_participants > 0:
        progress = (registrations / event.max_participants) * 100
    else:
        progress = 0

    is_registered = False
    is_waitlisted = False
    if request.user.is_authenticated:
        is_registered = Registration.objects.filter(user=request.user, event=event).exists()
        is_waitlisted = Waitlist.objects.filter(user=request.user, event=event).exists()

    context = {
        "event": event,
        "registrations": registrations,
        "seats_left": seats_left,
        "progress": progress,
        "is_registered": is_registered,
        "is_waitlisted": is_waitlisted,
    }
    return render(request, "event_detail.html", context)


def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            if user.profile.role == "organizer":
                return redirect("organizer_dashboard")
            return redirect("student_dashboard")

    return render(request, "login.html")


@login_required
def logout_user(request):
    logout(request)
    return redirect("login")


@login_required
def event_list(request):
    category = request.GET.get("category")
    search = request.GET.get("search")

    events = Event.objects.all()
    if category:
        events = events.filter(category=category)
    if search:
        events = events.filter(title__icontains=search)

    featured_events = Event.objects.filter(featured=True)

    for event in events:
        _set_event_percent(event)
    for event in featured_events:
        _set_event_percent(event)

    return render(
        request,
        "event_list.html",
        {"events": events, "featured_events": featured_events},
    )


@login_required
def register_event(request, event_id):
    if not _student_required(request):
        return redirect("organizer_dashboard")

    event = get_object_or_404(Event, id=event_id)

    if Registration.objects.filter(user=request.user, event=event).exists():
        messages.info(request, f"You are already registered for {event.title}.")
        return redirect("event_detail", event.id)

    if event.seats_left() <= 0:
        _, created = Waitlist.objects.get_or_create(user=request.user, event=event)
        if created:
            messages.success(request, f"{event.title} is full, so you were added to the waitlist.")
        else:
            messages.info(request, f"You are already on the waitlist for {event.title}.")
        return redirect("event_detail", event.id)

    Registration.objects.create(user=request.user, event=event)
    Waitlist.objects.filter(user=request.user, event=event).delete()
    messages.success(request, f"Registration confirmed for {event.title}.")
    return redirect("event_detail", event.id)


@login_required
def cancel_registration(request, event_id):
    if not _student_required(request):
        return redirect("organizer_dashboard")

    event = get_object_or_404(Event, id=event_id)

    if request.method == "POST":
        deleted, _ = Registration.objects.filter(user=request.user, event=event).delete()
        Waitlist.objects.filter(user=request.user, event=event).delete()
        if deleted:
            _promote_waitlisted_student(event)
            messages.success(request, f"Your registration for {event.title} has been cancelled.")
        else:
            messages.info(request, f"No active registration found for {event.title}.")

    return redirect("my_events")


@login_required
def my_events(request):
    registrations = Registration.objects.filter(user=request.user).select_related("event").order_by("event__date")
    return render(request, "my_events.html", {"registrations": registrations})


@login_required
def organizer_dashboard(request):
    if not _organizer_required(request):
        return redirect("student_dashboard")

    events = Event.objects.filter(created_by=request.user)
    for event in events:
        _set_event_percent(event)

    total_events = events.count()
    total_registrations = Registration.objects.filter(event__created_by=request.user).count()

    context = {
        "events": events,
        "total_events": total_events,
        "total_registrations": total_registrations,
    }
    return render(request, "organizer_dashboard.html", context)


@login_required
def create_event(request):
    if not _organizer_required(request):
        return redirect("event_list")

    if request.method == "POST":
        Event.objects.create(
            title=request.POST["title"],
            description=request.POST["description"],
            date=request.POST["date"],
            venue=request.POST["venue"],
            category=request.POST["category"],
            max_participants=request.POST["max_participants"],
            featured=bool(request.POST.get("featured")),
            image=request.FILES.get("image"),
            created_by=request.user,
        )
        messages.success(request, "Event created successfully.")
        return redirect("organizer_dashboard")

    return render(
        request,
        "create_event.html",
        {"form_title": "Create New Event", "submit_label": "Create Event", "event_data": None},
    )


@login_required
def edit_event(request, event_id):
    if not _organizer_required(request):
        return redirect("student_dashboard")

    event = get_object_or_404(Event, id=event_id, created_by=request.user)

    if request.method == "POST":
        event.title = request.POST["title"]
        event.description = request.POST["description"]
        event.date = request.POST["date"]
        event.venue = request.POST["venue"]
        event.category = request.POST["category"]
        event.max_participants = request.POST["max_participants"]
        event.featured = bool(request.POST.get("featured"))

        image = request.FILES.get("image")
        if image:
            event.image = image

        event.save()
        messages.success(request, f"{event.title} was updated successfully.")
        return redirect("organizer_dashboard")

    return render(
        request,
        "create_event.html",
        {"form_title": "Edit Event", "submit_label": "Save Changes", "event_data": event},
    )


@login_required
def delete_event(request, event_id):
    if not _organizer_required(request):
        return redirect("student_dashboard")

    event = get_object_or_404(Event, id=event_id, created_by=request.user)
    if request.method == "POST":
        title = event.title
        event.delete()
        messages.success(request, f"{title} was deleted.")
    return redirect("organizer_dashboard")


@login_required
def event_attendees(request, event_id):
    if not _organizer_required(request):
        return redirect("student_dashboard")

    event = get_object_or_404(Event, id=event_id, created_by=request.user)
    registrations = Registration.objects.filter(event=event).select_related("user").order_by("registered_at")
    waitlist = Waitlist.objects.filter(event=event).select_related("user").order_by("joined_at")

    return render(
        request,
        "event_attendees.html",
        {"event": event, "registrations": registrations, "waitlist": waitlist},
    )


@login_required
def student_dashboard(request):
    if not _student_required(request):
        return redirect("organizer_dashboard")

    registrations = Registration.objects.filter(user=request.user).select_related("event").order_by("event__date")
    return render(request, "student_dashboard.html", {"registrations": registrations})


@login_required
def profile_view(request):
    profile = request.user.profile
    created_events = Event.objects.filter(created_by=request.user)
    registered_events = Registration.objects.filter(user=request.user)

    context = {
        "profile": profile,
        "created_events": created_events,
        "registered_events": registered_events,
    }
    return render(request, "profile.html", context)
