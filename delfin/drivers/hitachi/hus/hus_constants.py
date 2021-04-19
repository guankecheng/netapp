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

STORAGE_VENDOR = "HITACHI"

STORAGE_INFO_COMMAND = "auunitref -unit %(unit_name)"
POOL_INFO_COMMAND = "audppool -unit %(unit_name) -refer"
RAIDGROUP_INFO_COMMAND = "aurgref -unit %(unit_name)"
VERSION_INFO_COMMAND = "auunitinfo -unit %(unit_name)"
DISK_INFO_COMMAND = "audrive -vendor -unit %(unit_name)"
STATUS_INFO_COMMAND = "auparts  -unit %(unit_name)"
VOLUMES_INFO_COMMAND = "auluref -unit %(unit_name)"
POOL_DETAIL_INFO_COMMAND = "audppool  -unit %(unit_name) -detail -refer -dppoolno %(pool_no)"

