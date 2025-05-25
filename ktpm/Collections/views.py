from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from .models import Collection
from .serializers import CollectionSerializer
from .permissions import CollectionPermission

class CollectionViewSet(viewsets.ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    permission_classes = [CollectionPermission]

    def get_queryset(self):
        user = self.request.user
        return Collection.objects.filter(unit_code=user.unit_code)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(
                {"detail": "Tạo khoản thu thành công", "data": serializer.data},
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response({"error": str(e), "data": request.data}, status=500)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(
            {"detail": "Sửa khoản thu thành công", "data": serializer.data},
            status=status.HTTP_200_OK
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"detail": "Xóa khoản thu thành công"}, status=status.HTTP_200_OK)