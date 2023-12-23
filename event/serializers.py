from rest_framework import serializers

from event.models import Book, Coupon, UserCouponList


class BookSerializer(serializers.ModelSerializer):
	class Meta:
		model = Book
		fields = '__all__'


class CouponEventSerializer(serializers.ModelSerializer):
	book = BookSerializer()
	received = serializers.SerializerMethodField()

	class Meta:
		model = Coupon
		fields = '__all__'

	def get_received(self, obj):
		return UserCouponList.objects.filter(coupon=obj, user=self.context['user']).exists()
