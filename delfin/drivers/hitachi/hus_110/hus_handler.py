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
from delfin.drivers.hitachi.hus_110 import constants as constant
from delfin import exception
from delfin.common import constants
from delfin.drivers.utils.cli_client import NaviClient
from delfin.drivers.utils.tools import Tools

LOG = logging.getLogger(__name__)


def cli_handler(command_str):
    storage_info = NaviClient.exec(
        command_str.split(),
        constant.STORAGE_MODEL,
        constant.EXCEPTION_MAP)
    return storage_info


class HusHandler(object):

    def __init__(self, **kwargs):
        storage_info = cli_handler(constant.STORAGE_NAME_COMMAND)
        cli_access = kwargs.get('cli')
        storage_array = storage_info.split("\r\n")
        for storage in storage_array:
            storage_str = storage.split()
            for _ in storage_str:
                if _ == cli_access['host']:
                    self.storage_name = storage_str[0]
                else:
                    pass

    @staticmethod
    def get_detail(system_info, storage_map, split, is_raid_group=False):
        detail_array = system_info.split('\r\n')
        for detail in detail_array:
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
                constant.STORAGE_INFO_COMMAND %
                {'unit_name': self.storage_name})
            self.get_detail(storage_info, storage_map, ":")
            disk_info = cli_handler(
                constant.DISK_INFO_COMMAND %
                {'unit_name': self.storage_name})
            pool_list = self.list_storage_pools(None)
            disk_array = disk_info.split("\r\n")
            if len(disk_array) > 1:
                for disk in disk_array[1:]:
                    disk_array = disk.split()
                    if len(disk_array) > 1:
                        raw_capacity += int(
                            Tools.get_capacity_size(disk_array[2]))
            for pool in pool_list:
                used_capacity += pool['used_capacity']
                total_capacity += pool['total_capacity']
                free_capacity += pool['free_capacity']
            storage = {
                'name': self.storage_name,
                'vendor': constant.STORAGE_VENDOR,
                'description': '',
                'model': storage_map['arrayayUnitType'],
                'status': 'normal',
                'serial_number': storage_map['SerialNumber'],
                'firmware_version': storage_map['FirmwareRevision(CTL0)'],
                'location': '',
                'total_capacity': total_capacity,
                'used_capacity': used_capacity,
                'free_capacity': free_capacity,
                'raw_capacity': raw_capacity
            }
            return storage
        except exception.DelfinException as e:
            err_msg = "Failed to get storage pool from " \
                      "hus_110, : %s" % (six.text_type(e))
            LOG.error(err_msg)
            raise e
        except Exception as err:
            err_msg = "Failed to get storage pool from " \
                      "hus_110, : %s" % (six.text_type(err))
            LOG.error(err_msg)
            raise exception.InvalidResults(err_msg)

    def get_pools(self, storage_id):
        pool_list = []
        pool_map = {}
        pools_info = cli_handler(
            (constant.POOL_INFO_COMMAND %
             {'unit_name': self.storage_name}))
        pools_array = pools_info.split("\r\n")
        if len(pools_array) > 2:
            for pool_info in pools_array[2:]:
                pool_array = pool_info.split()
                if len(pool_array) > 2:
                    pool_detail = cli_handler(
                        constant.POOL_DETAIL_INFO_COMMAND %
                        {'unit_name': self.storage_name,
                         'pool_no': pool_array[0]})
                    self.get_detail(pool_detail, pool_map, ":")
                    pool_model = {
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
                            int(Tools.get_capacity_size
                                (pool_map['TotalCapacity'])),
                        'used_capacity':
                            int(Tools.get_capacity_size(
                                pool_map['Total'])) +
                            int(Tools.get_capacity_size(
                                pool_map['UserData'])) +
                            int(Tools.get_capacity_size(
                                pool_map['ReplicationData'])) +
                            int(Tools.get_capacity_size(
                                pool_map['ManagementArea'])),
                        'free_capacity':
                            int(Tools.get_capacity_size(
                                pool_map['ReplicationAvailableCapacity']))
                    }
                    pool_list.append(pool_model)
        return pool_list

    def get_raid_groups(self, storage_id):
        pool_list = []
        raid_group_map = {}
        raid_group_info = cli_handler(
            (constant.RAIDGROUP_INFO_COMMAND %
             {'unit_name': self.storage_name}))
        raid_group_array = raid_group_info.split("\r\n")
        if len(raid_group_array) > 2:
            for raid_array in raid_group_array[2:]:
                raid_group = raid_array.split()
                if len(raid_group) > 2:
                    raid_detail = cli_handler(
                        constant.RAIDGROUP_DETAIL_INFO_COMMAND %
                        {'unit_name': self.storage_name,
                         'raidgroup_no': raid_group[0]})
                    self.get_detail(raid_detail, raid_group_map, ":", True)
                    raid_group_model = {
                        'name': raid_group_map['RAIDGroup'],
                        'storage_id': storage_id,
                        'native_storage_pool_id': raid_group_map['RAIDGroup'],
                        'description': '',
                        'status':
                            constants.StoragePoolStatus.NORMAL
                            if raid_group_map['Status'] == 'Normal'
                            else constants.StoragePoolStatus.OFFLINE,
                        'storage_type': constants.StorageType.BLOCK,
                        'subscribed_capacity': '',
                        'total_capacity':
                            int(Tools.get_capacity_size(
                                raid_group_map['TotalCapacity'])),
                        'used_capacity':
                            int(Tools.get_capacity_size(
                                raid_group_map['TotalCapacity'])) -
                            int(Tools.get_capacity_size(
                                raid_group_map['FreeCapacity'])),
                        'free_capacity':
                            int(Tools.get_capacity_size(
                                raid_group_map['FreeCapacity']))
                    }
                    pool_list.append(raid_group_model)
            return pool_list

    def list_storage_pools(self, storage_id):
        try:
            pool_list = []
            pool_list += self.get_pools(storage_id)
            pool_list += self.get_raid_groups(storage_id)
            return pool_list
        except exception.DelfinException as e:
            err_msg = "Failed to get storage pool from " \
                      "hus_110, : %s" % (six.text_type(e))
            LOG.error(err_msg)
            raise e
        except Exception as err:
            err_msg = "Failed to get storage pool from " \
                      "hus_110, : %s" % (six.text_type(err))
            LOG.error(err_msg)
            raise exception.InvalidResults(err_msg)

    @staticmethod
    def list_alerts(query_para):
        try:
            alert_list = []
            alerts_info = cli_handler(constant.ALERT_INFO_COMMAND)
            alerts_array = alerts_info.split('\r\n')
            for alert_info in alerts_array:
                alert_array = alert_info.split('/')
                occur_time = int(time.mktime(time.strptime(
                    alert_array[0], constant.ALTER_TIME_TYPE)))
                if query_para is None or \
                        (query_para['begin_time']
                         <= occur_time
                         <= query_para['end_time']):
                    alert_model = {
                        'alert_id': '',
                        'alert_name': '',
                        'severity': '',
                        'category': '',
                        'type': '',
                        'occur_time': alert_array[0],
                        'description': alert_array[2],
                        'sequence_number': '',
                        'resource_type': constants.DEFAULT_RESOURCE_TYPE,
                        'location': alert_array[1]
                    }
                    alert_list.append(alert_model)
            return alert_list
        except exception.DelfinException as e:
            err_msg = "Failed to get storage alert from " \
                      "hus_110, : %s" % (six.text_type(e))
            LOG.error(err_msg)
            raise e
        except Exception as err:
            err_msg = "Failed to get storage alert from " \
                      "hus_110, : %s" % (six.text_type(err))
            LOG.error(err_msg)
            raise exception.InvalidResults(err_msg)

    def get_pools_volumes(self, storage_id):
        volumes_list = []
        pool_list = cli_handler(
            (constant.POOL_INFO_COMMAND %
             {'unit_name': self.storage_name}))
        pools_array = pool_list.split("\r\n")
        if len(pools_array) > 2:
            for pool in pools_array[2:]:
                pool_array = pool.split()
                pool_info = cli_handler(
                    constant.POOL_DETAIL_INFO_COMMAND %
                    {'unit_name': self.storage_name, 'pool_no': pool_array[0]})
                volumes = pool_info.split("Logical Unit")
                if len(volumes) > 1:
                    volume_array = volumes[1].split('\r\n')
                    for volume_info in volume_array[3:]:
                        volume = volume_info.split()
                        if len(volume) > 9:
                            volume_model = {
                                'name': volume[0],
                                'storage_id': storage_id,
                                'description': '',
                                'status':
                                    constants.StoragePoolStatus.NORMAL
                                    if volume[9] == 'normal'
                                    else constants.StoragePoolStatus.ABNORMAL,
                                'native_volume_id': volume[0],
                                'native_storage_pool_id': pool_array[0],
                                'wwn': '',
                                'compressed': '',
                                'deduplicated': '',
                                'type': constants.VolumeType.THIN,
                                'total_capacity':
                                    int(Tools.get_capacity_size(
                                        volume[1] + 'GB')),
                                'used_capacity':
                                    int(Tools.get_capacity_size(
                                        volume[3] + 'GB')),
                                'free_capacity':
                                    int(Tools.get_capacity_size(
                                        volume[1] + 'GB')) -
                                    int(Tools.get_capacity_size(
                                        volume[3] + 'GB'))
                            }
                            volumes_list.append(volume_model)
                    return volumes_list

    def get_raid_group_volumes(self, storage_id):
        volumes_list = []
        volumes_info = cli_handler(
            (constant.VOLUMES_INFO_COMMAND %
             {'unit_name': self.storage_name}))
        volumes_array = volumes_info.split("\r\n")
        if len(volumes_array) > 2:
            for volume_info in volumes_array[2:]:
                volume_array = volume_info.split()
                if len(volume_array) > 4 and volume_array[4] != 'N/A':
                    volume_model = {
                        'name': volume_array[0],
                        'storage_id': storage_id,
                        'description': '',
                        'status':
                            constants.VolumeStatus.AVAILABLE
                            if volume_array[13] == 'normal'
                            else constants.VolumeStatus.ERROR,
                        'native_volume_id': volume_array[0],
                        'native_storage_pool_id': volume_array[4],
                        'wwn': '',
                        'compressed': '',
                        'deduplicated': '',
                        'type': constants.VolumeType.THICK,
                        'total_capacity':
                            int(Tools.get_capacity_size(
                                volume_array[1] + 'GB')),
                        'used_capacity': int(Tools.get_capacity_size(
                                volume_array[1] + 'GB')),
                        'free_capacity': 0
                    }
                    volumes_list.append(volume_model)
            return volumes_list

    def list_volumes(self, storage_id):
        try:
            raid_group_volumes_list = self.get_raid_group_volumes(storage_id)
            pool_volumes_list = self.get_pools_volumes(storage_id)
            return raid_group_volumes_list + pool_volumes_list
        except exception.DelfinException as e:
            err_msg = "Failed to get storage pool from " \
                      "hus_110, : %s" % (six.text_type(e))
            LOG.error(err_msg)
            raise e
        except Exception as err:
            err_msg = "Failed to get storage pool from " \
                      "hus_110, : %s" % (six.text_type(err))
            LOG.error(err_msg)
            raise exception.InvalidResults(err_msg)

    def list_controllers(self, storage_id):
        try:
            controller_list = []
            status_info = cli_handler(
                constant.STATUS_INFO_COMMAND %
                {'unit_name': self.storage_name})
            status_array = status_info.split("Cache")
            controllers_array = status_array[1].split("Interface Board")
            controller_array = controllers_array[0].split("\r\n")
            v_map = {}
            version_info = cli_handler(
                constant.STORAGE_INFO_COMMAND %
                {'unit_name': self.storage_name})
            self.get_detail(version_info, v_map, ":")
            if len(controller_array) > 2:
                for controller in controller_array[2:]:
                    c_array = controller.split()
                    if len(c_array) > 2:
                        v = v_map['FirmwareRevision(CTL' + c_array[0] + ')']
                        c = {
                            'name': 'controller' + c_array[0],
                            'storage_id': storage_id,
                            'native_controller_id': c_array[0],
                            'status':
                                constants.ControllerStatus.NORMAL
                                if c_array[3] == 'normal'
                                else constants.ControllerStatus.OFFLINE,
                            'location': '',
                            'soft_version': v,
                            'cpu_info': '',
                            'memory_size': c_array[2],
                        }
                        controller_list.append(c)
                return controller_list
        except exception.DelfinException as e:
            err_msg = "Failed to get storage controllers " \
                      "from hus_110, : %s" % (six.text_type(e))
            LOG.error(err_msg)
            raise e

        except Exception as err:
            err_msg = "Failed to get storage controllers " \
                      "from hus_110, : %s" % (six.text_type(err))
            LOG.error(err_msg)
            raise exception.InvalidResults(err_msg)

    def get_fc_ports(self, storage_id):
        fc_list = []
        key = ''
        fc_info = cli_handler(
            constant.FC_PORT_INFO_COMMAND %
            {'unit_name': self.storage_name})
        port_status_info = cli_handler(
            constant.STATUS_INFO_COMMAND %
            {'unit_name': self.storage_name})
        port_wwn_info = cli_handler(
            constant.WWN_INFO_COMMAND %
            {'unit_name': self.storage_name})
        wwns_array = port_wwn_info.split("\r\n")
        wwn_map = {}
        for wwn_info in wwns_array:
            wwn_array = wwn_info.split()
            if len(wwn_array) > 5:
                key = wwn_array[1]
            elif len(wwn_array) == 2 and wwn_array[1] != 'WWN':
                value = wwn_array[0]
                wwn_map[key] = value
        port_status = \
            port_status_info.split("Host Connector")[1].split('Fan')[0]
        info = fc_info.split('Transfer Rate')
        ports_array = info[0].split('\r\n')
        info = info[1].split('Topology Information')
        speeds_array = info[0].split('\r\n')
        info = info[1].split('Link Status')
        status_array = info[1].split('\r\n')
        if len(ports_array) > 3:
            for ports in ports_array[3:]:
                status_info = speed_info = []
                health_status = constants.PortHealthStatus.NORMAL
                port_info = ports.split()
                if len(port_info) > 5:
                    port_status_array = port_status.split("\r\n")
                    if len(port_status_array) > 2:
                        for port_status in port_status_array[2:]:
                            health = port_status.split()
                            if len(health) > 1 \
                                    and health[0] == \
                                    port_info[0] + port_info[1]:
                                health_status = \
                                    constants.PortHealthStatus.NORMAL if \
                                    health[1] == 'Normal' else \
                                    constants.PortHealthStatus.ABNORMAL
                    if len(speeds_array) > 2:
                        for speeds in speeds_array[2:]:
                            speed_info = speeds.split()
                            if len(speed_info) > 1 and \
                                    speed_info[0] + speed_info[1] == \
                                    port_info[0] + port_info[1]:
                                break
                    if len(status_array) > 2:
                        for status in status_array[2:]:
                            status_info = status.split()
                            if len(status_info) > 1 and \
                                    status_info[0] + status_info[1] == \
                                    port_info[0] + port_info[1]:
                                break
                    port_model = {
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
                        'logical_type': '',
                        'speed': speed_info[3],
                        'max_speed': speed_info[3],
                        'native_parent_id': '',
                        'wwn': wwn_map.get(port_info[0] + port_info[1]),
                        'mac_address': '',
                        'ipv4': '',
                        'ipv4_mask': '',
                        'ipv6': '',
                        'ipv6_mask': ''
                    }
                    fc_list.append(port_model)
            return fc_list

    def get_iscsi_port(self, storage_id):
        port_list = []
        ports_info = cli_handler(
            constant.ISCSI_PORT_INFO_COMMAND %
            {'unit_name': self.storage_name})
        ports_array = ports_info.split("Delayed Ack")
        port_map = {}
        for port_info in ports_array:
            port_info_array = port_info.split("\r\n")
            if len(port_info_array) > 9:
                if port_info_array[0].split()[0] == ':':
                    name = port_info_array[2].split()[1]
                else:
                    name = port_info_array[0].split()[1]
                self.get_detail(port_info, port_map, ":")
                port_map['IPAddress'] = ''
                if port_map.get('IPv6Status') == 'Enable':
                    port_str = port_info.split('Global IP Address')
                    if len(port_str) > 0:
                        port_info_array = port_str[0].split("\r\n")
                        for detail in port_info_array:
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
                port_model = {
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
                port_list.append(port_model)
        return port_list

    def list_ports(self, storage_id):
        try:
            port_list = self.get_iscsi_port(storage_id)
            port_list += self.get_fc_ports(storage_id)
            return port_list
        except exception.DelfinException as e:
            err_msg = "Failed to get storage ports from " \
                      "hus_110, : %s" % (six.text_type(e))
            LOG.error(err_msg)
            raise e

        except Exception as err:
            err_msg = "Failed to get storage ports from " \
                      "hus_110, : %s" % (six.text_type(err))
            LOG.error(err_msg)
            raise exception.InvalidResults(err_msg)

    def list_disks(self, storage_id):
        try:
            disks_list = []
            disk_info = cli_handler(
                constant.DISK_INFO_COMMAND %
                {'unit_name': self.storage_name})
            disk_array = disk_info.split("\r\n")
            if len(disk_array) > 1:
                for disk in disk_array[1:]:
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
                                int(Tools.get_capacity_size(disk[2])),
                            'status': '',
                            'physical_type': disk[3],
                            'logical_type': '',
                            'health_score': '',
                            'native_disk_group_id': '',
                            'location': '',
                        }
                        disks_list.append(d)
                return disks_list
        except exception.DelfinException as e:
            err_msg = "Failed to get storage disks from " \
                      "hus_110, : %s" % (six.text_type(e))
            LOG.error(err_msg)
            raise e
        except Exception as err:
            err_msg = "Failed to get storage disks from " \
                      "hus_110, : %s" % (six.text_type(err))
            LOG.error(err_msg)
            raise exception.InvalidResults(err_msg)
