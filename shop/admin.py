from django.contrib import admin
from .models import Category, Product

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name','slug']
    #auto-populates the slug field with the input in the name
    prepopulated_fields = {'slug':('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','slug','price','available','created',
                    'updated']
    list_filter = ['available','created','updated']
    #list editable makes it easy to edit from the list page
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}


