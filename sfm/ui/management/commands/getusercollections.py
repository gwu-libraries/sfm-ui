from ui.models import *
from django.core.management.base import BaseCommand
from django.db.models import Max, F
import csv 

USER_FIELDS = ['email', 'last_login', 'first_name', 'last_name', 'id']
COLLECTION_FIELDS = ['id', 'collection_set_id', 'harvest_type', 'name', 'is_on', 'date_added', 'end_date', 'is_active']

def export_data(filepath):
    '''Export collections with user info as CSV to the specified path.'''

    # Prefetch tables to allow many-to-many joins
    query_set = User.objects.prefetch_related('credentials', 'credentials__collections', 'credentials__collections__harvests')
    # simplify working with Django's ORM syntax
    collection_fields_expanded = [f'credentials__collections__{field}' for field in COLLECTION_FIELDS]
    fields = USER_FIELDS + collection_fields_expanded
    # .values() will retrieve the requests fields from the pre-joined tables
    # Include the last harvest date associated with each collection
    results = query_set.values(*fields).annotate(last_harvest=Max('credentials__collections__harvests__date_ended'))
    # Create aliases for clarity
    aliases = [f'user_{field}' if not '__' in field else field.replace('credentials__collections__', '') for field in fields]
    # Can't give an alias the name of a field already on the model
    aliases[5] = 'collection_id'
    # Apply aliases
    results = results.annotate(**{alias: F(field) for alias, field in zip(aliases, fields)})
    aliases.append('last_harvest')
    results = results.values(*aliases)
    
    with open(filepath, 'w') as f:
        writer = csv.DictWriter(f, fieldnames=aliases)
        writer.writeheader()
        writer.writerows(results)

class Command(BaseCommand):

    help = '''Retrieve collections & user info. Supply a path to a JSON file for output. To run in Docker, use 
                    docker-compose run ui /opt/sfm-ui/sfm/manage.py getusercollections /sfm-data-shared/output.csv
        where output.csv is the name of the desired output file.'''
    
    def add_arguments(self, parser):
        parser.add_argument('filepath')

    def handle(self, *args, **options):
        export_data(options['filepath'])