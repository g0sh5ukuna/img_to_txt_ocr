"""
Django management command pour créer un utilisateur admin par défaut.

Cette commande est utilisée pour les projets open source afin de faciliter
les tests et la démonstration avec un utilisateur admin par défaut.

Usage:
    python manage.py create_default_admin
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import IntegrityError


class Command(BaseCommand):
    """
    Commande Django pour créer un utilisateur admin par défaut.
    
    Crée un superutilisateur avec :
    - Username: admin
    - Password: admin
    - Email: admin@example.com
    - Is_staff: True
    - Is_superuser: True
    
    Si l'utilisateur existe déjà, la commande affiche un message et ne fait rien.
    """
    help = 'Crée un utilisateur admin par défaut (username: admin, password: admin)'

    def add_arguments(self, parser):
        """
        Ajoute les arguments optionnels de la commande.
        """
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force la réinitialisation du mot de passe si l\'utilisateur existe déjà',
        )
        parser.add_argument(
            '--skip-existing',
            action='store_true',
            help='Ignore silencieusement si l\'utilisateur existe déjà',
        )

    def handle(self, *args, **options):
        """
        Exécute la commande pour créer l'utilisateur admin par défaut.
        """
        User = get_user_model()
        
        username = 'admin'
        email = 'admin@example.com'
        password = 'admin'
        
        try:
            # Vérifier si l'utilisateur existe déjà
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'is_staff': True,
                    'is_superuser': True,
                    'is_active': True,
                }
            )
            
            if created:
                # Utilisateur créé avec succès
                user.set_password(password)
                user.save()
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✅ Utilisateur admin créé avec succès!\n'
                        f'   Username: {username}\n'
                        f'   Password: {password}\n'
                        f'   Email: {email}'
                    )
                )
            else:
                # L'utilisateur existe déjà
                if options['force']:
                    # Forcer la réinitialisation du mot de passe
                    user.set_password(password)
                    user.email = email
                    user.is_staff = True
                    user.is_superuser = True
                    user.is_active = True
                    user.save()
                    self.stdout.write(
                        self.style.WARNING(
                            f'⚠️  Utilisateur admin existant mis à jour!\n'
                            f'   Username: {username}\n'
                            f'   Password: {password} (réinitialisé)\n'
                            f'   Email: {email}'
                        )
                    )
                elif options['skip_existing']:
                    # Ignorer silencieusement
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'ℹ️  Utilisateur admin existe déjà. Ignoré (--skip-existing).'
                        )
                    )
                else:
                    # Afficher un message d'information
                    self.stdout.write(
                        self.style.WARNING(
                            f'⚠️  L\'utilisateur "{username}" existe déjà!\n'
                            f'   Utilisez --force pour réinitialiser le mot de passe.\n'
                            f'   Utilisez --skip-existing pour ignorer silencieusement.'
                        )
                    )
                    
        except IntegrityError as e:
            self.stdout.write(
                self.style.ERROR(
                    f'❌ Erreur lors de la création de l\'utilisateur: {e}'
                )
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(
                    f'❌ Erreur inattendue: {e}'
                )
            )
