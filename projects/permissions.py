from rest_framework import permissions
from django.shortcuts import get_object_or_404
from .models import Project, Contributor, Issue, Comment

class IsContributor(permissions.BasePermission):
    """
    Permission pour vérifier que l'utilisateur est contributeur du projet.
    Autorise les méthodes de lecture et de création pour les contributeurs.
    Seuls les auteurs peuvent modifier ou supprimer les objets qu'ils ont créés.
    """

    def has_permission(self, request, view):

        # Récupère les identifiants depuis les kwargs
        project_id = view.kwargs.get('project_pk')

        if project_id:
            # Vérifie que l'utilisateur est contributeur du projet
            return Contributor.objects.filter(project_id=project_id, user=request.user).exists()
        # Si aucun identifiant n'est fourni, refuser l'accès
        return False

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow authors of an object to edit or delete it.
    """

    def has_object_permission(self, request, view, obj):
        # Autoriser les méthodes de lecture pour tout le monde (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True

        # Seuls les auteurs peuvent modifier ou supprimer l'objet
        return obj.author == request.user
