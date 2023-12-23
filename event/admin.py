from django.contrib import admin

from event.models import Book, Coupon, UserCouponList


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    pass


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    pass


@admin.register(UserCouponList)
class UserCouponListAdmin(admin.ModelAdmin):
    pass