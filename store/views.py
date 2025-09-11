from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .models import User

def signup(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        password = request.POST.get("password")

        # Save user in DB with hashed password
        try:
            user = User(
                first_name=first_name,
                last_name=last_name,
                email=email,
                mobile=mobile,
                password=make_password(password)  # Hash password for security
            )
            user.save()
            messages.success(request, "Signup successful! You can now log in.")
            return redirect("login")
        except Exception as e:
            messages.error(request, f"Error: {e}")

    return render(request, "store/signup.html")


def cart(request):
    return render(request, "store/cart.html")

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
            if check_password(password, user.password):  # compare hash
                # ✅ Store user info in session
                request.session["user_id"] = user.id
                request.session["user_name"] = user.first_name
                messages.success(request, f"Welcome back, {user.first_name}!")
                return redirect("home")
            else:
                messages.error(request, "Invalid password.")
        except User.DoesNotExist:
            messages.error(request, "No account found with this email.")

    return render(request, "store/login.html")

def logout_view(request):
    request.session.flush()  # clear session
    messages.success(request, "You have been logged out.")
    return redirect("login")

def home(request):
    products = [
        {"name": "Wireless Headphones", "price": 50, "img": "https://via.placeholder.com/200"},
        {"name": "Smart Watch", "price": 120, "img": "https://via.placeholder.com/200"},
        {"name": "Gaming Keyboard", "price": 75, "img": "https://via.placeholder.com/200"},
        {"name": "Bluetooth Speaker", "price": 40, "img": "https://via.placeholder.com/200"},
        {"name": "Laptop Backpack", "price": 35, "img": "https://via.placeholder.com/200"},
        {"name": "Wireless Mouse", "price": 20, "img": "https://via.placeholder.com/200"},
        {"name": "Mechanical Keyboard", "price": 90, "img": "https://via.placeholder.com/200"},
        {"name": "USB-C Charger", "price": 25, "img": "https://via.placeholder.com/200"},
        {"name": "4K Monitor", "price": 300, "img": "https://via.placeholder.com/200"},
        {"name": "External Hard Drive", "price": 80, "img": "https://via.placeholder.com/200"},
        {"name": "Power Bank", "price": 45, "img": "https://via.placeholder.com/200"},
        {"name": "Smartphone", "price": 600, "img": "https://via.placeholder.com/200"},
        {"name": "Tablet", "price": 400, "img": "https://via.placeholder.com/200"},
        {"name": "Wireless Earbuds", "price": 60, "img": "https://via.placeholder.com/200"},
        {"name": "Smart TV", "price": 700, "img": "https://via.placeholder.com/200"},
        {"name": "VR Headset", "price": 350, "img": "https://via.placeholder.com/200"},
        {"name": "Portable Projector", "price": 250, "img": "https://via.placeholder.com/200"},
        {"name": "DSLR Camera", "price": 900, "img": "https://via.placeholder.com/200"},
        {"name": "Drone", "price": 500, "img": "https://via.placeholder.com/200"},
        {"name": "Smart Light Bulb", "price": 15, "img": "https://via.placeholder.com/200"},
        {"name": "Electric Kettle", "price": 30, "img": "https://via.placeholder.com/200"},
        {"name": "Air Purifier", "price": 150, "img": "https://via.placeholder.com/200"},
        {"name": "Microwave Oven", "price": 180, "img": "https://via.placeholder.com/200"},
        {"name": "Refrigerator", "price": 1000, "img": "https://via.placeholder.com/200"},
        {"name": "Washing Machine", "price": 850, "img": "https://via.placeholder.com/200"},
        {"name": "Coffee Maker", "price": 90, "img": "https://via.placeholder.com/200"},
        {"name": "Fitness Tracker", "price": 70, "img": "https://via.placeholder.com/200"},
        {"name": "Smart Home Hub", "price": 110, "img": "https://via.placeholder.com/200"},
        {"name": "Electric Scooter", "price": 450, "img": "https://via.placeholder.com/200"},
        {"name": "Portable Fan", "price": 25, "img": "https://via.placeholder.com/200"},
        {"name": "Smart Door Lock", "price": 220, "img": "https://via.placeholder.com/200"},
        {"name": "Electric Toothbrush", "price": 60, "img": "https://via.placeholder.com/200"},

    ]
    return render(request, "store/home.html", {"products": products})

