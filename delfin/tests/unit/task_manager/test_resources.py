# Copyright 2020 The SODA Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from unittest import mock
from delfin.common import config # noqa
from delfin.drivers import fake_storage
from delfin.task_manager.tasks import resources
from delfin.task_manager.tasks.resources import StorageDeviceTask

from delfin import test, context, coordination

storage = {
    'id': '12c2d52f-01bc-41f5-b73f-7abf6f38a2a6',
    'name': 'fake_driver',
    'description': 'it is a fake driver.',
    'vendor': 'fake_vendor',
    'model': 'fake_model',
    'status': 'normal',
    'serial_number': '2102453JPN12KA000011',
    'firmware_version': '1.0.0',
    'location': 'HK',
    'total_capacity': 1024 * 1024,
    'used_capacity': 3126,
    'free_capacity': 1045449,
}

pools_list = [{
    'id': '12c2d52f-01bc-41f5-b73f-7abf6f38a2a6',
    "name": "fake_pool_" + str(id),
    "storage_id": '12c2d52f-01bc-41f5-b73f-7abf6f38a2a6',
    "native_storage_pool_id": "fake_original_id_" + str(id),
    "description": "Fake Pool",
    "status": "normal",
    "total_capacity": 1024 * 1024,
    "used_capacity": 3126,
    "free_capacity": 1045449,
}
]

vols_list = [{
    'id': '12c2d52f-01bc-41f5-b73f-7abf6f38a340',
    "name": "fake_vol_" + str(id),
    "storage_id": '12c2d52f-01bc-41f5-b73f-7abf6f38a2a6',
    "description": "Fake Volume",
    "status": "normal",
    "native_volume_id": "fake_original_id_" + str(id),
    "wwn": "fake_wwn_" + str(id),
    "total_capacity": 1024 * 1024,
    "used_capacity": 3126,
    "free_capacity": 1045449,
}
]

ports_list = [{
    'id': '12c2d52f-01bc-41f5-b73f-7abf6f38a2a6',
    "name": "fake_pool_" + str(id),
    "storage_id": '12c2d52f-01bc-41f5-b73f-7abf6f38a2a6',
    "native_port_id": "fake_original_id_" + str(id),
    "location": "location_25",
    "connection_status": "disconnected",
    "health_status": "normal",
    "type": "iscsi",
    "logical_type": "service",
    "speed": 1000,
    "max_speed": 7200,
    "native_parent_id": "parent_id",
    "wwn": "wwn",
    "mac_address": "mac_352",
    "ipv4": "127.0.0.1",
    "ipv4_mask": "255.255.255.0",
    "ipv6": "",
    "ipv6_mask": ""
}
]

controllers_list = [{
    'id': '12c2d52f-01bc-41f5-b73f-7abf6f38a222',
    "name": "fake_controller_" + str(id),
    "storage_id": '12c2d52f-01bc-41f5-b73f-7abf6f38a2a6',
    "native_controller_id": "fake_original_id_" + str(id),
    "status": "normal",
    "location": "loc_100",
    "soft_version": "ver_321",
    "cpu_info": "Intel Xenon",
    "memory_size": 200000,
}
]

disks_list = [{
    'id': '12c2d52f-01bc-41f5-b73f-7abf6f38a2a6',
    "name": "fake_pool_" + str(id),
    "storage_id": '12c2d52f-01bc-41f5-b73f-7abf6f38a2a6',
    "native_disk_id": "fake_original_id_" + str(id),
    "serial_number": "serial_3299",
    "manufacturer": "Intel",
    "model": "model_4565",
    "firmware": "firmware_9541",
    "speed": 751,
    "capacity": 1074,
    "status": "offline",
    "physical_type": "sata",
    "logical_type": "cache",
    "health_score": 34,
    "native_disk_group_id": "",
}
]


