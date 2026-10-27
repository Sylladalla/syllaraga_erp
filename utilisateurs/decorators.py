

from functools import wraps

from django.shortcuts import redirect
from django.contrib import messages


def role_requis(roles, redirection_refus="accueil_clients"):
    def decorateur(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            # 1. Vérifier la connexion
            if not request.user.is_authenticated:
                return redirect("connexion")

            # 2. Récupérer et normaliser le rôle
            role_brut = getattr(request.user, "role", "")
            role_utilisateur = str(role_brut).upper().strip()

            # 3. Autoriser l'administrateur, quel que soit son libellé
            if role_utilisateur in ("ADMIN", "ADMINISTRATEUR"):
                return view_func(request, *args, **kwargs)

            # 4. Vérifier les rôles autorisés pour cette page
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
