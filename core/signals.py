from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import PaymentLog, Order

@receiver(post_save, sender=PaymentLog)
def update_order_status(sender, instance, created, **kwargs):
    if not created:
        return

    order = instance.order
    method = instance.method
    status = instance.status.lower()

    if status == 'initiated' and order.status == 'pending':
        order.status = 'paid'
        order.save()

    elif status == 'verified' and order.status in ['paid', 'pending']:
        order.status = 'verified'
        order.save()

    elif status == 'failed':
        order.status = 'cancelled'
        order.save()
