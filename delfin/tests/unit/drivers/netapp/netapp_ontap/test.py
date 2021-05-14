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

from unittest import TestCase
from delfin import context
from delfin.drivers.netapp.dataontap.cluster_mode import NetAppCmodeDriver


class Request:
    def __init__(self):
        self.environ = {'delfin.context': context.RequestContext()}
        pass


ACCESS_INFO = {
    "storage_id": "12345",
    "vendor": "hpe",
    "model": "3par",
    "rest": {
        "host": "10.0.0.1",
        "port": 8443,
        "username": "user",
        "password": "pass"
    },
    "ssh": {
        "host": "192.168.159.130",
        "port": 22,
        "username": "admin",
        "password": "aq114477",
    }
}


def create_driver():
    # SSHHandler.login = mock.Mock(
    #     return_value={""})

    return NetAppCmodeDriver(**ACCESS_INFO)


class TestNetAppStorageDriver(TestCase):
    driver = create_driver()

    # def test_init(self):
    #     SSHHandler.login = mock.Mock(
    #         return_value={""})
    #     NetAppDriver(**ACCESS_INFO)
    def test_list_storage(self):
        # SSHPool.get = mock.Mock(
        #     return_value={paramiko.SSHClient()})
        # SSHHandler.do_exec = mock.Mock(
        #     side_effect=[system_info, enclosure_info])

        rs = self.driver.get_storage(context)
        print(rs)

    #
    # def test_list_storage_pools(self):
    #     SSHPool.get = mock.Mock(
    #         return_value={paramiko.SSHClient()})
    #     SSHHandler.do_exec = mock.Mock(
    #         side_effect=[pools_info, pool_info])
    #     self.driver.list_storage_pools(context)
    #
    def test_list_volumes(self):
        rs = self.driver.list_storage_pools(context)

        print(rs)
    #
    # def test_list_alerts(self):
    #     query_para = {
    #         "begin_time": 160508506000,
    #         "end_time": 160508507000
    #     }
    #     SSHPool.get = mock.Mock(
    #         return_value={paramiko.SSHClient()})
    #     SSHHandler.do_exec = mock.Mock(
    #         side_effect=[alerts_info, alert_info])
    #     self.driver.list_alerts(context, query_para)
    #
    # def test_list_storage_with_error(self):
    #     with self.assertRaises(Exception) as exc:
    #         self.driver.get_storage(context)
    #     self.assertIn('Exception in SSH protocol negotiation or logic',
    #                   str(exc.exception))
    #
    # def test_list_pool_with_error(self):
    #     with self.assertRaises(Exception) as exc:
    #         self.driver.list_storage_pools(context)
    #     self.assertIn('Exception in SSH protocol negotiation or logic',
    #                   str(exc.exception))
    #
    # def test_list_volume_with_error(self):
    #     with self.assertRaises(Exception) as exc:
    #         self.driver.list_volumes(context)
    #     self.assertIn('Exception in SSH protocol negotiation or logic',
    #                   str(exc.exception))
    #
    # def test_init_ssh_exec(self):
    #     with self.assertRaises(Exception) as exc:
    #         ssh = paramiko.SSHClient()
    #         SSHHandler.do_exec('lssystem', ssh)
    #     self.assertIn('', str(exc.exception))
    #
    # def test_ssh_pool_create(self):
    #     with self.assertRaises(Exception) as exc:
    #         kwargs = ACCESS_INFO
    #         ssh_pool = SSHPool(**kwargs)
    #         ssh_pool.create()
    #     self.assertIn('Exception in SSH protocol negotiation or logic',
    #                   str(exc.exception))
    #
    # def test_ssh_pool_put(self):
    #     ssh_pool = SSHPool(**ACCESS_INFO)
    #     ssh = paramiko.SSHClient()
    #     ssh_pool.put(ssh)
    #     ssh_pool.remove(ssh)
    #
    # def test_parse_alert(self):
    #     self.driver.parse_alert(context, trap_info)
    #
    # def test_reset_connection(self):
    #     self.driver.reset_connection(context, **ACCESS_INFO)
    #
    # def test_add_trap_config(self):
    #     trap_config = ''
    #     self.driver.add_trap_config(context, trap_config)
    #
    # def test_remove_trap_config(self):
    #     trap_config = ''
    #     self.driver.remove_trap_config(context, trap_config)
    #
    # def test_clear_alert(self):
    #     alert = ''
    #     self.driver.clear_alert(context, alert)
