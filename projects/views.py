from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import MiniProject
from .serializers import MiniProjectSerializer

class MiniProjectViewSet(viewsets.ModelViewSet):
    serializer_class = MiniProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == "trainee":
            return MiniProject.objects.filter(assigned_to=user)  # only their projects
        return MiniProject.objects.all()  # trainers see all

    def create(self, request, *args, **kwargs):
        if request.user.role != "trainer":
            return Response({"detail": "Only trainers can create projects."}, status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        project = self.get_object()
        if request.user.role == "trainee":
            # Trainee can update only status
            if "status" in request.data:
                project.status = request.data["status"]
                project.save()
                return Response(ProjectSerializer(project).data)
            return Response({"detail": "Trainees can only update status."}, status=status.HTTP_403_FORBIDDEN)

        # Trainer can update everything
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if request.user.role != "trainer":
            return Response({"detail": "Only trainers can delete projects."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)
