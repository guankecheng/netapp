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
import paramiko
import six
from oslo_log import log as logging
from oslo_utils import units

from delfin.drivers.netapp.netapp_fas import netapp_constants

from delfin.drivers.netapp.netapp_fas.alert_handler import AlertHandler
from delfin import exception, utils
from delfin.common import constants, alert_util
from delfin.drivers.utils.ssh_client import SSHPool

LOG = logging.getLogger(__name__)


class NetAppHandler(object):
    # TODO
    OID_SERIAL_NUM = '1.3.6.1.4.1.789.1.1.9.0'
    OID_TRAP_DATA = '1.3.6.1.4.1.789.1.1.12.0'

    SECONDS_TO_MS = 1000

    def __init__(self, **kwargs):
        self.ssh_pool = SSHPool(**kwargs)

    @staticmethod
    def parse_alert(alert):
        # TODO
        pass

    def login(self):
        try:
            with self.ssh_pool.item() as ssh:
                NetAppHandler.do_exec('lssystem', ssh)
        except Exception as e:
            LOG.error("Failed to login netapp_fas %s" %
                      (six.text_type(e)))
            raise e

    @staticmethod
    def do_exec(command_str, ssh):
        """Execute command"""
        global result
        try:
            utils.check_ssh_injection(command_str)
            if command_str is not None and ssh is not None:
                stdin, stdout, stderr = ssh.exec_command(command_str)
                res, err = stdout.read(), stderr.read()
                re = res if res else err
                result = re.decode()
        except paramiko.AuthenticationException as ae:
            LOG.error('doexec Authentication error:{}'.format(ae))
            raise exception.InvalidUsernameOrPassword()
        except Exception as e:
            err = six.text_type(e)
            LOG.error('doexec InvalidUsernameOrPassword error')
            if 'timed out' in err:
                raise exception.SSHConnectTimeout()
            elif 'No authentication methods available' in err \
                    or 'Authentication failed' in err:
                raise exception.InvalidUsernameOrPassword()
            elif 'not a valid RSA private key file' in err:
                raise exception.InvalidPrivateKey()
            else:
                raise exception.SSHException(err)
        return result

    def exec_ssh_command(self, command):
        try:
            with self.ssh_pool.item() as ssh:
                ssh_info = NetAppHandler.do_exec(command, ssh)
            return ssh_info
        except Exception as e:
            msg = "Failed to ssh netapp_fas %s: %s" % \
                  (command, six.text_type(e))
            raise exception.SSHException(msg)

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

    def get_storage(self):
        try:
            raw_capacity = total_capacity = used_capacity = free_capacity = 0
            system_info = self.exec_ssh_command(netapp_constants.CLUSTER_SHOW_COMMAND)
            enclosure_info = self.exec_ssh_command(netapp_constants.AGGREGATE_SHOW_COMMAND)
            version = self.exec_ssh_command(netapp_constants.VERSION_SHOW_COMMAND)
            disk_info = self.exec_ssh_command(netapp_constants.DISK_SHOW_COMMAND)
            version_arr = version.split(":")
            storage_map = {}
            enclosure_arr = enclosure_info.split("\r\n")
            """Calculate storage size"""
            if len(enclosure_arr) > 3:
                for detail in enclosure_arr[3:]:
                    detail_arr = detail.split()
                    if len(detail_arr) == 8 and '---' not in detail_arr[0]:
                        if detail_arr[1] != '-':
                            total_capacity += int(self.parse_string(detail_arr[1]))
                            if detail_arr[2] != '-':
                                free_capacity += int(self.parse_string(detail_arr[2]))
                            if detail_arr[3] != '-':
                                used_capacity += int(self.parse_string(detail_arr[1])) \
                                                 * float(detail_arr[3].strip('%')) / 100.0
            self.handle_detail(system_info, storage_map, split=':')
            disk_arr = disk_info.split("\r\n")
            if len(disk_arr) > 3:
                for disk_detail in enclosure_arr[3:]:
                    detail_arr = disk_detail.split()
                    if len(detail_arr) == 8 and '---' not in detail_arr[0]:
                        if detail_arr[1] != '-':
                            raw_capacity += int(self.parse_string(detail_arr[1]))
            status = "normal" if storage_map.get("Health") is True else "offline"
            s = {
                "name": storage_map.get('ClusterName'),
                "vendor": 'NetApp',
                "model": 'Cluster Model',
                "status": status,
                "serial_number": storage_map.get("ClusterSerialNumber"),
                "firmware_version": version_arr[0],
                "location": storage_map.get('ClusterLocation'),
                "total_capacity": total_capacity,
                "raw_capacity": raw_capacity,
                "used_capacity": used_capacity,
                "free_capacity": free_capacity
            }
            return s
        except exception.DelfinException as e:
            err_msg = "Failed to get storage from netapp_fas fas: %s" % (six.text_type(e.msg))
            LOG.error(err_msg)
            raise e
        except Exception as err:
            err_msg = "Failed to get storage from netapp_fas fas: %s" % (six.text_type(err))
            LOG.error(err_msg)
            raise exception.InvalidResults(err_msg)

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

    def list_storage_pools(self, storage_id):
        try:
            pool_list = []
            pool_info = self.exec_ssh_command(netapp_constants.POOLS_SHOW_DETAIL_COMMAND)
            pool_arr = pool_info.split(netapp_constants.POOLS_SPLIT_STR)
            agg_info = self.exec_ssh_command(netapp_constants.AGGREGATE_SHOW__DETAIL_COMMAND)
            agg_arr = agg_info.split(netapp_constants.AGGREGATE_SPLIT_STR)
            pool_map = {}
            for pool_str in pool_arr[1:]:
                self.handle_detail(pool_str, pool_map, split=':')
                p = {
                    'name': pool_map.get('ame'),
                    'storage_id': storage_id,
                    'native_storage_pool_id': pool_map.get('UUIDofStoragePool'),
                    'description': '',
                    'status': pool_map.get('StateoftheStoragePool'),
                    'storage_type': constants.StorageType.BLOCK,
                    # TODO
                    'subscribed_capacity': '',
                    'total_capacity': int(self.parse_string(pool_map.get('StoragePoolTotalSize'))),
                    'used_capacity': int(self.parse_string(pool_map.get('StoragePoolTotalSize'))) -
                                     int(self.parse_string(pool_map.get('StoragePoolUsableSize'))),
                    'free_capacity': int(self.parse_string(pool_map.get('StoragePoolUsableSize')))
                }
                pool_list.append(p)
            for agg in agg_arr[1:]:
                self.handle_detail(agg, pool_map, split=':')
                p = {
                    'name': pool_map.get('e'),
                    'storage_id': storage_id,
                    'native_storage_pool_id': pool_map.get('UUIDString'),
                    'description': '',
                    'status': 'normal' if pool_map.get('online') == 'online' else 'offline',
                    'storage_type': pool_map.get("ChecksumStyle"),
                    'subscribed_capacity': '',
                    'total_capacity': int(self.parse_string(pool_map.get('Size'))),
                    'used_capacity': int(self.parse_string(pool_map.get('UsedSize'))),
                    'free_capacity': int(self.parse_string(pool_map.get('AvailableSize'))),
                }
                pool_list.append(p)
            return pool_list
        except exception.DelfinException as e:
            err_msg = "Failed to get storage pool from netapp_fas fas: %s" % (six.text_type(e))
            LOG.error(err_msg)
            raise e
        except Exception as err:
            err_msg = "Failed to get storage pool from netapp_fas fas: %s" % (six.text_type(err))
            LOG.error(err_msg)
            raise exception.InvalidResults(err_msg)

    def list_volumes(self, storage_id):
        try:
            volume_list = []
            volume_info = self.exec_ssh_command(netapp_constants.VOLUME_SHOW_DETAIL_COMMAND)
            volume_arr = volume_info.split(netapp_constants.VOLUME_SPLIT_STR)
            pool_list = self.list_storage_pools(storage_id)

            volume_map = {}
            for volume_str in volume_arr[1:]:
                self.handle_detail(volume_str, volume_map, split=':')
                pool_id = ""

                """get pool id"""
                for pool in pool_list:
                    if pool['name'] == volume_map.get("AggregateName"):
                        pool_id = pool['native_storage_pool_id']

                deduplicated = False if volume_map.get('SpaceSavedbyDeduplication') == '0B' else True
                v = {
                    'name': volume_map.get('VolumeName'),
                    'storage_id': storage_id,
                    'description': '',
                    'status': 'normal' if volume_map.get('VolumeState') == 'online' else 'offline',
                    'native_volume_id': volume_map.get('VolumeDataSetID'),
                    'native_storage_pool_id': pool_id,
                    'wwn': '',
                    'compressed': volume_map.get('VolumeContainsSharedorCompressedData'),
                    'deduplicated': deduplicated,
                    'type': constants.VolumeType.THIN,
                    'total_capacity': int(self.parse_string(volume_map.get('VolumeSize'))),
                    'used_capacity': int(self.parse_string(volume_map.get('UsedSize'))),
                    'free_capacity': int(self.parse_string(volume_map.get('VolumeSize'))) -
                                     int(self.parse_string(volume_map.get('UsedSize')))
                }
                volume_list.append(v)
            return volume_list
        except exception.DelfinException as e:
            err_msg = "Failed to get storage volume from netapp_fas fas: %s" % (six.text_type(e))
            LOG.error(err_msg)
            raise e
        except Exception as err:
            err_msg = "Failed to get storage volume from netapp_fas fas: %s" % (six.text_type(err))
            LOG.error(err_msg)
            raise exception.InvalidResults(err_msg)

    def list_alerts(self, query_para):
        try:
            alert_list = []
            alert_info = self.exec_ssh_command(netapp_constants.ALTER_SHOW_DETAIL_COMMAND)
            event_info = self.exec_ssh_command(netapp_constants.EVENT_SHOW_DETAIL_COMMAND)
            """Query the two alarms separately"""
            AlertHandler.list_events(self, event_info, query_para, alert_list)
            AlertHandler.list_alerts(self, alert_info, query_para, alert_list)
            return alert_list
        except exception.DelfinException as e:
            err_msg = "Failed to get storage alert: %s" % (six.text_type(e))
            LOG.error(err_msg)
            raise e
        except Exception as err:
            err_msg = "Failed to get storage alert: %s" % (six.text_type(err))
            LOG.error(err_msg)
            raise exception.InvalidResults(err_msg)

    def clear_alert(self, alert):
        try:
            ssh_command = netapp_constants.CLEAR_ALERT_COMMAND + alert.get('alert_id')
            self.exec_ssh_command(ssh_command)
        except exception.DelfinException as e:
            err_msg = "Failed to get storage alert from netapp_fas fas: %s" % (six.text_type(e))
            LOG.error(err_msg)
            raise e
        except Exception as err:
            err_msg = "Failed to get storage alert from netapp_fas fas: %s" % (six.text_type(err))
            LOG.error(err_msg)
            raise exception.InvalidResults(err_msg)

    def list_controllers(self, storage_id):
        try:
            controller_list = []
            controller_info = self.exec_ssh_command(netapp_constants.CONTROLLER_SHOW_DETAIL_COMMAND)
            controller_arr = controller_info.split(netapp_constants.CONTROLLER_SPLIT_STR)
            controller_map = {}
            for controller_str in controller_arr[1:]:
                self.handle_detail(controller_str, controller_map, split=':')
                status = 'normal' if controller_map['Status'] == 'ok' else 'offline'
                c = {
                    'name': controller_map['e'],
                    'storage_id': storage_id,
                    'native_controller_id': controller_map['SystemID'],
                    'status': status,
                    'location': '-',
                    'soft_version': controller_map['Revision'],
                    'cpu_info': '-',
                    'memory_size': '-',
                }
                controller_list.append(c)
            return controller_list

        except exception.DelfinException as e:
            err_msg = "Failed to get storage controllers from netapp_fas fas: %s" % (six.text_type(e))
            LOG.error(err_msg)
            raise e

        except Exception as err:
            err_msg = "Failed to get storage controllers from netapp_fas fas: %s" % (six.text_type(err))
            LOG.error(err_msg)
            raise exception.InvalidResults(err_msg)

    def list_ports(self, storage_id):
        try:
            ports_list = []
            ports_info = self.exec_ssh_command(netapp_constants.PORT_SHOW_DETAIL_COMMAND)
            interfaces_info = self.exec_ssh_command(netapp_constants.INTERFACE_SHOW_DETAIL_COMMAND)
            ports_arr = ports_info.split(netapp_constants.PORT_SPLIT_STR)
            interface_arr = interfaces_info.split(netapp_constants.INTERFACE_SPLIT_STR)
            ports_map = {}
            interface_map = {}
            for port_info in ports_arr[1:]:
                ipv4 = ipv4_mask = ipv6 = ipv6_mask = '-'
                self.handle_detail(port_info, ports_map, split=':')

                """Traversal to get port IP address information"""
                for interface_info in interface_arr:
                    self.handle_detail(interface_info, interface_map, split=':')
                    if interface_map.get('CurrentPort') == ports_map.get('Port') and interface_map.get(
                            'IsHome') is True:
                        if interface_map.get('Addressfamily') == 'ipv4':
                            ipv4 = interface_map.get('NetworkAddress')
                            ipv4_mask = interface_map.get('Netmask')
                        else:
                            ipv6 = interface_map.get('NetworkAddress')
                            ipv6_mask = interface_map.get('Netmask')
                c = {
                    'name': ports_map['Port'],
                    'storage_id': storage_id,
                    'native_port_id': '',
                    'location': '',
                    'connection_status': ports_map['Link'],
                    'health_status': ports_map['PortHealthStatus'],
                    'type': ports_map['PortType'],
                    'logical_type': '-',
                    'speed': ports_map['SpeedOperational'],
                    'max_speed': ports_map['MTU'],
                    'native_parent_id': '-',
                    'wwn': '-',
                    'mac_address': ports_map['MACAddress'],
                    'ipv4': ipv4,
                    'ipv4_mask': ipv4_mask,
                    'ipv6': ipv6,
                    'ipv6_mask': ipv6_mask,
                }
                ports_list.append(c)
            return ports_list
        except exception.DelfinException as e:
            err_msg = "Failed to get storage ports from netapp_fas fas: %s" % (six.text_type(e))
            LOG.error(err_msg)
            raise e

        except Exception as err:
            err_msg = "Failed to get storage ports from netapp_fas fas: %s" % (six.text_type(err))
            LOG.error(err_msg)
            raise exception.InvalidResults(err_msg)

    def list_disks(self, storage_id):
        try:
            disks_list = []
            physicals_list = []
            disks_info = self.exec_ssh_command(netapp_constants.DISK_SHOW_DETAIL_COMMAND)
            disks_arr = disks_info.split(netapp_constants.DISK_SPLIT_STR)
            physicals_info = self.exec_ssh_command(netapp_constants.DISK_SHOW_PHYSICAL_COMMAND)
            disks_map = {}
            physical_arr = physicals_info.split('\r\n')
            speed = physical_type = firmware = '-'
            for i in range(2, len(physical_arr), 2):
                physicals_list.append(physical_arr[i].split())
            for disk_str in disks_arr[1:]:
                self.handle_detail(disk_str, disks_map, split=':')

                """Map disk physical information"""
                for physical_info in physicals_list:
                    if len(physical_info) > 6:
                        if physical_info[0] == disks_map.get('Disk'):
                            physical_type = physical_info[1]
                            speed = physical_info[5]
                            firmware = physical_info[4]
                status = 'normal' if disks_map.get('Errors') is None or disks_map.get('Errors') == "" else 'offline'
                d = {
                    'name': disks_map.get('k'),
                    'storage_id': storage_id,
                    'native_disk_id': disks_map.get('UID'),
                    'serial_number': disks_map.get('SerialNumber'),
                    'manufacturer': disks_map.get('Vendor'),
                    'model': disks_map.get('Model'),
                    'firmware': firmware,
                    'speed': speed,
                    'capacity': int(self.parse_string(disks_map.get('PhysicalSize'))),
                    'status': status,
                    'physical_type': physical_type,
                    'logical_type': disks_map.get('ContainerType'),
                    'health_score': '-',
                    'native_disk_group_id': None,
                    'location': '-',
                }
                disks_list.append(d)
            return disks_list
        except exception.DelfinException as e:
            err_msg = "Failed to get storage disks from netapp_fas fas: %s" % (six.text_type(e))
            LOG.error(err_msg)
            raise e

        except Exception as err:
            err_msg = "Failed to get storage disks from netapp_fas fas: %s" % (six.text_type(err))
            LOG.error(err_msg)
            raise exception.InvalidResults(err_msg)

    def list_qtrees(self, storage_id):
        try:
            qt_list = []
            qt_info = self.exec_ssh_command(netapp_constants.QTREE_SHOW_DETAIL_COMMAND)
            qt_arr = qt_info.split(netapp_constants.QTREE_SPLIT_STR)
            qt_map = {}
            for qt in qt_arr[1:]:
                self.handle_detail(qt, qt_map, split=':')
                q = {
                    'name': qt_map.get("QtreeName"),
                    'storage_id': storage_id,
                    'native_qtree_id': qt_map.get("QtreeId"),
                    'native_filesystem_id': '-',
                    'security_mode': qt_map.get("SecurityStyle"),
                }
                qt_list.append(q)

            return qt_list
        except exception.DelfinException as err:
            err_msg = "Failed to get storage qtrees from netapp_fas fas: %s" % \
                      (six.text_type(err))
            LOG.error(err_msg)
            raise err

        except Exception as err:
            err_msg = "Failed to get storage qtrees from netapp_fas fas: %s" % \
                      (six.text_type(err))
            LOG.error(err_msg)
            raise exception.InvalidResults(err_msg)

    def list_shares(self, storage_id):
        try:
            shares_list = []
            cifs_share_info = self.exec_ssh_command(netapp_constants.CIFS_SHARE_SHOW_DETAIL_COMMAND)
            cifs_share_arr = cifs_share_info.split(netapp_constants.CIFS_SHARE_SPLIT_STR)
            cifs_share_map = {}
            nfs_share_info = self.exec_ssh_command(netapp_constants.NFS_SHARE_SHOW_COMMAND)
            nfs_share_arr = nfs_share_info.split("\r\n")
            for nfs_share in nfs_share_arr[3:]:
                share_arr = nfs_share.split()
                if share_arr[3] is True:
                    s = {
                        'name': share_arr[0],
                        'storage_id': storage_id,
                        'native_share_id': '-',
                        'native_filesystem_id': '-',
                        'path': share_arr[4],
                        'protocol': constants.ShareProtocol.NFS
                    }
                    shares_list.append(s)
            for cifs_share in cifs_share_arr[1:]:
                self.handle_detail(cifs_share, cifs_share_map, split=':')
                s = {
                    'name': cifs_share_map.get("Share"),
                    'storage_id': storage_id,
                    'native_share_id': '-',
                    'native_filesystem_id': '-',
                    'path': cifs_share_map.get("Path"),
                    'protocol': constants.ShareProtocol.CIFS
                }
                shares_list.append(s)
            return shares_list
        except exception.DelfinException as err:
            err_msg = "Failed to get storage shares from netapp_fas fas: %s" % \
                      (six.text_type(err))
            LOG.error(err_msg)
            raise err

        except Exception as err:
            err_msg = "Failed to get storage shares from netapp_fas fas: %s" % \
                      (six.text_type(err))
            LOG.error(err_msg)
            raise exception.InvalidResults(err_msg)

    def list_filesystems(self, storage_id):
        try:
            fs_list = []
            fs_info = self.exec_ssh_command(netapp_constants.FS_SHOW_COMMAND)
            vserver_info = self.exec_ssh_command(netapp_constants.VSERVER_SHOW_COMMAND)
            deduplicated_info = self.exec_ssh_command(netapp_constants.FS_DEDUPLICATED_SHOW_COMMAND)
            deduplicated_arr = deduplicated_info.split("\r\n")
            deduplicated_map = {}
            compressed_map = {}
            for deduplicated in deduplicated_arr[1:]:
                d_arr = deduplicated.spilt()
                if len(d_arr) > 8:
                    deduplicated_map[d_arr[0]] = True if int(d_arr[4]) > 0 else False
                    compressed_map[d_arr[0]] = True if int(d_arr[6]) > 0 else False

            pool_list = self.list_storage_pools(storage_id)
            vserver_arr = vserver_info.split("\r\n")
            vserver_map = {}
            if len(vserver_arr) > 3:
                for vserver in vserver_arr[3:]:
                    v_arr = vserver.split()
                    if len(v_arr) > 5:
                        if v_arr[6] == '-':
                            vserver_map[v_arr[0]] = '-'
                        else:
                            for pool in pool_list:
                                if pool['name'] == v_arr[6]:
                                    vserver_map[v_arr[0]] = pool['native_storage_pool_id']
            fs_arr = fs_info.split("\r\n")
            if len(fs_arr) > 1:
                for fs in fs_arr[1:]:
                    f_info = fs.split()
                    if len(f_info) > 6:
                        f = {
                            'name': f_info[0],
                            'storage_id': storage_id,
                            'native_filesystem_id': '-',
                            'native_pool_id': vserver_map[f_info[6]],
                            'compressed': compressed_map[f_info[0]],
                            'deduplicated': deduplicated_map[f_info[0]],
                            'worm': '-',
                            'status': '-',
                            'type': '-',
                            'total_capacity': int(self.parse_string(f_info[1] + 'KB')),
                            'used_capacity': int(self.parse_string(f_info[2] + 'KB')),
                            'free_capacity': int(self.parse_string(f_info[3] + 'KB')),
                        }
                        fs_list.append(f)
            return fs_list
        except exception.DelfinException as err:
            err_msg = "Failed to get storage filesystems from netapp_fas fas: %s" % \
                      (six.text_type(err))
            LOG.error(err_msg)
            raise err

        except Exception as err:
            err_msg = "Failed to get storage filesystems from netapp_fas fas: %s" % \
                      (six.text_type(err))
            LOG.error(err_msg)
            raise exception.InvalidResults(err_msg)

    def add_trap_config(self, context, trap_config):
        pass

    def remove_trap_config(self, context, trap_config):
        pass
