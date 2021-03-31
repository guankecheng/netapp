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

from delfin import exception
from delfin import context
from delfin.drivers.netapp.netapp_fas.netapp_handler import NetAppHandler
from delfin.drivers.netapp.netapp_fas.netapp_fas import NetAppFasDriver
from delfin.drivers.utils.ssh_client import SSHPool


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

SYSTEM_INFO = """Cluster UUID: 47096983-8018-11eb-bd5b-000c293284bd\r
          Cluster Name: cl\r
 Cluster Serial Number: -\r
      Cluster Location:\r 
       Cluster Contact: \r"""

AGGREGATE_INFO = """\r
Aggregate     Size Available Used% State   #Vols  Nodes            RAID Status\r
--------- -------- --------- ----- ------- ------ ---------------- ------------\r
aggr0        855MB   42.14MB   95% online       1 cl-01            raid_dp,\r
                                                                   normal\r
aggr1       8.79GB    3.98GB   55% online       3 cl-01            raid_dp,\r
                                                                   normal\r
aggr2       8.79GB    4.98GB   43% online       3 cl-01            raid_dp,\r
                                                                   normal\r"""

VERSION = """NetApp Release 9.0: Fri Aug 19 06:39:33 UTC 2016"""

DISK_INFO = """
                     Usable           Disk    Container   Container\r
Disk                   Size Shelf Bay Type    Type        Name      Owner\r
---------------- ---------- ----- --- ------- ----------- --------- --------\r
NET-1.1              1020MB     -  16 FCAL    aggregate   aggr0     cl-01\r
NET-1.2              1020MB     -  17 FCAL    aggregate   aggr1     cl-01\r
NET-1.3              1020MB     -  18 FCAL    aggregate   aggr1     cl-01\r
NET-1.4              1020MB     -  19 FCAL    aggregate   aggr1     cl-01\r
NET-1.5              1020MB     -  20 FCAL    aggregate   aggr1     cl-01\r
NET-1.6              1020MB     -  21 FCAL    aggregate   aggr1     cl-01\r
NET-1.7              1020MB     -  22 FCAL    aggregate   aggr1     cl-01\r
NET-1.8              1020MB     -  24 FCAL    aggregate   aggr2     cl-01\r
NET-1.9              1020MB     -  16 FCAL    aggregate   aggr0     cl-01\r
NET-1.10             1020MB     -  17 FCAL    aggregate   aggr0     cl-01\r
NET-1.11             1020MB     -  18 FCAL    aggregate   aggr1     cl-01\r
NET-1.12             1020MB     -  19 FCAL    aggregate   aggr1     cl-01\r
NET-1.13             1020MB     -  20 FCAL    aggregate   aggr1     cl-01\r
NET-1.14             1020MB     -  25 FCAL    aggregate   aggr2     cl-01\r
NET-1.15             1020MB     -  26 FCAL    aggregate   aggr2     cl-01\r
NET-1.16             1020MB     -  27 FCAL    aggregate   aggr2     cl-01\r
NET-1.17             1020MB     -  28 FCAL    aggregate   aggr2     cl-01\r
NET-1.18             1020MB     -  21 FCAL    aggregate   aggr1     cl-01\r
NET-1.19             1020MB     -  22 FCAL    aggregate   aggr1     cl-01\r
NET-1.20             1020MB     -  24 FCAL    aggregate   aggr1     cl-01\r
NET-1.21             1020MB     -  25 FCAL    aggregate   aggr2     cl-01\r
NET-1.22             1020MB     -  26 FCAL    aggregate   aggr2     cl-01\r
NET-1.23             1020MB     -  27 FCAL    aggregate   aggr2     cl-01\r
NET-1.24             1020MB     -  28 FCAL    aggregate   aggr2     cl-01\r
NET-1.25             1020MB     -  29 FCAL    aggregate   aggr2     cl-01\r
NET-1.26             1020MB     -  32 FCAL    aggregate   aggr2     cl-01\r
NET-1.27             1020MB     -  29 FCAL    aggregate   aggr2     cl-01\r
NET-1.28             1020MB     -  32 FCAL    spare       Pool0     cl-01\r
28 entries were displayed."""

POOLS_INFO = """
\r
                        Storage Pool Name: Pool1\r
                     UUID of Storage Pool: 60f2f1b9-e60f-11e3-a5e7-00a0981899a2\r
           Nodes Sharing the Storage Pool: node-a, node-b\r
          Number of Disks in Storage Pool: 2\r
                     Allocation Unit Size: 372.5GB\r
                             Storage Type: SSD\r
                 Storage Pool Usable Size: 1.09TB\r
                  Storage Pool Total Size: 1.45TB\r
                         Is Pool Healthy?: true\r
                State of the Storage Pool: normal\r
  Reason for storage pool being unhealthy: -\r
Job ID of the Currently Running Operation: - \r
\r
                        Storage Pool Name: Pool2\r
                     UUID of Storage Pool: 60f2f1b9-e60f-11e3-a5e7-00a0981899a1\r
           Nodes Sharing the Storage Pool: node-a, node-b\r
          Number of Disks in Storage Pool: 2\r
                     Allocation Unit Size: 372.5GB\r
                             Storage Type: SSD\r
                 Storage Pool Usable Size: 1.09TB\r
                  Storage Pool Total Size: 1.45TB\r
                         Is Pool Healthy?: true\r
                State of the Storage Pool: normal\r
  Reason for storage pool being unhealthy: -\r
Job ID of the Currently Running Operation: - \r"""

