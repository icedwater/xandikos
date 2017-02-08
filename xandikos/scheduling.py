# Xandikos
# Copyright (C) 2016 Jelmer Vernooij <jelmer@jelmer.uk>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; version 2
# of the License or (at your option) any later version of
# the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA  02110-1301, USA.

"""Scheduling.

See https://tools.ietf.org/html/rfc6638
"""

from defusedxml.ElementTree import fromstring as xmlparse
from xml.etree import ElementTree as ET

from xandikos import caldav, webdav


SCHEDULE_INBOX_RESOURCE_TYPE = '{%s}schedule-inbox' % caldav.NAMESPACE


class ScheduleInbox(caldav.Calendar):

    resource_types = caldav.Calendar.resource_types + [SCHEDULE_INBOX_RESOURCE_TYPE]

    def get_schedule_inbox_url(self):
        raise NotImplementedError(elf.get_schedule_inbox_url)

    def get_schedule_outbox_url(self):
        raise NotImplementedError(elf.get_schedule_inbox_url)

    def get_calendar_user_type(self):
        # Default, per section 2.4.2
        return "INDIVIDUAL"


class ScheduleInboxURLProperty(webdav.Property):
    """Schedule-inbox-URL property.

    See https://tools.ietf.org/html/rfc6638, section 2.2
    """

    name = '{%s}schedule-inbox-URL' % caldav.NAMESPACE
    resource_type = caldav.CALENDAR_RESOURCE_TYPE
    in_allprops = True

    def get_value(self, resource, el):
        el.append(webdav.create_href_element(resource.get_schedule_inbox_url()))


class ScheduleOutboxURLProperty(webdav.Property):
    """Schedule-outbox-URL property.

    See https://tools.ietf.org/html/rfc6638, section 2.1
    """

    name = '{%s}schedule-outbox-URL' % caldav.NAMESPACE
    resource_type = caldav.CALENDAR_RESOURCE_TYPE
    in_allprops = True

    def get_value(self, resource, el):
        el.append(webdav.create_href_element(resource.get_schedule_outbox_url()))


class CalendarUserAddressSetProperty(webdav.Property):
    """calendar-user-address-set property

    See https://tools.ietf.org/html/rfc6638, section 2.4.1
    """

    name = '{urn:ietf:params:xml:ns:caldav}calendar-user-address-set'
    resource_type = webdav.PRINCIPAL_RESOURCE_TYPE
    in_allprops = False

    def get_value(self, resource, el):
        for href in resource.get_calendar_user_address_set():
            el.append(webdav.create_href_element(href))


class CalendarUserTypeProperty(webdav.Property):
    """calendar-user-type property

    See https://tools.ietf.org/html/rfc6638, section 2.4.2
    """

    name = '{urn:ietf:params:xml:ns:caldav}calendar-user-type'
    resource_type = caldav.CALENDAR_RESOURCE_TYPE
    in_allprops = False

    def get_value(self, resource, el):
        el.text = resource.get_calendar_user_type()