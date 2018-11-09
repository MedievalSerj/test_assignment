from os import getenv


class Config:
    broker_url = getenv('BROKER_URL', default='amqp://localhost:5672')
    broker_transport_options = {
        'fanout_prefix': True,
        'fanout_patterns': True,
        'visibility_timeout': 60,
    }

    timezone = 'UTC'
    enable_utc = True

    task_default_queue = 'default'
    task_default_exchange = 'default'
    task_default_exchange_type = 'direct'
    task_default_routing_key = 'default'


class DevelopmentConfig(Config):
    ...
