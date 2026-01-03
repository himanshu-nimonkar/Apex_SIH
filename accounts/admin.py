from django.contrib import admin
from .models import GraphicalPassword

# Register your models here.

@admin.register(GraphicalPassword)
class GraphicalPasswordAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('image_sequence_hash', 'salt', 'created_at', 'updated_at')

