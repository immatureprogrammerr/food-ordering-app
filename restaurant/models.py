from django.db import models
from accounts.models import User, UserProfile
from accounts.utils import send_notification_email

class Restaurant(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    user_profile = models.OneToOneField(UserProfile, related_name='userprofile', on_delete=models.CASCADE)
    restaurant_name = models.CharField(max_length=50)
    restaurant_license = models.ImageField(upload_to='restaurant/license')
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.restaurant_name

    def save(self, *args, **kwargs):
        if self.pk is not None:
            # Update
            origin = Restaurant.objects.get(pk=self.pk)
            if origin.is_approved != self.is_approved:
                context = {
                    'user': self.user,
                    'is_approved': self.is_approved
                }
                mail_template = "accounts/emails/admin_approval_email.html"
                if self.is_approved:
                    # send notification email
                    mail_subject = "Congratulation, you restaurant has been approved."
                else:
                    # send notification email
                    mail_subject = "Sorry, you're not eligible for publishing your food menu on our marketplace"
                send_notification_email(mail_subject, mail_template, context)
        return super(Restaurant, self).save(*args, **kwargs)