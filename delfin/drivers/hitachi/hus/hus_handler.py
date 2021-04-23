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


import six
from oslo_log import log as logging
from oslo_utils import units
from delfin.drivers.hitachi.hus import hus_constants
from delfin import exception
from delfin.common import constants
from delfin.drivers.hitachi.hus.navicli_client import NaviClient

LOG = logging.getLogger(__name__)


class HusHandler(object):

    def __init__(self, **kwargs):
        self.storage_name = "HUS110_91110206"

    @staticmethod
    def change_capacity_to_bytes(unit):
        unit = unit.upper()
        if unit == 'TB':
            result = units.Ti
        elif unit == 'GB':
            result = units.Gi
        elif unit == 'MB':
            result = units.Mi
        elif unit == 'KB':
            result = units.Ki
        elif unit == 'blocks':
            result = units.Ki * 4
        else:
            result = 1
        return int(result)

    def parse_string(self, value):
        capacity = 0
        if value:
            if value.isdigit():
                capacity = float(value)
            else:
                unit = value[-2:]
                capacity = float(value[:-2]) * int(
                    self.change_capacity_to_bytes(unit))
        return capacity

    @staticmethod
    def handle_detail(system_info, storage_map, split):
        detail_arr = system_info.split('\n')
        for detail in detail_arr:
            if detail is not None and detail != '':
                strinfo = detail.split(split + "")
                key = strinfo[0].replace(' ', '')
                value = ''
                if len(strinfo) > 1:
                    value = strinfo[1].replace(' ', '')
                storage_map[key] = value

    def get_storage(self):
        try:
            storage_map = {}
            raw_capacity = used_capacity = total_capacity = free_capacity = 0
            storage_info = NaviClient.exec(
                (hus_constants.STORAGE_INFO_COMMAND %
                 {self.storage_name}).split())
            self.handle_detail(storage_info, storage_map, ":")
            disk_info = NaviClient.exec(
                (hus_constants.DISK_INFO_COMMAND %
                 {self.storage_name}).split())
            pool_list = self.list_storage_pools(None)
            disk_arr = disk_info.split("\n")
            if len(disk_arr) > 1:
                for c in disk_arr[1:]:
                    c_arr = c.split()
                    raw_capacity += int(self.parse_string(c_arr[2]))
            for pool in pool_list:
                used_capacity += pool['used_capacity']
                total_capacity += pool['total_capacity']
                free_capacity += pool['free_capacity']
            s = {
                'name': self.storage_name,
                'vendor': hus_constants.STORAGE_VENDOR,
                'description': '-',
                'model': storage_map['ArrayUnitType'],
                'status': 'normal',
                'serial_number': storage_map['SerialNumber'],
                'firmware_version': storage_map['FirmwareRevision(CTL0)'],
                'location': '-',
                'total_capacity': total_capacity,
                'used_capacity': used_capacity,
                'free_capacity': free_capacity,
                'raw_capacity': raw_capacity
            }
            return s
        except exception.DelfinException as e:
            err_msg = "Failed to get storage pool from " \
                      "hus, : %s" % (six.text_type(e))
            LOG.error(err_msg)
            raise e
        except Exception as err:
            err_msg = "Failed to get storage pool from " \
                      "hus, : %s" % (six.text_type(err))
            LOG.error(err_msg)
            raise exception.InvalidResults(err_msg)

    def get_pools(self, storage_id):
        pool_list = []
        pool_map = {}
        pool_info = NaviClient.exec(
            (hus_constants.POOL_INFO_COMMAND % {self.storage_name}).split())
        pool_arr = pool_info.split("\n")
        if len(pool_arr) > 2:
            for p in pool_arr[2:]:
                pool = p.split()
                pool_detail = NaviClient.exec(
                    (hus_constants.POOL_DETAIL_INFO_COMMAND %
                     {self.storage_name, pool[0]}).split())
                self.handle_detail(pool_detail, pool_map, ":")
                p = {
                    'name': pool_map['DpPool'],
                    'storage_id': storage_id,
                    'native_storage_pool_id': pool_map['DpPool'],
                    'description': '',
                    'status':
                        constants.StoragePoolStatus.NORMAL
                        if pool_map['Status'] == 'Normal'
                        else constants.StoragePoolStatus.OFFLINE,
                    'storage_type': constants.StorageType.BLOCK,
                    'subscribed_capacity': '',
                    'total_capacity':
                        int(self.parse_string(pool_map['TotalCapacity'])),
                    'used_capacity':
                        int(self.parse_string(pool_map['Total'])) +
                        int(self.parse_string(pool_map['UserData'])) +
                        int(self.parse_string(pool_map['ReplicationData'])) +
                        int(self.parse_string(pool_map['ManagementArea'])),
                    'free_capacity':
                        int(self.parse_string(
                            pool_map['ReplicationAvailableCapacity']))
                }
                pool_list.append(p)
        return pool_list

    def get_raid_groups(self, storage_id):
        pool_list = []
        riad_group_info = ""
        raid_group_arr = riad_group_info.split("\n")
        if len(raid_group_arr) > 2:
            for r in raid_group_arr[2:]:
                raidgroup = r.split()
                if len(raidgroup) > 16:
                    p = {
                        'name': raidgroup[0],
                        'storage_id': storage_id,
                        'native_storage_pool_id': raidgroup[0],
                        'description': '',
                        'status':
                            constants.StoragePoolStatus.NORMAL
                            if raidgroup[15] == 'Normal'
                            else constants.StoragePoolStatus.OFFLINE,
                        'storage_type': constants.StorageType.BLOCK,
                        'subscribed_capacity': '',
                        'total_capacity':
                            int(self.parse_string(raidgroup[7] + 'GB')),
                        'used_capacity':
                            int(self.parse_string(raidgroup[7] + 'GB')) -
                            int(self.parse_string(raidgroup[9] + 'GB')),
                        'free_capacity':
                            int(self.parse_string(raidgroup[9] + 'GB'))
                    }
                    pool_list.append(p)
            return pool_list

    def list_storage_pools(self, storage_id):
        try:
            pool_list = []
            pool_list += self.get_pools(storage_id)
            pool_list += self.get_raid_groups(storage_id)
            return pool_list
        except exception.DelfinException as e:
            err_msg = "Failed to get storage pool from " \
                      "hus, : %s" % (six.text_type(e))
            LOG.error(err_msg)
            raise e
        except Exception as err:
            err_msg = "Failed to get storage pool from " \
                      "hus, : %s" % (six.text_type(err))
            LOG.error(err_msg)
            raise exception.InvalidResults(err_msg)

    def get_pools_volumes(self, storage_id):
        volumes_list = []
        pool_list = NaviClient.exec(
            (hus_constants.POOL_INFO_COMMAND % {self.storage_name}).split())
        pool_arr = pool_list.split("\n")
        if len(pool_arr) > 2:
            for pool in pool_arr:
                p_arr = pool.split()
                pool_info = NaviClient.exec(
                    (hus_constants.POOL_DETAIL_INFO_COMMAND %
                     {self.storage_name, p_arr[0]}).split())
                volumes = pool_info[1].split("Logical Unit")
                if len(volumes) > 1:
                    volume_arr = volumes[1].split('\n')
                    for volume_info in volume_arr:
                        volume = volume_info.split()
                        if len(volume) > 9:
                            v = {
                                'name': volume[0],
                                'storage_id': storage_id,
                                'description': '',
                                'status':
                                    constants.PortHealthStatus.NORMAL
                                    if volume[9] == 'normal'
                                    else constants.PortHealthStatus.ABNORMAL,
                                'native_volume_id': volume[0],
                                'native_storage_pool_id': p_arr[0],
                                'wwn': '',
                                'compressed': '',
                                'deduplicated': '',
                                'type': constants.VolumeType.THIN,
                                'total_capacity':
                                    int(self.parse_string(volume[1] + 'GB')),
                                'used_capacity':
                                    int(self.parse_string(volume[3] + 'GB')),
                                'free_capacity':
                                    int(self.parse_string(volume[1] + 'GB')) -
                                    int(self.parse_string(volume[3] + 'GB'))
                            }
                            volumes_list.append(v)
                    return volumes_list

    def get_raid_group_volumes(self, storage_id):
        volumes_list = []
        volumes_info = NaviClient.exec(
            (hus_constants.VOLUMES_INFO_COMMAND %
             {self.storage_name}).split())
        volumes_arr = volumes_info.split("\n")
        if len(volumes_arr) > 2:
            for volume_info in volumes_arr[2:]:
                volume_arr = volume_info.split()
                if len(volumes_arr) > 4 and volume_arr[3] != 'N/A':
                    v = {
                        'name': volumes_arr[0],
                        'storage_id': storage_id,
                        'description': '',
                        'status':
                            constants.PortHealthStatus.NORMAL
                            if volumes_arr[0] == 'normal'
                            else constants.PortHealthStatus.ABNORMAL,
                        'native_volume_id': volumes_arr[0],
                        'native_storage_pool_id': volumes_arr[4],
                        'wwn': '',
                        'compressed': '',
                        'deduplicated': '',
                        'type': constants.VolumeType.THICK,
                        'total_capacity':
                            int(self.parse_string(volumes_arr[1] + 'GB')),
                        'used_capacity': 'N/A',
                        'free_capacity': 'N/A'
                    }
                    volumes_list.append(v)
                return volumes_list

    def list_volumes(self, storage_id):
        try:
            volumes_list = []
            volumes_list += self.get_raid_group_volumes(storage_id)
            volumes_list += self.get_pools_volumes(storage_id)
            return volumes_list
        except exception.DelfinException as e:
            err_msg = "Failed to get storage pool from " \
                      "hus, : %s" % (six.text_type(e))
            LOG.error(err_msg)
            raise e
        except Exception as err:
            err_msg = "Failed to get storage pool from " \
                      "hus, : %s" % (six.text_type(err))
            LOG.error(err_msg)
            raise exception.InvalidResults(err_msg)

    def list_controllers(self, storage_id):
        try:
            controller_list = []
            status_info = NaviClient.exec(
                hus_constants.STATUS_INFO_COMMAND % {self.storage_name})
            status_arr = status_info.split("Cache")
            controllers_arr = status_arr[1].split("Interface Board")
            controller_arr = controllers_arr[0].split("\n")
            if len(controller_arr) > 1:
                for controller in controllers_arr[1:]:
                    c_arr = controller.split()
                    c = {
                        'name': 'controller' + c_arr[0],
                        'storage_id': storage_id,
                        'native_controller_id': c_arr[0],
                        'status':
                            constants.ControllerStatus.NORMAL
                            if c_arr[3] == 'normal'
                            else constants.ControllerStatus.OFFLINE,
                        'location': '-',
                        'soft_version': '-',
                        'cpu_info': '-',
                        'memory_size': c_arr[2],
                    }
                    controller_list.append(c)
                return controller_list
        except exception.DelfinException as e:
            err_msg = "Failed to get storage controllers " \
                      "from hus, : %s" % (six.text_type(e))
            LOG.error(err_msg)
            raise e

        except Exception as err:
            err_msg = "Failed to get storage controllers " \
                      "from hus, : %s" % (six.text_type(err))
            LOG.error(err_msg)
            raise exception.InvalidResults(err_msg)

    def get_fc_ports(self, storage_id):
        fc_list = []
        fc_info = NaviClient.exec(
            hus_constants.FC_PORT_INFO_COMMAND % {self.storage_name})
        port_status_info = NaviClient.exec(
            hus_constants.STATUS_INFO_COMMAND % {self.storage_name})
        port_status_arr = \
            port_status_info.split("Host Connector")[1].split('Fan')[0]
        info = fc_info.split('Transfer Rate')
        ports_arr = info[0].split('\n')
        info = info.split('Topology Information')
        speeds_arr = info[0].split('\n')
        info = info.split('Link Status')
        status_arr = info[1].split('\n')
        if len(ports_arr) > 3:
            for ports in ports_arr[3:]:
                status_info = speed_info = []
                health_status = constants.PortHealthStatus.NORMAL
                port_info = ports.split()
                if len(port_status_arr) > 1:
                    for port_status in port_status_arr:
                        health = port_status.split()
                        if health[0] == port_info[0] + port_info[1]:
                            health_status = \
                                constants.PortHealthStatus.NORMAL \
                                if health[1] == 'Normal' \
                                else constants.PortHealthStatus.ABNORMAL
                if len(speeds_arr) > 1:
                    for speeds in speeds_arr[1:]:
                        speed_info = speeds.split()
                        if speed_info[0] + speed_info[1] == \
                                port_info[0] + port_info[1]:
                            break
                if len(status_arr) > 1:
                    for status in status_arr[1:]:
                        status_info = status.split()
                        if status_info[0] + status_info[1] == \
                                port_info[0] + port_info[1]:
                            break
                p = {
                    'name': port_info[0] + port_info[1],
                    'storage_id': storage_id,
                    'native_port_id': port_info[3],
                    'location': '',
                    'connection_status':
                        constants.PortConnectionStatus.CONNECTED
                        if status_info[2] != 'Link Failure'
                        else constants.PortConnectionStatus.DISCONNECTED,
                    'health_status': health_status,
                    'type': constants.PortType.FC,
                    'logical_type': '-',
                    'speed': speed_info[3],
                    'max_speed': speed_info[3],
                    'native_parent_id': '-',
                    'wwn': '-',
                    'mac_address': '',
                    'ipv4': '',
                    'ipv4_mask': 'ipv4_mask',
                    'ipv6': '',
                    'ipv6_mask': ''
                }
                fc_list.append(p)
            return fc_list

    def list_ports(self, storage_id):
        try:
            return self.get_fc_ports(storage_id)
        except exception.DelfinException as e:
            err_msg = "Failed to get storage ports from " \
                      "hus, : %s" % (six.text_type(e))
            LOG.error(err_msg)
            raise e

        except Exception as err:
            err_msg = "Failed to get storage ports from " \
                      "hus, : %s" % (six.text_type(err))
            LOG.error(err_msg)
            raise exception.InvalidResults(err_msg)
