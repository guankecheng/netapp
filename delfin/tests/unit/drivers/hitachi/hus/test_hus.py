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

from delfin.tests.unit.drivers.hitachi.hus import test_constans
from delfin import context
from delfin.drivers.hitachi.hus_110.hitachi_hus import HitachiHUSDriver
from delfin.drivers.utils.cli_client import NaviClient


class Request:
    def __init__(self):
        self.environ = {'delfin.context': context.RequestContext()}
        pass


class TestHUSStorageDriver(TestCase):
    NaviClient.exec = mock.Mock(
        side_effect=[test_constans.STORAGE_NAME_INFO])
    hus_client = HitachiHUSDriver(**test_constans.ACCESS_INFO)

    def test_get_storage(self):
        NaviClient.exec = mock.Mock(
            side_effect=[test_constans.STORAGE_INFO,
                         test_constans.DISK_INFO,
                         test_constans.POOL_INFO,
                         test_constans.POOL_DETAIL_INFO,
                         test_constans.RAID_GROUP_INFO])
        data = self.hus_client.get_storage(context)
        self.assertEqual(data['name'], 'HUS110_91110206')

    def test_list_storage_pools(self):
        NaviClient.exec = mock.Mock(
            side_effect=[test_constans.POOL_INFO,
                         test_constans.POOL_DETAIL_INFO,
                         test_constans.RAID_GROUP_INFO,
                         test_constans.RAID_GROUP_DETAIL_INFO])
        data = self.hus_client.list_storage_pools(context)
        self.assertEqual(data[0]['name'], '2')

    def test_list_volumes(self):
        NaviClient.exec = mock.Mock(
            side_effect=[
                test_constans.VOLUMES_INFO,
                test_constans.POOL_INFO,
                test_constans.POOL_DETAIL_INFO])
        data = self.hus_client.list_volumes(context)
        self.assertEqual(data[0]['name'], '1')

    def test_list_controllers(self):
        NaviClient.exec = mock.Mock(
            side_effect=[
                test_constans.STATUS_INFO,
                test_constans.STORAGE_INFO])
        data = self.hus_client.list_controllers(context)
        self.assertEqual(data[0]['name'], 'controller0')

    def test_list_ports(self):
        NaviClient.exec = mock.Mock(
            side_effect=[
                test_constans.ISCSI_PORT_INFO,
                test_constans.PORT_INFO,
                test_constans.STATUS_INFO,
                test_constans.WWN_INFO])
        data = self.hus_client.list_ports(context)
        self.assertEqual(data[0]['name'], '0A')

    def test_list_disks(self):
        NaviClient.exec = mock.Mock(
            side_effect=[test_constans.DISK_INFO])
        data = self.hus_client.list_disks(context)
        self.assertEqual(data[0]['name'], '0')
