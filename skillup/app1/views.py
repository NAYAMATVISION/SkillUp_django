
from django.shortcuts import render, redirect ,get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required , user_passes_test
from django.urls import reverse_lazy , reverse
from .models import Course  # Ensure Course model is imported
from .decorators import is_admin  # Assuming you have this decorator defined somewhere


# Create your views here.
def home(request):
    return render(request,"index.html" , context = home)

def signup(request):
    if request.method == "POST":
        fullname = request.POST.get("fullname")
        email = request.POST.get("email")
        password = request.POST.get("password").strip()
        confirm_password = request.POST.get("confirm_password").strip()
        mobile = request.POST.get("mobile")

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect("signup")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect("signup")

        try:
            new_user = User.objects.create(
                username=email,  
                email=email,
                first_name=fullname,
                password=make_password(password)  
            )
            messages.success(request, "Registered successfully")
            return redirect("login")
        except Exception as e:
            messages.error(request, "Registration failed. Please check all fields")
            return redirect("signup")

    return render(request, "signup.html",context = signup)


def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password").strip()

        # Define admin credentials
        ADMIN_EMAIL = "admin@example.com"  # Replace with actual admin email
        ADMIN_PASSWORD = "admin123"  # Replace with a secure admin password

        # Check for admin login
        if email == ADMIN_EMAIL:
            user = User.objects.filter(email=ADMIN_EMAIL).first()
            if not user:
                user = User.objects.create_superuser(username="admin", email=ADMIN_EMAIL, password=ADMIN_PASSWORD)
            
            admin_user = authenticate(request, username=user.username, password=password)
            if admin_user:
                login(request, admin_user)
                messages.success(request, "Admin login successful!")
                return redirect("admindashboard")
            else:
                messages.error(request, "Invalid admin credentials!")
                return redirect("login")

        # Regular user login
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid credentials!")
            return redirect("login")

    return render(request, "login.html")


def forget_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        new_password = request.POST.get('password')
        confirm_password = request.POST.get('confirmPassword')

        # Basic validation
        if not email or not new_password or not confirm_password:
            messages.error(request, "All fields are required!")
            return redirect("forget_password")

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect("forget_password")

        # Find user by email
        user = User.objects.filter(email=email).first()
        if not user:
            messages.error(request, "No account found with that email!")
            return redirect("forget_password")

        # Update password
        user.password = make_password(new_password)
        user.save()

        messages.success(request, "Password updated successfully!")
        return redirect("login")

    return render(request, "forgetPassword.html")




def dashboard(request):
    if request.user.is_superuser:  # Redirect admin users to the admin dashboard
        return redirect("admindashboard")
    
    return render(request, "dashboard.html", {"user": request.user})


def is_admin(user):
    return user.is_superuser  # Check if the user is an admin

@login_required
@user_passes_test(is_admin, login_url='dashboard')  # Redirect non-admins to dashboard
def admin_view(request):
    return render(request, "index.html")


def is_admin(user):
    return user.is_superuser  # Check if the user is an admin

@login_required
@user_passes_test(is_admin, login_url=reverse_lazy('dashboard'))  # Redirect non-admins
def admindashboard(request):
    if not request.user.is_superuser:
        messages.error(request, "Access Denied! Admins only.")
        return redirect("dashboard")  # Redirect non-admins

    courses = Course.objects.all()  # Fetch all courses
    return render(request, "admindashboard.html", {"courses": courses})


@login_required
@user_passes_test(is_admin, login_url=reverse_lazy('dashboard'))
def create_course(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        image_url = request.POST.get('image_url')

        # Create a new course and add it to the database
        Course.objects.create(
            title=title, 
            description=description, 
            image_url=image_url
        )
        messages.success(request, "Course created successfully!")
        return redirect("admindashboard")
    
    return render(request, "createcourse.html") 


@login_required
@user_passes_test(is_admin, login_url=reverse_lazy('dashboard'))
def delete_course(request, id):
    course = get_object_or_404(Course, id=id)
    course.delete()
    messages.success(request, "Course deleted successfully!")
    return redirect(reverse_lazy("admindashboard"))


def edit_course(request, id):
    course = get_object_or_404(Course, id=id)
    if request.method == 'POST':
        course.title = request.POST.get('title')
        course.description = request.POST.get('description')
        course.image_url = request.POST.get('image_url')
        course.save()
        return redirect(reverse('admin_dashboard'))
    return render(request, 'editcourse.html', {'course': course})



def courses(request):
    return render(request,"courses.html" )
def course(request):
    return render(request,"course.html" )
def terms(request):
    return render(request,"termscondition.html" , context = home)


@login_required
def profile(request):
    
    if request.GET.get('next'):
        messages.info(request, "Please log in to access your profile.")
    
    return render(request, 'profile.html', {'user': request.user})

def fullstack(request):
    return render(request,"webdev.html")
def datascience(request):
    return render(request,"datascience.html")
def AIML(request):
    return render(request,"AIML.html")
def checkout(request):
    return render(request,"checkout.html")

def add_to_cart(request):
    if request.method == "POST":
        course_id = request.POST.get("course_id")
        course_name = request.POST.get("course_name")
        price = float(request.POST.get("price"))  

        if "cart" not in request.session:
            request.session["cart"] = []

       
        existing_item = next((item for item in request.session["cart"] if item["id"] == course_id), None)
        if existing_item:
            messages.info(request, "Course is already in the cart!")
        else:
            request.session["cart"].append({"id": course_id, "name": course_name, "price": price})
            request.session.modified = True
            messages.success(request, "Course added to cart!")

    return redirect(reverse("cart"))

def cart(request):
    cart_items = request.session.get("cart", [])
    total_price = sum(item["price"] for item in cart_items) 
    return render(request, "cart.html", {"cart_items": cart_items, "total_price": total_price})

def remove_from_cart(request, course_id):
    if "cart" in request.session:
        request.session["cart"] = [item for item in request.session["cart"] if item["id"] != course_id]
        request.session.modified = True
        messages.warning(request, "Course removed from cart!")
    return redirect(reverse("cart"))

def clear_cart(request):
    request.session.pop("cart", None)  
    messages.error(request, "Cart cleared!")
    return redirect(reverse("cart"))


