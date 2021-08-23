LOGS = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s"
        },
        "simple": {
            "format": "%(levelname)s %(message)s"
        },
        "rich": {"datefmt": "[%X]"},
        "django.server": {
            "()": "django.utils.log.ServerFormatter",
            "format": "[{server_time}] {message}",
            "style": "{"
        }
    },
    "handlers": {
        "file": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "formatter": "verbose",
            "filename": "log/error.log"
        },
        "null": {
            "level": "DEBUG",
            "class": "logging.NullHandler"
        },

        "console": {
            "level": "DEBUG",
            "class": "rich.logging.RichHandler",
            "formatter": "rich"
        }
    },
    "loggers": {
        "django": {
            "handlers": ["console", "null"],
            "propagate": True,
            "level": "INFO"
        },
        "django.request": {
            "handlers": ["console", "file"],
            "level": "ERROR",
            "propagate": False
        },
        "django.security.DisallowedHost": {
            "handlers": ["null"],
            "propagate": False
        }
    }
}