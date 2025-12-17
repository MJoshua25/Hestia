"""
Configuration Gunicorn pour Django en production
"""
import multiprocessing
import os

# Nombre de workers (2-4 x CPU cores)
workers = int(os.environ.get('GUNICORN_WORKERS', multiprocessing.cpu_count() * 2 + 1))

# Threads par worker
threads = int(os.environ.get('GUNICORN_THREADS', 2))

# Type de worker
worker_class = 'sync'

# Timeout (en secondes)
timeout = 300

# Bind
bind = '0.0.0.0:8082'

# Reload automatique en dev (désactivé en prod)
reload = False

# Logs
accesslog = '-'
errorlog = '-'
loglevel = 'info'

# Process naming
proc_name = 'django_hestia'

# Max requests par worker (pour éviter les fuites mémoire)
max_requests = 1000
max_requests_jitter = 50

# Preload app (charge l'app avant de forker les workers)
preload_app = True
