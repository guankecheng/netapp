# Copyright 2020 The SODA Authors.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.


import time
from delfin.drivers.netapp.netapp_fas import netapp_constants
from delfin.common import constants

ALERT_SEVERITY_MAP = {
    'Unknown': constants.Severity.NOT_SPECIFIED,
    'Other': constants.Severity.NOT_SPECIFIED,
    'Information': constants.Severity.INFORMATIONAL,
    'Degraded': constants.Severity.WARNING,
    'Minor': constants.Severity.MINOR,
    'Major': constants.Severity.MAJOR,
    'Critical': constants.Severity.CRITICAL,
    'Fatal': constants.Severity.FATAL,
}


class AlertHandler(object):
    @staticmethod
    def handle_detail(system_info, storage_map, split):
        detail_arr = system_info.split('\r\n')
        for detail in detail_arr:
            if detail is not None and detail != '':
                strinfo = detail.split(split + " ")
                key = strinfo[0].replace(' ', '')
                value = ''
                if len(strinfo) > 1:
                    value = strinfo[1]
                storage_map[key] = value

    @staticmethod
    def list_events(self, event_info, query_para, alert_list):
        event_arr = event_info.split(netapp_constants.ALTER_SPLIT_STR)
        event_map = {}
        for event_str in event_arr[1:]:
            self.handle_detail(event_str, event_map, split=':')
            occur_time = int(time.mktime(time.strptime(
                event_map['Time'],
                netapp_constants.EVENT_TIME_TYPE)))
            if query_para is None or \
                    (query_para['begin_time']
                     <= occur_time
                     <= query_para['end_time']):
                alert_model = {
                    'alert_id': event_map['Sequence#'],
                    'alert_name': event_map['MessageName'],
                    'severity': event_map['Severity'],
                    'category': constants.Category.EVENT,
                    'type': constants.EventType.EQUIPMENT_ALARM,
                    'occur_time': occur_time,
                    'description': event_map['Event'],
                    'sequence_number': event_map['Sequence#'],
                    'resource_type': constants.DEFAULT_RESOURCE_TYPE,
                    'location': event_map['Source']
                }
                alert_list.append(alert_model)

    @staticmethod
    def list_alerts(self, alert_info, query_para, alert_list):
        alert_arr = alert_info.split(netapp_constants.ALTER_SPLIT_STR)
        alert_map = {}
        for alert_str in alert_arr[1:]:
            self.handle_detail(alert_str, alert_map, split=':')
            occur_time = int(time.mktime(time.strptime(
                alert_map['IndicationTime'],
                netapp_constants.ALTER_TIME_TYPE)))
            if query_para is None or \
                    (query_para['begin_time']
                     <= occur_time
                     <= query_para['end_time']):
                alert_model = {
                    'alert_id': alert_map['AlertID'],
                    'alert_name': alert_map['ProbableCause'],
                    'severity':
                        ALERT_SEVERITY_MAP[alert_map['PerceivedSeverity']],
                    'category': constants.Category.FAULT,
                    'type': constants.EventType.EQUIPMENT_ALARM,
                    'occur_time': occur_time,
                    'description': alert_map['Description'],
                    'sequence_number': alert_map['AlertID'],
                    'resource_type': constants.DEFAULT_RESOURCE_TYPE,
                    'location': alert_map['AlertingResourceName']
                }
                alert_list.append(alert_model)
