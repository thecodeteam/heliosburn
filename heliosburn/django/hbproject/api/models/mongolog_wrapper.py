# Wrapper to return a python logging object configured for mongolog


def connect():
    from mongolog.handlers import MongoHandler
    from configurations import importer
    import os
    import logging
    from hbproject import settings
    import dotenv

    dotenv.read_dotenv()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hbproject.settings')
    os.environ.setdefault('DJANGO_CONFIGURATION', 'Development')

    importer.install()

    log = logging.getLogger('heliosburn')
    log.setLevel(logging.DEBUG)
    log.addHandler(MongoHandler.to(db=settings.MONGODB_DATABASE['production'], collection='log'))
    return log