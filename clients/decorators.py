from functools import wraps
from django.shortcuts import redirect
from django.urls import reverse


def client_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get("client_id"):
            url = reverse("connexion_client")
            return redirect(f"{url}?next={request.get_full_path()}")
        return view_func(request, *args, **kwargs)

    return wrapper