AGGREGATE_DETAIL_INFO = """\r
\r
                                         Aggregate: aggr0\r
                                      Storage Type: hdd\r
                                    Checksum Style: block\r
                                   Number Of Disks: 3\r
                                            Mirror: false\r
                              Disks for First Plex: NET-1.9, NET-1.1, NET-1.10\r
                           Disks for Mirrored Plex: -\r
                         Partitions for First Plex: -\r
                      Partitions for Mirrored Plex: -\r
                                              Node: cl-01\r
                           Free Space Reallocation: off\r
                                         HA Policy: cfo\r
                               Ignore Inconsistent: off\r
                Space Reserved for Snapshot Copies: 5%\r
           Aggregate Nearly Full Threshold Percent: 97%\r
                  Aggregate Full Threshold Percent: 98%\r
                             Checksum Verification: on\r
                                   RAID Lost Write: on\r
                             Enable Thorough Scrub: off\r
                                    Hybrid Enabled: false\r
                                    Available Size: 30.34MB\r
                                  Checksum Enabled: true\r
                                   Checksum Status: active\r
                                           Cluster: cl\r
                                   Home Cluster ID: 47096983-8018-11eb-bd5b-000c293284bd\r
                                        DR Home ID: -\r
                                      DR Home Name: -\r
                                   Inofile Version: 4\r
                                  Has Mroot Volume: true\r
                     Has Partner Node Mroot Volume: false\r
                                           Home ID: 4082368507\r
                                         Home Name: cl-01\r
                           Total Hybrid Cache Size: 0B\r
                                            Hybrid: false\r
                                      Inconsistent: false\r
                                 Is Aggregate Home: true\r
                                     Max RAID Size: 16\r
       Flash Pool SSD Tier Maximum RAID Group Size: -\r
                                          Owner ID: 4082368507\r
                                        Owner Name: cl-01\r
                                   Used Percentage: 96%\r
                                            Plexes: /aggr0/plex0\r
                                       RAID Groups: /aggr0/plex0/rg0 (block)\r
                             RAID Lost Write State: on\r
                                       RAID Status: raid_dp, normal\r
                                         RAID Type: raid_dp\r
   SyncMirror Resync Snapshot Frequency in Minutes: 5\r
                                           Is Root: true\r
      Space Used by Metadata for Volume Efficiency: 0B\r
                                              Size: 855MB\r
                                             State: online\r
                        Maximum Write Alloc Blocks: 0\r
                                         Used Size: 824.7MB\r
                                 Uses Shared Disks: false\r
                                       UUID String: a71b1e4e-d151-4868-986a-e71d84beabf8\r
                                 Number Of Volumes: 1
                             Is Flash Pool Caching: -\r
            Is Eligible for Auto Balance Aggregate: false\r
             State of the aggregate being balanced: ineligible\r
                          Total Physical Used Size: 712.3MB\r
                          Physical Used Percentage: 79%\r
            State Change Counter for Auto Balancer: 0\r
                                      Is Encrypted: false\r
                                     SnapLock Type: non-snaplock\r
                                 Encryption Key ID: -\r
 Is in the precommit phase of Copy-Free Transition: false\r
Is a 7-Mode transitioning aggregate that is not yet committed in clustered Data ONTAP and is currently out of space: false\r
Threshold When Aggregate Is Considered Unbalanced (%): 70\r
Threshold When Aggregate Is Considered Balanced (%): 40\r
                        Resynchronization Priority: -\r
                    Space Saved by Data Compaction: 0B\r
               Percentage Saved by Data Compaction: 0%\r
                          Amount of compacted data: 0B\r
\r
                                         Aggregate: aggr1\r
                                      Storage Type: hdd\r
                                    Checksum Style: block\r
                                   Number Of Disks: 12\r
                                            Mirror: false\r
                              Disks for First Plex: NET-1.2, NET-1.11, NET-1.3,\r
                                                    NET-1.12, NET-1.4,\r
                                                    NET-1.13, NET-1.5,\r
                                                    NET-1.18, NET-1.6,\r
                                                    NET-1.19, NET-1.7, NET-1.20\r
                           Disks for Mirrored Plex: -\r
                         Partitions for First Plex: -\r
                      Partitions for Mirrored Plex: -\r
                                              Node: cl-01\r
                           Free Space Reallocation: off\r
                                         HA Policy: sfo\r
                               Ignore Inconsistent: off\r
                Space Reserved for Snapshot Copies: -\r
           Aggregate Nearly Full Threshold Percent: 95%\r
                  Aggregate Full Threshold Percent: 98%\r
                             Checksum Verification: on\r
                                   RAID Lost Write: on\r
                             Enable Thorough Scrub: off\r
                                    Hybrid Enabled: false\r
                                    Available Size: 5.97GB\r
                                  Checksum Enabled: true\r
                                   Checksum Status: active\r
                                           Cluster: cl\r
                                   Home Cluster ID: 47096983-8018-11eb-bd5b-000c293284bd\r
                                        DR Home ID: -\r
                                      DR Home Name: -\r
                                   Inofile Version: 4\r
                                  Has Mroot Volume: false\r
                     Has Partner Node Mroot Volume: false\r
                                           Home ID: 4082368507\r
                                         Home Name: cl-01\r
                           Total Hybrid Cache Size: 0B\r
                                            Hybrid: false\r
                                      Inconsistent: false\r
                                 Is Aggregate Home: true\r
                                     Max RAID Size: 16\r
       Flash Pool SSD Tier Maximum RAID Group Size: -\r
                                          Owner ID: 4082368507\r
                                        Owner Name: cl-01\r
                                   Used Percentage: 32%\r
                                            Plexes: /aggr1/plex0\r
                                       RAID Groups: /aggr1/plex0/rg0 (block)\r
                             RAID Lost Write State: on\r
                                       RAID Status: raid_dp, normal\r
                                         RAID Type: raid_dp\r
   SyncMirror Resync Snapshot Frequency in Minutes: 5\r
                                           Is Root: false\r
      Space Used by Metadata for Volume Efficiency: 0B\r
                                              Size: 8.79GB\r
                                             State: online\r
                        Maximum Write Alloc Blocks: 0\r
                                         Used Size: 2.82GB\r
                                 Uses Shared Disks: false\r
                                       UUID String: 68ffbbca-eb73-4eeb-86bd-1a8e19c4c415\r
                                 Number Of Volumes: 3\r
                             Is Flash Pool Caching: -\r
            Is Eligible for Auto Balance Aggregate: false\r
             State of the aggregate being balanced: ineligible\r
                          Total Physical Used Size: 154.7MB\r
                          Physical Used Percentage: 2%\r
            State Change Counter for Auto Balancer: 0\r
                                      Is Encrypted: false\r
                                     SnapLock Type: non-snaplock\r
                                 Encryption Key ID: -\r
 Is in the precommit phase of Copy-Free Transition: false\r
Is a 7-Mode transitioning aggregate that is not yet committed in clustered Data ONTAP and is currently out of space: false\r
Threshold When Aggregate Is Considered Unbalanced (%): 70
Threshold When Aggregate Is Considered Balanced (%): 40\r
                        Resynchronization Priority: -\r
                    Space Saved by Data Compaction: 0B\r
               Percentage Saved by Data Compaction: 0%\r
                          Amount of compacted data: 0B\r
\r
                                         Aggregate: aggr2\r
                                      Storage Type: hdd\r
                                    Checksum Style: block\r
                                   Number Of Disks: 12\r
                                            Mirror: false\r
                              Disks for First Plex: NET-1.8, NET-1.21,\r
                                                    NET-1.14, NET-1.22,\r
                                                    NET-1.15, NET-1.23,\r
                                                    NET-1.16, NET-1.24,\r
                                                    NET-1.17, NET-1.25,\r
                                                    NET-1.27, NET-1.26\r
                           Disks for Mirrored Plex: -\r
                         Partitions for First Plex: -\r
                      Partitions for Mirrored Plex: -\r
                                              Node: cl-01\r
                           Free Space Reallocation: off\r
                                         HA Policy: sfo\r
                               Ignore Inconsistent: off\r
                Space Reserved for Snapshot Copies: -\r
           Aggregate Nearly Full Threshold Percent: 95%\r
                  Aggregate Full Threshold Percent: 98%\r
                             Checksum Verification: on\r
                                   RAID Lost Write: on\r
                             Enable Thorough Scrub: off\r
                                    Hybrid Enabled: false\r
                                    Available Size: 2.93GB\r
                                  Checksum Enabled: true\r
                                   Checksum Status: active\r
                                           Cluster: cl\r
                                   Home Cluster ID: 47096983-8018-11eb-bd5b-000c293284bd\r
                                        DR Home ID: -\r
                                      DR Home Name: -\r
                                   Inofile Version: 4\r
                                  Has Mroot Volume: false\r
                     Has Partner Node Mroot Volume: false\r
                                           Home ID: 4082368507\r
                                         Home Name: cl-01\r
                           Total Hybrid Cache Size: 0B\r
                                            Hybrid: false\r
                                      Inconsistent: false\r
                                 Is Aggregate Home: true\r
                                     Max RAID Size: 16\r
       Flash Pool SSD Tier Maximum RAID Group Size: -\r
                                          Owner ID: 4082368507\r
                                        Owner Name: cl-01\r
                                   Used Percentage: 67%\r
                                            Plexes: /aggr2/plex0\r
                                       RAID Groups: /aggr2/plex0/rg0 (block)\r
                             RAID Lost Write State: on\r
                                       RAID Status: raid_dp, normal\r
                                         RAID Type: raid_dp\r
   SyncMirror Resync Snapshot Frequency in Minutes: 5\r
                                           Is Root: false\r
      Space Used by Metadata for Volume Efficiency: 0B\r
                                              Size: 8.79GB\r
                                             State: online\r
                        Maximum Write Alloc Blocks: 0\r
                                         Used Size: 5.85GB\r
                                 Uses Shared Disks: false\r
                                       UUID String: b5cfe36e-eaed-433b-8a25-f333aa51b553\r
                                 Number Of Volumes: 6
                             Is Flash Pool Caching: -\r
            Is Eligible for Auto Balance Aggregate: false\r
             State of the aggregate being balanced: ineligible\r
                          Total Physical Used Size: 68.84MB\r
                          Physical Used Percentage: 1%\r
            State Change Counter for Auto Balancer: 0\r
                                      Is Encrypted: false\r
                                     SnapLock Type: non-snaplock\r
                                 Encryption Key ID: -\r
 Is in the precommit phase of Copy-Free Transition: false\r
Is a 7-Mode transitioning aggregate that is not yet committed in clustered Data ONTAP and is currently out of space: false\r
Threshold When Aggregate Is Considered Unbalanced (%): 70\r
Threshold When Aggregate Is Considered Balanced (%): 40\r
                        Resynchronization Priority: -\r
                    Space Saved by Data Compaction: 0B\r
               Percentage Saved by Data Compaction: 0%\r
                          Amount of compacted data: 0B\r
3 entries were displayed.\r
"""

