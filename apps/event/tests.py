from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from apps.member.models import Member
from .models import Event, Commission
from django.utils import timezone

class EventTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='admin', password='password')
        self.member = Member.objects.create(
            user=self.user, 
            first_name='Admin', 
            last_name='User', 
            role=Member.Role.ADMIN,
            phone_number='+33612345678',
            room_number='101'
        )
        self.client.force_login(self.user)
        
        self.event = Event.objects.create(
            title='Test Event',
            date=timezone.now() + timezone.timedelta(days=1),
            location='Test Location'
        )

    def test_event_list(self):
        response = self.client.get(reverse('event_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Event')

    def test_event_detail(self):
        response = self.client.get(reverse('event_detail', kwargs={'pk': self.event.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Event')

    def test_event_create(self):
        response = self.client.post(reverse('event_create'), {
            'title': 'New Event',
            'description': 'Description',
            'location': 'Location',
            'date': (timezone.now() + timezone.timedelta(days=2)).strftime('%Y-%m-%dT%H:%M')
        })
        self.assertEqual(response.status_code, 302) # Redirects to detail
        self.assertTrue(Event.objects.filter(title='New Event').exists())

    def test_commission_create(self):
        response = self.client.post(reverse('commission_create', kwargs={'event_id': self.event.pk}), {
            'name': 'Deco',
            'max_capacity': 5
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Commission.objects.filter(name='Deco', event=self.event).exists())

    def test_home_page(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Bonjour, Admin')
