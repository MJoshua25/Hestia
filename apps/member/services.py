import openpyxl
import phonenumbers
from django.db import transaction
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Member

class MemberService:
    @staticmethod
    def import_from_excel(file):
        """
        Import members from an Excel file.
        Expected columns: Prénom | Nom | Numéro | Chambre
        """
        try:
            workbook = openpyxl.load_workbook(file)
            sheet = workbook.active
        except Exception as e:
            raise ValidationError(_("Impossible de lire le fichier Excel. Assurez-vous qu'il est valide."))

        created_count = 0
        errors = []
        
        # Skip header row
        rows = list(sheet.iter_rows(min_row=2, values_only=True))
        
        if len(rows) > 100:
             raise ValidationError(_("Maximum 100 membres par import."))

        with transaction.atomic():
            for index, row in enumerate(rows, start=2):
                if not any(row):  # Skip empty rows
                    continue
                
                try:
                    # Unpack row (handle potential missing columns safely)
                    first_name = row[0] if len(row) > 0 else None
                    last_name = row[1] if len(row) > 1 else None
                    phone_raw = row[2] if len(row) > 2 else None
                    room_number = row[3] if len(row) > 3 else None
                    
                    if not all([first_name, last_name, phone_raw, room_number]):
                         raise ValidationError(_("Champs obligatoires manquants (Prénom, Nom, Numéro, Chambre)."))

                    # Phone validation
                    try:
                        parsed_phone = phonenumbers.parse(str(phone_raw), "FR") # Assume FR by default
                        if not phonenumbers.is_valid_number(parsed_phone):
                             raise ValidationError(_("Numéro de téléphone invalide."))
                        phone_number = phonenumbers.format_number(parsed_phone, phonenumbers.PhoneNumberFormat.E164)
                    except Exception:
                         # Fallback or strict fail
                         phone_number = str(phone_raw) # Let model validator handle it if regex matches
                    
                    # Create member
                    Member.objects.create(
                        first_name=first_name,
                        last_name=last_name,
                        phone_number=phone_number,
                        room_number=str(room_number)
                    )
                    created_count += 1
                    
                except Exception as e:
                    errors.append(f"Ligne {index}: {str(e)}")
        
        if errors:
            # If we want to rollback on ANY error, we should raise an exception here that triggers rollback
            # But transaction.atomic() only rolls back if exception escapes the block.
            # Here we caught exceptions inside the loop. 
            # If we want "All or Nothing", we should re-raise.
            # PRD says: "Import bloqué jusqu'à correction" if errors. 
            # So yes, all or nothing.
            raise ValidationError(errors)
            
        return created_count
