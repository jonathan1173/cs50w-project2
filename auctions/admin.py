from django.contrib import admin
from .models import Category, User, Lista , comentarios ,bid
# Register your models here.

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Lista)
admin.site.register(comentarios)
admin.site.register(bid)