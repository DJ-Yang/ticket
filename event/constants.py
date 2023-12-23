from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class EventStatus(TextChoices):
    ACTIVE = ("ACTIVE", _("ACTIVE")) 
    COMPLETE = ("COMPLETE", _("COMPLETE"))
