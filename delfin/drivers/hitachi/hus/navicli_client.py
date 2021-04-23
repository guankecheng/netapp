# Copyright 2021 The SODA Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http:#www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from subprocess import Popen, PIPE

from oslo_log import log as logging

from delfin.drivers.hitachi.hus import hus_constants

LOG = logging.getLogger(__name__)


class NaviClient(object):

    @staticmethod
    def exec(command_str, stdin_value=None):
        """execute command_str using Popen
        :param command_str: should be list type
        :param stdin_value: same as stdin of Popen
        :return: output of Popen.communicate
        """
        p = Popen(command_str, stdin=PIPE, stdout=PIPE, stderr=PIPE,
                  shell=False)
        """Call method when input is needed"""
        if stdin_value:
            out, err = p.communicate(
                input=bytes(stdin_value, encoding='gbk'))
        else:
            """Call method when no input is required"""
            out = p.stdout.read()
        if isinstance(out, bytes):
            out = out.decode("gbk")
        result = out.strip()
        if result:
            """
            Determine whether an exception occurs according
            to the returned information
            """
            for exception_key in hus_constants.EXCEPTION_MAP.keys():
                if stdin_value is None \
                        or stdin_value == hus_constants.CER_STORE:
                    if exception_key == hus_constants.CER_ERR:
                        continue
                if exception_key in result:
                    raise hus_constants.EXCEPTION_MAP.get(
                        exception_key)(result)
        return result
