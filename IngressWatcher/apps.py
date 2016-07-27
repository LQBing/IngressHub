from django.apps import AppConfig


class IngressWatcherConfig(AppConfig):
    name = 'IngressWatcher'
    verbose_name = 'ingress watcher'

    INSTALLED_APPS = [
        'models.Agents',
        'models.Portals',
        'models.Senders',
    ]
