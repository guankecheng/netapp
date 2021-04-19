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
from delfin.drivers.hitachi.hus import hus_constants
from delfin import exception, utils
from delfin.common import constants, alert_util
from delfin.drivers.utils.ssh_client import SSHPool

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

    def get_storage(self):
        try:
            storage = [], raw_capacity = used_capacity = total_capacity = free_capacity = 0
            storage_info = ""
            raw_capacity_info = ""
            version_info = ""
            status_info = ""
            pool_info = ""
            riadgroup_info = ""
            storage_arr = storage_info.split("\n")
            if len(storage_arr) > 1:
                storage = storage_arr[1].split()
                raw_capacity_arr = raw_capacity_info.split("\n")
                if len(raw_capacity_arr) > 1:
                    for c in raw_capacity_arr[1:]:
                        c_arr = c.split()
                        raw_capacity += int(self.parse_string(c_arr[2]))
                version_arr = version_info.split("\n")
                raidgroup_arr = riadgroup_info.split("\n")
                if len(raidgroup_arr) > 2:
                    for r in raidgroup_arr[2:]:
                        raidgroup = r.split()
                        total_capacity += int(self.parse_string(raidgroup[6]))
                        free_capacity += int(self.parse_string(raidgroup[7]))
                        used_capacity += int(self.parse_string(raidgroup[6])) - int(self.parse_string(raidgroup[7]))
                pool_arr = pool_info.split("\n")
                if len(pool_arr) > 4:
                    for p in pool_arr[2:]:
                        pool = p.split()
                        total_capacity += int(self.parse_string(pool[3]))
                        free_capacity += int(self.parse_string(pool[3])) - int(self.parse_string(pool[4]))
                        used_capacity += int(self.parse_string(pool[4]))

                # TODO
                s = {
                    'name': storage[0],
                    'vendor': hus_constants.STORAGE_VENDOR,
                    'description': '-',
                    'model': storage[1],
                    'status': 'normal',
                    'serial_number': version_arr[3].split(":")[2],
                    'firmware_version': version_arr[5].split(":")[2],
                    'location': '-',
                    'total_capacity': total_capacity,
                    'used_capacity': used_capacity,
                    'free_capacity': free_capacity,
                    'raw_capacity': raw_capacity
                }
                return s
            raise exception.DelfinException("The corresponding storage could not be found")
        except exception.DelfinException as e:
            err_msg = "Failed to get storage pool from netapp_fas fas: %s" % (six.text_type(e))
            LOG.error(err_msg)
            raise e
        except Exception as err:
            err_msg = "Failed to get storage pool from netapp_fas fas: %s" % (six.text_type(err))
            LOG.error(err_msg)
            raise exception.InvalidResults(err_msg)

    def list_storage_pools(self, storage_id):
        try:
            pool_list = []
            pool_info = ""
            riadgroup_info = ""
            raidgroup_arr = riadgroup_info.split("\n")
            if len(raidgroup_arr) > 2:
                for r in raidgroup_arr[2:]:
                    raidgroup = r.split()
                    p = {
                        'name': raidgroup[0],
                        'storage_id': storage_id,
                        'native_storage_pool_id': raidgroup[0],
                        'description': '',
                        'status': raidgroup[9],
                        'storage_type': constants.StorageType.BLOCK,
                        'subscribed_capacity': '',
                        'total_capacity': int(self.parse_string(raidgroup[6])),
                        'used_capacity': int(self.parse_string(raidgroup[6])) -
                                         int(self.parse_string(raidgroup[7])),
                        'free_capacity': int(self.parse_string(raidgroup[7]))
                    }
                    pool_list.append(p)
            pool_arr = pool_info.split("\n")
            if len(pool_arr) > 4:
                for p in pool_arr[2:]:
                    pool = p.split()
                    p = {
                        'name': pool[0],
                        'storage_id': storage_id,
                        'native_storage_pool_id': pool[0],
                        'description': '',
                        'status': pool[11],
                        'storage_type': constants.StorageType.BLOCK,
                        'subscribed_capacity': '',
                        'total_capacity': int(self.parse_string(pool[3])),
                        'used_capacity': int(self.parse_string(pool[4])),
                        'free_capacity': int(self.parse_string(pool[3])) -
                                         int(self.parse_string(pool[4]))
                    }
                    pool_list.append(p)
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
            volumes_list = []
            volumes_info = ""
            pool_list = self.list_storage_pools(storage_id)
            used_capacity_map = {}
            for pool in pool_list:
                pool_info = ""
                pool_arr = pool_info.split("Logical Unit")
                volumes = pool_arr[1].split("\n")
                used_capacity_map[volumes[0]] = volumes[2]
            volumes_arr = volumes_info.split("\n")
            if len(volumes_arr) > 2:

                for volume in volumes_arr[2:]:
                    volumes_arr = volume.split()
                    used_capacity = free_capacity = ''
                    if used_capacity_map[volumes_arr[0]]:
                        used_capacity = used_capacity_map[volumes_arr[0]] if used_capacity_map[volumes_arr[0]] else '-'
                        free_capacity = int(self.parse_string(volumes_arr[1])) - used_capacity
                    v = {
                        'name': volumes_arr[0],
                        'storage_id': storage_id,
                        'description': '',
                        'status': 'normal' if volumes_arr[0] == 'normal' else 'offline',
                        'native_volume_id': volumes_arr[0],
                        'native_storage_pool_id': volumes_arr[3] if volumes_arr[4] == 'N/A' else volumes_arr[4],
                        'wwn': '',
                        'compressed': '',
                        'deduplicated': '',
                        'type': constants.VolumeType.THIN,
                        'total_capacity': int(self.parse_string(volumes_arr[1])),
                        'used_capacity': used_capacity,
                        'free_capacity': free_capacity
                    }
                    volumes_list.append(v)
            return volumes_list
        except exception.DelfinException as e:
            err_msg = "Failed to get storage pool from netapp_fas fas: %s" % (six.text_type(e))
            LOG.error(err_msg)
            raise e
        except Exception as err:
            err_msg = "Failed to get storage pool from netapp_fas fas: %s" % (six.text_type(err))
            LOG.error(err_msg)
            raise exception.InvalidResults(err_msg)

    def list_controllers(self, storage_id):
        try:
            controller_list = []
            status_info = ""
            status_arr = status_info.split("Cache")
            controllers_arr = status_arr[0].split("\n")
            if len(controllers_arr) > 2:
                for controller in controllers_arr[2:]:
                    controller_arr = controller.split()
                    c = {
                        'name': 'controller' + controller_arr[0],
                        'storage_id': storage_id,
                        'native_controller_id': controller_arr[0],
                        'status': 'normal' if controller_arr[1] == 'normal' else 'offline',
                        'location': '-',
                        'soft_version': '-',
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
            pass
        except exception.DelfinException as e:
            err_msg = "Failed to get storage ports from netapp_fas fas: %s" % (six.text_type(e))
            LOG.error(err_msg)
            raise e

        except Exception as err:
            err_msg = "Failed to get storage ports from netapp_fas fas: %s" % (six.text_type(err))
            LOG.error(err_msg)
            raise exception.InvalidResults(err_msg)
