from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

from event.constants import EventStatus


# 원래 Book 객체 테이블 같은 경우는 다른 앱에 있어야하지만 구현의 편의성을 위해 해당 프로젝트에서는 여기에 구현
class Book(models.Model):
  	title = models.CharField(_("Title"), max_length=64)


class Coupon(models.Model):
	book = models.ForeignKey(Book, on_delete=models.CASCADE)
	number = models.CharField(_("Number"), max_length=8, unique=True)
	quantity = models.PositiveIntegerField(_("quantity"), default=1000000)
	status = models.CharField(_("Status"), max_length=16, choices=EventStatus.choices)

	# redis를 사용할 경우 한번에 다수의 개수를 줄이게 될 경우가 있어서 count를 별도의 인자를 받는 형태로 구성.
	def decrease_coupon_aquantity(self, count):
		self.quantity -= count
		self.save()
		

class UserCouponList(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
	is_used = models.BooleanField(_("Is used?"), default=False)
	created_at = models.DateTimeField(_("Created At"), auto_now_add=True)