class TestStorageDeviceTask(test.TestCase):
    def setUp(self):
        super(TestStorageDeviceTask, self).setUp()
        self.driver_api = mock.Mock()
        self.task_manager = StorageDeviceTask(
            context, "12c2d52f-01bc-41f5-b73f-7abf6f38a2a6")
        self.mock_object(self.task_manager, 'driver_api', self.driver_api)

    @mock.patch.object(coordination.LOCK_COORDINATOR, 'get_lock')
    @mock.patch('delfin.drivers.api.API.get_storage')
    @mock.patch('delfin.db.storage_update')
    @mock.patch('delfin.db.storage_get')
    @mock.patch('delfin.db.storage_delete')
    @mock.patch('delfin.db.access_info_delete')
    @mock.patch('delfin.db.alert_source_delete')
    def test_sync_successful(self, alert_source_delete, access_info_delete,
                             mock_storage_delete, mock_storage_get,
                             mock_storage_update, mock_get_storage, get_lock):
        storage_obj = resources.StorageDeviceTask(
            context, 'c5c91c98-91aa-40e6-85ac-37a1d3b32bda')

        storage_obj.sync()
        self.assertTrue(get_lock.called)
        self.assertTrue(mock_storage_get.called)
        self.assertTrue(mock_storage_delete.called)
        self.assertTrue(access_info_delete.called)
        self.assertTrue(alert_source_delete.called)
        self.assertTrue(mock_storage_update.called)
        mock_get_storage.assert_called_with(
            context, 'c5c91c98-91aa-40e6-85ac-37a1d3b32bda')

        fake_storage_obj = fake_storage.FakeStorageDriver()
        mock_get_storage.return_value = fake_storage_obj.get_storage(context)
        storage_obj.sync()

    @mock.patch('delfin.db.storage_delete')
    @mock.patch('delfin.db.alert_source_delete')
    def test_successful_remove(self, mock_alert_del, mock_strg_del):
        storage_obj = resources.StorageDeviceTask(
            context, 'c5c91c98-91aa-40e6-85ac-37a1d3b32bda')
        storage_obj.remove()

        mock_strg_del.assert_called_with(
            context, 'c5c91c98-91aa-40e6-85ac-37a1d3b32bda')
        mock_alert_del.assert_called_with(
            context, 'c5c91c98-91aa-40e6-85ac-37a1d3b32bda')


class TestStoragePoolTask(test.TestCase):
    @mock.patch.object(coordination.LOCK_COORDINATOR, 'get_lock')
    @mock.patch('delfin.drivers.api.API.list_storage_pools')
    @mock.patch('delfin.db.storage_pool_get_all')
    @mock.patch('delfin.db.storage_pools_delete')
    @mock.patch('delfin.db.storage_pools_update')
    @mock.patch('delfin.db.storage_pools_create')
    def test_sync_successful(self, mock_pool_create, mock_pool_update,
                             mock_pool_del, mock_pool_get_all,
                             mock_list_pools, get_lock):
        pool_obj = resources.StoragePoolTask(
            context, 'c5c91c98-91aa-40e6-85ac-37a1d3b32bda')
        pool_obj.sync()

        self.assertTrue(mock_list_pools.called)
        self.assertTrue(mock_pool_get_all.called)
        self.assertTrue(get_lock.called)

        # collect the pools from fake_storage
        fake_storage_obj = fake_storage.FakeStorageDriver()

        # add the new pool to DB
        mock_list_pools.return_value = fake_storage_obj.list_storage_pools(
            context)
        mock_pool_get_all.return_value = list()
        pool_obj.sync()
        self.assertTrue(mock_pool_create.called)

        # update the new pool of DB
        mock_list_pools.return_value = pools_list
        mock_pool_get_all.return_value = pools_list
        pool_obj.sync()
        self.assertTrue(mock_pool_update.called)

        # delete the new pool to DB
        mock_list_pools.return_value = list()
        mock_pool_get_all.return_value = pools_list
        pool_obj.sync()
        self.assertTrue(mock_pool_del.called)

    @mock.patch('delfin.db.storage_pool_delete_by_storage')
    def test_remove(self, mock_pool_del):
        pool_obj = resources.StoragePoolTask(
            context, 'c5c91c98-91aa-40e6-85ac-37a1d3b32bda')
        pool_obj.remove()
        self.assertTrue(mock_pool_del.called)


