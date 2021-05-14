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


ACCESS_INFO = {
    "storage_id": "12345",
    "vendor": "HITACHI",
    "model": "hus",
    "cli": {
        "host": "192.168.3.97",
        "port": 22,
        "username": "root",
        "password": "aq114477"
    }
}

STORAGE_NAME_INFO = \
    "Name Group Type Construction Connection Type Error Monitoring " \
    "Communication Type IP Address/Host Name/Device Name\n" \
    " HUS110_91110206 --- Dual TCP/IP(LAN) " \
    "Enable Non-secure 192.168.3.96 192.168.3.97"

STORAGE_INFO = """
Array Unit Type             : HUS110
H/W Rev.                    : 0100
Construction                : Dual
Serial Number               : 91110206
Array ID                    : 91110206
Firmware Revision(CTL0)     : 0988/H-W
Firmware Revision(CTL1)     : 0988/H-W
CTL0
  IPv4
    IPv4 Address            : 192.168.3.96
    IPv4 Subnet Mask        : 255.255.255.0
    IPv4 Default Gateway    : 192.168.3.1
  IPv6
    IPv6 Address            : 3003::21f:67ff:fe6f:ba29
    Subnet Prefix Length    : 64
    IPv6 Default Gateway    : fe80::7a58:60ff:fe80:cb44
CTL1
  IPv4
    IPv4 Address            : 192.168.3.97
    IPv4 Subnet Mask        : 255.255.255.0
    IPv4 Default Gateway    : 192.168.3.1
  IPv6
    IPv6 Address            : 3003::21f:67ff:fe6f:322f
    Subnet Prefix Length    : 64
    IPv6 Default Gateway    : fe80::7a58:60ff:fe80:cb44"""
DISK_INFO = """Unit  HDU  Capacity  Type  Speed  Vendor ID  Product Serial No.
   0    0  600GB     SAS  10000rpm  HITACHI    DKR5D-J600SS G6G6     KNJY0W6F
   0    1  600GB     SAS  10000rpm  SEAGATE    DKS5E-J600SS 7F0D     S0M78BX5
   0    2  600GB     SAS  10000rpm  HITACHI    DKR5C-J600SS G0G0     PZH02WZD
   0    3  600GB     SAS  10000rpm  HITACHI    DKR5C-J600SS G0G0     PVKUMK0D
   0    4  600GB     SAS  10000rpm  HITACHI    DKR5D-J600SS G6G6     KNJXWGRF
   """
POOL_INFO = "DP RAID Current Utilization  Current Over Replication " \
            "Available " "Current Replication   Rotational   Stripe  " \
            "Needing Preparation\n Pool Tier Mode  Level Total Capacity  " \
            "Consumed Capacity  Percent Provisioning Percent  Capacity  " \
            "Utilization Percent  Type Speed  Encryption  Status  " \
            "Reconstruction Progress  Size Capacity\n 2  N/A  1( 1D+1D) " \
            "1115684864 blocks 0 blocks 0% 18% 1115684864 blocks 0% " \
            "SAS 10000rpm N/A Normal  N/A  256KB 0 blocks" \

RAID_GROUP_INFO = "RAID   RAID         Parity   Rotational\n" \
    "Group  Level Groups  Type Speed  Encryption   Total Capacity " \
    "Free Capacity Priority Status Reconstruction Progress\n" \
    "1 1( 1D+1D) 1 SAS 10000rpm  N/A  535.7 GB 425.7 GB ( 79.5%) " \
    "Host Access Normal  N/A"

