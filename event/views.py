import logging

from django.shortcuts import render
from django.db import transaction

from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, ParseError
from rest_framework.renderers import TemplateHTMLRenderer

from event.models import Book, UserCouponList, Coupon
from event.serializers import CouponEventSerializer
from event.constants import EventStatus

# logging setup
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter("LOGGING -> %(levelname)s %(asctime)s:%(message)s")
handler = logging.FileHandler("log_event.log")
handler.setFormatter(formatter)
logger.addHandler(handler)


class EventBookListAPI(generics.ListAPIView):
	queryset = Coupon.objects.filter(status=EventStatus.ACTIVE)
	serializer_class = CouponEventSerializer

	def get_serializer_context(self):
		context = super().get_serializer_context()
		context['user'] = self.request.user
		
		return context

	def get_queryset(self):
		return Coupon.objects.filter(status=EventStatus.ACTIVE).select_related('book')


class UserGetCouponAPI(APIView):
	def post(self, request, *args, **kwargs):
		coupon_number = request.data.get('couponNumber')

		with transaction.atomic():
			try:
				coupon = Coupon.objects.select_for_update().get(number=coupon_number)
			except Coupon.DoesNotExist:
				logger.info("Invalid Request: Get Coupon", extra={
					'user': request.user.id,
					'coupon': coupon_number,
				})
				return Response({'message': 'Invalid Coupon Number'}, status=status.HTTP_400_BAD_REQUEST)

			if coupon.quantity < 1:
				return Response({'message': 'Coupon expired'}, status=status.HTTP_400_BAD_REQUEST)

			obj, created = UserCouponList.objects.get_or_create(
				user=request.user,
				coupon=coupon,
			)

			if not created:
				return Response({'message': 'This coupon has already been received.'}, status=status.HTTP_400_BAD_REQUEST)

			coupon.decrease_coupon_aquantity(count=1)

			return Response({"coupon_id": obj.coupon.id}, status=status.HTTP_201_CREATED)


class EventPageView(APIView):
	renderer_classes = [TemplateHTMLRenderer]
	template_name = 'event/event_list.html'

	def get(self, request, *args, **kwargs):
		return Response(status=status.HTTP_200_OK)
