# coding=utf-8
from django.db import models
import ingress_json_parser
import ast
import time
from intel import Intel

TEAM_CHOICES = (
    ("ENLIGHTENED", u"启萌菌"),
    ("RESISTANCE", u"懒菌"),
)
WELCOME_MESSAGE_SEND_CONDITION_CHOICES = (
    (None, u"不发送"),
    ("freshman", u"只发送给新注册者"),
    ("new_come", u"发送给所有新到来者"),
)

FETCH_MESSAGE_TAB_CHOICES = (
    ('all', u"所有消息"),
    ('faction', u"阵营消息"),
    ("alerts", u"警告消息"),
)

FRESHMAN_MESSAGE_TYPES = [
    'faction_first_field',
    'faction_complete_training',
    'faction_first_portal',
    'faction_first_link',
]


# Create your models here.

class Sender(models.Model):
    name = models.CharField(verbose_name=u"消息发送账号名字", max_length=50, blank=False, null=False)
    cookies = models.TextField(verbose_name=u"cookies", blank=False, null=False)

    maxLatE6 = models.IntegerField(verbose_name=u"maxLatE6")
    minLatE6 = models.IntegerField(verbose_name=u"minLatE6")
    maxLngE6 = models.IntegerField(verbose_name=u"maxLngE6")
    minLngE6 = models.IntegerField(verbose_name=u"minLngE6")

    team = models.CharField(verbose_name=u"阵营", max_length=11, choices=TEAM_CHOICES, blank=False, null=False)
    remark = models.CharField(verbose_name=u"备注", max_length=50, blank=True, null=True)
    disable = models.BooleanField(verbose_name=u"禁用", default=False)

    def get_sender_dict(self):
        if self.disable:
            raise ValueError("Sender [%s]%s is disabled." % (self.id, self.name))
        sender_dict = dict()
        sender_dict['cookies'] = self.cookies
        field = dict()
        field['minLatE6'] = self.minLatE6
        field['maxLngE6'] = self.maxLngE6
        field['minLngE6'] = self.minLngE6
        field['maxLatE6'] = self.maxLatE6
        sender_dict['field'] = field
        sender_dict['team'] = self.team
        return sender_dict


class Watcher(models.Model):
    name = models.CharField(verbose_name=u"观察账号名", max_length=50, blank=False, null=False)
    cookies = models.TextField(verbose_name=u"cookies", blank=False, null=False)
    remark = models.CharField(verbose_name=u"备注", max_length=50, blank=True, null=True)
    disable = models.BooleanField(verbose_name=u"禁用", default=False)

    def get_watcher_cookie(self):
        if self.disable:
            raise ValueError("Watcher %s is disabled." % self.id)
        return self.cookies


class WatchPoint(models.Model):
    name = models.CharField(verbose_name="watcher point name", max_length=50, blank=False, null=False)
    maxLatE6 = models.IntegerField(verbose_name=u"maxLatE6")
    minLatE6 = models.IntegerField(verbose_name=u"minLatE6")
    maxLngE6 = models.IntegerField(verbose_name=u"maxLngE6")
    minLngE6 = models.IntegerField(verbose_name=u"minLngE6")
    disable = models.BooleanField(verbose_name=u"禁用", default=False)

    def get_watch_point_field(self):
        if self.disable:
            raise ValueError("watch point [%s]%s is disabled." % (self.id, self.name))
        field = dict()
        field['maxLatE6'] = self.maxLatE6
        field['minLatE6'] = self.minLatE6
        field['maxLngE6'] = self.maxLngE6
        field['minLngE6'] = self.minLngE6
        return field


