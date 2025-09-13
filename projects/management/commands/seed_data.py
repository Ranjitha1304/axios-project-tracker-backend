from django.core.management.base import BaseCommand
from django.utils import timezone
from users.models import User
from projects.models import MiniProject

class Command(BaseCommand):
    help = "Seed database with sample users and projects"

    def handle(self, *args, **kwargs):
        trainer = User.objects.create_user(
            username="trainer1",
            password="trainerpass",
            role="trainer"
        )
        trainee = User.objects.create_user(
            username="trainee1",
            password="traineepass",
            role="trainee"
        )

        MiniProject.objects.create(
            title="Sample Project 1",
            description="First demo project",
            status="pending",
            priority="medium",
            due_date=timezone.now().date(),
            assigned_by=trainer,
            assigned_to=trainee,
        )

        self.stdout.write(self.style.SUCCESS("Seeded sample users and project"))
