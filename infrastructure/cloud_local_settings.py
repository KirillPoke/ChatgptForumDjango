import os
import openai

JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
JWT_ALGORITHM = "HS256"
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET")
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
        "USER": os.environ.get("RDS_DB_USER"),
        "PASSWORD": os.environ.get("RDS_DB_PASSWORD"),
        "HOST": os.environ.get("DB_HOST"),
        "PORT": "5432",
    }
}
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": f"{os.environ.get('REDIS_HOST')}:6379",
    }
}
SESSION_COOKIE_SECURE = False
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "test3")
openai.api_key = os.environ.get("OPENAI_API_KEY")
CORS_ALLOWED_ORIGINS = [
    "https://chatgpt-forum-fe.vercel.app",
    "http://chatgpt-forum-fe.vercel.app",
]
CSRF_TRUSTED_ORIGINS = [
    "https://chatgpt-forum-fe.vercel.app",
    "http://chatgpt-forum-fe.vercel.app",
    "https://kirillras.net",
]

# settings.py example
Q_CLUSTER = {
    "name": "qcluster",
    "recycle": 500,
    "timeout": 15,
    "queue_limit": 4,
    "cpu_affinity": 1,
    "label": "Django Q",
    "max_attempts": 1,
    "redis": {
        "host": os.environ.get("REDIS_HOST"),
        "port": 6379,
        "db": 0,
    },
}