VOLUMES_INFO = """\r
                                   Vserver Name: cl-01\r
                                    Volume Name: vol0\r
                                 Aggregate Name: aggr0\r
  List of Aggregates for FlexGroup Constituents: -\r
                                    Volume Size: 807.3MB\r
                             Volume Data Set ID: -\r
                      Volume Master Data Set ID: -\r
                                   Volume State: online\r
                                   Volume Style: flex\r
                          Extended Volume Style: flexvol\r
                         Is Cluster-Mode Volume: false\r
                          Is Constituent Volume: false\r
                                  Export Policy: -\r
                                        User ID: -\r
                                       Group ID: -\r
                                 Security Style: -\r
                               UNIX Permissions: ------------\r
                                  Junction Path: -\r
                           Junction Path Source: -\r
                                Junction Active: -\r
                         Junction Parent Volume: -\r
                                        Comment: -\r
                                 Available Size: 135.4MB\r
                                Filesystem Size: 807.3MB\r
                        Total User-Visible Size: 766.9MB\r
                                      Used Size: 631.5MB\r
                                Used Percentage: 83%\r
           Volume Nearly Full Threshold Percent: 95%\r
                  Volume Full Threshold Percent: 98%\r
           Maximum Autosize (for flexvols only): 968.7MB\r
                               Minimum Autosize: 807.3MB\r
             Autosize Grow Threshold Percentage: 85%\r
           Autosize Shrink Threshold Percentage: 50%\r
                                  Autosize Mode: off\r
            Total Files (for user-visible data): 24539\r
             Files Used (for user-visible data): 16715\r
                      Space Guarantee in Effect: true\r
                            Space SLO in Effect: true\r
                                      Space SLO: none\r
                          Space Guarantee Style: volume\r
                             Fractional Reserve: 100%\r
                                    Volume Type: RW\r
              Snapshot Directory Access Enabled: true\r
             Space Reserved for Snapshot Copies: 5%\r
                          Snapshot Reserve Used: 604%\r
                                Snapshot Policy: -\r
                                  Creation Time: Mon Mar 08 14:09:37 2021\r
                                       Language: -\r
                                   Clone Volume: -\r
                                      Node name: cl-01\r
                      Clone Parent Vserver Name: -\r
                        FlexClone Parent Volume: -\r
                                  NVFAIL Option: on\r
                          Volume's NVFAIL State: false\r
        Force NVFAIL on MetroCluster Switchover: off\r
                      Is File System Size Fixed: false\r
                     (DEPRECATED)-Extent Option: off\r
                  Reserved Space for Overwrites: 0B\r
              Primary Space Management Strategy: volume_grow\r
                       Read Reallocation Option: off\r
    Naming Scheme for Automatic Snapshot Copies: ordinal\r
               Inconsistency in the File System: false\r
                   Is Volume Quiesced (On-Disk): false\r
                 Is Volume Quiesced (In-Memory): false\r
      Volume Contains Shared or Compressed Data: false\r
              Space Saved by Storage Efficiency: 0B\r
         Percentage Saved by Storage Efficiency: 0%\r
                   Space Saved by Deduplication: 0B\r
              Percentage Saved by Deduplication: 0%\r
                  Space Shared by Deduplication: 0B\r
                     Space Saved by Compression: 0B\r
          Percentage Space Saved by Compression: 0%\r
            Volume Size Used by Snapshot Copies: 243.7MB\r
                                     Block Type: 64-bit\r
                               Is Volume Moving: -\r
                 Flash Pool Caching Eligibility: read-write\r
  Flash Pool Write Caching Ineligibility Reason: -\r
                     Managed By Storage Service: -\r
Create Namespace Mirror Constituents For SnapDiff Use: -\r
                        Constituent Volume Role: -\r
                          QoS Policy Group Name: -\r
                            Caching Policy Name: -\r
                Is Volume Move in Cutover Phase: -\r
        Number of Snapshot Copies in the Volume: 8\r
VBN_BAD may be present in the active filesystem: false\r
                Is Volume on a hybrid aggregate: false\r
                       Total Physical Used Size: 671.8MB\r
                       Physical Used Percentage: 83%\r
                                  List of Nodes: -\r
                          Is Volume a FlexGroup: false\r
                                  SnapLock Type: non-snaplock\r
                          Vserver DR Protection: -\r
\r
                                   Vserver Name: svm1\r
                                    Volume Name: svm1_root\r
                                 Aggregate Name: aggr1\r
  List of Aggregates for FlexGroup Constituents: -\r
                                    Volume Size: 800MB\r
                             Volume Data Set ID: 1025\r
                      Volume Master Data Set ID: 2155388521\r
                                   Volume State: online\r
                                   Volume Style: flex\r
                          Extended Volume Style: flexvol\r
                         Is Cluster-Mode Volume: true\r
                          Is Constituent Volume: false\r
                                  Export Policy: default\r
                                        User ID: -\r
                                       Group ID: -\r
                                 Security Style: ntfs\r
                               UNIX Permissions: ------------\r
                                  Junction Path: /\r
                           Junction Path Source: -\r
                                Junction Active: true\r
                         Junction Parent Volume: -\r
                                        Comment:\r
                                 Available Size: 759.8MB\r
                                Filesystem Size: 800MB\r
                        Total User-Visible Size: 760MB\r
                                      Used Size: 244KB\r
                                Used Percentage: 5%\r
           Volume Nearly Full Threshold Percent: 95%\r
                  Volume Full Threshold Percent: 98%\r
           Maximum Autosize (for flexvols only): 960MB\r
                               Minimum Autosize: 800MB\r
             Autosize Grow Threshold Percentage: 85%\r
           Autosize Shrink Threshold Percentage: 50%\r
                                  Autosize Mode: off\r
            Total Files (for user-visible data): 24313\r
             Files Used (for user-visible data): 103\r
                      Space Guarantee in Effect: true\r
                            Space SLO in Effect: true\r
                                      Space SLO: none\r
                          Space Guarantee Style: volume\r
                             Fractional Reserve: 100%\r
                                    Volume Type: RW\r
              Snapshot Directory Access Enabled: false\r
             Space Reserved for Snapshot Copies: 5%\r
                          Snapshot Reserve Used: 0%\r
                                Snapshot Policy: none\r
                                  Creation Time: Mon Mar 08 14:31:03 2021\r
                                       Language: C.UTF-8\r
                                   Clone Volume: false\r
                                      Node name: cl-01\r
                      Clone Parent Vserver Name: -\r
                        FlexClone Parent Volume: -\r
                                  NVFAIL Option: off\r
                          Volume's NVFAIL State: false\r
        Force NVFAIL on MetroCluster Switchover: off\r
                      Is File System Size Fixed: false\r
                     (DEPRECATED)-Extent Option: off\r
                  Reserved Space for Overwrites: 0B\r
              Primary Space Management Strategy: volume_grow\r
                       Read Reallocation Option: off\r
    Naming Scheme for Automatic Snapshot Copies: create_time\r
               Inconsistency in the File System: false\r
                   Is Volume Quiesced (On-Disk): false\r
                 Is Volume Quiesced (In-Memory): false\r
      Volume Contains Shared or Compressed Data: false\r
              Space Saved by Storage Efficiency: 0B\r
         Percentage Saved by Storage Efficiency: 0%\r
                   Space Saved by Deduplication: 0B\r
              Percentage Saved by Deduplication: 0%\r
                  Space Shared by Deduplication: 0B\r
                     Space Saved by Compression: 0B\r
          Percentage Space Saved by Compression: 0%\r
            Volume Size Used by Snapshot Copies: 0B\r
                                     Block Type: 64-bit\r
                               Is Volume Moving: false\r
                 Flash Pool Caching Eligibility: read-write\r
  Flash Pool Write Caching Ineligibility Reason: -\r
                     Managed By Storage Service: -\r
Create Namespace Mirror Constituents For SnapDiff Use: -\r
                        Constituent Volume Role: -\r
                          QoS Policy Group Name: -\r
                            Caching Policy Name: -\r
                Is Volume Move in Cutover Phase: false\r
        Number of Snapshot Copies in the Volume: 0\r
VBN_BAD may be present in the active filesystem: false\r
                Is Volume on a hybrid aggregate: false\r
                       Total Physical Used Size: 244KB\r
                       Physical Used Percentage: 0%\r
                                  List of Nodes: -\r
                          Is Volume a FlexGroup: false\r
                                  SnapLock Type: non-snaplock\r
                          Vserver DR Protection: -\r
\r
                                   Vserver Name: svm1\r
                                    Volume Name: vol_svm1_1\r
                                 Aggregate Name: aggr1\r
  List of Aggregates for FlexGroup Constituents: -\r
                                    Volume Size: 2GB\r
                             Volume Data Set ID: 1027\r
                      Volume Master Data Set ID: 2155388523\r
                                   Volume State: online\r
                                   Volume Style: flex\r
                          Extended Volume Style: flexvol\r
                         Is Cluster-Mode Volume: true\r
                          Is Constituent Volume: false\r
                                  Export Policy: default\r
                                        User ID: -\r
                                       Group ID: -\r
                                 Security Style: ntfs\r
                               UNIX Permissions: ------------\r
                                  Junction Path: -\r
                           Junction Path Source: -\r
                                Junction Active: -\r
                         Junction Parent Volume: -\r
                                        Comment:\r
                                 Available Size: 2.00GB\r
                                Filesystem Size: 2GB\r
                        Total User-Visible Size: 2GB\r
                                      Used Size: 3.84MB\r
                                Used Percentage: 0%\r
           Volume Nearly Full Threshold Percent: 95%\r
                  Volume Full Threshold Percent: 98%\r
           Maximum Autosize (for flexvols only): 2.40GB\r
                               Minimum Autosize: 2GB\r
             Autosize Grow Threshold Percentage: 85%\r
           Autosize Shrink Threshold Percentage: 50%\r
                                  Autosize Mode: off\r
            Total Files (for user-visible data): 62258\r
             Files Used (for user-visible data): 97\r
                      Space Guarantee in Effect: true\r
                            Space SLO in Effect: true\r
                                      Space SLO: none\r
                          Space Guarantee Style: volume\r
                             Fractional Reserve: 100%\r
                                    Volume Type: RW\r
              Snapshot Directory Access Enabled: true\r
             Space Reserved for Snapshot Copies: 0%\r
                          Snapshot Reserve Used: 0%\r
                                Snapshot Policy: default\r
                                  Creation Time: Mon Mar 08 14:32:54 2021\r
                                       Language: C.UTF-8\r
                                   Clone Volume: false\r
                                      Node name: cl-01\r
                      Clone Parent Vserver Name: -\r
                        FlexClone Parent Volume: -\r
                                  NVFAIL Option: off\r
                          Volume's NVFAIL State: false\r
        Force NVFAIL on MetroCluster Switchover: off\r
                      Is File System Size Fixed: false\r
                     (DEPRECATED)-Extent Option: off\r
                  Reserved Space for Overwrites: 0B\r
              Primary Space Management Strategy: volume_grow\r
                       Read Reallocation Option: off\r
    Naming Scheme for Automatic Snapshot Copies: create_time\r
               Inconsistency in the File System: false\r
                   Is Volume Quiesced (On-Disk): false\r
                 Is Volume Quiesced (In-Memory): false\r
      Volume Contains Shared or Compressed Data: false\r
              Space Saved by Storage Efficiency: 0B\r
         Percentage Saved by Storage Efficiency: 0%\r
                   Space Saved by Deduplication: 0B\r
              Percentage Saved by Deduplication: 0%\r
                  Space Shared by Deduplication: 0B\r
                     Space Saved by Compression: 0B\r
          Percentage Space Saved by Compression: 0%\r
            Volume Size Used by Snapshot Copies: 2.98MB\r
                                     Block Type: 64-bit\r
                               Is Volume Moving: false\r
                 Flash Pool Caching Eligibility: read-write\r
  Flash Pool Write Caching Ineligibility Reason: -\r
                     Managed By Storage Service: -\r
Create Namespace Mirror Constituents For SnapDiff Use: -\r
                        Constituent Volume Role: -\r
                          QoS Policy Group Name: -\r
                            Caching Policy Name: -\r
                Is Volume Move in Cutover Phase: false\r
        Number of Snapshot Copies in the Volume: 8\r
VBN_BAD may be present in the active filesystem: false\r
                Is Volume on a hybrid aggregate: false\r
                       Total Physical Used Size: 3.84MB\r
                       Physical Used Percentage: 0%\r
                                  List of Nodes: -\r
                          Is Volume a FlexGroup: false\r
                                  SnapLock Type: non-snaplock\r
                          Vserver DR Protection: -\r
7 entries were displayed."""