POOL_DETAIL_INFO = """
DP Pool : 2
  Tier Mode                                 : N/A
  RAID Level                                : 1(1D+1D)
  Page Size                                 : 32MB
  Stripe Size                               : 256KB
  Type                                      : SAS
  Rotational Speed                          : 10000rpm
  Encryption                                : N/A
  Status                                    : Normal
  Reconstruction Progress                   : N/A
  Capacity
    Total Capacity                          : 532.0 GB
    Replication Available Capacity          : 532.0 GB
    Consumed Capacity
      Total                                 : 0.0 GB
      User Data                             : 0.0 GB
      Replication Data                      : 0.0 GB
      Management Area                       : 0.0 GB
    Needing Preparation Capacity            : 0.0 GB
  DP Pool Consumed Capacity
    Current Utilization Percent             : 0%
    Early Alert Threshold                   : 40%
    Depletion Alert Threshold               : 50%
    Notifications Active                    : Enable
  Over Provisioning
    Current Over Provisioning Percent       : 18%
    Warning Threshold                       : 100%
    Limit Threshold                         : 130%
    Notifications Active                    : Disable
    Limit Enforcement                       : Disable
  Replication
    Current Replication Utilization Percent : 0%
    Replication Depletion Alert Threshold   : 40%
    Replication Data Released Threshold     : 95%
  Defined LU Count                          : 10
  DP RAID Group
                                Rotational
    DP RAID Group    Tier  Type      Speed      Chunk Size  RAID LevelCapacity
    20    N/A   SAS    10000rpm 1GB 1(1D+1D) 532.0 GB 0.0 GB  0%  Normal
  Drive Configuration
        Rotational
    DP RAID Group    RAID Level   Unit  HDU  Type     Speed  Capacity  Status
               20      1(1D+1D)      0    2  SAS   10000rpm  600GB     Normal
               20      1(1D+1D)      0    3  SAS   10000rpm  600GB     Normal
  Logical Unit
  Consumed              Stripe Cache     Pair Cache    Number
    LU Capacity   Capacity   Consumed % Size Partition Partition Status Paths
     2    10.0 GB     0.0 GB         0%  256KB         0       Auto  Normal  0
     3    10.0 GB     0.0 GB         0%  256KB         1       Auto  Normal  0
     4    10.0 GB     0.0 GB         0%  256KB         0       Auto  Normal  0
     5    10.0 GB     0.0 GB         0%  256KB         1       Auto  Normal  0
     6    10.0 GB     0.0 GB         0%  256KB         0       Auto  Normal  0
     7    10.0 GB     0.0 GB         0%  256KB         1       Auto  Normal  0
     8    10.0 GB     0.0 GB         0%  256KB         0       Auto  Normal  0
     9    10.0 GB     0.0 GB         0%  256KB         1       Auto  Normal  0
    10    10.0 GB     0.0 GB         0%  256KB         0       Auto  Normal  0
    11    10.0 GB     0.0 GB         0%  256KB         1       Auto  Normal  0
    """

VOLUMES_INFO = """Stripe  RAID     DP    Tier     RAID
   LU       Capacity
    1  20.0 GB 256KB   1  N/A  N/A 1( 1D+1D)  SAS 10000rpm  N/A 0  Normal
    2  10.0 GB 256KB N/A    2  N/A 1( 1D+1D)  SAS 10000rpm  N/A 0  Normal
    3  10.0 GB 256KB N/A    2  N/A 1( 1D+1D)  SAS 10000rpm  N/A 0  Normal
    4  10.0 GB 256KB N/A    2  N/A 1( 1D+1D)  SAS 10000rpm  N/A 0  Normal
    5  10.0 GB 256KB N/A    2  N/A 1( 1D+1D)  SAS 10000rpm  N/A 0  Normal
    6  10.0 GB 256KB N/A    2  N/A 1( 1D+1D)  SAS 10000rpm  N/A 0  Normal
    7  10.0 GB 256KB N/A    2  N/A 1( 1D+1D)  SAS 10000rpm  N/A 0  Normal
    8  10.0 GB 256KB N/A    2  N/A 1( 1D+1D)  SAS 10000rpm  N/A 0  Normal
    9  10.0 GB 256KB N/A    2  N/A 1( 1D+1D)  SAS 10000rpm  N/A 0  Normal
   10  10.0 GB 256KB N/A    2  N/A 1( 1D+1D)  SAS 10000rpm  N/A 0  Normal
   11  10.0 GB 256KB N/A    2  N/A 1( 1D+1D)  SAS 10000rpm  N/A 0  Normal
   12  20.0 GB 256KB   1  N/A  N/A 1( 1D+1D)  SAS 10000rpm  N/A 0  Normal
   13  20.0 GB 256KB   1  N/A  N/A 1( 1D+1D)  SAS 10000rpm  N/A 0  Normal
   14  20.0 GB 256KB   1  N/A  N/A 1( 1D+1D)  SAS 10000rpm  N/A 0  Normal
   15  20.0 GB 256KB   1  N/A  N/A 1( 1D+1D)  SAS 10000rpm  N/A 0  Normal
   16  10.0 GB 256KB   1  N/A  N/A 1( 1D+1D)  SAS 10000rpm  N/A 0  Normal"""

