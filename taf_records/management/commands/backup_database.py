import os
import datetime
from django.core.management.base import BaseCommand
from django.conf import settings
import subprocess

class Command(BaseCommand):
    help = 'Backs up the PostgreSQL database.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting database backup...'))

        db_settings = settings.DATABASES['default']
        db_name = db_settings['NAME']
        db_user = db_settings['USER']
        db_password = db_settings['PASSWORD']
        db_host = db_settings['HOST']
        db_port = db_settings['PORT']

        backup_dir = os.path.join(settings.BASE_DIR, 'backups', 'database')
        os.makedirs(backup_dir, exist_ok=True)

        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f'{db_name}_backup_{timestamp}.sql.gz' # Compressed SQL dump
        backup_filepath = os.path.join(backup_dir, backup_filename)

        # Ensure PGPASSWORD is set for non-interactive password input if needed
        env = os.environ.copy()
        if db_password:
            env['PGPASSWORD'] = db_password

        # Using pg_dump to create a gzipped SQL dump
        # pg_dump command might vary slightly based on exact pg_dump version and OS
        # Ensure pg_dump is in PATH or provide full path
        command = [
            'pg_dump',
            '--dbname=' + db_name,
            '--username=' + db_user,
            '--host=' + db_host,
            '--port=' + str(db_port),
            '--format=c', # Custom format, good for pg_restore, often smaller
            '--blobs',    # Include large objects if any
            '--compress=9', # Max compression for gzip within custom format
            '--file=' + backup_filepath
        ]
        # For plain SQL dump compressed with gzip externally:
        # command_pg_dump = f'pg_dump --dbname={db_name} --username={db_user} --host={db_host} --port={str(db_port)}'
        # command_gzip = f'gzip > {backup_filepath}'
        # full_command = f'{command_pg_dump} | {command_gzip}'


        try:
            self.stdout.write(f'Running command: {" ".join(command)}')
            process = subprocess.Popen(command, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()

            if process.returncode == 0:
                self.stdout.write(self.style.SUCCESS(f'Database backup successful: {backup_filepath}'))
            else:
                self.stderr.write(f'Database backup failed. Return code: {process.returncode}')
                self.stderr.write(f'stdout: {stdout.decode()}')
                self.stderr.write(f'stderr: {stderr.decode()}')
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR('pg_dump command not found. Ensure PostgreSQL client tools are installed and in PATH.'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'An error occurred during database backup: {e}'))
