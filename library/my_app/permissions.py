from rest_framework.permissions import BasePermission

class ReadBookPermission(BasePermission):


    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        if request.user.has_perm('my_app.read_book'):
            if view.action is 'list' or view.action is 'retrieve':
                return True
            else:
                return False
        else:
            return False

class ReadUpdateStudentPermission(BasePermission):


    def has_permission(self, request, view):
            """
            Return `True` if permission is granted, `False` otherwise.
            """
            import ipdb; ipdb.set_trace()
            if request.user.has_perm('my_app.read_borrower'):
                perms = ['retrieve', 'partial_update']
                if view.action in perms:
                    return True
                else:
                    return False
            else:
                return False

    def has_object_permission(self, request, view, obj):
                    
        if request.user.username == obj.name:
            return True
        else:
            return False
