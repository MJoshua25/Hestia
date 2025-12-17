from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.member.models import Member
from django.core import mail
from core.models import User

# User = get_user_model() # Already imported above but core.models.User is specifically our user

class AuthIntegrationTest(TestCase):
    def setUp(self):
        self.client = Client()
        # Create a member, which should auto-create a user
        self.member = Member.objects.create(
            first_name="Alice",
            last_name="Dupont",
            phone_number="+33612345678",
            room_number="101"
        )
        self.user = self.member.user
        self.user.set_pin("123456")
        self.user.save()
        
        # Admin user
        self.admin = User.objects.create_superuser('admin', 'admin@example.com', 'adminpass')
        self.admin.require_password_change = False
        self.admin.save()
        self.admin_member = Member.objects.create(
             first_name="Admin", last_name="User", phone_number="+33600000000", room_number="000",
             user=self.admin, role=Member.Role.ADMIN
        )

    def test_user_creation_signal(self):
        """Test US-A01: User created automatically"""

        self.assertIsNotNone(self.user)
        self.assertEqual(self.user.username, "alice.dupont")
        self.assertTrue(self.user.check_password("pass_Default1"))
        self.assertEqual(self.user.phone_number, "+33612345678")
        self.assertTrue(self.user.require_password_change)

    def test_login_username_password(self):
        """Test US-A03: Login with Username + Password"""
        response = self.client.post(reverse('login'), {
            'method': 'username_password',
            'username': 'alice.dupont',
            'password': 'pass_Default1'
        })
        # Should redirect to first connection because require_password_change is True
        # But wait, login view redirects to HOME. Middleware redirects to FIRST_CONNECTION.
        # So expectation is redirection to HOME then middleware intercepts next request?
        # NO, if middleware intercepts, it intercepts ANY request.
        # But login_view returns redirect('home').
        # The client follows redirect? Defaults to false.
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('home'))
        
        # Follow redirect
        response = self.client.get(response.url)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('first_connection'))

    def test_login_phone_password(self):
        """Test US-A04: Login with Phone + Password"""
        response = self.client.post(reverse('login'), {
            'method': 'phone_password',
            'phone': '+33612345678',
            'password': 'pass_Default1'
        })
        self.assertEqual(response.status_code, 302)
        
    def test_login_phone_pin(self):
        """Test US-A05: Login with Phone + PIN"""
        response = self.client.post(reverse('login'), {
            'method': 'phone_pin',
            'phone': '+33612345678',
            'pin': '123456'
        })
        self.assertEqual(response.status_code, 302)
        self.client.logout()

    def test_first_connection_flow(self):
        """Test US-A06: Forced password change"""
        self.client.login(username='alice.dupont', password='pass_Default1')
        
        # Accessing home should redirect
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('first_connection'), response.url)
        
        # Submit new password
        response = self.client.post(reverse('first_connection'), {
            'new_password': 'NewPassword123!',
            'confirm_password': 'NewPassword123!',
            'pin_code': '654321'
        })
        
        self.assertEqual(response.status_code, 302) # Redirects to home
        self.user.refresh_from_db()
        self.assertFalse(self.user.require_password_change)
        self.assertTrue(self.user.check_password('NewPassword123!'))
        self.assertTrue(self.user.check_pin('654321'))

    def test_admin_reset_password(self):
        """Test US-A08: Admin reset password"""
        # Set user to have changed password
        self.user.set_password("NewPass")
        self.user.require_password_change = False
        self.user.save()
        
        # Login as admin
        self.client.force_login(self.admin)
        
        response = self.client.post(reverse('reset_password', args=[self.user.id]), follow=True)
        self.assertEqual(response.status_code, 200)
        
        # Check messages
        messages = list(response.context['messages'])
        self.assertTrue(any("réinitialisé avec succès" in str(m) for m in messages), "Success message not found")

        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("pass_Default1"))
        self.assertTrue(self.user.require_password_change)

    def test_admin_delete_pin(self):
        """Test US-A08: Admin delete PIN"""
        self.client.force_login(self.admin)
        
        response = self.client.post(reverse('delete_pin', args=[self.user.id]), follow=True)
        self.assertEqual(response.status_code, 200)
        
        messages = list(response.context['messages'])
        self.assertTrue(any("supprimé avec succès" in str(m) for m in messages), "Success message not found")
        
        self.user.refresh_from_db()
        self.assertIsNone(self.user.pin_code)

