from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Member
from django.contrib.auth import get_user_model
from django.utils.text import slugify

User = get_user_model()

@receiver(post_save, sender=Member)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created and not instance.user:
        # Generate username
        first_name = slugify(instance.first_name)
        last_name = slugify(instance.last_name)
        base_username = f"{first_name}.{last_name}"
        username = base_username
        counter = 2
        
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1
            
        user = User.objects.create_user(
            username=username,
            password="pass_Default1",
            first_name=instance.first_name,
            last_name=instance.last_name,
            phone_number=instance.phone_number,
            require_password_change=True
        )
        # Set default pin code
        user.set_pin("012345")

        
        # Link Member to User
        instance.user = user
        # We need to save instance again, but avoid recursion loop or specific handling
        # Using update to avoid triggering signal again for this field update if simpler
        Member.objects.filter(pk=instance.pk).update(user=user)

@receiver(post_save, sender=Member)
def save_user_profile(sender, instance, **kwargs):
    if instance.user:
        # Sync simple fields if needed, like phone number update?
        # For now, let's keep it simple. If member phone changes, should user phone change?
        # PRD doesn't explicitly say, but it makes sense.
        if instance.user.phone_number != instance.phone_number:
            instance.user.phone_number = instance.phone_number
            instance.user.save()

@receiver(post_delete, sender=Member)
def delete_user_profile(sender, instance, **kwargs):
    if instance.user:
        instance.user.delete()
