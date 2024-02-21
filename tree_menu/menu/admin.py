from django.contrib import admin

from menu.models import Section, Menu


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    model = Menu
    fields = ('title',)


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    model = Section
    fields = (
        'menu',
        'title',
        'url',
        'parent',
    )
