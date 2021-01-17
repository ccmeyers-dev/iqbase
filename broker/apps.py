from django.apps import AppConfig

class BrokerConfig(AppConfig):
    name = 'broker'

    def ready(self):
        import broker.signals
