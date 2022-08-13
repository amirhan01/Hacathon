from django.contrib import admin
from product.models import Category, Product, Comment, Image, Rating, Like, Favorite


class ImageInAdmin(admin.TabularInline):
    model = Image
    fields = ['image']
    max_num = 6


class ProductAdmin(admin.ModelAdmin):
    inlines = [ImageInAdmin]


admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Comment)
admin.site.register(Image)
admin.site.register(Rating)
admin.site.register(Like)
admin.site.register(Favorite)