EVENT_INFO = """\r
                  Node: cl-01\r
             Sequence#: 9102\r
                  Time: 3/10/2021 18:19:14\r
              Severity: ERROR\r
                Source: mgwd\r
          Message Name: mgmtgwd.configbr.noSNCBackup\r
                 Event: mgmtgwd.configbr.noSNCBackup: Cluster backup is saved on only one node and no offsite configuration backup destination URL is configured.\r
     Corrective Action: Configure an offsite configuration backup destination URL as soon as possible, using the command "system configuration backup settings modify -destination <destination-url> -username <username-on-destination-url>" and the command "system configuration backup settings set-password". See the "system configuration backup settings" man pages for more information.\r
           Description: This message occurs when the cluster backup is saved on only one node and no offsite configuration backup destination URL is configured.\r
\r
                  Node: cl-01\r
             Sequence#: 7855\r
                  Time: 3/10/2021 10:18:36\r
              Severity: ERROR\r
                Source: mgwd\r
          Message Name: mgmtgwd.configbr.noSNCBackup\r
                 Event: mgmtgwd.configbr.noSNCBackup: Cluster backup is saved on only one node and no offsite configuration backup destination URL is configured.\r
     Corrective Action: Configure an offsite configuration backup destination URL as soon as possible, using the command "system configuration backup settings modify -destination <destination-url> -username <username-on-destination-url>" and the command "system configuration backup settings set-password". See the "system configuration backup settings" man pages for more information.\r
           Description: This message occurs when the cluster backup is saved on only one node and no offsite configuration backup destination URL is configured."""

