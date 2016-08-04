from django.contrib import admin
from IngressWatcher.models import Agent, Portal, Message, WatchPoint, Watcher, Sender, Setting


# Register your models here.
class AgentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'team', 'level', 'sent_welcome_message')
    search_fields = ('name',)


admin.site.register(Agent, AgentAdmin)


class SettingAdmin(admin.ModelAdmin):
    list_display = ('id', 'welcome_message_send_condition', 'fetch_message_tab', 'welcome_message')


admin.site.register(Setting, SettingAdmin)


class PortalAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'guid', 'name', 'latE6', 'lngE6', 'owner', 'team', 'update_time_stamp', 'last_captured_time_stamp')


admin.site.register(Portal, PortalAdmin)


class SenderAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'cookies', 'maxLatE6', 'minLatE6', 'maxLngE6', 'minLngE6', 'team', 'remark', 'disable')


admin.site.register(Sender, SenderAdmin)


class WatchPointAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'maxLatE6', 'minLatE6', 'maxLngE6', 'minLngE6', 'disable')


admin.site.register(WatchPoint, WatchPointAdmin)


class WatcherAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'cookies', 'remark', 'disable')


admin.site.register(Watcher, WatcherAdmin)


class MessageAdmin(admin.ModelAdmin):
    list_display = (
        'guid', 'time_stamp', 'message_type', 'plext', 'portal_name', 'portal_guid', 'portal_lat', 'portal_lng')


admin.site.register(Message, MessageAdmin)