STATUS_INFO = """Controller
  CTL   Status
    0   Normal
    1   Normal

Cache
  CTL      Slot   Capacity(MB)   Status
    0         0           4096   Normal
    1         0           4096   Normal

Interface Board
  CTL       Interface Board  Type           Status
    0                     1  iSCSI          Normal
    1                     1  ---            Alarm

Battery
  Battery   Status
        0   Normal
        1   Normal

Host Connector
  Port  Status
    0A  Normal
    0B  Normal
    0C  Normal
    0D  Normal
    1A  Normal
    1B  Alarm
    1C  Normal
    1D  Normal

Fan
  Unit     Fan   Status

AC PS
  Unit   AC PS   Status
     0       0   Normal
     0       1   Normal

ENC
  Unit  ENC   Type                   Status

Unit
  Unit  Type              Serial Number
     0  StandardS         91110206"""

PORT_INFO = """Port Information
                                                    Port Address
  CTL  Port   Node Name          Port Name          Setting Current
    0     A   50060E80105394E0   50060E80105394E0   0000EF  000000
    0     B   50060E80105394E1   50060E80105394E1   0000EF  000000
    0     C   50060E80105394E2   50060E80105394E2   0000EF  000000
    0     D   50060E80105394E3   50060E80105394E3   0000EF  000000
    1     A   50060E80105394E8   50060E80105394E8   0000EF  000000
    1     B   50060E80105394E9   50060E80105394E9   0000EF  000000
    1     C   50060E80105394EA   50060E80105394EA   0000EF  000000
    1     D   50060E80105394EB   50060E80105394EB   0000EF  000000

Transfer Rate
  CTL  Port   Setting Current
    0     A   Auto    8Gbps
    0     B   Auto    8Gbps
    0     C   Auto    8Gbps
    0     D   Auto    8Gbps
    1     A   Auto    8Gbps
    1     B   Auto    8Gbps
    1     C   Auto    8Gbps
    1     D   Auto    8Gbps

Topology Information
  CTL  Port   Topology
    0     A   Loop
    0     B   Loop
    0     C   Loop
    0     D   Loop
    1     A   Loop
    1     B   Loop
    1     C   Loop
    1     D   Loop

Link Status
  CTL  Port   Status
    0     A   Link Failure
    0     B   Link Failure
    0     C   Link Failure
    0     D   Link Failure
    1     A   Link Failure
    1     B   Link Failure
    1     C   Link Failure
    1     D   Link Failure"""

RAID_GROUP_DETAIL_INFO = """RAID Group : 1
  RAID Level              : 1(1D+1D)
  Parity Groups           : 1
  Type                    : SAS
  Rotational Speed        : 10000rpm
  Encryption              : N/A
  Total Capacity          : 1123504128 blocks
  Free Capacity           : 892817408 blocks (79.5%)
  Priority                : Host Access
  Status                  : Normal
  Reconstruction Progress : N/A
  Defined LU Count        : 6
  Drive Configuration
                                       Rotational
    Parity Group  Unit  HDU  Capacity       Speed
               0     0    0  600GB       10000rpm
               0     0    1  600GB       10000rpm
  Assignment Information
     No.         Capacity        Assignment Status
       0        41943040 blocks  LUN1
       1        41943040 blocks  LUN12
       2        41943040 blocks  LUN13
       3        41943040 blocks  LUN14
       4        41943040 blocks  LUN15
       5        20971520 blocks  LUN16
       6       892817408 blocks  Free"""

