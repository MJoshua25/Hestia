from django.test import TestCase
from .models import Member

class MemberModelTest(TestCase):
    def test_create_member(self):
        member = Member.objects.create(
            first_name="Alice",
            last_name="Dupont",
            phone_number="+33612345678",
            room_number="101"
        )
        self.assertEqual(str(member), "Alice Dupont")
        self.assertEqual(member.role, Member.Role.MEMBER)
