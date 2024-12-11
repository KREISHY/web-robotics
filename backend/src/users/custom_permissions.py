from rest_framework.permissions import BasePermission


class IsAuthenticatedAndIsJudge(BasePermission):
    def has_permission(self, request, view):
        return bool((request.user and request.user.is_authenticated and request.user.is_judge) or
                    request.user.is_superuser or request.user.is_operator)


class IsAuthenticatedAndIsOperator(BasePermission):
    def has_permission(self, request, view):
        return bool((request.user and request.user.is_authenticated and request.user.is_operator) or
                    request.user.is_superuser)


class IsAuthenticatedAndIsJudgeOrOperator(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_superuser or (request.user and request.user.is_authenticated and
                    (request.user.is_judge or request.user.is_operator)))


class IsAuthenticatedAndIsSuperuser(BasePermission):
    def has_permission(self, request, view):
        return bool((request.user and request.user.is_authenticated and request.user.is_superuser))