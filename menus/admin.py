from django.contrib import admin
from menus.models import Menu, MenuItem, MenuVote

# Register your models here.
class MenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 1  # Number of empty rows to show for new items
    fields = ['name', 'description', 'price']

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'name', 'date', 'vote_count', 'total_price')
    fields = ('name', 'restaurant', 'date', 'vote_count', 'total_price')
    inlines = [MenuItemInline]
    readonly_fields = ('items', 'total_price', 'vote_count')

    @admin.display(description='Votes')
    def vote_count_display(self, obj):
        return obj.vote_count

    @admin.display(description='Total Price')
    def total_price_display(self, obj):
        return f"${obj.total_price:.2f}"


@admin.register(MenuVote)
class MenuVoteAdmin(admin.ModelAdmin):
    list_display = ('menu', 'employee', 'created_at')
    fields = ('menu', 'employee', 'created_at')
    readonly_fields = ('created_at',)