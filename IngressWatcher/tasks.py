from __future__ import absolute_import
import os
from celery import Celery
import django

# import logging
#
# logger = logging.getLogger(__name__)

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'IngressHub.settings')

app = Celery('IngressWatcher')

django.setup()
# Using a string here means the worker will not have to
# pickle the object when using Windows.
# app.config_from_object('django.conf:settings')
# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

from IngressWatcher.models import Message, Sender, Setting, Watcher, WatchPoint
from IngressWatcher.intel import Intel
from IngressWatcher.ingress_json_parser import MessageParser


@app.task
def fetch_messages():
    setting = Setting.get_setting()
    watcher_cookies = setting.watcher.get_watcher_cookie()
    watch_point_field = setting.watch_point.get_watch_point_field()
    intel = Intel(watcher_cookies, watch_point_field)
    fetch_message_tab = setting.fetch_message_tab
    msg_result = intel.fetch_msg(tab=fetch_message_tab)

    add_msg_list = list()
    for msg_result_item in msg_result:
        # print(msg_result_item)
        msg_parser = MessageParser(msg_result_item)
        msg_guid = Message.add_message(msg_parser)
        if msg_guid:
            add_msg_list.append(msg_guid)
            # print("fetch %s messages , add %s messages: %s" % (len(msg_result), len(add_msg_list), add_msg_list))


if __name__ == '__main__':
    fetch_messages()
