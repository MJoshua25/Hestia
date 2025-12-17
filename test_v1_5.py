import os
import django
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from apps.notification.models import Notification
from apps.member.models import Member
from apps.event.models import Commission
from django.urls import reverse

def test_models():
    print("Testing Models...")
    try:
        # Check Notification
        assert hasattr(Notification, 'type')
        print("✅ Notification model OK")
        
        # Check Member Photo
        assert hasattr(Member, 'photo')
        print("✅ Member photo field OK")
        
    except AssertionError as e:
        print(f"❌ Model test failed: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_urls():
    print("\nTesting URLs...")
    try:
        print(f"Profile URL: {reverse('member:profile')}")
        print(f"Notifications URL: {reverse('notification:list')}")
        print(f"Commission Detail URL: {reverse('commission_detail', args=[1])}")
        print("✅ URLs OK")
    except Exception as e:
        print(f"❌ URL test failed: {e}")

if __name__ == "__main__":
    test_models()
    test_urls()
