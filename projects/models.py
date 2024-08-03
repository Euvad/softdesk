from django.db import models
from users.models import CustomUser
import uuid


class Project(models.Model):
    TYPE_CHOICES = [
        ('BACKEND', 'Back-end'),
        ('FRONTEND', 'Front-end'),
        ('IOS', 'iOS'),
        ('ANDROID', 'Android'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='owned_projects')
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Contributor(models.Model):
    ROLE_CHOICES = [
        ('AUTHOR', 'Author'),
        ('CONTRIBUTOR', 'Contributor'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='contributors')
    role = models.CharField(max_length=12, choices=ROLE_CHOICES)

    class Meta:
        unique_together = ('user', 'project')

    def __str__(self):
        return f"{self.user.username} - {self.project.name} ({self.role})"

class Issue(models.Model):
    STATUS_CHOICES = [
        ('TODO', 'To Do'),
        ('IN_PROGRESS', 'In Progress'),
        ('FINISHED', 'Finished'),
    ]

    TAG_CHOICES = [
        ('BUG', 'Bug'),
        ('FEATURE', 'Feature'),
        ('TASK', 'Task'),
    ]

    PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    tag = models.CharField(max_length=10, choices=TAG_CHOICES)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default='TODO')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='issues')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='created_issues')
    assignee = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='assigned_issues')
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='comments')
    description = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='created_comments')
    created_time = models.DateTimeField(auto_now_add=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.issue.title}"
