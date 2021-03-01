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

from delfin import exception, utils
from delfin.common import constants, alert_util
from delfin.drivers.utils.ssh_client import SSHPool

LOG = logging.getLogger(__name__)


class SSHHandler(object):
    # TODO
    OID_ERR_ID = '1.3.6.1.4.1.2.6.190.4.3'
    OID_SEQ_NUMBER = '1.3.6.1.4.1.2.6.190.4.9'
    OID_LAST_TIME = '1.3.6.1.4.1.2.6.190.4.10'
    OID_OBJ_TYPE = '1.3.6.1.4.1.2.6.190.4.11'
    OID_OBJ_NAME = '1.3.6.1.4.1.2.6.190.4.17'
    OID_SEVERITY = '1.3.6.1.6.3.1.1.4.1.0'

    TRAP_SEVERITY_MAP = {
        '1.3.6.1.4.1.2.6.190.1': constants.Severity.CRITICAL,
        '1.3.6.1.4.1.2.6.190.2': constants.Severity.WARNING,
        '1.3.6.1.4.1.2.6.190.3': constants.Severity.INFORMATIONAL,
    }

    SEVERITY_MAP = {"warning": "Warning",
                    "informational": "Informational",
                    "error": "Major"}

    SECONDS_TO_MS = 1000

    def __init__(self, **kwargs):
        self.ssh_pool = SSHPool(**kwargs)

    @staticmethod
    def handle_split(split_str, split_char, arr_number):
        split_value = ''
        if split_str is not None and split_str != '':
            tmp_value = split_str.split(split_char, 1)
            if arr_number == 1 and len(tmp_value) > 1:
                split_value = tmp_value[arr_number].strip()
            elif arr_number == 0:
                split_value = tmp_value[arr_number].strip()
        return split_value

    @staticmethod
    def parse_alert(alert):
        # TODO
        pass

    def login(self):
        try:
            with self.ssh_pool.item() as ssh:
                SSHHandler.do_exec('lssystem', ssh)
        except Exception as e:
            LOG.error("Failed to login netapp %s" %
                      (six.text_type(e)))
            raise e

    @staticmethod
    def do_exec(command_str, ssh):
        """Execute command"""
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
                ssh_info = SSHHandler.do_exec(command, ssh)
            return ssh_info
        except Exception as e:
            msg = "Failed to ssh netapp %s: %s" % \
                  (command, six.text_type(e))
            raise exception.SSHException(msg)

    def change_capacity_to_bytes(self, unit):
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
            raw_capacity = used_capacity = free_capacity = 0
            system_info = self.exec_ssh_command('system show -instance')
            enclosure_info = self.exec_ssh_command('storage aggregate show')
            version = self.exec_ssh_command('version')
            version_arr = version.split(":")
            storage_map = {}
            enclosure_arr = enclosure_info.split("\r\n")
            if len(enclosure_arr) > 2:
                for detail in enclosure_arr[2:]:
                    detail_arr = detail.split()
                    if len(detail_arr) == 8 and '---' not in detail_arr[0]:
                        raw_capacity += int(self.parse_string(detail_arr[1]))
                        free_capacity += int(self.parse_string(detail_arr[2]))
                        used_capacity += int(self.parse_string(detail_arr[1])) \
                                         * float(detail_arr[3].strip('%')) / 100.0
            self.handle_detail(system_info, storage_map, split=':')
            status = "online" if storage_map.get("Health") is True else "offline"
            s = {
                "name": storage_map.get('Node'),
                "vendor": storage_map.get('Vendor'),
                "model": storage_map.get('Model'),
                "status": status,
                "serial_number": storage_map.get("SerialNumber"),
                "firmware_version": version_arr[0],
                "location": storage_map.get('Location'),
                "total_capacity": free_capacity + used_capacity,
                "raw_capacity": raw_capacity,
                "subscribed_capacity": "",
                "used_capacity": used_capacity,
                "free_capacity": free_capacity
            }
            return s
        except exception.DelfinException as e:
            err_msg = "Failed to get storage: %s" % (six.text_type(e.msg))
            LOG.error(err_msg)
            raise e
        except Exception as err:
            err_msg = "Failed to get storage: %s" % (six.text_type(err))
            LOG.error(err_msg)
            raise exception.InvalidResults(err_msg)

    def handle_detail(self, system_info, storage_map, split):
        detail_arr = system_info.split('\r\n')
        for detail in detail_arr:
            if detail is not None and detail != '':
                detail = detail.replace(' ', '')
                strinfo = detail.split(split)
                key = strinfo[0]
                value = ''
                if len(strinfo) > 1:
                    value = strinfo[1]
                storage_map[key] = value

    def list_storage_pools(self, storage_id):
        try:
            pool_list = []
            pool_info = self.exec_ssh_command('storage pool show')
            pool_arr = pool_info.split("\n")
            if len(pool_arr) > 2:
                for pool_detail in pool_arr[2:]:
                    if pool_detail is None or pool_detail == '':
                        continue
                    detail_arr = pool_detail.split()
                    if len(detail_arr) > 7:
                        pool = self.exec_ssh_command('storage pool show -storage-pool %s' % detail_arr[0])
                        pool_map = {}
                        self.handle_detail(pool, pool_map, split=':')
                        total_cap = self.parse_string(pool_map.get('Storage Pool Total Size'))
                        free_cap = self.parse_string(pool_map.get('Storage Pool Usable Size'))
                        p = {
                            'name': pool_map.get('Storage Pool Name'),
                            'storage_id': storage_id,
                            'native_storage_pool_id': pool_map.get('UUID of Storage Pool'),
                            'description': '',
                            'status': pool_map.get('State of the Storage Pool'),
                            'storage_type': constants.StorageType.BLOCK,
                            # TODO
                            # 'subscribed_capacity': int(subscribed_capacity),
                            'total_capacity': int(total_cap),
                            'used_capacity': int(total_cap) - int(free_cap),
                            'free_capacity': int(free_cap)
                        }
                        pool_list.append(p)
            return pool_list
        except exception.DelfinException as e:
            err_msg = "Failed to get storage pool: %s" % (six.text_type(e))
            LOG.error(err_msg)
            raise e
        except Exception as err:
            err_msg = "Failed to get storage pool: %s" % (six.text_type(err))
            LOG.error(err_msg)
            raise exception.InvalidResults(err_msg)

    def list_volumes(self, storage_id):
        try:
            volume_list = []
            volume_info = self.exec_ssh_command('volume show')
            volume_arr = volume_info.split('\r\n')
            if len(volume_arr) > 2:
                for volume in volume_arr[2:]:
                    detail_arr = volume.split()
                    if len(detail_arr) == 8 and '---' not in detail_arr[0]:
                        v = {
                            'name': detail_arr[1],
                            'storage_id': storage_id,
                            'description': '',
                            'status': detail_arr[3],
                            # TODO
                            'native_volume_id': '',
                            'native_storage_pool_id': '',
                            'wwn': '',
                            'compressed': '',
                            'deduplicated': '',
                            'type': detail_arr[4],
                            'total_capacity': int(self.parse_string(detail_arr[5])),
                            'used_capacity': int(self.parse_string(detail_arr[5])) * \
                                             float(detail_arr[7].strip('%')) / 100.0,
                            'free_capacity': int(self.parse_string(detail_arr[6]))
                        }
                        volume_list.append(v)
            return volume_list

        except exception.DelfinException as e:
            err_msg = "Failed to get storage volume: %s" % (six.text_type(e))
            LOG.error(err_msg)
            raise e

        except Exception as err:
            err_msg = "Failed to get storage volume: %s" % (six.text_type(err))
            LOG.error(err_msg)
            raise exception.InvalidResults(err_msg)

    def list_alerts(self, query_para):
        try:
            alert_list = []
            alert_info = self.exec_ssh_command('system health autosupport trigger history show')
            alert_arr = alert_info.split('\n')
            if len(alert_arr) > 2:
                for i in range(2, len(alert_arr) - 3):
                    if alert_arr[i] is None or alert_arr[i] == '':
                        continue
                    detail = alert_arr[i].split()
                    if len(detail) < 3:
                        continue
                    alert_detail = self.exec_ssh_command('system health alert show -instance -alert-id %s' % detail[3])
                    alert_map = {}
                    self.handle_detail(alert_detail, alert_map, split=':')
                    alert_model = {
                        'alert_id': alert_map.get('Alert ID'),
                        'alert_name': alert_map.get('Probable Cause'),
                        'severity': alert_map.get('Perceived Severity'),
                        'category': constants.Category.FAULT,
                        'type': 'EquipmentAlarm',
                        'occur_time': alert_map.get('Indication Time'),
                        'description': alert_map.get('Description'),
                        # TODO
                        'sequence_number': alert_map.get('sequence_number'),
                        'resource_type': '',
                        'location': alert_map.get('Alerting Resource Name')
                    }
                    alert_list.append(alert_model)
            return alert_list
        except exception.DelfinException as e:
            err_msg = "Failed to get storage alert: %s" % (six.text_type(e))
            LOG.error(err_msg)
            raise e
        except Exception as err:
            err_msg = "Failed to get storage alert: %s" % (six.text_type(err))
            LOG.error(err_msg)
            raise exception.InvalidResults(err_msg)
