from django.core.management.base import BaseCommand
from datetime import date
from bailti.models import Location, Quittance

class Command(BaseCommand):
    help = "Génère automatiquement la quittance du mois pour chaque location active."

    def handle(self, *args, **kwargs):
        today = date.today()
        mois = today.month
        annee = today.year

        #locations = Location.objects.filter(active=True)
        locations = Location.objects.all()

        count = 0
        
        for loc in locations:
            # Vérifier si une quittance pour ce mois existe déjà
            exist = Quittance.objects.filter(
                location=loc,
                mois=mois,
                annee=annee
            ).exists()

            if not exist:
                Quittance.objects.create(
                    location=loc,
                    montant=loc.loyer,
                    mois=mois,
                    annee=annee,
                    status='non_paye'
                )
                count += 1

        self.stdout.write(self.style.SUCCESS(f"{count} quittances générées."))
