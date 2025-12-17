from django.contrib.auth.mixins import UserPassesTestMixin
from apps.member.models import Member

class AdminOrDelegateRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        if not self.request.user.is_authenticated:
            return False
        try:
            member = self.request.user.member_profile
            return member.is_admin or member.is_delegate
        except Member.DoesNotExist:
            return False

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        if not self.request.user.is_authenticated:
            return False
        try:
            member = self.request.user.member_profile
            return member.is_admin
        except Member.DoesNotExist:
            return False
