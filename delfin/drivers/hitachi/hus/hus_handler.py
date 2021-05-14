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

import six
from oslo_log import log as logging
from oslo_utils import units
from delfin.drivers.hitachi.hus import hus_constants
from delfin import exception
from delfin.common import constants
from delfin.drivers.utils.cli_client import NaviClient

LOG = logging.getLogger(__name__)


def cli_handler(command_str):
    storage_info = NaviClient.exec(
        command_str.split(),
        hus_constants.STORAGE_MODEL,
        hus_constants.EXCEPTION_MAP)
    return storage_info


class HusHandler(object):

    def __init__(self, **kwargs):
        storage_info = cli_handler(hus_constants.STORAGE_NAME_COMMAND)
        cli_access = kwargs.get('cli')
        storage_arr = storage_info.split("\n")
        for storage in storage_arr:
            storage_str = storage.split()
            for _ in storage_str:
                if _ == cli_access['host']:
                    self.storage_name = storage_str[0]
                else:
                    pass

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
        elif unit == 'bl':
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
    def handle_detail(system_info, storage_map, split, is_raid_group=False):
        detail_arr = system_info.split('\n')
        for detail in detail_arr:
            if detail is not None and detail != '':
                strinfo = detail.split(split + "")
                key = strinfo[0].replace(' ', '')
                value = ''
                if is_raid_group and \
                        (key == 'FreeCapacity' or key == 'TotalCapacity'):
                    value = strinfo[1].split()[0] + 'bl'
                if len(strinfo) == 2:
                    value = strinfo[1].replace(' ', '')
                elif len(strinfo) > 2:
                    for i in range(1, len(strinfo)):
                        if i == len(strinfo) - 1:
                            value += strinfo[i]
                        else:
                            value += strinfo[i] + ':'
                storage_map[key] = value

    def get_storage(self):
        try:
            storage_map = {}
            raw_capacity = used_capacity = total_capacity = free_capacity = 0
            storage_info = cli_handler(
                hus_constants.STORAGE_INFO_COMMAND %
                {'unit_name': self.storage_name})
            self.handle_detail(storage_info, storage_map, ":")
            disk_info = cli_handler(
                hus_constants.DISK_INFO_COMMAND %
                {'unit_name': self.storage_name})
            pool_list = self.list_storage_pools(None)
            disk_arr = disk_info.split("\n")
            if len(disk_arr) > 1:
                for c in disk_arr[1:]:
                    c_arr = c.split()
                    if len(c_arr) > 1:
                        raw_capacity += int(self.parse_string(c_arr[2]))
            for pool in pool_list:
                used_capacity += pool['used_capacity']
                total_capacity += pool['total_capacity']
                free_capacity += pool['free_capacity']
            s = {
                'name': self.storage_name,
                'vendor': hus_constants.STORAGE_VENDOR,
                'description': '',
                'model': storage_map['ArrayUnitType'],
                'status': 'normal',
                'serial_number': storage_map['SerialNumber'],
                'firmware_version': storage_map['FirmwareRevision(CTL0)'],
                'location': '',
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
        pool_info = cli_handler(
            (hus_constants.POOL_INFO_COMMAND %
             {'unit_name': self.storage_name}))
        pool_arr = pool_info.split("\n")
        if len(pool_arr) > 2:
            for p in pool_arr[2:]:
                pool = p.split()
                if len(pool) > 2:
                    pool_detail = cli_handler(
                        hus_constants.POOL_DETAIL_INFO_COMMAND %
                        {'unit_name': self.storage_name, 'pool_no': pool[0]})
                    self.handle_detail(pool_detail, pool_map, ":")
                    p = {
                        'name': pool_map['DPPool'],
                        'storage_id': storage_id,
                        'native_storage_pool_id': pool_map['DPPool'],
                        'description': '',
                        'status':
                            constants.StoragePoolStatus.NORMAL
                            if pool_map['Status'] == 'Normal'
                            else constants.StoragePoolStatus.OFFLINE,
                        'storage_type': constants.StorageType.BLOCK,
                        'subscribed_capacity': '',
                        'total_capacity':
                            int(self.parse_string
                                (pool_map['TotalCapacity'])),
                        'used_capacity':
                            int(self.parse_string(
                                pool_map['Total'])) +
                            int(self.parse_string(
                                pool_map['UserData'])) +
                            int(self.parse_string(
                                pool_map['ReplicationData'])) +
                            int(self.parse_string(
                                pool_map['ManagementArea'])),
                        'free_capacity':
                            int(self.parse_string(
                                pool_map['ReplicationAvailableCapacity']))
                    }
                    pool_list.append(p)
        return pool_list

    def get_raid_groups(self, storage_id):
        pool_list = []
        raidgroup_map = {}
        raid_group_info = cli_handler(
            (hus_constants.RAIDGROUP_INFO_COMMAND %
             {'unit_name': self.storage_name}))
        raid_group_arr = raid_group_info.split("\n")
        if len(raid_group_arr) > 2:
            for r in raid_group_arr[2:]:
                raidgroup = r.split()
                if len(raidgroup) > 2:
                    raid_detail = cli_handler(
                        hus_constants.RAIDGROUP_DETAIL_INFO_COMMAND %
                        {'unit_name': self.storage_name,
                         'raidgroup_no': raidgroup[0]})
                    self.handle_detail(raid_detail, raidgroup_map, ":", True)
                    g = {
                        'name': raidgroup_map['RAIDGroup'],
                        'storage_id': storage_id,
                        'native_storage_pool_id': raidgroup_map['RAIDGroup'],
                        'description': '',
                        'status':
                            constants.StoragePoolStatus.NORMAL
                            if raidgroup_map['Status'] == 'Normal'
                            else constants.StoragePoolStatus.OFFLINE,
                        'storage_type': constants.StorageType.BLOCK,
                        'subscribed_capacity': '',
                        'total_capacity':
                            int(self.parse_string(
                                raidgroup_map['TotalCapacity'])),
                        'used_capacity':
                            int(self.parse_string(
                                raidgroup_map['TotalCapacity'])) -
                            int(self.parse_string(
                                raidgroup_map['FreeCapacity'])),
                        'free_capacity':
                            int(self.parse_string(
                                raidgroup_map['FreeCapacity']))
                    }
                    pool_list.append(g)
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

    @staticmethod
    def list_alerts(query_para):
        try:
            alert_list = []
            alerts_info = cli_handler(hus_constants.ALERT_INFO_COMMAND)
            alerts_arr = alerts_info.split('\n')
            for alert_info in alerts_arr:
                alert_arr = alert_info.split('/')
                occur_time = int(time.mktime(time.strptime(
                    alert_arr[0],
                    hus_constants.ALTER_TIME_TYPE)))
                if query_para is None or \
                        (query_para['begin_time']
                         <= occur_time
                         <= query_para['end_time']):
                    a = {
                        'alert_id': '',
                        'alert_name': '',
                        'severity': '',
                        'category': '',
                        'type': '',
                        'occur_time': alert_arr[0],
                        'description': alert_arr[2],
                        'sequence_number': '',
                        'resource_type': constants.DEFAULT_RESOURCE_TYPE,
                        'location': alert_arr[1]
                    }
                    alert_list.append(a)
            return alert_list
        except exception.DelfinException as e:
            err_msg = "Failed to get storage alert from " \
                      "hus, : %s" % (six.text_type(e))
            LOG.error(err_msg)
            raise e
        except Exception as err:
            err_msg = "Failed to get storage alert from " \
                      "hus, : %s" % (six.text_type(err))
            LOG.error(err_msg)
            raise exception.InvalidResults(err_msg)

    def get_pools_volumes(self, storage_id):
        volumes_list = []
        pool_list = cli_handler(
            (hus_constants.POOL_INFO_COMMAND %
             {'unit_name': self.storage_name}))
        pool_arr = pool_list.split("\n")
        if len(pool_arr) > 2:
            for pool in pool_arr[2:]:
                p_arr = pool.split()
                pool_info = cli_handler(
                    hus_constants.POOL_DETAIL_INFO_COMMAND %
                    {'unit_name': self.storage_name, 'pool_no': pool_arr[0]})
                volumes = pool_info.split("Logical Unit")
                if len(volumes) > 1:
                    volume_arr = volumes[1].split('\n')
                    for volume_info in volume_arr[3:]:
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
        volumes_info = cli_handler(
            (hus_constants.VOLUMES_INFO_COMMAND %
             {'unit_name': self.storage_name}))
        volumes_arr = volumes_info.split("\n")
        if len(volumes_arr) > 2:
            for volume_info in volumes_arr[2:]:
                volume_arr = volume_info.split()
                if len(volume_arr) > 4 and volume_arr[4] != 'N/A':
                    v = {
                        'name': volume_arr[0],
                        'storage_id': storage_id,
                        'description': '',
                        'status':
                            constants.PortHealthStatus.NORMAL
                            if volume_arr[13] == 'normal'
                            else constants.PortHealthStatus.ABNORMAL,
                        'native_volume_id': volume_arr[0],
                        'native_storage_pool_id': volume_arr[4],
                        'wwn': '',
                        'compressed': '',
                        'deduplicated': '',
                        'type': constants.VolumeType.THICK,
                        'total_capacity':
                            int(self.parse_string(volume_arr[1] + 'GB')),
                        'used_capacity': '',
                        'free_capacity': ''
                    }
                    volumes_list.append(v)
            return volumes_list

    def list_volumes(self, storage_id):
        try:
            raid_group_volumes_list = self.get_raid_group_volumes(storage_id)
            pool_volumes_list = self.get_pools_volumes(storage_id)
            return raid_group_volumes_list + pool_volumes_list
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
            status_info = cli_handler(
                hus_constants.STATUS_INFO_COMMAND %
                {'unit_name': self.storage_name})
            status_arr = status_info.split("Cache")
            controllers_arr = status_arr[1].split("Interface Board")
            controller_arr = controllers_arr[0].split("\n")
            v_map = {}
            version_info = cli_handler(
                hus_constants.STORAGE_INFO_COMMAND %
                {'unit_name': self.storage_name})
            self.handle_detail(version_info, v_map, ":")
            if len(controller_arr) > 2:
                for controller in controller_arr[2:]:
                    c_arr = controller.split()
                    if len(c_arr) > 2:
                        v = v_map['FirmwareRevision(CTL' + c_arr[0] + ')']
                        c = {
                            'name': 'controller' + c_arr[0],
                            'storage_id': storage_id,
                            'native_controller_id': c_arr[0],
                            'status':
                                constants.ControllerStatus.NORMAL
                                if c_arr[3] == 'normal'
                                else constants.ControllerStatus.OFFLINE,
                            'location': '',
                            'soft_version': v,
                            'cpu_info': '',
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
        fc_info = cli_handler(
            hus_constants.FC_PORT_INFO_COMMAND %
            {'unit_name': self.storage_name})
        port_status_info = cli_handler(
            hus_constants.STATUS_INFO_COMMAND %
            {'unit_name': self.storage_name})
        # port_wwn_info = cli_handler(
        #     hus_constants.WWN_INFO_COMMAND %
        #     {'unit_name': self.storage_name})
        port_status = \
            port_status_info.split("Host Connector")[1].split('Fan')[0]
        info = fc_info.split('Transfer Rate')
        ports_arr = info[0].split('\r\n')
        info = info[1].split('Topology Information')
        speeds_arr = info[0].split('\r\n')
        info = info[1].split('Link Status')
        status_arr = info[1].split('\r\n')
        if len(ports_arr) > 3:
            for ports in ports_arr[3:]:
                status_info = speed_info = []
                health_status = constants.PortHealthStatus.NORMAL
                port_info = ports.split()
                if len(port_info) > 5:
                    port_status_arr = port_status.split("\r\n")
                    if len(port_status_arr) > 2:
                        for port_status in port_status_arr[2:]:
                            health = port_status.split()
                            if len(health) > 1 \
                                    and health[0] == \
                                    port_info[0] + port_info[1]:
                                health_status = \
                                    constants.PortHealthStatus.NORMAL if \
                                    health[1] == 'Normal' else \
                                    constants.PortHealthStatus.ABNORMAL
                    if len(speeds_arr) > 2:
                        for speeds in speeds_arr[2:]:
                            speed_info = speeds.split()
                            if len(speed_info) > 1 and \
                                    speed_info[0] + speed_info[1] == \
                                    port_info[0] + port_info[1]:
                                break
                    if len(status_arr) > 2:
                        for status in status_arr[2:]:
                            status_info = status.split()
                            if len(status_info) > 1 and \
                                    status_info[0] + status_info[1] == \
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
                        'ipv4_mask': '-',
                        'ipv6': '',
                        'ipv6_mask': ''
                    }
                    fc_list.append(p)
            return fc_list

    def get_iscsi_port(self, storage_id):
        port_list = []
        ports_info = cli_handler(
            hus_constants.ISCSI_PORT_INFO_COMMAND %
            {'unit_name': self.storage_name})
        ports_arr = ports_info.split("Delayed Ack")
        port_map = {}
        for port_info in ports_arr:
            port_info_arr = port_info.split("\r\n")
            if len(port_info_arr) > 9:
                if port_info_arr[0].split()[0] == ':':
                    name = port_info_arr[2].split()[1]
                else:
                    name = port_info_arr[0].split()[1]
                self.handle_detail(port_info, port_map, ":")
                port_map['IPAddress'] = ''
                if port_map.get('IPv6Status') == 'Enable':
                    port_str = port_info.split('Global IP Address')
                    if len(port_str) > 0:
                        port_info_arr = port_str[0].split("\r\n")
                        for detail in port_info_arr:
                            if detail is not None and detail != '':
                                strinfo = detail.split(":")
                                key = strinfo[0].replace(' ', '')
                                value = ''
                                if len(strinfo) == 2:
                                    value = strinfo[1].replace(' ', '')
                                elif len(strinfo) > 2:
                                    for i in range(1, len(strinfo)):
                                        if i == len(strinfo) - 1:
                                            value += strinfo[i]
                                        else:
                                            value += strinfo[i] + ':'
                                port_map[key] = value
                p = {
                    'name': name,
                    'storage_id': storage_id,
                    'native_port_id': port_map['PortNumber'],
                    'location': '',
                    'connection_status':
                        constants.PortConnectionStatus.CONNECTED
                        if port_map['LinkStatus'] == 'LinkUp'
                        else constants.PortConnectionStatus.DISCONNECTED,
                    'health_status': '',
                    'type': constants.PortType.ISCSI,
                    'logical_type': '',
                    'speed': port_map['TransferRate'],
                    'max_speed': port_map['MTU'],
                    'native_parent_id': '',
                    'wwn': '',
                    'mac_address': '',
                    'ipv4': port_map['IPv4Address'],
                    'ipv4_mask': port_map['IPv4SubnetMask'],
                    'ipv6': port_map['IPAddress'],
                    'ipv6_mask': ''
                }
                port_list.append(p)
        return port_list

    def list_ports(self, storage_id):
        try:
            port_list = self.get_iscsi_port(storage_id)
            port_list += self.get_fc_ports(storage_id)
            return port_list
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

    def list_disks(self, storage_id):
        try:
            disks_list = []
            disk_info = cli_handler(
                hus_constants.DISK_INFO_COMMAND %
                {'unit_name': self.storage_name})
            disk_arr = disk_info.split("\n")
            if len(disk_arr) > 1:
                for disk in disk_arr[1:]:
                    disk = disk.split()
                    if len(disk) > 8:
                        d = {
                            'name': disk[1],
                            'storage_id': storage_id,
                            'native_disk_id': disk[1],
                            'serial_number': disk[8],
                            'manufacturer': disk[5],
                            'model': '',
                            'firmware': disk[7],
                            'speed': disk[4],
                            'capacity':
                                int(self.parse_string(disk[2])),
                            'status': '-',
                            'physical_type': disk[3],
                            'logical_type': '-',
                            'health_score': '-',
                            'native_disk_group_id': '',
                            'location': '-',
                        }
                        disks_list.append(d)
                return disks_list
        except exception.DelfinException as e:
            err_msg = "Failed to get storage disks from " \
                      "hus, : %s" % (six.text_type(e))
            LOG.error(err_msg)
            raise e
        except Exception as err:
            err_msg = "Failed to get storage disks from " \
                      "hus, : %s" % (six.text_type(err))
            LOG.error(err_msg)
            raise exception.InvalidResults(err_msg)
