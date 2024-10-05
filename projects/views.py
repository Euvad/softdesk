from rest_framework import viewsets, permissions
from .models import Project, Contributor, Issue, Comment
from .serializers import ProjectSerializer, ContributorSerializer, IssueSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly, IsContributor
from .pagination import CustomPageNumberPagination
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()  # select_related retiré
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]
    pagination_class = CustomPageNumberPagination

    def perform_create(self, serializer):
        project = serializer.save(author=self.request.user)
        Contributor.objects.create(user = self.request.user, project = project)

class ContributorViewSet(viewsets.ModelViewSet):
    serializer_class = ContributorSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        project_id = self.kwargs.get("project_pk")
        if project_id:
            return Contributor.objects.filter(project_id=project_id)
        return Contributor.objects.none()

    def perform_create(self, serializer):
        project_id = self.kwargs.get("project_pk")
        project = get_object_or_404(Project, pk=project_id)

        if project.author != self.request.user:
            raise PermissionDenied("Vous n'êtes pas autorisé à ajouter des contributeurs à ce projet.")

        serializer.save(project=project)

class IssueViewSet(viewsets.ModelViewSet):
    serializer_class = IssueSerializer
    permission_classes = [permissions.IsAuthenticated, IsContributor, IsAuthorOrReadOnly]
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        project_id = self.kwargs.get("project_pk")
        if project_id:
            queryset = Issue.objects.filter(project_id=project_id)
            # Si nécessaire, décommentez la ligne suivante :
            # queryset = queryset.select_related('author', 'assignee')
        else:
            queryset = Issue.objects.none()
        return queryset

    def perform_create(self, serializer):
        project_id = self.kwargs.get("project_pk")
        project = get_object_or_404(Project, pk=project_id)

        if not project.contributors.filter(user=self.request.user).exists():
            raise PermissionDenied("Vous n'êtes pas contributeur de ce projet.")

        serializer.save(project=project, author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsContributor, IsAuthorOrReadOnly]
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        project_id = self.kwargs.get("project_pk")
        issue_id = self.kwargs.get("issue_pk")

        if project_id and issue_id:
            queryset = Comment.objects.filter(
                issue_id=issue_id,
                issue__project_id=project_id,
                issue__project__contributors__user=self.request.user
            ).order_by('-created_time')
            # Si nécessaire, décommentez la ligne suivante :
            # queryset = queryset.select_related('author', 'issue')
        else:
            queryset = Comment.objects.none()
        return queryset

    def perform_create(self, serializer):
        project_id = self.kwargs.get("project_pk")
        issue_id = self.kwargs.get("issue_pk")
        project = get_object_or_404(Project, pk=project_id)
        issue = get_object_or_404(Issue, pk=issue_id, project=project)

        if not project.contributors.filter(user=self.request.user).exists():
            raise PermissionDenied("Vous n'êtes pas contributeur de ce projet.")

        serializer.save(issue=issue, author=self.request.user)
