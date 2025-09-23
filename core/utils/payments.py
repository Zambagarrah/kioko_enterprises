from core.models import PaymentLog

def log_payment(order, method, status, message='', reference='', metadata=None):
    PaymentLog.objects.create(
        order=order,
        method=method,
        status=status,
        reference=reference,
        message=message,
        metadata=metadata or {}
    )
