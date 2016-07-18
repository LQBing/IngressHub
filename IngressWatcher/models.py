from django.db import models
from IngressWatcher import ingress_json_parser
import ast
import time

TEAM_CHOICES = (
    ("ENLIGHTENED", "启萌菌"),
    ("RESISTANCE", "懒菌"),
)


# Create your models here.

class Senders(models.Model):
    name = models.TextField(verbose_name="sender name", max_length=50, blank=False, null=False)
    cookies = models.TextField(verbose_name="sender cookies", blank=False, null=False)
    field = models.TextField(verbose_name="sender field", blank=False, null=False)
    team = models.CharField(verbose_name="sender team", max_length=11, choices=TEAM_CHOICES, blank=False, null=False)


class Watchers(models.Model):
    name = models.TextField(verbose_name="watcher name", max_length=50, blank=False, null=False)
    cookies = models.TextField(verbose_name="sender cookies", blank=False, null=False)


class WatcherPoints(models.Model):
    name = models.TextField(verbose_name="watcher point name", max_length=50, blank=False, null=False)
    field = models.TextField(verbose_name="sender field", blank=False, null=False)

    def get_field(self):
        try:
            field = ast.literal_eval(self.field)
        except ValueError:
            return None
        if type(field) is not dict:
            return None
        return field


class Portals(models.Model):
    uuid = models.CharField(verbose_name="portal uuid", max_length=35, null=True, blank=True)
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

    def get_portal_uuid(self, lat, lng):
        obj = self.objects.filter(latE6=lat).filter(lngE6=lng)
        if obj.count():
            return obj.uuid
        return None

    def neutralize_portal(self, uuid, portal_details_json):
        # TODO: when fetch messages, take portal neutralize message, update portal info include last_captured_time_stamp
        portal = self.objects.filter(uuid=uuid)
        if portal:
            pass
            # portal_detail = ingress_json_parser.PortalDetailParser(portal_details_json)
        else:
            raise ValueError("can not find portal with uuid")

    @staticmethod
    def capture_portal(lat, lng, times_tamp):
        # TODO: when fetch messages, take portal capture message, update portal info include last_captured_time_stamp.
        portal_records = Portals.objects.filter(latE6=lat).filter(lngE6=lng)
        if portal_records.count() > 0:
            raise ValueError("portal record duplicate, lat %s, lng %s" % (lat, lng))
        elif portal_records.count() == 1:
            portal_record = portal_records[0]
            if (not portal_record.last_captured_time_stamp) or (portal_record.last_captured_time_stamp < times_tamp):
                portal_record.last_captured_time_stamp = times_tamp
                portal_record.save()
        else:
            raise ValueError("portal record not exist with lat %s, lng %s" % (lat, lng))

    def add_portal_info(self, uuid, portal_details_json):
        portals = self.objects.filter(uuid=uuid)
        if portals:
            portal = self.objects.filter(uuid=uuid)[0]
            portal.update_portal_info(uuid, portal_details_json)
        else:
            portal_parser = ingress_json_parser.PortalDetailParser(portal_details_json)
            portal = Portals()
            portal.uuid = uuid
            portal.name = portal_parser.name
            portal.latE6 = portal_parser.latE6
            portal.lngE6 = portal_parser.lngE6
            portal.owner = portal_parser.owner
            portal.team = portal_parser.team
            portal.update_time_stamp = time

    # run it with regular task, or stop
    def update_portal_info(self, name, lat, lng, team, owner, update_time_stamp, action):
        # TODO: redesign pars
        if self.uuid:
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


class Agents(models.Model):
    pass
    # TODO portal pars


class Messages(models.Model):
    pass
    # TODO messages pars
