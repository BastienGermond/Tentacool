from rest_framework.permissions import BasePermission
from rest_framework.exceptions import NotAuthenticated, PermissionDenied

from backend.models import Blob


class BlobPermission(BasePermission):
    perms_map = {
        'PUT': ['create'],
    }

    object_perms_map = {
        'GET': ['access'],
        'DELETE': ['owner'],
    }

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            raise NotAuthenticated()
        if request.user.is_superuser:
            return True
        for fn_name in self.perms_map.get(request.method, []):
            if not hasattr(self, fn_name):
                raise NotImplementedError("object_perms_map map to nothing")
            else:
                fn = getattr(self, fn_name)
                if not fn(request, view, None):
                    raise PermissionDenied()
        return True

    def has_object_permission(self, request, view, obj: Blob):
        # root is root
        if request.user.is_superuser:
            return True
        if request.method not in self.object_perms_map:
            # Default behaviour is denied
            raise PermissionDenied()
        for fn_name in self.object_perms_map.get(request.method):
            if not hasattr(self, fn_name):
                raise NotImplementedError("object_perms_map map to nothing")
            else:
                fn = getattr(self, fn_name)
                if not fn(request, view, obj):
                    raise PermissionDenied()
        return True

    def access(self, request, view, obj: Blob):
        """check if user can access this blob

            User can access it if:
                - he is the owner
                - he share the same group
        """
        if obj.owner == request.user:
            return True
        raise PermissionDenied()

    def owner(self, request, view, obj: Blob):
        """restrict to owner only"""
        return obj.owner == request.user

    def create(self, request, view, obj: Blob):
        """check if user can create

            User can create if:
                - he has 'backend.add_blob'
        """
        return request.user.has_perm('backend.add_blob')