ALERT_INFO = """\r
                  Node: node1\r
               Monitor: node-connect\r
              Alert ID: DualPathToDiskShelf_Alert\r
     Alerting Resource: 50:05:0c:c1:02:00:0f:02\r
             Subsystem: SAS-connect\r
       Indication Time: Mon Mar 10 10:26:38 2021\r
    Perceived Severity: Major\r
        Probable Cause: Connection_establishment_error\r
           Description: Disk shelf 2 does not have two paths to controller node1.\r
    Corrective Actions: 1. Halt controller node1 and all controllers attached to disk shelf 2.\r
                        2. Connect disk shelf 2 to controller node1 via two paths following the rules in the Universal SAS and ACP Cabling Guide.\r
                        3. Reboot the halted controllers.\r
                        4. Contact support personnel if the alert persists.\r
       Possible Effect: Access to disk shelf 2 via controller node1 will be lost with a single hardware component failure (e.g. cable, HBA, or IOM failure).\r
           Acknowledge: false\r
              Suppress: false\r
                Policy: DualPathToDiskShelf_Policy\r
          Acknowledger: -\r
            Suppressor: -   \r                                                   
Additional Information: Shelf uuid: 50:05:0c:c1:02:00:0f:02\r
                        Shelf id: 2\r
                        Shelf Name: 4d.shelf2\r
                        Number of Paths: 1\r
                        Number of Disks: 6\r
                        Adapter connected to IOMA:\r
                        Adapter connected to IOMB: 4d\r
Alerting Resource Name: Shelf ID 2\r
 Additional Alert Tags: quality-of-service, nondisruptive-upgrade\r"""

CONTROLLER_INFO = """\r
                     Node: node1\r
                System ID: 140733730268652\r
               Model Name: FAS2520\r
              Part Number: 111-01316\r
                 Revision: 21\r
            Serial Number: 700001456939\r
          Controller Type: none\r
                   Status: ok\r
               Chassis ID: 4591227214\r"""

PORTS_INFO = """\r
                                        Node: cl-01\r
                                        Port: e0a\r
                                        Link: up\r
                                         MTU: 1500\r
             Auto-Negotiation Administrative: true\r
                Auto-Negotiation Operational: true\r
                  Duplex Mode Administrative: auto\r
                     Duplex Mode Operational: full\r
                        Speed Administrative: auto\r
                           Speed Operational: 1000\r
                 Flow Control Administrative: full\r
                    Flow Control Operational: none\r
                                 MAC Address: 00:0c:29:32:84:bd\r
                                   Port Type: physical\r
                 Interface Group Parent Node: -\r
                 Interface Group Parent Port: -\r
                       Distribution Function: -\r
                               Create Policy: -\r
                            Parent VLAN Node: -\r
                            Parent VLAN Port: -\r
                                    VLAN Tag: -\r
                            Remote Device ID: -\r
                                IPspace Name: Default\r
                            Broadcast Domain: Default\r
                          MTU Administrative: 1500\r
                          Port Health Status: healthy\r
                   Ignore Port Health Status: false\r
                Port Health Degraded Reasons: -\r
\r
                                        Node: cl-01\r
                                        Port: e0b\r
                                        Link: up\r
                                         MTU: 1500\r
             Auto-Negotiation Administrative: true\r
                Auto-Negotiation Operational: true\r
                  Duplex Mode Administrative: auto\r
                     Duplex Mode Operational: full\r
                        Speed Administrative: auto\r
                           Speed Operational: 1000\r
                 Flow Control Administrative: full\r
                    Flow Control Operational: none\r
                                 MAC Address: 00:0c:29:32:84:c7\r
                                   Port Type: physical\r
                 Interface Group Parent Node: -\r
                 Interface Group Parent Port: -\r
                       Distribution Function: -\r
                               Create Policy: -\r
                            Parent VLAN Node: -\r
                            Parent VLAN Port: -\r
                                    VLAN Tag: -\r
                            Remote Device ID: -\r
                                IPspace Name: Default\r
                            Broadcast Domain: Default\r
                          MTU Administrative: 1500\r
                          Port Health Status: healthy\r
                   Ignore Port Health Status: false\r
                Port Health Degraded Reasons: -\r"""

