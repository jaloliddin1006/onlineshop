from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from .models import Category, Brand, Color, Product, ProductImage, Review, Tag, Size, ProductSize
from django.utils.html import mark_safe


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    prepopulated_fields = {"slug": ('name',)}
    search_fields = ('id', 'name')
    mptt_indent_field = "name"
    list_display = ('tree_actions', 'indented_title', 'display_icon',  'created_at', 'is_active',   'id')
    list_display_links = ('indented_title', 'display_icon', 'id')
    readonly_fields = ('id',  'display_icon')
    # list_editable = ('is_active',)

    def display_icon(self, obj):
        return mark_safe('<img src="%s" width="50" />' % obj.icon.url)

    display_icon.allow_tags = True
    display_icon.short_description = 'Icon'


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    search_fields = ('id', 'name')
    list_display = ['name', 'display_icon', 'id', 'created_at']
    list_display_links = ('name', 'id')
    readonly_fields = ('id', 'display_icon')

    def display_icon(self, obj):
        # return mark_safe('<img src="%s" width="100" height="100" />' % obj.icon.url)
        return mark_safe('<img src="{}" width="100" height="100" />'.format(obj.icon.url))

    display_icon.allow_tags = True
    display_icon.short_description = 'Icon'


@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'created_at', 'id', 'is_active')
    list_editable = ('code', 'is_active')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    list_display_links = ('name', 'created_at')
    search_fields = ('name', 'id')


@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    list_display_links = ('name', 'created_at')
    search_fields = ('name', 'id')


class ProductImageInline(admin.StackedInline):
    readonly_fields = ('get_image', 'updated_at')
    model = ProductImage
    extra = 1


class ProductSizeAdmin(admin.TabularInline):
    model = ProductSize
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductSizeAdmin, ProductImageInline]
    prepopulated_fields = {"slug": ('title',)}
    list_display = ('title', 'percentage','brand', 'id', 'status', 'is_active')
    search_fields = ('title', 'status', 'brand',)
    list_filter = ['created_at', 'status', 'is_active']
    list_display_links = ('title', 'brand', 'id')
    filter_horizontal = ('categories', 'tags', )
    list_editable = ('status', 'is_active')
    list_per_page = 25


@admin.register(Review)
class RateAdmin(admin.ModelAdmin):
    list_display = ('user', 'rate', 'product', 'created_at')
    list_display_links = ('user', 'rate', 'product', 'created_at')
    search_fields = ('product', 'id', 'user')



