from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .models import User, Product, CartItem

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
    if not request.session.get('user_id'):
        messages.error(request, "Please log in to view your cart.")
        return redirect('login')
    user = User.objects.get(id=request.session['user_id'])
    cart_items = CartItem.objects.filter(user=user).select_related('product')
    total = sum(item.total_price for item in cart_items)
    return render(request, "store/cart.html", {"cart_items": cart_items, "total": total})

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
    products = Product.objects.all()
    return render(request, "store/home.html", {"products": products})

def add_to_cart(request, product_id):
    if not request.session.get('user_id'):
        messages.error(request, "Please log in to add items to cart.")
        return redirect('login')
    user = User.objects.get(id=request.session['user_id'])
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=user, product=product, defaults={'quantity': 1})
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, f"{product.name} added to cart.")
    return redirect('home')

def update_quantity(request, cart_item_id):
    if not request.session.get('user_id'):
        messages.error(request, "Please log in to update cart.")
        return redirect('login')
    cart_item = get_object_or_404(CartItem, id=cart_item_id, user_id=request.session['user_id'])
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, "Quantity updated.")
        else:
            cart_item.delete()
            messages.success(request, "Item removed from cart.")
    return redirect('cart')

