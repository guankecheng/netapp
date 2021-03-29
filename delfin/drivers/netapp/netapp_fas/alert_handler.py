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

from netapp_handler import NetAppHandler
import time
import netapp_constants
from delfin.common import constants


class AlertHandler(object):

    @staticmethod
    def list_events(event_info, query_para, alert_list):
        event_arr = event_info.split(netapp_constants.ALTER_SPLIT_STR)
        event_map = {}
        for event_str in event_arr[1:]:
            NetAppHandler.handle_detail(event_str, event_map, split=':')
            occur_time = int(time.mktime(time.strptime(
                event_map.get('Time'),
                netapp_constants.EVENT_TIME_TYPE)))
            if query_para is None or (query_para.get('begin_time') <= occur_time <= query_para.get('end_time')):
                alert_model = {
                    'alert_id': event_map.get('Sequence#'),
                    'alert_name': event_map.get('MessageName'),
                    'severity': event_map.get('Severity'),
                    'category': constants.Category.EVENT,
                    'type': 'EquipmentAlarm',
                    'occur_time': event_map.get('Time'),
                    'description': event_map.get('Event'),
                    'sequence_number': event_map.get('Sequence#'),
                    'resource_type': constants.DEFAULT_RESOURCE_TYPE,
                    'location': event_map.get('Source')
                }
                alert_list.append(alert_model)

    @staticmethod
    def list_alerts(alert_info, query_para, alert_list):
        alert_arr = alert_info.split(netapp_constants.ALTER_SPLIT_STR)
        alert_map = {}
        for alert_str in alert_arr[1:]:
            NetAppHandler.handle_detail(alert_str, alert_map, split=':')
            occur_time = int(time.mktime(time.strptime(
                alert_map.get('IndicationTime'),
                netapp_constants.ALTER_TIME_TYPE)))
            if query_para is None or (query_para.get('begin_time') <= occur_time <= query_para.get('end_time')):
                alert_model = {
                    'alert_id': alert_map.get('AlertID'),
                    'alert_name': alert_map.get('ProbableCause'),
                    'severity': alert_map.get('PerceivedSeverity'),
                    'category': constants.Category.FAULT,
                    'type': 'EquipmentAlarm',
                    'occur_time': alert_map.get('IndicationTime'),
                    'description': alert_map.get('Description'),
                    'sequence_number': alert_map.get('AlertID'),
                    'resource_type': constants.DEFAULT_RESOURCE_TYPE,
                    'location': alert_map.get('AlertingResourceName')
                }
                alert_list.append(alert_model)