class TestStorageVolumeTask(test.TestCase):
    @mock.patch.object(coordination.LOCK_COORDINATOR, 'get_lock')
    @mock.patch('delfin.drivers.api.API.list_volumes')
    @mock.patch('delfin.db.volume_get_all')
    @mock.patch('delfin.db.volumes_delete')
    @mock.patch('delfin.db.volumes_update')
    @mock.patch('delfin.db.volumes_create')
    def test_sync_successful(self, mock_vol_create, mock_vol_update,
                             mock_vol_del, mock_vol_get_all, mock_list_vols,
                             get_lock):
        vol_obj = resources.StorageVolumeTask(
            context, 'c5c91c98-91aa-40e6-85ac-37a1d3b32bda')
        vol_obj.sync()
        self.assertTrue(mock_list_vols.called)
        self.assertTrue(mock_vol_get_all.called)
        self.assertTrue(get_lock.called)

        # collect the volumes from fake_storage
        fake_storage_obj = fake_storage.FakeStorageDriver()

        # add the volumes to DB
        mock_list_vols.return_value = fake_storage_obj.list_volumes(context)
        mock_vol_get_all.return_value = list()
        vol_obj.sync()
        self.assertTrue(mock_vol_create.called)

        # update the volumes to DB
        mock_list_vols.return_value = vols_list
        mock_vol_get_all.return_value = vols_list
        vol_obj.sync()
        self.assertTrue(mock_vol_update.called)

        # delete the volumes to DB
        mock_list_vols.return_value = list()
        mock_vol_get_all.return_value = vols_list
        vol_obj.sync()
        self.assertTrue(mock_vol_del.called)

    @mock.patch('delfin.db.volume_delete_by_storage')
    def test_remove(self, mock_vol_del):
        vol_obj = resources.StorageVolumeTask(
            context, 'c5c91c98-91aa-40e6-85ac-37a1d3b32bda')
        vol_obj.remove()
        self.assertTrue(mock_vol_del.called)


class TestStoragecontrollerTask(test.TestCase):
    @mock.patch.object(coordination.LOCK_COORDINATOR, 'get_lock')
    @mock.patch('delfin.drivers.api.API.list_controllers')
    @mock.patch('delfin.db.controller_get_all')
    @mock.patch('delfin.db.controllers_delete')
    @mock.patch('delfin.db.controllers_update')
    @mock.patch('delfin.db.controllers_create')
    def test_sync_successful(self,
                             mock_controller_create, mock_controller_update,
                             mock_controller_del, mock_controller_get_all,
                             mock_list_controllers, get_lock):
        controller_obj = resources.StorageControllerTask(
            context, 'c5c91c98-91aa-40e6-85ac-37a1d3b32bda')
        controller_obj.sync()

        self.assertTrue(mock_list_controllers.called)
        self.assertTrue(mock_controller_get_all.called)
        self.assertTrue(get_lock.called)

        # collect the controllers from fake_storage
        fake_storage_obj = fake_storage.FakeStorageDriver()

        # add the new controller to DB
        mock_list_controllers.return_value = \
            fake_storage_obj.list_controllers(context)
        mock_controller_get_all.return_value = list()
        controller_obj.sync()
        self.assertTrue(mock_controller_create.called)

        # update the new controller of DB
        mock_list_controllers.return_value = controllers_list
        mock_controller_get_all.return_value = controllers_list
        controller_obj.sync()
        self.assertTrue(mock_controller_update.called)

        # delete the new controller to DB
        mock_list_controllers.return_value = list()
        mock_controller_get_all.return_value = controllers_list
        controller_obj.sync()
        self.assertTrue(mock_controller_del.called)

    @mock.patch('delfin.db.controller_delete_by_storage')
    def test_remove(self, mock_controller_del):
        controller_obj = resources.StorageControllerTask(
            context, 'c5c91c98-91aa-40e6-85ac-37a1d3b32bda')
        controller_obj.remove()
        self.assertTrue(mock_controller_del.called)