ISCSI_PORT_INFO = """Port 0A
    Port Number : 3260
    Keep Alive Timer[sec.] : 60
    MTU : 1500
    Transfer Rate : 1Gbps
    Link Status : Link Up
    Ether Address : 00:01:02:03:04:05
    IPv4
        IPv4 Address : 100.101.102.103
        IPv4 Subnet Mask : 255.255.255.0
        IPv4 Default Gateway : 150.151.152.153
    IPv6 Status : Enable
    IPv6
        Link Local IP Address
            Address Type : Manual
            IP Address : fe80::2022
            Address Status : ---
        Global IP Address
            Address Type : Manual
                IP Address 1
                    IP Address : 2080::2022
                    Address Status : ---
                IP Address 2
                    IP Address : 2081::2022
                    Address Status : ---
        Subnet Prefix Length : 22l
        Default Gateway
            IP Address
                Current : 3034::2022
                Setting : 3033::2022
            Address Status : Unconfigured
            Link MTU : 1500`
    Connecting Hosts : 10000
    Result : Setting
    VLAN Status : Enable
    VLAN ID : 22
    Header Digest : Enable
    Data Digest : Enable
    Windows Scale : Enable
    Delayed Ack : Enable

Port 0B
    Port Number : 3260
    Keep Alive Timer[sec.] : 60
    MTU : 1500
    Transfer Rate : 1Gbps
    Link Status : Link Up
    Ether Address : 00:01:02:03:04:05
    IPv4
        IPv4 Address : 100.101.102.103
        IPv4 Subnet Mask : 255.255.255.0
        IPv4 Default Gateway : 150.151.152.153
    IPv6 Status : Enable
    IPv6
        Link Local IP Address
            Address Type : Manual
            IP Address : fe80::2022
            Address Status : ---
        Global IP Address
            Address Type : Manual
                IP Address 1
                    IP Address : 2080::2022
                    Address Status : ---
                IP Address 2
                    IP Address : 2081::2022
                    Address Status : ---
        Subnet Prefix Length : 22l
        Default Gateway
            IP Address
                Current : 3034::2022
                Setting : 3033::2022
            Address Status : Unconfigured
            Link MTU : 1500
    Connecting Hosts : 10000
    Result : Setting
    VLAN Status : Enable
    VLAN ID : 22
    Header Digest : Enable
    Data Digest : Enable
    Windows Scale : Enable
    Delayed Ack : Enable"""

WWN_INFO = """Port  0A  Host Group Security  ON
  Detected WWN
    Name                              Port Name
  Assigned WWN
    Name                              Port Name         Host Group
                                      1000006900001200  001:test001
  Assignable WWN
    Name                              Port Name
Port  0B  Host Group Security  ON
  Detected WWN
    Name                              Port Name
  Assigned WWN
    Name                              Port Name         Host Group
                                      1000006900001201  001:test001
  Assignable WWN
    Name                              Port Name
Port  0C  Host Group Security  ON
  Detected WWN
    Name                              Port Name
  Assigned WWN
    Name                              Port Name         Host Group
  Assignable WWN
    Name                              Port Name
Port  0D  Host Group Security  ON
  Detected WWN
    Name                              Port Name
  Assigned WWN
    Name                              Port Name         Host Group
  Assignable WWN
    Name                              Port Name
Port  1A  Host Group Security  ON
  Detected WWN
    Name                              Port Name
  Assigned WWN
    Name                              Port Name         Host Group
  Assignable WWN
    Name                              Port Name
Port  1B  Host Group Security  ON
  Detected WWN
    Name                              Port Name
  Assigned WWN
    Name                              Port Name         Host Group
  Assignable WWN
    Name                              Port Name
Port  1C  Host Group Security  ON
  Detected WWN
    Name                              Port Name
  Assigned WWN
    Name                              Port Name         Host Group
  Assignable WWN
    Name                              Port Name
Port  1D  Host Group Security  ON
  Detected WWN
    Name                              Port Name
  Assigned WWN
    Name                              Port Name         Host Group
  Assignable WWN
    Name                              Port Name"""
