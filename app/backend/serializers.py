from rest_framework import serializers

from backend.models import Blob


class BlobSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(source='get_owner_name', read_only=True)

    class Meta:
        model = Blob
        fields = ['owner', 'filename', 's3_name']