INTERFACE_INFO = """\r
                    Vserver Name: cl\r
          Logical Interface Name: cl-01_mgmt1\r
                            Role: node-mgmt\r
                   Data Protocol: none\r
                       Home Node: cl-01\r
                       Home Port: e0c\r
                    Current Node: cl-01\r
                    Current Port: e0c\r
              Operational Status: up\r
                 Extended Status: -\r
                         Is Home: true\r
                 Network Address: 192.168.159.130\r
                         Netmask: 255.255.255.0\r
             Bits in the Netmask: 24\r
                     Subnet Name: -\r
           Administrative Status: up\r
                 Failover Policy: local-only\r
                 Firewall Policy: mgmt\r
                     Auto Revert: true\r
   Fully Qualified DNS Zone Name: none\r
         DNS Query Listen Enable: false\r
             Failover Group Name: Default\r
                        FCP WWPN: -\r
                  Address family: ipv4\r
                         Comment: -\r
                  IPspace of LIF: Default\r
  Is Dynamic DNS Update Enabled?: -\r
\r
                    Vserver Name: cl\r
          Logical Interface Name: cluster_mgmt\r
                            Role: cluster-mgmt\r
                   Data Protocol: none\r
                       Home Node: cl-01\r
                       Home Port: e0d\r
                    Current Node: cl-01\r
                    Current Port: e0a\r
              Operational Status: up\r
                 Extended Status: -\r
                         Is Home: false\r
                 Network Address: 192.168.159.131\r
                         Netmask: 255.255.255.0\r
             Bits in the Netmask: 24\r
                     Subnet Name: -\r
           Administrative Status: up\r
                 Failover Policy: broadcast-domain-wide\r
                 Firewall Policy: mgmt\r
                     Auto Revert: false\r
   Fully Qualified DNS Zone Name: none\r
         DNS Query Listen Enable: false\r
             Failover Group Name: Default\r
                        FCP WWPN: -\r
                  Address family: ipv4\r
                         Comment: -\r
                  IPspace of LIF: Default\r
  Is Dynamic DNS Update Enabled?: -\r
2 entries were displayed.\r"""

DISKS_INFO = """\r                  
                  Disk: NET-1.1\r
        Container Type: aggregate\r
            Owner/Home: cl-01 / cl-01\r
               DR Home: -\r
    Stack ID/Shelf/Bay: -  / -  / 16\r
                   LUN: 0\r
                 Array: NETAPP_VD_1\r
                Vendor: NETAPP\r
                 Model: VD-1000MB-FZ-520\r
         Serial Number: 07294300
                   UID: 4E455441:50502020:56442D31:3030304D:422D465A:2D353230:30373239:34333030:00000000:00000000\r
                   BPS: 520\r
         Physical Size: 1.00GB\r
              Position: parity\r
Checksum Compatibility: block\r
             Aggregate: aggr0\r
                  Plex: plex0\r
Paths:\r
                                LUN  Initiator Side        Target Side                                                        Link\r\r
Controller         Initiator     ID  Switch Port           Switch Port           Acc Use  Target Port                TPGN    Speed      I/O KB/s          IOPS\r
------------------ ---------  -----  --------------------  --------------------  --- ---  -----------------------  ------  -------  ------------  ------------\r
cl-01              v1             0  N/A                   N/A                   AO  INU  0000000000000000              0   0 Gb/S            71             2\r
cl-01              v5             0  N/A                   N/A                   AO  RDY  0000000000000000              0   0 Gb/S             0             0\r
\r
Errors:\r
-
                  Disk: NET-1.2\r
        Container Type: aggregate\r
            Owner/Home: cl-01 / cl-01\r
               DR Home: -\r
    Stack ID/Shelf/Bay: -  / -  / 17\r
                   LUN: 0\r
                 Array: NETAPP_VD_1\r
                Vendor: NETAPP\r
                 Model: VD-1000MB-FZ-520\r
         Serial Number: 07294301\r
                   UID: 4E455441:50502020:56442D31:3030304D:422D465A:2D353230:30373239:34333031:00000000:00000000\r
                   BPS: 520\r
         Physical Size: 1.00GB\r
              Position: dparity\r
Checksum Compatibility: block\r
             Aggregate: aggr1\r
                  Plex: plex0\r
Paths:\r
                                LUN  Initiator Side        Target Side                                                        Link\r
Controller         Initiator     ID  Switch Port           Switch Port           Acc Use  Target Port                TPGN    Speed      I/O KB/s          IOPS\r
------------------ ---------  -----  --------------------  --------------------  --- ---  -----------------------  ------  -------  ------------  ------------\r
cl-01              v1             0  N/A                   N/A                   AO  INU  0000000000000000              0   0 Gb/S             0             0\r
cl-01              v5             0  N/A                   N/A                   AO  RDY  0000000000000000              0   0 Gb/S             0             0\r
\r
Errors:\r
-\r
"""

