from django.core.files.storage import get_storage_class
from django.http import FileResponse

from rest_framework import views
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser

from backend.serializers import BlobSerializer
from backend.permissions import BlobModelPermission
from backend.models import Blob


class BlobViewSet(views.APIView):
    permission_classes = (BlobModelPermission,)
    parser_classes = [FileUploadParser]
    serializer_class = BlobSerializer
    queryset = Blob.objects.all()

    def get(self, request, filename):
        if not self.get_queryset().filter(filename=filename).exists():
            return Response(status=403)
        blob = self.get_queryset().filter(filename=filename).get()
        storage = get_storage_class()()
        file = storage.open(blob.s3_name, 'rb')

        return FileResponse(file)

    def put(self, request, filename):
        if self.get_queryset().filter(filename=filename).exists():
            return Response(
                {"detail": "There is already a file with the same path."},
                status=400,
            )

        storage = get_storage_class()()

        if 'file' not in request.data:
            return Response(
                {"detail": "No file provided (or at least detected)"},
                status=400,
            )

        file_obj = request.data['file']

        # May be different than filename in some edges cases where a file with
        # the same filename already exists.
        s3_name = storage.save(filename, file_obj)

        blob = Blob.objects.create(
            owner=request.user,
            filename=filename,
            s3_name=s3_name,
            content_type=file_obj.content_type,
        )

        return Response(BlobSerializer(blob).data, status=204)

    def get_queryset(self):
        return self.queryset
