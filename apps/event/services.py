from django.db import transaction
from django.utils.translation import gettext as _
import random
from .models import Commission, Assignment
from apps.member.models import Member

class AssignmentService:
    @staticmethod
    def assign_automatically(event, selected_member_ids, user):
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
        members = list(Member.objects.filter(id__in=selected_member_ids))
        
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
            return {
                'status': 'error', # Using error here to block, PRD said warning but implies action needed. 
                                   # We can handle warning in frontend effectively, but service usually returns success/error structure.
                                   # For now, treat as error blocking auto-assign unless "forced" (not implemented yet).
                'message': _("Le nombre de membres sélectionnés ({}) est insuffisant pour couvrir les besoins minimums ({})").format(total_members_count, total_min_capacity)
            }

        # 2. Préparation
        random.shuffle(members)
        assignments_map = {c.id: [] for c in commissions}
        members_pool = members.copy()
        
        # 3. Remplissage des Minimums
        # On trie les commissions par min_capacity décroissant pour d'abord remplir les plus exigentes ? 
        # Non, ordre arbitraire ok ou ordre de création.
        
        for commission in commissions:
            needed = commission.min_capacity
            for i in range(needed):
                if members_pool:
                    member = members_pool.pop(0)
                    assignments_map[commission.id].append(member)
        
        # 4. Équilibrage du Reste
        # Tant qu'il reste des membres
        while members_pool:
            # Trouver la commission éligible avec le MOINS de membres assignés
            # Éligible = n'a pas atteint son MAX
            
            eligible_commissions = [
                c for c in commissions 
                if (c.max_capacity is None or len(assignments_map[c.id]) < c.max_capacity)
            ]
            
            if not eligible_commissions:
                # Plus de place nulle part !
                # On arrête là et on retourne ce qu'on a, ou une erreur ?
                # Les membres restants ne sont pas assignés.
                break
                
            # On prend celle qui a le moins de membres actuellement
            target_commission = min(eligible_commissions, key=lambda c: len(assignments_map[c.id]))
            
            member_to_assign = members_pool.pop(0)
            assignments_map[target_commission.id].append(member_to_assign)
            
        unassigned_count = len(members_pool)
        
        # 5. Sauvegarde Atomique
        with transaction.atomic():
            # Supprimer les anciennes attributions pour cet événement
            # Attention : cela supprime TOUT pour l'événement, même ce qui était manuel ?
            # PRD: "L'attribution actuelle sera effacée et remplacée" -> OUI.
            Assignment.objects.filter(commission__event=event).delete()
            
            assignments_to_create = []
            for commission_id, members_list in assignments_map.items():
                for member in members_list:
                    assignments_to_create.append(
                        Assignment(
                            commission_id=commission_id,
                            member=member,
                            assigned_by=user
                        )
                    )
            
            Assignment.objects.bulk_create(assignments_to_create)
            
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
