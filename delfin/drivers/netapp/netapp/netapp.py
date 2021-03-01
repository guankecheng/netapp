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

from delfin.drivers import driver
from delfin.drivers.netapp.netapp import ssh_handler
from delfin.drivers.netapp.netapp.ssh_handler import SSHHandler


class NetAppDriver(driver.StorageDriver):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ssh_hanlder = ssh_handler.SSHHandler(**kwargs)
        self.ssh_hanlder.login()

    def reset_connection(self, context, **kwargs):
        self.ssh_hanlder.login()

    def get_storage(self, context):
        return self.ssh_hanlder.get_storage()

    def list_storage_pools(self, context):
        return self.ssh_hanlder.list_storage_pools(self.storage_id)

    def list_volumes(self, context):
        return self.ssh_hanlder.list_volumes(self.storage_id)

    def list_controllers(self, context):
        pass

    def list_ports(self, context):
        pass

    def list_disks(self, context):
        pass

    def list_alerts(self, context, query_para=None):
        return self.ssh_hanlder.list_alerts(query_para)

    def add_trap_config(self, context, trap_config):
        pass

    def remove_trap_config(self, context, trap_config):
        pass

    @staticmethod
    def parse_alert(context, alert):
        return SSHHandler.parse_alert(alert)

    def clear_alert(self, context, alert):
        pass

