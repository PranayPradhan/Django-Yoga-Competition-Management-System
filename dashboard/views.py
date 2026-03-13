from django.shortcuts import render
from django.contrib import messages
from .models import AuthUser
from django.shortcuts import render, redirect


def index(request):

    role = request.session.get("role")
    username = request.session.get("username")

    context = {
        "is_logged_in": role is not None,
        "is_admin": role == "admin",
        "is_user": role == "user",
        "role": role,
        "username": username
    }

    return render(request, "dashboard/index.html", context)


def login_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user = AuthUser.objects.select_related("role").get(username=username)

            if user.password == password:

                # create session
                request.session["username"] = user.username
                request.session["role"] = user.role.name

                messages.success(request, "Login successful")

                return redirect("dashboard:index")

            else:
                messages.error(request, "Invalid password")

        except AuthUser.DoesNotExist:
            messages.error(request, "User not found")

    return render(request, "dashboard/login.html")

def logout_view(request):

    request.session.flush()

    return redirect("dashboard:index")

