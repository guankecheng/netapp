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
from delfin import exception
STORAGE_VENDOR = "HITACHI"

STORAGE_COMMAND = "auunitref -unit %(unit_name)s"
POOL_INFO_COMMAND = "audppool -unit %(unit_name)s -refer"
RAIDGROUP_INFO_COMMAND = "aurgref -unit %(unit_name)s -g"
STORAGE_INFO_COMMAND = "auunitinfo -unit %(unit_name)s"
DISK_INFO_COMMAND = "audrive -vendor -unit %(unit_name)s"
STATUS_INFO_COMMAND = "auparts  -unit %(unit_name)s"
VOLUMES_INFO_COMMAND = "auluref -unit %(unit_name)s -g"
POOL_DETAIL_INFO_COMMAND = \
    "audppool  -unit %(unit_name)s -detail -refer -dppoolno %(pool_no)s -g"
FC_PORT_INFO_COMMAND = "aufibre1 -unit -unit %(unit_name)s -refer"

SOCKET_TIMEOUT = 30
CER_ERR = 'Unable to validate the identity of the server'
CALLER_ERR = 'Caller not privileged'
SECURITY_ERR = 'Security file not found'
TRYING_CONNECT_ERR = 'error occurred while trying to connect'
CONNECTION_ERR = 'connection refused'
INVALID_ERR = 'invalid username, password and/or scope'
EXCEPTION_MAP = {CER_ERR: exception.SSLCertificateFailed,
                 CALLER_ERR: exception.InvalidUsernameOrPassword,
                 SECURITY_ERR: exception.InvalidUsernameOrPassword,
                 TRYING_CONNECT_ERR: exception.ConnectTimeout,
                 CONNECTION_ERR: exception.ConnectTimeout,
                 INVALID_ERR: exception.InvalidUsernameOrPassword}
CER_STORE = '2'
CER_REJECT = '3'
