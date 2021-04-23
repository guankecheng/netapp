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

import paramiko
import six
from oslo_log import log as logging
from oslo_utils import units

from delfin.drivers.netapp.netapp_fas import netapp_constants

from delfin.drivers.netapp.netapp_fas.alert_handler import AlertHandler
from delfin import exception, utils
from delfin.common import constants
from delfin.drivers.utils.ssh_client import SSHPool

LOG = logging.getLogger(__name__)


class NetAppHandler(object):
    DISK_LOGICAL_TYPE = {
        'aggregate': constants.DiskLogicalType.MEMBER,
        'spare': constants.DiskLogicalType.HOTSPARE,
        'pool': constants.DiskLogicalType.MEMBER,
        'free': constants.DiskLogicalType.FREE,
    }

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
            res = units.Ti
        elif unit == 'GB':
            res = units.Gi
        elif unit == 'MB':
            res = units.Mi
        elif unit == 'KB':
            res = units.Ki
        else:
            res = 1
        return int(res)

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
            system_info = self.exec_ssh_command(
                netapp_constants.CLUSTER_SHOW_COMMAND)
            version = self.exec_ssh_command(
                netapp_constants.VERSION_SHOW_COMMAND)
            disk_list = self.list_disks(None)
            pool_list = self.list_storage_pools(None)
            version_arr = version.split(":")
            storage_map = {}
            self.handle_detail(system_info, storage_map, split=':')
            for disk in disk_list:
                raw_capacity += disk['capacity']

            for pool in pool_list:
                total_capacity += pool['total_capacity']
                free_capacity += pool['free_capacity']
                used_capacity += pool['used_capacity']

            status = constants.StorageStatus.NORMAL
            s = {
                "name": storage_map['ClusterName'],
                "vendor": 'NetApp',
                "model": 'Cluster Model',
                "status": status,
                "serial_number": storage_map['ClusterSerialNumber'],
                "firmware_version": version_arr[0],
                "location": '',
                "total_capacity": total_capacity,
                "raw_capacity": raw_capacity,
                "used_capacity": used_capacity,
                "free_capacity": free_capacity
            }
            return s
        except exception.DelfinException as e:
            err_msg = "Failed to get storage from " \
                      "netapp_fas fas: %s" % (six.text_type(e.msg))
            LOG.error(err_msg)
            raise e
        except Exception as err:
            err_msg = "Failed to get storage from " \
                      "netapp_fas fas: %s" % (six.text_type(err))
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

    def get_aggregate(self, storage_id):
        agg_list = []
        agg_info = self.exec_ssh_command(
            netapp_constants.AGGREGATE_SHOW_DETAIL_COMMAND)
        agg_arr = agg_info.split(
            netapp_constants.AGGREGATE_SPLIT_STR)
        agg_map = {}
        for agg in agg_arr[1:]:
            self.handle_detail(agg, agg_map, split=':')
            p = {
                'name': agg_map['e'],
                'storage_id': storage_id,
                'native_storage_pool_id': agg_map['UUIDString'],
                'description': '',
                'status':
                    constants.StoragePoolStatus.NORMAL
                    if agg_map['State'] == 'online'
                    else constants.StoragePoolStatus.OFFLINE,
                'storage_type': agg_map['ChecksumStyle'],
                'subscribed_capacity': '',
                'total_capacity':
                    int(self.parse_string(agg_map['Size'])),
                'used_capacity':
                    int(self.parse_string(agg_map['UsedSize'])),
                'free_capacity':
                    int(self.parse_string(agg_map['AvailableSize'])),
            }
            agg_list.append(p)
        return agg_list

    def get_pool(self, storage_id):
        pool_list = []
        pool_info = self.exec_ssh_command(
            netapp_constants.POOLS_SHOW_DETAIL_COMMAND)
        pool_arr = pool_info.split(netapp_constants.POOLS_SPLIT_STR)
        pool_map = {}
        for pool_str in pool_arr[1:]:
            self.handle_detail(pool_str, pool_map, split=':')
            p = {
                'name': pool_map['ame'],
                'storage_id': storage_id,
                'native_storage_pool_id': pool_map['UUIDofStoragePool'],
                'description': '',
                'status':
                    constants.StoragePoolStatus.NORMAL
                    if pool_map['IsPoolHealthy?'] == 'true'
                    else constants.StoragePoolStatus.OFFLINE,
                'storage_type': constants.StorageType.BLOCK,
                # TODO
                'subscribed_capacity': '',
                'total_capacity':
                    int(self.parse_string(pool_map['StoragePoolTotalSize'])),
                'used_capacity':
                    int(self.parse_string(pool_map['StoragePoolTotalSize'])) -
                    int(self.parse_string(pool_map['StoragePoolUsableSize'])),
                'free_capacity':
                    int(self.parse_string(pool_map['StoragePoolUsableSize']))
            }
            pool_list.append(p)
        return pool_list

    def list_storage_pools(self, storage_id):
        try:
            pool_list = self.get_pool(storage_id)
            agg_list = self.get_aggregate(storage_id)
            return agg_list + pool_list
        except exception.DelfinException as e:
            err_msg = "Failed to get storage pool from " \
                      "netapp_fas fas: %s" % (six.text_type(e))
            LOG.error(err_msg)
            raise e
        except Exception as err:
            err_msg = "Failed to get storage pool from " \
                      "netapp_fas fas: %s" % (six.text_type(err))
            LOG.error(err_msg)
            raise exception.InvalidResults(err_msg)

    def list_volumes(self, storage_id):
        try:
            volume_list = []
            volume_info = self.exec_ssh_command(
                netapp_constants.VOLUME_SHOW_DETAIL_COMMAND)
            volume_arr = volume_info.split(
                netapp_constants.VOLUME_SPLIT_STR)
            thin_vol_info = self.exec_ssh_command(
                netapp_constants.THIN_VOLUME_SHOW_COMMAND)
            pool_list = self.list_storage_pools(storage_id)
            thin_vol_arr = thin_vol_info.split("\r\n")
            type = constants.VolumeType.THICK
            volume_map = {}
            for volume_str in volume_arr[1:]:
                self.handle_detail(volume_str, volume_map, split=':')
                if volume_map is not None or volume_map != {}:
                    pool_id = ""
                    """get pool id"""
                    for pool in pool_list:
                        if pool['name'] == volume_map['AggregateName']:
                            pool_id = pool['native_storage_pool_id']
                    deduplicated = False \
                        if volume_map['SpaceSavedbyDeduplication'] == '0B' \
                        else True
                    if len(thin_vol_arr) > 2:
                        for thin_vol in thin_vol_arr[2:]:
                            thin_arr = thin_vol.split()
                            if len(thin_arr) > 4:
                                if thin_arr[1] == volume_map['VolumeName']:
                                    type = constants.VolumeType.THIN
                    v = {
                        'name': volume_map['VolumeName'],
                        'storage_id': storage_id,
                        'description': '',
                        'status':
                            constants.VolumeStatus.AVAILABLE
                            if volume_map['VolumeState'] == 'online'
                            else constants.VolumeStatus.ERROR,
                        'native_volume_id': volume_map['VolumeDataSetID'],
                        'native_storage_pool_id': pool_id,
                        'wwn': '',
                        'compressed':
                            False if
                            volume_map['VolumeContainsSharedorCompressedData']
                            == 'false'
                            else True,
                        'deduplicated': deduplicated,
                        'type': type,
                        'total_capacity':
                            int(self.parse_string(volume_map['VolumeSize'])),
                        'used_capacity':
                            int(self.parse_string(volume_map['UsedSize'])),
                        'free_capacity':
                            int(self.parse_string(volume_map['VolumeSize'])) -
                            int(self.parse_string(volume_map['UsedSize']))
                    }
                    volume_list.append(v)
            return volume_list
        except exception.DelfinException as e:
            err_msg = "Failed to get storage volume from " \
                      "netapp_fas fas: %s" % (six.text_type(e))
            LOG.error(err_msg)
            raise e
        except Exception as err:
            err_msg = "Failed to get storage volume from " \
                      "netapp_fas fas: %s" % (six.text_type(err))
            LOG.error(err_msg)
            raise exception.InvalidResults(err_msg)

    def list_alerts(self, query_para):
        try:
            alert_list = []
            alert_info = self.exec_ssh_command(
                netapp_constants.ALTER_SHOW_DETAIL_COMMAND)
            event_info = self.exec_ssh_command(
                netapp_constants.EVENT_SHOW_DETAIL_COMMAND)
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
            ssh_command = \
                netapp_constants.CLEAR_ALERT_COMMAND + alert['alert_id']
            self.exec_ssh_command(ssh_command)
        except exception.DelfinException as e:
            err_msg = "Failed to get storage alert from " \
                      "netapp_fas fas: %s" % (six.text_type(e))
            LOG.error(err_msg)
            raise e
        except Exception as err:
            err_msg = "Failed to get storage alert from " \
                      "netapp_fas fas: %s" % (six.text_type(err))
            LOG.error(err_msg)
            raise exception.InvalidResults(err_msg)

    def list_controllers(self, storage_id):
        try:
            controller_list = []
            controller_info = self.exec_ssh_command(
                netapp_constants.CONTROLLER_SHOW_DETAIL_COMMAND)
            controller_arr = controller_info.split(
                netapp_constants.CONTROLLER_SPLIT_STR)
            controller_map = {}
            for controller_str in controller_arr[1:]:
                self.handle_detail(controller_str, controller_map, split=':')
                status = constants.ControllerStatus.NORMAL \
                    if controller_map['Status'] == 'ok' \
                    else constants.ControllerStatus.OFFLINE
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
            err_msg = "Failed to get storage controllers from " \
                      "netapp_fas fas: %s" % (six.text_type(e))
            LOG.error(err_msg)
            raise e

        except Exception as err:
            err_msg = "Failed to get storage controllers from " \
                      "netapp_fas fas: %s" % (six.text_type(err))
            LOG.error(err_msg)
            raise exception.InvalidResults(err_msg)

    def get_network_port(self, storage_id):
        try:
            ports_list = []
            ports_info = self.exec_ssh_command(
                netapp_constants.PORT_SHOW_DETAIL_COMMAND)
            interfaces_info = self.exec_ssh_command(
                netapp_constants.INTERFACE_SHOW_DETAIL_COMMAND)
            ports_arr = ports_info.split(
                netapp_constants.PORT_SPLIT_STR)
            interface_arr = interfaces_info.split(
                netapp_constants.INTERFACE_SPLIT_STR)
            ports_map = {}
            interface_map = {}

            for port_info in ports_arr[1:]:
                ipv4 = ipv4_mask = ipv6 = ipv6_mask = '-'
                self.handle_detail(port_info, ports_map, split=':')

                """Traversal to get port IP address information"""
                for interface_info in interface_arr[1:]:
                    self.handle_detail(interface_info,
                                       interface_map,
                                       split=':')
                    if interface_map['Addressfamily'] == 'ipv4':
                        ipv4 += interface_map['NetworkAddress'] + ','
                        ipv4_mask += interface_map['Netmask'] + ','
                    else:
                        ipv6 += interface_map['NetworkAddress'] + ','
                        ipv6_mask += interface_map['Netmask'] + ','
                p = {
                    'name': ports_map['Port'],
                    'storage_id': storage_id,
                    'native_port_id': ports_map['Port'],
                    'location': '',
                    'connection_status':
                        constants.PortConnectionStatus.CONNECTED
                        if ports_map['Link'] == 'up'
                        else constants.PortConnectionStatus.DISCONNECTED,
                    'health_status':
                        constants.PortHealthStatus.NORMAL
                        if ports_map['PortHealthStatus'] == 'healthy'
                        else constants.PortHealthStatus.ABNORMAL,
                    'type': constants.PortType.ETH,
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
                ports_list.append(p)
            return ports_list
        except exception.DelfinException as e:
            err_msg = "Failed to get storage ports from " \
                      "netapp_fas fas: %s" % (six.text_type(e))
            LOG.error(err_msg)
            raise e

        except Exception as err:
            err_msg = "Failed to get storage ports from " \
                      "netapp_fas fas: %s" % (six.text_type(err))
            LOG.error(err_msg)
            raise exception.InvalidResults(err_msg)

    def get_fc_port(self, storage_id):
        try:
            fc_list = []
            fc_info = self.exec_ssh_command(
                netapp_constants.FC_PORT_SHOW_DETAIL_COMMAND)
            fc_arr = fc_info.split(
                netapp_constants.PORT_SPLIT_STR)
            for fc in fc_arr[1:]:
                fc_map = {}
                self.handle_detail(fc, fc_map, split=':')
                f = {
                    'name': fc_map['Adapter'],
                    'storage_id': storage_id,
                    'native_port_id': fc_map['Adapter'],
                    'location': '',
                    'connection_status':
                        constants.PortConnectionStatus.CONNECTED
                        if fc_map['AdministrativeStatus'] == 'up'
                        else constants.PortConnectionStatus.DISCONNECTED,
                    'health_status':
                        constants.PortHealthStatus.NORMAL
                        if fc_map['OperationalStatus'] == 'online'
                        else constants.PortHealthStatus.ABNORMAL,
                    'type': constants.PortType.FC,
                    'logical_type': '-',
                    'speed': fc_map['DataLinkRate(Gbit)'],
                    'max_speed': fc_map['MaximumSpeed'],
                    'native_parent_id': '-',
                    'wwn': fc_map['AdapterWWNN'],
                    'mac_address': '',
                    'ipv4': '',
                    'ipv4_mask': '',
                    'ipv6': '',
                    'ipv6_mask': '',
                }
                fc_list.append(f)
            return fc_list
        except exception.DelfinException as e:
            err_msg = "Failed to get storage ports from " \
                      "netapp_fas fas: %s" % (six.text_type(e))
            LOG.error(err_msg)
            raise e

        except Exception as err:
            err_msg = "Failed to get storage ports from " \
                      "netapp_fas fas: %s" % (six.text_type(err))
            LOG.error(err_msg)
            raise exception.InvalidResults(err_msg)

    def list_ports(self, storage_id):
        ports_list = \
            self.get_network_port(storage_id) + \
            self.get_fc_port(storage_id)
        return ports_list

    def list_disks(self, storage_id):
        try:
            disks_list = []
            physicals_list = []
            disks_info = self.exec_ssh_command(
                netapp_constants.DISK_SHOW_DETAIL_COMMAND)
            disks_arr = disks_info.split(
                netapp_constants.DISK_SPLIT_STR)
            physicals_info = self.exec_ssh_command(
                netapp_constants.DISK_SHOW_PHYSICAL_COMMAND)
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
                        if physical_info[0] == disks_map['k']:
                            physical_type = physical_info[1]
                            speed = physical_info[5]
                            firmware = physical_info[4]
                status = constants.DiskStatus.NORMAL \
                    if disks_map['Errors:'] is None \
                    or disks_map['Errors:'] == "" \
                    else constants.DiskStatus.OFFLINE
                d = {
                    'name': disks_map['k'],
                    'storage_id': storage_id,
                    'native_disk_id': disks_map['k'],
                    'serial_number': disks_map['SerialNumber'],
                    'manufacturer': disks_map['Vendor'],
                    'model': disks_map['Model'],
                    'firmware': firmware,
                    'speed': speed,
                    'capacity':
                        int(self.parse_string(disks_map['PhysicalSize'])),
                    'status': status,
                    'physical_type': physical_type,
                    'logical_type':
                        self.DISK_LOGICAL_TYPE[disks_map['ContainerType']],
                    'health_score': '-',
                    'native_disk_group_id': disks_map['Aggregate'],
                    'location': '-',
                }
                disks_list.append(d)
            return disks_list
        except exception.DelfinException as e:
            err_msg = "Failed to get storage disks from " \
                      "netapp_fas fas: %s" % (six.text_type(e))
            LOG.error(err_msg)
            raise e

        except Exception as err:
            err_msg = "Failed to get storage disks from " \
                      "netapp_fas fas: %s" % (six.text_type(err))
            LOG.error(err_msg)
            raise exception.InvalidResults(err_msg)

    def list_qtrees(self, storage_id):
        try:
            qt_list = []
            qt_info = self.exec_ssh_command(
                netapp_constants.QTREE_SHOW_DETAIL_COMMAND)
            qt_arr = qt_info.split(netapp_constants.QTREE_SPLIT_STR)
            qt_map = {}
            for qt in qt_arr[1:]:
                self.handle_detail(qt, qt_map, split=':')
                q = {
                    'name': qt_map['QtreeName'],
                    'storage_id': storage_id,
                    'native_qtree_id': qt_map['QtreeId'],
                    'native_filesystem_id':
                        '/vol/' + qt_map['VolumeName'] + '/',
                    'security_mode': qt_map['SecurityStyle'],
                }
                qt_list.append(q)

            return qt_list
        except exception.DelfinException as err:
            err_msg = "Failed to get storage qtrees from " \
                      "netapp_fas fas: %s" % (six.text_type(err))
            LOG.error(err_msg)
            raise err

        except Exception as err:
            err_msg = "Failed to get storage qtrees from " \
                      "netapp_fas fas: %s" % (six.text_type(err))
            LOG.error(err_msg)
            raise exception.InvalidResults(err_msg)

    def list_shares(self, storage_id):
        try:
            shares_list = []
            cifs_share_info = self.exec_ssh_command(
                netapp_constants.CIFS_SHARE_SHOW_DETAIL_COMMAND)
            cifs_share_arr = cifs_share_info.split(
                netapp_constants.CIFS_SHARE_SPLIT_STR)
            protocol_info = self.exec_ssh_command(
                netapp_constants.SHARE_AGREEMENT_SHOW_COMMAND)
            cifs_share_map = {}
            protocol_map = {}
            protocol_arr = protocol_info.split('\r\n')
            for protocol in protocol_arr[2:]:
                agr_arr = protocol.split()
                if len(agr_arr) > 1:
                    protocol_map[agr_arr[0]] = agr_arr[1]
            for cifs_share in cifs_share_arr[1:]:
                self.handle_detail(cifs_share, cifs_share_map, split=':')
                cifs = nfs = ""
                if protocol_map.get(cifs_share_map['r']) is not None:
                    if constants.ShareProtocol.CIFS in \
                            protocol_map.get(cifs_share_map['r']):
                        cifs = constants.ShareProtocol.CIFS
                    if constants.ShareProtocol.NFS in \
                            protocol_map.get(cifs_share_map['r']):
                        nfs = constants.ShareProtocol.NFS
                s = {
                    'name': cifs_share_map['Share'],
                    'storage_id': storage_id,
                    'native_share_id': cifs_share_map['Share'],
                    'native_filesystem_id':
                        '/vol/' + cifs_share_map['VolumeName'] + '/',
                    'path': cifs_share_map['Path'],
                    'protocol': nfs + ',' + cifs
                    if nfs != "" and cifs != ""
                    else nfs + cifs
                }
                shares_list.append(s)
            return shares_list
        except exception.DelfinException as err:
            err_msg = "Failed to get storage shares from " \
                      "netapp_fas fas: %s" % (six.text_type(err))
            LOG.error(err_msg)
            raise err

        except Exception as err:
            err_msg = "Failed to get storage shares from " \
                      "netapp_fas fas: %s" % (six.text_type(err))
            LOG.error(err_msg)
            raise exception.InvalidResults(err_msg)

    def list_filesystems(self, storage_id):
        try:
            fs_list = []
            fs_info = \
                self.exec_ssh_command(netapp_constants.FS_SHOW_COMMAND)
            vserver_info = \
                self.exec_ssh_command(netapp_constants.VSERVER_SHOW_COMMAND)
            pool_list = self.list_storage_pools(storage_id)
            vol_list = self.list_volumes(storage_id)
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
                                    vserver_map[v_arr[0]] = \
                                        pool['native_storage_pool_id']
            fs_arr = fs_info.split("\r\n")
            if len(fs_arr) > 1:
                for fs in fs_arr[1:]:
                    f_info = fs.split()
                    if len(f_info) > 6:
                        status = constants.FilesystemStatus.FAULTY
                        type = constants.FSType.THICK
                        compressed = deduplicated = False
                        for vol in vol_list:
                            if '/vol/' + vol['name'] + '/' == f_info[0]:
                                status = constants.FilesystemStatus.NORMAL \
                                    if vol['status'] == constants.\
                                    VolumeStatus.AVAILABLE \
                                    else constants.FilesystemStatus.FAULTY
                                type = vol['type']
                                compressed = vol['compressed']
                                deduplicated = vol['deduplicated']
                        f = {
                            'name': f_info[0],
                            'storage_id': storage_id,
                            'native_filesystem_id': f_info[0],
                            'native_pool_id': vserver_map[f_info[6]],
                            'compressed': compressed,
                            'deduplicated': deduplicated,
                            'worm': '-',
                            'status': status,
                            'type': type,
                            'total_capacity':
                                int(self.parse_string(f_info[1] + 'KB')),
                            'used_capacity':
                                int(self.parse_string(f_info[2] + 'KB')),
                            'free_capacity':
                                int(self.parse_string(f_info[3] + 'KB')),
                        }
                        fs_list.append(f)
            return fs_list
        except exception.DelfinException as err:
            err_msg = "Failed to get storage filesystems " \
                      "from netapp_fas fas: %s" % (six.text_type(err))
            LOG.error(err_msg)
            raise err

        except Exception as err:
            err_msg = "Failed to get storage filesystems " \
                      "from netapp_fas fas: %s" % (six.text_type(err))
            LOG.error(err_msg)
            raise exception.InvalidResults(err_msg)

    def add_trap_config(self, context, trap_config):
        pass

    def remove_trap_config(self, context, trap_config):
        pass
