from app.imports import json,os,psutil

# Load environment variables
workers_per_core_str = os.getenv("WORKERS_PER_CORE", "1")
max_workers_str = os.getenv("MAX_WORKERS", "10")
web_concurrency_str = os.getenv("WEB_CONCURRENCY", None)
host = os.getenv("HOST", "0.0.0.0")
port = os.getenv("PORT", "3030")
bind_env = os.getenv("BIND", None)
use_loglevel = os.getenv("LOG_LEVEL", "info")

# Determine number of cores in use
total_cores = psutil.cpu_count(logical=False)  # Physical cores
available_cores = total_cores - psutil.cpu_count()  # Adjust for cores in use by other services

workers_per_core = float(workers_per_core_str)
default_web_concurrency = workers_per_core * available_cores

if web_concurrency_str:
    web_concurrency = int(web_concurrency_str)
    assert web_concurrency > 0
else:
    web_concurrency = max(int(default_web_concurrency), 2)
    if max_workers_str:
        use_max_workers = int(max_workers_str)
        web_concurrency = min(web_concurrency, use_max_workers)

accesslog_var = os.getenv("ACCESS_LOG", "-")
errorlog_var = os.getenv("ERROR_LOG", "-")
graceful_timeout_str = os.getenv("GRACEFUL_TIMEOUT", "60")
timeout_str = os.getenv("TIMEOUT", "60")
keepalive_str = os.getenv("KEEP_ALIVE", "5")

# Gunicorn configuration variables
worker_class = "uvicorn.workers.UvicornWorker"
loglevel = use_loglevel
workers = web_concurrency
bind = bind_env or f"{host}:{port}"
errorlog = errorlog_var or None
worker_tmp_dir = "/tmp"
accesslog = accesslog_var or None
graceful_timeout = int(graceful_timeout_str)
timeout = int(timeout_str)
keepalive = int(keepalive_str)

# Optional: Print configuration for debugging
log_data = {
    "loglevel": loglevel,
    "workers": workers,
    "bind": bind,
    "graceful_timeout": graceful_timeout,
    "timeout": timeout,
    "keepalive": keepalive,
    "errorlog": errorlog,
    "accesslog": accesslog,
    "workers_per_core": workers_per_core,
    "available_cores": available_cores,
    # "half_physical_cores": half_physical_cores,
    "total_cores": total_cores,
    "web_concurrency": web_concurrency,
    "host": host,
    "port": port,
}
print(json.dumps(log_data))