PHYSICAL_INFO = """\r
Disk             Type    Vendor   Model                Revision     RPM     BPS\r
---------------- ------- -------- -------------------- -------- ------- -------\r
NET-1.1          FCAL    NETAPP   VD-1000MB-FZ-520     0042       15000     520\r
                 SerialNumber: 07294300\r
NET-1.2          FCAL    NETAPP   VD-1000MB-FZ-520     0042       15000     520\r
                 SerialNumber: 07294301\r
NET-1.3          FCAL    NETAPP   VD-1000MB-FZ-520     0042       15000     520\r
                 SerialNumber: 07294302\r
NET-1.4          FCAL    NETAPP   VD-1000MB-FZ-520     0042       15000     520\r
                 SerialNumber: 07294303\r
NET-1.5          FCAL    NETAPP   VD-1000MB-FZ-520     0042       15000     520\r
                 SerialNumber: 07294304\r
NET-1.6          FCAL    NETAPP   VD-1000MB-FZ-520     0042       15000     520\r
                 SerialNumber: 07294305\r
NET-1.7          FCAL    NETAPP   VD-1000MB-FZ-520     0042       15000     520\r
                 SerialNumber: 07294306\r
NET-1.8          FCAL    NETAPP   VD-1000MB-FZ-520     0042       15000     520\r
                 SerialNumber: 07294307\r
NET-1.9          FCAL    NETAPP   VD-1000MB-FZ-520     0042       15000     520\r
                 SerialNumber: 07904200\r
NET-1.10         FCAL    NETAPP   VD-1000MB-FZ-520     0042       15000     520\r
                 SerialNumber: 07904201\r
NET-1.11         FCAL    NETAPP   VD-1000MB-FZ-520     0042       15000     520\r
                 SerialNumber: 07904202\r
NET-1.12         FCAL    NETAPP   VD-1000MB-FZ-520     0042       15000     520\r
                 SerialNumber: 07904203\r
NET-1.13         FCAL    NETAPP   VD-1000MB-FZ-520     0042       15000     520\r
                 SerialNumber: 07904204\r
NET-1.14         FCAL    NETAPP   VD-1000MB-FZ-520     0042       15000     520\r
                 SerialNumber: 07294308\r
NET-1.15         FCAL    NETAPP   VD-1000MB-FZ-520     0042       15000     520\r
                 SerialNumber: 07294309\r
NET-1.16         FCAL    NETAPP   VD-1000MB-FZ-520     0042       15000     520\r
                 SerialNumber: 07294310\r
NET-1.17         FCAL    NETAPP   VD-1000MB-FZ-520     0042       15000     520\r
                 SerialNumber: 07294311\r
NET-1.18         FCAL    NETAPP   VD-1000MB-FZ-520     0042       15000     520\r
                 SerialNumber: 07904205\r
NET-1.19         FCAL    NETAPP   VD-1000MB-FZ-520     0042       15000     520\r
                 SerialNumber: 07904206\r
NET-1.20         FCAL    NETAPP   VD-1000MB-FZ-520     0042       15000     520\r
                 SerialNumber: 07904207\r
NET-1.21         FCAL    NETAPP   VD-1000MB-FZ-520     0042       15000     520\r
                 SerialNumber: 07904208\r
NET-1.22         FCAL    NETAPP   VD-1000MB-FZ-520     0042       15000     520\r
                 SerialNumber: 07904209\r
NET-1.23         FCAL    NETAPP   VD-1000MB-FZ-520     0042       15000     520\r
                 SerialNumber: 07904210\r
NET-1.24         FCAL    NETAPP   VD-1000MB-FZ-520     0042       15000     520\r
                 SerialNumber: 07904311\r
NET-1.25         FCAL    NETAPP   VD-1000MB-FZ-520     0042       15000     520\r
                 SerialNumber: 07904312\r
NET-1.26         FCAL    NETAPP   VD-1000MB-FZ-520     0042       15000     520\r
                 SerialNumber: 07904313\r
NET-1.27         FCAL    NETAPP   VD-1000MB-FZ-520     0042       15000     520\r
                 SerialNumber: 07294312\r
NET-1.28         FCAL    NETAPP   VD-1000MB-FZ-520     0042       15000     520\r
                 SerialNumber: 07294313\r
28 entries were displayed.\r"""

QTREES_INFO = """
\r
                      Vserver Name: svm1\r
                       Volume Name: svm1_root\r
                        Qtree Name: ""\r
  Actual (Non-Junction) Qtree Path: /vol/svm1_root\r
                    Security Style: ntfs\r
                       Oplock Mode: enable\r
                  Unix Permissions: -\r
                          Qtree Id: 0\r
                      Qtree Status: normal\r
                     Export Policy: default\r
        Is Export Policy Inherited: true\r
\r
                      Vserver Name: svm1\r
                       Volume Name: vol_svm1_1\r
                        Qtree Name: ""\r
  Actual (Non-Junction) Qtree Path: /vol/vol_svm1_1\r
                    Security Style: ntfs\r
                       Oplock Mode: enable\r
                  Unix Permissions: -\r
                          Qtree Id: 0\r
                      Qtree Status: normal\r
                     Export Policy: default\r
        Is Export Policy Inherited: true\r
\r
                      Vserver Name: svm1\r
                       Volume Name: vol_svm1_1\r
                        Qtree Name: qtree_svm1_1\r
  Actual (Non-Junction) Qtree Path: /vol/vol_svm1_1/qtree_svm1_1\r
                    Security Style: unix\r
                       Oplock Mode: enable\r
                  Unix Permissions: ---rwxrwxrwx\r
                          Qtree Id: 1\r
                      Qtree Status: normal\r
                     Export Policy: default\r
        Is Export Policy Inherited: true\r
\r
                      Vserver Name: svm1\r
                       Volume Name: vol_svm1_2\r
                        Qtree Name: ""\r
  Actual (Non-Junction) Qtree Path: /vol/vol_svm1_2\r
                    Security Style: ntfs\r
                       Oplock Mode: enable\r
                  Unix Permissions: -\r
                          Qtree Id: 0\r
                      Qtree Status: normal\r
                     Export Policy: default\r
        Is Export Policy Inherited: true"""

SHARES_INFO = """
\r
                            Vserver: vs1\r
                              Share: SALES_SHARE1\r
           CIFS Server NetBIOS Name: WINDATA\r
                               Path: /sales\r
                   Share Properties: oplocks\r
                                     browsable\r
                 Symlink Properties: enable\r
            File Mode Creation Mask: -\r
       Directory Mode Creation Mask: -\r
                      Share Comment: -\r
                          Share ACL: Everyone / Full Control\r
      File Attribute Cache Lifetime: -\r
                      Offline Files: manual\r
      Vscan File-Operations Profile: standard\r
      \r
                                  Vserver: vs1\r
                              Share: SALES_SHARE2\r
           CIFS Server NetBIOS Name: WINDATA\r
                               Path: /sales\r
                   Share Properties: oplocks\r
                                     browsable\r
                 Symlink Properties: enable\r
            File Mode Creation Mask: -\r
       Directory Mode Creation Mask: -\r
                      Share Comment: -\r
                          Share ACL: Everyone / Full Control\r
      File Attribute Cache Lifetime: -\r
                      Offline Files: manual\r
      Vscan File-Operations Profile: standard"""

FILE_SYSTEM_INFO = """
Filesystem              kbytes       used      avail capacity  Mounted on                 Vserver\r
/vol/vol0/              785324     678268     107056      86%  ---                        cl-01\r
/vol/vol0/.snapshot      41332     236540          0     572%  ---                        cl-01\r
/vol/svm1_root/         778240        288     777952       0%  /                          svm1\r
/vol/svm1_root/.snapshot 40960          0      40960       0%  //.snapshot                svm1\r
/vol/vol_svm1_1/       2097152       2564    2094588       0%  ---                        svm1\r
/vol/vol_svm1_1/.snapshot    0       2028          0       0%  ---                        svm1\r
/vol/vol_svm1_2/       2097152       3160    2093992       0%  ---                        svm1\r
/vol/vol_svm1_2/.snapshot    0       1816          0       0%  ---                        svm1\r
/vol/svm2_root/         778240        280     777960       0%  /                          svm2\r
/vol/svm2_root/.snapshot 40960          0      40960       0%  //.snapshot                svm2\r
/vol/vol_svm2_1/       2097152       3420    2093732       0%  ---                        svm2\r
/vol/vol_svm2_1/.snapshot    0       1912          0       0%  ---                        svm2\r
/vol/vol_svm2_2/       1048576       2960    1045616       0%  ---                        svm2\r
/vol/vol_svm2_2/.snapshot    0       1716          0       0%  ---                        svm2\r
/vol/vol_svm2_3/         19456        244      19212       1%  ---                        svm2\r
/vol/vol_svm2_3/.snapshot 1024        704        320      69%  ---                        svm2\r
/vol/vol_svm2_4/         19456        244      19212       1%  ---                        svm2\r
/vol/vol_svm2_4/.snapshot 1024        704        320      69%  ---                        svm2\r
/vol/vol_svm2_5/       1992296       1608    1990688       0%  ---                        svm2\r
/vol/vol_svm2_5/.snapshot  104856        592     104264       1%  ---                        svm2\r
20 entries were displayed\r."""

