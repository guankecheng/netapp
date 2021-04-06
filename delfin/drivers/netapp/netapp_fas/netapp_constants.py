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

CLUSTER_SHOW_COMMAND = "cluster identity show"
AGGREGATE_SHOW_COMMAND = "storage aggregate show"
VERSION_SHOW_COMMAND = "version"
DISK_SHOW_COMMAND = "disk show"

POOLS_SHOW_DETAIL_COMMAND = "storage pool show -instance"
AGGREGATE_SHOW__DETAIL_COMMAND = "storage aggregate show -instance"
POOLS_SPLIT_STR = "Storage Pool N"
AGGREGATE_SPLIT_STR = "                                         Aggregat"

VOLUME_SHOW_DETAIL_COMMAND = "vol show -instance"
VOLUME_SPLIT_STR = "                                   Vserver"

ALTER_SHOW_DETAIL_COMMAND = "system health alert show -instance"
EVENT_SHOW_DETAIL_COMMAND = "event show -instance -severity EMERGENCY"
ALTER_SPLIT_STR = " Node"
EVENT_TIME_TYPE = '%m/%d/%Y %H:%M:%S'
ALTER_TIME_TYPE = '%a %b %d %H:%M:%S %Y'

CLEAR_ALERT_COMMAND = "system health alert delete -alerting-resource * -alert-id "

CONTROLLER_SHOW_DETAIL_COMMAND = "system controller show -instance"
CONTROLLER_SPLIT_STR = "  Nod"

PORT_SHOW_DETAIL_COMMAND = "port show -instance"
INTERFACE_SHOW_DETAIL_COMMAND = ""
PORT_SPLIT_STR = "  Nod"
INTERFACE_SPLIT_STR = " Vserver "

DISK_SHOW_DETAIL_COMMAND = "disk show -instance"
DISK_SHOW_PHYSICAL_COMMAND = "disk show -physical"
DISK_SPLIT_STR = "     Dis"

QTREE_SHOW_DETAIL_COMMAND = "qtree show -instance"
QTREE_SPLIT_STR = " Vserver "


CIFS_SHARE_SHOW_DETAIL_COMMAND = "vserver cifs share show -instance"
CIFS_SHARE_SPLIT_STR = " Vserve"

FS_SHOW_COMMAND = "df -skip-snapshot-lines"
VSERVER_SHOW_COMMAND = "vserver show"
FS_DEDUPLICATED_SHOW_COMMAND = "df -S"