class Setting(models.Model):
    welcome_message_send_condition = models.CharField(verbose_name="welcome message send condition, default not send",
                                                      max_length=10, blank=True, null=True, default=None,
                                                      choices=WELCOME_MESSAGE_SEND_CONDITION_CHOICES)
    welcome_message = models.TextField(verbose_name="welcome message", blank=False, null=False)
    fetch_message_tab = models.CharField(verbose_name="fetch message tab, default faction", max_length=7,
                                         choices=FETCH_MESSAGE_TAB_CHOICES, default="faction")
    sender = models.ForeignKey(Sender, blank=False, null=False)
    watcher = models.ForeignKey(Watcher, blank=False, null=False)
    watch_point = models.ForeignKey(WatchPoint, blank=False, null=False)

    def check_setting(self):
        if not self.welcome_message:
            return False
        if self.sender:
            if self.sender.disable:
                return False
        else:
            return False
        if self.watcher:
            if self.watcher.disable:
                return False
        else:
            return False
        if self.watch_point:

            if self.watch_point.disable:
                return False
        else:
            return False
        return True

    def get_dict(self):
        setting_dict = dict()
        setting_dict['welcome_condition'] = self.welcome_message_send_condition
        setting_dict['welcome_message'] = self.welcome_message
        setting_dict['fetch_message_tab'] = self.fetch_message_tab
        setting_dict['sender_id'] = self.sender_id
        setting_dict['watcher_id'] = self.watcher_id
        setting_dict['watch_point_id'] = self.watch_point_id
        return setting_dict

    @staticmethod
    def get_setting():
        setting = Setting.objects.all()
        if setting:
            return setting[0]
        else:
            raise ValueError("no setting record, please add setting record in admin.")

    @staticmethod
    def get_setting_dict():
        setting = Setting.get_setting()
        return setting.get_dict()


class Portal(models.Model):
    guid = models.CharField(verbose_name="portal guid", max_length=35, null=True, blank=True)
    name = models.TextField(verbose_name="portal name")
    latE6 = models.CharField(verbose_name="portal latitude, without decimal point", max_length=11, choices=TEAM_CHOICES,
                             blank=False, null=False)
    lngE6 = models.CharField(verbose_name="portal longitude, without decimal point", max_length=11,
                             choices=TEAM_CHOICES, blank=False, null=False)
    owner = models.TextField(verbose_name="sender name", max_length=50, blank=True, null=True)
    team = models.CharField(verbose_name="sender team", max_length=11, choices=TEAM_CHOICES, blank=True, null=True)
    update_time_stamp = models.CharField(verbose_name="portal info update time stamp", max_length=16, blank=False,
                                         null=False)
    last_captured_time_stamp = models.CharField(verbose_name="portal last captured time stamp", max_length=16,
                                                blank=False, null=False)

    def get_portal_guid(self, lat, lng):
        obj = self.objects.filter(latE6=lat).filter(lngE6=lng)
        if len(obj):
            return obj[0].guid
        return None

    def neutralize_portal(self, guid, portal_details_json):
        # TODO: when fetch messages, take portal neutralize message, update portal info include last_captured_time_stamp
        portal = self.objects.filter(guid=guid)
        if portal:
            pass
            # portal_detail = ingress_json_parser.PortalDetailParser(portal_details_json)
        else:
            raise ValueError("can not find portal with guid")

    @staticmethod
    def capture_portal(lat, lng, times_tamp):
        # TODO: when fetch messages, take portal capture message, update portal info include last_captured_time_stamp.
        portal_records = Portal.objects.filter(latE6=lat).filter(lngE6=lng)
        if portal_records.count() > 0:
            raise ValueError("portal record duplicate, lat %s, lng %s" % (lat, lng))
        elif portal_records.count() == 1:
            portal_record = portal_records[0]
            if (not portal_record.last_captured_time_stamp) or (portal_record.last_captured_time_stamp < times_tamp):
                portal_record.last_captured_time_stamp = times_tamp
                portal_record.save()
        else:
            raise ValueError("portal record not exist with lat %s, lng %s" % (lat, lng))

    def add_portal_info(self, guid, portal_details_json):
        portals = self.objects.filter(guid=guid)
        if portals:
            portal = self.objects.filter(guid=guid)[0]
            portal.update_portal_info(guid, portal_details_json)
        else:
            portal_parser = ingress_json_parser.PortalDetailParser(portal_details_json)
            portal = Portal()
            portal.guid = guid
            portal.name = portal_parser.name
            portal.latE6 = portal_parser.latE6
            portal.lngE6 = portal_parser.lngE6
            portal.owner = portal_parser.owner
            portal.team = portal_parser.team
            portal.update_time_stamp = time

    # run it with regular task, or stop
    def update_portal_info(self, name, lat, lng, team, owner, update_time_stamp, action):
        # TODO: redesign pars
        if self.guid:
            pass
        if self.name == name and self.latE6 == lat and self.lngE6 == lng:
            if int(update_time_stamp) > int(self.update_time_stamp):
                if action in [' captured ', 'neutralized']:
                    self.team = team
                    self.owner = owner
                    self.update_time_stamp = update_time_stamp
                    self.save()
        else:
            raise Exception("can not find portal '%s' in %s, %s" % (name, lat, lng))