class TestStoragePortTask(test.TestCase):
    @mock.patch.object(coordination.LOCK_COORDINATOR, 'get_lock')
    @mock.patch('delfin.drivers.api.API.list_ports')
    @mock.patch('delfin.db.port_get_all')
    @mock.patch('delfin.db.ports_delete')
    @mock.patch('delfin.db.ports_update')
    @mock.patch('delfin.db.ports_create')
    def test_sync_successful(self, mock_port_create, mock_port_update,
                             mock_port_del, mock_port_get_all, mock_list_ports,
                             get_lock):
        port_obj = resources.StoragePortTask(
            context, 'c5c91c98-91aa-40e6-85ac-37a1d3b32bda')
        port_obj.sync()
        self.assertTrue(mock_list_ports.called)
        self.assertTrue(mock_port_get_all.called)
        self.assertTrue(get_lock.called)

        # collect the ports from fake_storage
        fake_storage_obj = fake_storage.FakeStorageDriver()

        # add the ports to DB
        mock_list_ports.return_value = fake_storage_obj.list_ports(context)
        mock_port_get_all.return_value = list()
        port_obj.sync()
        self.assertTrue(mock_port_create.called)

        # update the ports to DB
        mock_list_ports.return_value = ports_list
        mock_port_get_all.return_value = ports_list
        port_obj.sync()
        self.assertTrue(mock_port_update.called)

        # delete the ports to DB
        mock_list_ports.return_value = list()
        mock_port_get_all.return_value = ports_list
        port_obj.sync()
        self.assertTrue(mock_port_del.called)

    @mock.patch('delfin.db.port_delete_by_storage')
    def test_remove(self, mock_port_del):
        port_obj = resources.StoragePortTask(
            context, 'c5c91c98-91aa-40e6-85ac-37a1d3b32bda')
        port_obj.remove()
        self.assertTrue(mock_port_del.called)


class TestStorageDiskTask(test.TestCase):
    @mock.patch.object(coordination.LOCK_COORDINATOR, 'get_lock')
    @mock.patch('delfin.drivers.api.API.list_disks')
    @mock.patch('delfin.db.disk_get_all')
    @mock.patch('delfin.db.disks_delete')
    @mock.patch('delfin.db.disks_update')
    @mock.patch('delfin.db.disks_create')
    def test_sync_successful(self, mock_disk_create, mock_disk_update,
                             mock_disk_del, mock_disk_get_all, mock_list_disks,
                             get_lock):
        disk_obj = resources.StorageDiskTask(
            context, 'c5c91c98-91aa-40e6-85ac-37a1d3b32bda')
        disk_obj.sync()
        self.assertTrue(mock_list_disks.called)
        self.assertTrue(mock_disk_get_all.called)
        self.assertTrue(get_lock.called)

        # collect the disks from fake_storage
        fake_storage_obj = fake_storage.FakeStorageDriver()

        # add the disks to DB
        mock_list_disks.return_value = fake_storage_obj.list_disks(context)
        mock_disk_get_all.return_value = list()
        disk_obj.sync()
        self.assertTrue(mock_disk_create.called)

        # update the disks to DB
        mock_list_disks.return_value = disks_list
        mock_disk_get_all.return_value = disks_list
        disk_obj.sync()
        self.assertTrue(mock_disk_update.called)

        # delete the disks to DB
        mock_list_disks.return_value = list()
        mock_disk_get_all.return_value = disks_list
        disk_obj.sync()
        self.assertTrue(mock_disk_del.called)

    @mock.patch('delfin.db.disk_delete_by_storage')
    def test_remove(self, mock_disk_del):
        disk_obj = resources.StorageDiskTask(
            context, 'c5c91c98-91aa-40e6-85ac-37a1d3b32bda')
        disk_obj.remove()
        self.assertTrue(mock_disk_del.called)
