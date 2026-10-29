from functools import wraps

from django.shortcuts import redirect
from django.contrib import messages


def role_requis(roles, redirection_refus="accueil_clients"):
    def decorateur(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect("/utilisateurs/connexion/")

            role_brut = getattr(request.user, "role", "")
            role_utilisateur = str(role_brut).upper().strip()

            if role_utilisateur in ("ADMIN", "ADMINISTRATEUR"):
                return view_func(request, *args, **kwargs)

            roles_autorises = [
                str(role).upper().strip()
                for role in roles
            ]

            if role_utilisateur not in roles_autorises:
                messages.error(
                    request,
                    "Vous n'avez pas l'autorisation d'accéder à cette page."
                )
                return redirect(redirection_refus)

            return view_func(request, *args, **kwargs)

        return wrapper
    return decorateur
