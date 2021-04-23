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
from unittest import TestCase, mock

import paramiko
from delfin.tests.unit.drivers.netapp.netapp_fas import test_constans
from delfin import exception
from delfin import context
from delfin.drivers.netapp.netapp_fas.netapp_handler import NetAppHandler
from delfin.drivers.netapp.netapp_fas.netapp_fas import NetAppFasDriver
from delfin.drivers.utils.ssh_client import SSHPool


class Request:
    def __init__(self):
        self.environ = {'delfin.context': context.RequestContext()}
        pass


class TestNetAppStorageDriver(TestCase):
    SSHPool.get = mock.Mock(
        return_value={paramiko.SSHClient()})
    NetAppHandler.login = mock.Mock()
    netapp_client = NetAppFasDriver(**test_constans.ACCESS_INFO)

    def test_reset_connection(self):
        kwargs = test_constans.ACCESS_INFO
        NetAppHandler.login = mock.Mock()
        netapp_client = NetAppFasDriver(**kwargs)
        netapp_client.reset_connection(context, **kwargs)
        self.assertEqual(netapp_client.netapp_handler.ssh_pool.ssh_host,
                         "192.168.159.130")
        self.assertEqual(netapp_client.netapp_handler.ssh_pool.ssh_port, 22)

    def test_get_storage_success(self):
        NetAppHandler.do_exec = mock.Mock(
            side_effect=[test_constans.SYSTEM_INFO,
                         test_constans.VERSION,
                         test_constans.DISKS_INFO,
                         test_constans.PHYSICAL_INFO,
                         test_constans.POOLS_INFO,
                         test_constans.AGGREGATE_DETAIL_INFO])
        data = self.netapp_client.get_storage(context)
        self.assertEqual(data['vendor'], 'NetApp')

    def test_get_storage_failed(self):
        NetAppHandler.do_exec = mock.Mock(return_value={})
        with self.assertRaises(exception.DelfinException) as exc:
            self.netapp_client.get_storage(context)
        self.assertIn('Failed to get storage',
                      str(exc.exception))

        with self.assertRaises(Exception) as exc:
            self.netapp_client.get_storage(context)
        self.assertIn('Failed to get storage',
                      str(exc.exception))

    def test_list_storage_pools_success(self):
        NetAppHandler.do_exec = mock.Mock(
            side_effect=[test_constans.POOLS_INFO,
                         test_constans.AGGREGATE_DETAIL_INFO])
        data = self.netapp_client.list_storage_pools(context)
        self.assertEqual(data[0]['name'], 'aggr0')

    def test_list_storage_failed(self):
        NetAppHandler.do_exec = mock.Mock(side_effect=[{}, {}])
        with self.assertRaises(exception.DelfinException) as exc:
            self.netapp_client.list_storage_pools(context)
        self.assertIn('Failed to get storage',
                      str(exc.exception))

        with self.assertRaises(Exception) as exc:
            self.netapp_client.list_storage_pools(context)
        self.assertIn('Failed to get storage',
                      str(exc.exception))

    def test_list_volumes_success(self):
        NetAppHandler.do_exec = mock.Mock(
            side_effect=[test_constans.VOLUMES_INFO,
                         test_constans.THIN_VOLUME_INFO,
                         test_constans.POOLS_INFO,
                         test_constans.AGGREGATE_DETAIL_INFO])
        data = self.netapp_client.list_volumes(context)
        self.assertEqual(data[0]['name'], 'vol0')

    def test_list_volumes_failed(self):
        NetAppHandler.do_exec = mock.Mock(return_value={})
        with self.assertRaises(exception.DelfinException) as exc:
            self.netapp_client.list_volumes(context)
        self.assertIn('Failed to get storage',
                      str(exc.exception))

        with self.assertRaises(Exception) as exc:
            self.netapp_client.list_volumes(context)
        self.assertIn('Failed to get storage',
                      str(exc.exception))

    def test_list_alerts_success(self):
        NetAppHandler.do_exec = mock.Mock(
            side_effect=[test_constans.ALERT_INFO,
                         test_constans.EVENT_INFO])
        data = self.netapp_client.list_alerts(context)
        self.assertEqual(data[0]['alert_name'],
                         'mgmtgwd.configbr.noSNCBackup')

    def test_list_alerts_failed(self):
        NetAppHandler.do_exec = mock.Mock(return_value={})
        with self.assertRaises(exception.DelfinException) as exc:
            self.netapp_client.list_alerts(context)
        self.assertIn('Failed to get storage',
                      str(exc.exception))

        with self.assertRaises(Exception) as exc:
            self.netapp_client.list_alerts(context)
        self.assertIn('Failed to get storage',
                      str(exc.exception))

    def test_clear_alters(self):
        alert = {'alert_id': '123'}
        NetAppHandler.do_exec = mock.Mock()
        self.netapp_client.clear_alert(context, alert)

    def test_list_controllers_success(self):
        NetAppHandler.do_exec = mock.Mock(
            side_effect=[test_constans.CONTROLLER_INFO])
        data = self.netapp_client.list_controllers(context)
        self.assertEqual(data[0]['name'], 'node1')

    def test_list_controllers_failed(self):
        NetAppHandler.do_exec = mock.Mock(return_value={})
        with self.assertRaises(exception.DelfinException) as exc:
            self.netapp_client.list_controllers(context)
        self.assertIn('Failed to get storage',
                      str(exc.exception))

        with self.assertRaises(Exception) as exc:
            self.netapp_client.list_controllers(context)
        self.assertIn('Failed to get storage',
                      str(exc.exception))

    def test_list_ports_success(self):
        NetAppHandler.do_exec = mock.Mock(
            side_effect=[test_constans.PORTS_INFO,
                         test_constans.INTERFACE_INFO,
                         test_constans.FC_PORT_INFO])
        data = self.netapp_client.list_ports(context)
        self.assertEqual(data[0]['name'], 'e0a')

    def test_list_ports_failed(self):
        NetAppHandler.do_exec = mock.Mock(return_value={})
        with self.assertRaises(exception.DelfinException) as exc:
            self.netapp_client.list_ports(context)
        self.assertIn('Failed to get storage',
                      str(exc.exception))

        with self.assertRaises(Exception) as exc:
            self.netapp_client.list_ports(context)
        self.assertIn('Failed to get storage',
                      str(exc.exception))

    def test_list_disks_success(self):
        NetAppHandler.do_exec = mock.Mock(
            side_effect=[test_constans.DISKS_INFO,
                         test_constans.PHYSICAL_INFO])
        data = self.netapp_client.list_disks(context)
        self.assertEqual(data[0]['name'], 'NET-1.1')

    def test_list_disks_failed(self):
        NetAppHandler.do_exec = mock.Mock(return_value={})
        with self.assertRaises(exception.DelfinException) as exc:
            self.netapp_client.list_disks(context)
        self.assertIn('Failed to get storage',
                      str(exc.exception))

        with self.assertRaises(Exception) as exc:
            self.netapp_client.list_disks(context)
        self.assertIn('Failed to get storage',
                      str(exc.exception))

    def test_list_qtrees_success(self):
        NetAppHandler.do_exec = mock.Mock(side_effect=[
            test_constans.QTREES_INFO])
        data = self.netapp_client.list_qtrees(context)
        self.assertEqual(data[0]['security_mode'], 'ntfs')

    def test_list_qtrees_failed(self):
        NetAppHandler.do_exec = mock.Mock(return_value={})
        with self.assertRaises(exception.DelfinException) as exc:
            self.netapp_client.list_qtrees(context)
        self.assertIn('Failed to get storage',
                      str(exc.exception))

        with self.assertRaises(Exception) as exc:
            self.netapp_client.list_qtrees(context)
        self.assertIn('Failed to get storage',
                      str(exc.exception))

    def test_list_shares_success(self):
        NetAppHandler.do_exec = mock.Mock(
            side_effect=[test_constans.SHARES_INFO,
                         test_constans.SHARES_AGREEMENT_INFO])
        data = self.netapp_client.list_shares(context)
        self.assertEqual(data[0]['name'], 'admin$')

    def test_list_shares_failed(self):
        NetAppHandler.do_exec = mock.Mock(return_value={})
        with self.assertRaises(exception.DelfinException) as exc:
            self.netapp_client.list_shares(context)
        self.assertIn('Failed to get storage',
                      str(exc.exception))

        with self.assertRaises(Exception) as exc:
            self.netapp_client.list_shares(context)
        self.assertIn('Failed to get storage',
                      str(exc.exception))

    def test_list_filesystems_success(self):
        NetAppHandler.do_exec = mock.Mock(
            side_effect=[test_constans.FILE_SYSTEM_INFO,
                         test_constans.VSERVER_INFO,
                         test_constans.POOLS_INFO,
                         test_constans.AGGREGATE_DETAIL_INFO,
                         test_constans.VOLUMES_INFO,
                         test_constans.THIN_VOLUME_INFO,
                         test_constans.POOLS_INFO,
                         test_constans.AGGREGATE_DETAIL_INFO])
        data = self.netapp_client.list_filesystems(context)
        self.assertEqual(data[0]['name'], '/vol/vol0/')

    def test_list_filesystems_failed(self):
        NetAppHandler.do_exec = mock.Mock(return_value={})
        with self.assertRaises(exception.DelfinException) as exc:
            self.netapp_client.list_filesystems(context)
        self.assertIn('Failed to get storage',
                      str(exc.exception))

        with self.assertRaises(Exception) as exc:
            self.netapp_client.list_filesystems(context)
        self.assertIn('Failed to get storage',
                      str(exc.exception))
