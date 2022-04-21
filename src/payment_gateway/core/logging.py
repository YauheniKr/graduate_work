LOG_FORMAT = '%(asctime)s - %(levelname)s - %(name)s - %(message)s'
LOG_DEFAULT_HANDLERS = ['console', ]


def create_logging_cfg(level='INFO') -> dict:
    return {
        'version': 1,
        'disable_existing_loggers': False,

        'formatters': {
            'verbose': {
                'format': LOG_FORMAT
            },
            'default': {
                '()': 'uvicorn.logging.DefaultFormatter',
                'fmt': LOG_FORMAT,  # '%(levelprefix)s %(message)s',
                'use_colors': None,
            },
            'access': {
                '()': 'uvicorn.logging.AccessFormatter',
                'fmt': LOG_FORMAT,  # "%(levelprefix)s %(client_addr)s - '%(request_line)s' %(status_code)s",
            },
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose',
            },
            'default': {
                'formatter': 'default',
                'class': 'logging.StreamHandler',
                'stream': 'ext://sys.stdout',
            },
            'access': {
                'formatter': 'access',
                'class': 'logging.StreamHandler',
                'stream': 'ext://sys.stdout',
            },
        },
        'loggers': {
            'paygateway': {
                'handlers': LOG_DEFAULT_HANDLERS,
                'level': level,
                'propagate': True,
            },
            'uvicorn.error': {
                'level': level,
            },
            'uvicorn.access': {
                'handlers': ['access'],
                'level': level,
                'propagate': False,
            },
        },
    }
