from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.member.models import Member
from apps.event.models import Event, Commission, Assignment
from apps.event.services import AssignmentService
from datetime import datetime, timedelta

User = get_user_model()

class AssignmentServiceTests(TestCase):
    def setUp(self):
        # Users
        self.admin_user = User.objects.create_superuser('admin', 'admin@test.com', 'password')
        
        # Members (Create 20 members)
        self.members = []
        for i in range(20):
            m = Member.objects.create(
                first_name=f"Member{i}",
                last_name=f"Test{i}",
                phone_number=f"+12345678{i:02d}",
                room_number=f"10{i}",
                role='MEMBER' if i > 0 else 'ADMIN'
            )
            self.members.append(m)
            
        # Event
        self.event = Event.objects.create(
            title="Soirée Test",
            date=datetime.now() + timedelta(days=7)
        )
        
        # Commissions
        # C1: Min 3, Max 5
        self.c1 = Commission.objects.create(event=self.event, name="C1", min_capacity=3, max_capacity=5)
        # C2: Min 5, Max 10
        self.c2 = Commission.objects.create(event=self.event, name="C2", min_capacity=5, max_capacity=10)
        # C3: Min 0, Unlimited
        self.c3 = Commission.objects.create(event=self.event, name="C3", min_capacity=0, max_capacity=None)

    def test_auto_assignment_logic(self):
        # Select 15 members
        selected_ids = [m.id for m in self.members[:15]]
        
        # Run Assignment
        result = AssignmentService.assign_automatically(
            self.event, 
            selected_ids, 
            self.admin_user
        )
        
        self.assertEqual(result['status'], 'success')
        
        # Verify Assignments count
        total_assigned = Assignment.objects.filter(commission__event=self.event).count()
        self.assertEqual(total_assigned, 15)
        
        # Verify Constraints
        c1_count = self.c1.assignments.count()
        c2_count = self.c2.assignments.count()
        c3_count = self.c3.assignments.count()
        
        print(f"C1: {c1_count}, C2: {c2_count}, C3: {c3_count}")
        
        self.assertTrue(c1_count >= 3)
        self.assertTrue(c1_count <= 5)
        
        self.assertTrue(c2_count >= 5)
        self.assertTrue(c2_count <= 10)
        
        self.assertTrue(c3_count >= 0)
        
        # Verify Uniqueness
        # Ensure no member is assigned twice
        # (Database constraint enforces this, but let's check manually too)
        assigned_members = [a.member.id for a in Assignment.objects.filter(commission__event=self.event)]
        self.assertEqual(len(assigned_members), len(set(assigned_members)))

    def test_insufficient_members(self):
        # Min needed: 3 + 5 + 0 = 8
        # Select only 5 members
        selected_ids = [m.id for m in self.members[:5]]
        
        result = AssignmentService.assign_automatically(
            self.event, 
            selected_ids, 
            self.admin_user
        )
        
        self.assertEqual(result['status'], 'warning_min_capacity')
        self.assertIn("insuffisant", result['message'])

    def test_force_assignment(self):
        # Min needed: 3 + 5 + 0 = 8
        # Select only 5 members
        selected_ids = [m.id for m in self.members[:5]]
        
        # Try with force=True
        result = AssignmentService.assign_automatically(
            self.event, 
            selected_ids, 
            self.admin_user,
            force=True
        )
        
        self.assertEqual(result['status'], 'success')
        
        # Verify Assignments count (should be 5)
        total_assigned = Assignment.objects.filter(commission__event=self.event).count()
        self.assertEqual(total_assigned, 5)
        
        # Verify warnings in result (service logic returns warnings list?)
        # Let's check service logic...
        # It returns 'details' with 'filled_min' status.
        
        details = result['details']
        # Check if we have some commissions not filled
        not_filled = [d for d in details.values() if not d['filled_min']]
        self.assertTrue(len(not_filled) > 0)

    def test_reassignment_clears_previous(self):
        # First assignment
        AssignmentService.assign_automatically(self.event, [m.id for m in self.members[:10]], self.admin_user)
        count1 = Assignment.objects.count()
        
        # Second assignment
        AssignmentService.assign_automatically(self.event, [m.id for m in self.members[:12]], self.admin_user)
        count2 = Assignment.objects.count()
        
        self.assertEqual(count2, 12) # Should match new count, not add
