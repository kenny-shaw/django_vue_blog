from rest_framework.permissions import BasePermission

# 博主权限，只有博主才可以访问
class BloggerPermission(BasePermission):
    message="您不是博主，不能访问哦~"
    def has_permission(self, request, view):
        if request.user.role!=3:
            return False
        return True

# 管理员权限，博主以及管理员权限
class AdminPermission(BasePermission):
    message="您不是管理员，不能访问哦~"
    def has_permission(self, request, view):
        if request.user.role==1:
            return False
        return True