import os
import datetime
import tarfile
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'Backs up the application code and media files.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting application backup...'))

        backup_dir_base = os.path.join(settings.BASE_DIR, 'backups', 'application')
        os.makedirs(backup_dir_base, exist_ok=True)

        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f'application_backup_{timestamp}.tar.gz'
        backup_filepath = os.path.join(backup_dir_base, backup_filename)

        # What to include in the backup:
        # Project root (code) and media root
        paths_to_backup = [
            str(settings.BASE_DIR) # Convert PosixPath to string if it is
        ]
        # Media root is already inside BASE_DIR if using default setup (BASE_DIR / 'media')
        # If MEDIA_ROOT is outside BASE_DIR, it should be added explicitly.
        # For this example, we assume MEDIA_ROOT is settings.BASE_DIR / 'media'

        # Exclusions: .git, __pycache__, virtual environments, backup directory itself, etc.
        # tarfile's filter function can be used for more complex exclusions.
        def exclude_filter(tarinfo):
            path_to_check = tarinfo.name
            # Normalize path for comparison (e.g. remove leading ./ if present)
            normalized_path = os.path.normpath(path_to_check)

            # Exclude common unwanted directories/files
            excluded_patterns = [
                '.git', '__pycache__', '*.pyc', '*.pyo',
                'backups/', 'manage.pyc', '.DS_Store',
                '*.sqlite3', # If sqlite was used for dev
                'venv/', 'env/', '.env', # Common virtual env names
                'node_modules/'
            ]

            for pattern in excluded_patterns:
                if pattern.endswith('/') and normalized_path.startswith(pattern.rstrip('/')):
                    return None # Exclude directory and its contents
                if not pattern.endswith('/') and os.path.basename(normalized_path) == pattern:
                     return None # Exclude file
                # More complex globbing could be added here if needed

            self.stdout.write(f'Adding to archive: {tarinfo.name}')
            return tarinfo

        try:
            with tarfile.open(backup_filepath, "w:gz") as tar:
                # Add project directory (settings.BASE_DIR)
                # arcname='.' makes the paths relative inside the tarball
                tar.add(str(settings.BASE_DIR), arcname='application_root', filter=exclude_filter)

                # If MEDIA_ROOT is separate and needs explicit addition:
                # if os.path.isdir(settings.MEDIA_ROOT) and not str(settings.MEDIA_ROOT).startswith(str(settings.BASE_DIR)):
                #    tar.add(str(settings.MEDIA_ROOT), arcname='media_files', filter=exclude_filter)

            self.stdout.write(self.style.SUCCESS(f'Application backup successful: {backup_filepath}'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'An error occurred during application backup: {e}'))
