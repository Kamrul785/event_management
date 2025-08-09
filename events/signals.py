from django.contrib.auth.models import  Group
from django.db.models.signals import post_save , m2m_changed
from django.dispatch import receiver
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.core.mail import send_mail
from events.models import Event
from django.dispatch import Signal
from django.contrib.auth import get_user_model

User = get_user_model()


@receiver(m2m_changed, sender=Event.participants.through)
def send_rsvp_email(sender, instance, action, pk_set, **kwargs):
    if action == 'post_add':
        for user_id in pk_set:
            user = instance.participants.get(pk=user_id)
            subject = 'RSVP Confirmation - Event Management'
            message = f"Hi {user.first_name } {user.username},\n\nYou have successfully RSV'd to the event: {instance.name}.\n\nThank you for your interest!"
            try:
                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False
                )
            except Exception as e:
                print(f'Failed to send RSVP email to {user.email}: {str(e)}')
