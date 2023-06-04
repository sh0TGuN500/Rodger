from storages.backends.s3boto3 import S3Boto3Storage


class PublicMediaStorage(S3Boto3Storage):
    location = 'media'
    default_acl = 'public-read'
    file_overwrite = False


class StaticStorage(S3Boto3Storage):
    location = 'static'
    default_acl = 'public-read'
    file_overwrite = False
# SFTP


'''
DEFAULT_FILE_STORAGE = 'storages.backends.sftpstorage.SFTPStorage'

SFTP_STORAGE_HOST = '127.0.0.1'
SFTP_STORAGE_ROOT = '/var/www/media/'
SFTP_STORAGE_PARAMS = {
    'username': 'root',
    'password': 'password',
    'allow_agent': False,
    'look_for_keys': False,
}
# SFTP_KNOWN_HOST_FILE = '~/.ssh/known_hosts'
SFTP_STORAGE_INTERACTIVE = False
'''