class Agent(models.Model):
    name = models.CharField(verbose_name="agent name", max_length=50, null=False, blank=False)
    team = models.CharField(verbose_name="agent team", max_length=11, choices=TEAM_CHOICES, blank=False, null=False)
    level = models.SmallIntegerField(verbose_name="agent level")
    sent_welcome_message = models.BooleanField(verbose_name="sent welcome message", default=False)

    # TODO update portal pars
    @staticmethod
    def update_agent(agent_name, level=None):
        agents = Agent.objects.filter(name=agent_name)
        if agents:
            agent = agents[0]
            if level:
                if agent.level != level:
                    agent.level = level
                    agent.save()
        else:
            agent = Agent()
            agent.name = agent_name
            agent.level = level
            agent.save()


class Message(models.Model):
    guid = models.CharField(verbose_name="message guid", max_length=35, null=False, blank=False)
    time_stamp = models.CharField(verbose_name="message time stamp", max_length=16, blank=False, null=False)
    message_type = models.CharField(verbose_name="message type", max_length=30, null=True, blank=True)
    agent = models.CharField(verbose_name="agent name", max_length=50, blank=False, null=False)
    team = models.CharField(verbose_name="agent team", max_length=11, choices=TEAM_CHOICES, blank=True, null=True)
    plext = models.TextField(verbose_name="message content", null=False, blank=False)
    portal_name = models.CharField(verbose_name="portal name", max_length=50, null=True, blank=True)
    portal_guid = models.CharField(verbose_name="portal guid", max_length=35, null=True, blank=True)
    portal_lat = models.CharField(verbose_name="portal lat", max_length=15, null=True, blank=True)
    portal_lng = models.CharField(verbose_name="portal lng", max_length=15, null=True, blank=True)
    portal_address = models.TextField(verbose_name="portal lng", null=True, blank=True)

    @staticmethod
    def add_message(msg_parser):
        msg_guid = msg_parser.guid
        if not len(Message.objects.filter(guid=msg_guid)):
            msg_record = Message()
            msg_record.guid = msg_parser.guid
            msg_record.message_type = msg_parser.message_type
            msg_record.time_stamp = msg_parser.time_stamp
            msg_record.agent = msg_parser.agent
            msg_record.team = msg_parser.team
            msg_record.plext = msg_parser.text
            msg_record.portal_name = msg_parser.markup.portal_name
            msg_record.portal_lat = msg_parser.markup.portal_latE6
            msg_record.portal_lng = msg_parser.markup.portal_lngE6
            msg_record.portal_address = msg_parser.markup.portal_address
            msg_record.save()
            msg_record.send_welcome_message()
            return msg_guid
        return None

    def send_welcome_message(self):
        agents = Agent.objects.filter(name=self.agent)
        if agents:
            agent = agents[0]
            if agent.sent_welcome_message:
                return
        else:
            agent = Agent()
            agent.name = self.agent
            agent.team = self.team
            agent.level = 0
            agent.save()
        setting = Setting.get_setting()
        welcome_condition = setting.welcome_message_send_condition

        if (welcome_condition == "freshman" and self.message_type in FRESHMAN_MESSAGE_TYPES) \
                or welcome_condition == 'new_come':
            sender_dict = setting.sender.get_sender_dict()
            if sender_dict['team'] == self.team:
                welcome_message = "@%s %s" % (self.agent, setting.welcome_message)
                intel = Intel(sender_dict['cookies'], sender_dict['field'])
                intel.send_msg(welcome_message, setting.fetch_message_tab)
                agent.sent_welcome_message = True
                agent.save()
