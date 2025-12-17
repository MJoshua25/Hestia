from django.db import transaction
from django.utils.translation import gettext as _
from django.urls import reverse
import random
from .models import Commission, Assignment
from apps.member.models import Member
from apps.notification.services import NotificationService
from apps.notification.models import Notification

class AssignmentService:
    @staticmethod
    def assign_automatically(event, selected_member_ids, user, force=False):
        """
        Attribue automatiquement les membres sélectionnés aux commissions de l'événement.
        Algorithme:
        1. Vérifie si le nombre total de membres suffit pour le MIN total des commissions.
        2. Mélange les membres.
        3. Remplit les commissions jusqu'au MIN.
        4. Répartit le reste équitablement en respectant le MAX.
        """
        
        # 0. Récupération des données
        commissions = list(event.commissions.all()) # Force query to list to avoid reiteration issues
        members = list(Member.objects.filter(id__in=selected_member_ids).select_related('user'))
        
        if not commissions:
            return {
                'status': 'error',
                'message': _("Aucune commission définie pour cet événement.")
            }
            
        if not members:
            return {
                'status': 'error',
                'message': _("Aucun membre sélectionné.")
            }

        # 1. Vérifications Préliminaires
        total_min_capacity = sum(c.min_capacity for c in commissions)
        total_members_count = len(members)

        if total_min_capacity > total_members_count:
            if not force:
                return {
                    'status': 'warning_min_capacity',
                    'message': _("Le nombre de membres sélectionnés ({}) est insuffisant pour couvrir les besoins minimums ({})").format(total_members_count, total_min_capacity),
                    'details': {
                        'total_min': total_min_capacity,
                        'total_selected': total_members_count
                    }
                }
            # If force is True, we proceed (best effort)
        
        # 2. Préparation
        random.shuffle(members)
        assignments_map = {c.id: [] for c in commissions}
        members_pool = members.copy()
        
        # 3. Remplissage des Minimums
        for commission in commissions:
            needed = commission.min_capacity
            for i in range(needed):
                if members_pool:
                    member = members_pool.pop(0)
                    assignments_map[commission.id].append(member)
        
        # 4. Équilibrage du Reste
        while members_pool:
            eligible_commissions = [
                c for c in commissions 
                if (c.max_capacity is None or len(assignments_map[c.id]) < c.max_capacity)
            ]
            
            if not eligible_commissions:
                break
                
            target_commission = min(eligible_commissions, key=lambda c: len(assignments_map[c.id]))
            
            member_to_assign = members_pool.pop(0)
            assignments_map[target_commission.id].append(member_to_assign)
            
        unassigned_count = len(members_pool)
        
        # 5. Sauvegarde Atomique
        with transaction.atomic():
            # Supprimer les anciennes attributions pour cet événement
            Assignment.objects.filter(commission__event=event).delete()
            
            assignments_to_create = []
            notifications_to_create = []
            
            for commission_id, members_list in assignments_map.items():
                commission = next(c for c in commissions if c.id == commission_id)
                commission_url = reverse('commission_detail', args=[commission.id])
                
                for member in members_list:
                    assignments_to_create.append(
                        Assignment(
                            commission_id=commission_id,
                            member=member,
                            assigned_by=user
                        )
                    )
                    
                    # Prepare notification
                    if member.user:
                        notifications_to_create.append(
                            Notification(
                                user=member.user,
                                type=Notification.Type.ASSIGNMENT,
                                title=_("Nouvelle commission !"),
                                message=_("Vous avez été assignée à la commission {} pour l'événement {}").format(commission.name, event.title),
                                link=commission_url
                            )
                        )
            
            Assignment.objects.bulk_create(assignments_to_create)
            Notification.objects.bulk_create(notifications_to_create)
            
        # 6. Résultat
            
        # 6. Résultat
        results = {}
        for c in commissions:
            count = len(assignments_map[c.id])
            results[c.id] = {
                'name': c.name,
                'count': count,
                'min': c.min_capacity,
                'max': c.max_capacity,
                'filled_min': count >= c.min_capacity,
                'full': c.max_capacity is not None and count >= c.max_capacity
            }
            
        return {
            'status': 'success',
            'unassigned_count': unassigned_count,
            'details': results,
            'message': _("Attribution terminée avec succès.")
        }

    @staticmethod
    def get_assignment_stats(event):
        commissions = event.commissions.prefetch_related('assignments')
        stats = []
        for c in commissions:
            count = c.assignments.count()
            stats.append({
                'id': c.id,
                'name': c.name,
                'count': count,
                'min': c.min_capacity,
                'max': c.max_capacity,
                'is_full': c.is_full,
                'missing_min': max(0, c.min_capacity - count)
            })
        return stats