VSERVER_INFO = """
                               Admin      Operational Root\r
Vserver     Type    Subtype    State      State       Volume     Aggregate\r
----------- ------- ---------- ---------- ----------- ---------- ----------\r
cl          admin   -          -          -           -          -\r
cl-01       node    -          -          -           -          -\r
svm1        data    default    running    running     svm1_root  aggr1\r
svm2        data    default    running    running     svm2_root  aggr2\r
4 entries were displayed.\r
"""

STORAGE_POOL_LIST = [
    {'name': 'Pool1', 'storage_id': '12345', 'native_storage_pool_id': '60f2f1b9-e60f-11e3-a5e7-00a0981899a2',
     'description': '', 'status': 'normal', 'storage_type': 'block', 'subscribed_capacity': '',
     'total_capacity': 1594291860275, 'used_capacity': 395824186000, 'free_capacity': 1198467674275},
    {'name': 'Pool2', 'storage_id': '12345', 'native_storage_pool_id': '60f2f1b9-e60f-11e3-a5e7-00a0981899a1',
     'description': '', 'status': 'normal', 'storage_type': 'block', 'subscribed_capacity': '',
     'total_capacity': 1594291860275, 'used_capacity': 395824186000, 'free_capacity': 1198467674275},
    {'name': 'aggr0', 'storage_id': '12345', 'native_storage_pool_id': 'a71b1e4e-d151-4868-986a-e71d84beabf8',
     'description': '', 'status': 'offline', 'storage_type': 'block', 'subscribed_capacity': '',
     'total_capacity': 896532480, 'used_capacity': 864760627, 'free_capacity': 31771853},
    {'name': 'aggr1', 'storage_id': '12345', 'native_storage_pool_id': '68ffbbca-eb73-4eeb-86bd-1a8e19c4c415',
     'description': '', 'status': 'offline', 'storage_type': 'block', 'subscribed_capacity': '',
     'total_capacity': 9438190632, 'used_capacity': 3027951943, 'free_capacity': 6410238689},
    {'name': 'aggr2', 'storage_id': '12345', 'native_storage_pool_id': 'b5cfe36e-eaed-433b-8a25-f333aa51b553',
     'description': '', 'status': 'offline', 'storage_type': 'block', 'subscribed_capacity': '',
     'total_capacity': 9438190632, 'used_capacity': 6281389670, 'free_capacity': 3156800962}]


class TestNetAppStorageDriver(TestCase):
    SSHPool.get = mock.Mock(
        return_value={paramiko.SSHClient()})
    NetAppHandler.login = mock.Mock()
    netapp_client = NetAppFasDriver(**ACCESS_INFO)

    def test_reset_connection(self):
        kwargs = ACCESS_INFO
        NetAppHandler.login = mock.Mock()
        netapp_client = NetAppFasDriver(**kwargs)
        netapp_client.reset_connection(context, **kwargs)
        self.assertEqual(netapp_client.netapp_handler.ssh_pool.ssh_host, "192.168.159.130")
        self.assertEqual(netapp_client.netapp_handler.ssh_pool.ssh_port, 22)

    def test_get_storage_success(self):
        NetAppHandler.do_exec = mock.Mock(
            side_effect=[SYSTEM_INFO, AGGREGATE_INFO, VERSION, DISK_INFO])
        data = self.netapp_client.get_storage(context)
        self.assertEqual(data['vendor'], 'NetApp')

    def test_get_storage_failed(self):
        NetAppHandler.do_exec = mock.Mock(return_value={})
        with self.assertRaises(exception.DelfinException) as exc:
            self.netapp_client.get_storage(context)
        self.assertIn('Failed to get storage from netapp_fas fas',
                      str(exc.exception))

        with self.assertRaises(Exception) as exc:
            self.netapp_client.get_storage(context)
        self.assertIn('Failed to get storage from netapp_fas fas',
                      str(exc.exception))

    def test_list_storage_pools_success(self):
        NetAppHandler.do_exec = mock.Mock(
            side_effect=[POOLS_INFO, AGGREGATE_DETAIL_INFO])
        data = self.netapp_client.list_storage_pools(context)
        self.assertEqual(data[0]['name'], 'Pool1')

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
        NetAppHandler.do_exec = mock.Mock(return_value=VOLUMES_INFO)
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
        NetAppHandler.do_exec = mock.Mock(side_effect=[ALERT_INFO, EVENT_INFO])
        data = self.netapp_client.list_alerts(context)
        self.assertEqual(data[0]['alert_name'], 'mgmtgwd.configbr.noSNCBackup')

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
        NetAppHandler.do_exec = mock.Mock(side_effect=[CONTROLLER_INFO])
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
        SSHPool.get = mock.Mock(
            return_value={paramiko.SSHClient()})
        kwargs = ACCESS_INFO
        NetAppHandler.login = mock.Mock()
        netapp_client = NetAppFasDriver(**kwargs)
        NetAppHandler.do_exec = mock.Mock(side_effect=[PORTS_INFO, INTERFACE_INFO])
        data = netapp_client.list_ports(context)
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
        NetAppHandler.do_exec = mock.Mock(side_effect=[DISKS_INFO, PHYSICAL_INFO])
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
        NetAppHandler.do_exec = mock.Mock(side_effect=[QTREES_INFO])
        data = self.netapp_client.list_qtrees(context)
        self.assertEqual(data[0]['security_mode'], 'ntfs')

    def test_list_qtrees_failed(self):
        NetAppHandler.do_exec = mock.Mock(return_value={})
        NetAppHandler.get_storage = mock.Mock(return_value=STORAGE_POOL_LIST)
        with self.assertRaises(exception.DelfinException) as exc:
            self.netapp_client.list_qtrees(context)
        self.assertIn('Failed to get storage',
                      str(exc.exception))

        with self.assertRaises(Exception) as exc:
            self.netapp_client.list_qtrees(context)
        self.assertIn('Failed to get storage',
                      str(exc.exception))

    def test_list_shares_success(self):
        NetAppHandler.do_exec = mock.Mock(side_effect=[SHARES_INFO])
        data = self.netapp_client.list_shares(context)
        self.assertEqual(data[0]['name'], 'SALES_SHARE1')

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
        NetAppHandler.do_exec = mock.Mock(side_effect=[FILE_SYSTEM_INFO, VSERVER_INFO])
        NetAppHandler.list_storage_pools = mock.Mock(return_value=STORAGE_POOL_LIST)
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
