# admin.py
from django.contrib import admin
from .models import Workspace, Member, Mission, Task, Comment, Category

admin.site.register(Workspace)
admin.site.register(Member)
admin.site.register(Mission)
admin.site.register(Task)
admin.site.register(Comment)
admin.site.register(Category)
