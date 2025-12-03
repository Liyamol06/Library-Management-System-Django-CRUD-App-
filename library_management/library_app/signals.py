from datetime import timedelta

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import BorrowerList

@receiver(post_save, sender=BorrowerList)
def set_default_due_date(sender, instance, **kwargs):
    if instance.borrow_date and not instance.due_date:
        instance.due_date = instance.borrow_date + timedelta(days=14)
