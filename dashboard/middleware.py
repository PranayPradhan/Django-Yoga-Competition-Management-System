from django.shortcuts import redirect


class RoleRequiredMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        path = request.path
        role = request.session.get("role")

        # allow dashboard and login pages
        if path.startswith("/dashboard/login") or path.startswith("/dashboard/logout"):
            return self.get_response(request)

        # admin only areas
        admin_paths = [
            "/masters/",
            "/setting/"
        ]

        for admin_path in admin_paths:
            if path.startswith(admin_path):

                if role != "admin":
                    return redirect("dashboard:index")

        # login required areas
        protected_paths = [
            "/school/",
            "/participant/",
            "/dataentry/",
            "/report/"
        ]

        for protected in protected_paths:

            if path.startswith(protected):

                if role not in ["admin", "user"]:
                    return redirect("dashboard:login")

        return self.get_response(request)