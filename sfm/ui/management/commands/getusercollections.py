from ui.models import *
import json
from django.core.management.base import BaseCommand
import csv 

USER_FIELDS = ['email', 'last_login', 'first_name', 'last_name', 'is_active', 'date_joined', 'id']
CREDENTIAL_FIELDS = ['user_id', 'platform', 'date_added', 'date_updated', 'id']
COLLECTION_FIELDS = ['harvest_type', 'name', 'is_on', 'date_added', 'date_updated', 'end_date', 'is_active', 'credential_id']

def get_users():
    '''Retreive users from the database with email address and dates of last login'''
    users = User.objects.all()
    user_recs = [{prop: getattr(user, prop) for prop in USER_FIELDS} 
                for user in users]
    return user_recs

def get_credentials():
    '''Retreive all credentials from the dataabse.'''
    creds = Credential.objects.all()
    cred_recs = [{prop: getattr(cred, prop) for prop in CREDENTIAL_FIELDS} 
                for cred in creds]
    return cred_recs

def get_collections():
    '''Retreive all collections from the dataabse.'''
    collections = Collection.objects.all()
    coll_recs = [{prop: getattr(collection, prop) for prop in COLLECTION_FIELDS} 
                for collection in collections]
    return coll_recs

def merge_records(users, credentials, collections):
    '''Map users to collections via credentials and return unified list.
    :param users: list of user dictionaries (keys from USER_FIELDS
    :param credentials: list of credential dictionaries (keys from CREDENTIAL_FIELDS
    :param collections: list of collections dictionaries (keys from COLLECTION_FIELDS'''

    user_lookup = {user['id']: user for user in users}
    credential_lookup = {credential['id']: credential for credential in credentials}
    for collection in collections:
        cred_id = collection['credential_id']
        cred = credential_lookup[cred_id]
        user_id = cred['user_id']
        user = user_lookup[user_id]
        collection.update({f'user_{key}': value for key, value in user.items()})
        # Convert Python datetime to string for output
        for key, value in collection.items():
            if 'date' in key and value:
                collection[key] = collection[key].isoformat()
    return collections

def export_data(filepath):
    '''Export collections with user info as CSV to the specified path.'''

    users, credentials, collections = (get_users(), get_credentials(), get_collections())
    collections = merge_records(users, credentials, collections)

    with open(filepath, 'w') as f:
        writer = csv.DictWriter(f, fieldnames=collections[0].keys())
        writer.writeheader()
        writer.writerows(collections)

class Command(BaseCommand):

    help = '''Retrieve collections & user info. Supply a path to a JSON file for output. To run in Docker, use 
                    docker-compose run ui /opt/sfm-ui/sfm/manage.py getusercollections /sfm-data-shared/output.csv
        where output.csv is the name of the desired output file.'''
    
    def add_arguments(self, parser):
        parser.add_argument('filepath')

    def handle(self, *args, **options):
        export_data(options['filepath'])