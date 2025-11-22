import multiprocessing

# Server socket
bind = "0.0.0.0:8000"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
preload_app = True

# Timeout settings
timeout = 30
keepalive = 2

# Logging - use stdout/stderr to avoid permission issues
accesslog = "-"
errorlog = "-"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = "essenza_gunicorn"

# Server mechanics - disable pidfile to avoid permission issues
pidfile = None
tmp_upload_dir = None
# Note: user/group set via Docker USER directive

# SSL (if needed)
# keyfile = "/path/to/keyfile"
# certfile = "/path/to/certfile"