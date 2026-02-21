from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
from .models import ContactMessage, JobApplication, Coffee
import re
from django.core.exceptions import ValidationError
from django.core.validators import validate_email


from .models import Coffee

def home(request):
    specials = Coffee.objects.filter(is_available=True).order_by("-id")[:4]
    return render(request, "cafe/home.html", {"specials": specials})

def about(request):
    return render(request, "cafe/about.html")


def contact(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        message = request.POST.get("message", "").strip()

        # 1) Required fields
        if not name or not email or not message:
            messages.error(request, "Please fill in all fields.")
            return redirect("contact")

        # 2) Name validation (letters + spaces)
        if not re.fullmatch(r"[A-Za-z\s]+", name):
            messages.error(request, "Name must contain only letters and spaces.")
            return redirect("contact")

        # 3) Email validation
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Please enter a valid email address.")
            return redirect("contact")

        # OK -> save
        ContactMessage.objects.create(
            name=name,
            email=email,
            message=message
        )
        messages.success(request, "Message sent successfully.")
        return redirect("contact")

    return render(request, "cafe/contact.html")

def location(request):
    return render(request, 'cafe/location.html')
def careers(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name", "").strip()
        email = request.POST.get("email", "").strip()
        phone = request.POST.get("phone", "").strip()
        position = request.POST.get("position", "").strip()
        message_text = request.POST.get("message", "").strip()
        cv = request.FILES.get("cv")  # optional

        # Required
        if not full_name or not email or not position or not message_text:
            messages.error(request, "Please fill in all required fields.")
            return redirect("careers")

        # Name validation
        if not re.fullmatch(r"[A-Za-z\s]+", full_name):
            messages.error(request, "Full name must contain only letters and spaces.")
            return redirect("careers")

        # Email validation
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Please enter a valid email address.")
            return redirect("careers")

        # CV validation (if uploaded): must be PDF
        if cv is not None:
            if not cv.name.lower().endswith(".pdf"):
                messages.error(request, "CV must be a PDF file.")
                return redirect("careers")

        JobApplication.objects.create(
            full_name=full_name,
            email=email,
            phone=phone,
            position=position,
            message=message_text,
            cv=cv
        )

        messages.success(request, "Application submitted successfully.")
        return redirect("careers")

    return render(request, "cafe/careers.html")

def coffee_list(request):
    coffees = Coffee.objects.filter(is_available=True, category=Coffee.CATEGORY_COFFEE).order_by("name")
    desserts = Coffee.objects.filter(is_available=True, category=Coffee.CATEGORY_DESSERT).order_by("name")
    return render(request, "cafe/coffees.html", {"coffees": coffees, "desserts": desserts})
