ALERT_TEMPLATE = \
    {
        'AUSOTriggerFailed_Alert':
            {'severityofAlert': 'Major',
             'probableCause': 'Out_of_service',
             'description': '$(mcc_nhm_auso_info.auso-trigger-state-descr).',
             'PossibleEffect': 'Loss of DR protection.',
             'CorrectiveActions': 'Refer to the MetroCluster(tm) Disaster Rec'
                                  'overy Guide if the partner node is down.'},
        'AllPathToOneEndOfStack_Alert':
            {'severityofAlert': 'Major',
             'probableCause': 'Cable_tamper',
             'description': 'Controller $(LOCALHOST) is connected to only one'
                            ' end of stack $(storage_node_stack.stack-id) thr'
                            'ough disk shelf $(storage_node_stack.ioma-end-sh'
                            'elf).',
             'PossibleEffect': 'A single disk shelf failure within stack $(s'
                               'torage_node_stack.stack-id) might cause con'
                               'troller $(LOCALHOST) to lose access to mult'
                               'iple shelves in the stack.',
             'CorrectiveActions': '1. Consult the guide applicable to your '
                                  '$(storage_node_stack.module-type) disk s'
                                  'helf to review cabling rules and complete'
                                  ' the SAS cabling worksheet for your syst'
                                  'em.2. Connect controller $(LOCALHOST) to '
                                  'the first and last disk shelves of stack'
                                  ' $(storage_node_stack.stack-id).3. Verify'
                                  ' that controller $(LOCALHOST) is cabled'
                                  ' to IOM A and IOM B of stack $(storage_'
                                  'node_stack.stack-id).4. Contact support '
                                  'personnel if the alert persists.'},
        'DegradedShelfToShelfCabling_Alert':
            {'severityofAlert': 'Major',
             'probableCause': 'Cable_tamper',
             'description': 'Disk shelf $(storage_node_shelf.shelf) is conn'
                            'ected only through $(storage_node_shelf.ioma-'
                            'cabling-count) paths on IOM A and $(storage_node'
                            '_shelf.iomb-cabling-count) paths on IOM B to a'
                            'djacent disk shelves. Because controller $(LOCA'
                            'LHOST) is connected to stack $(storage_node_sh'
                            'elf.stack-id) through a quad-path configuration'
                            ', disk shelf $(storage_node_shelf.shelf) must b'
                            'e connected with double-wide cabling to adjacen'
                            't disk shelves.',
             'PossibleEffect': 'Inconsistent cabling might cause degraded '
                               'performance.',
             'CorrectiveActions': '1. Consult the guide applicable to your '
                                  '$(storage_node_shelf.module-type) disk she'
                                  'lf to review cabling rules and complete t'
                                  'he SAS cabling worksheet for your system.'
                                  '2. Connect disk shelf $(storage_node_shel'
                                  'f.shelf) to the adjacent disk shelf with '
                                  'double-wide cabling.3. Contact support '
                                  'personnel if the alert persists.'},
        'DisabledInuseSASPort_Alert':
            {'severityofAlert': 'Major',
             'probableCause': 'Cable_tamper',
             'description': 'SAS $(storage_node_port.port) port is disabled'
                            '. This might occur if the port has been admin'
                            'istratively disabled or the attached cable '
                            'is faulty.',
             'PossibleEffect': 'Controller $(LOCALHOST) might lose a path '
                               'to storage devices connected behind port '
                               '$(storage_node_port.port).',
             'CorrectiveActions': '1. Verify that the physical cable conn'
                                  'ection is secure and operational, and '
                                  'replace the cable, if necessary.2. Ver'
                                  'ify that SAS port $(storage_node_port.'
                                  'port) is online and enabled.3. If the '
                                  'SAS port $(storage_node_port.port) is '
                                  'connected to disk shelves, verify that'
                                  ' IOMs and disks are properly seated.'},
        'HaNotReadyCifsNdo_Alert':
            {'severityofAlert': 'Major',
             'probableCause': 'Configuration_error',
             'description': 'One or more files hosted by a volume in an '
                            'aggregate on node "$(cifs_ndo_node_resource.'
                            'node)" have been opened through a continuous'
                            'ly available CIFS share with the promise of '
                            'persistence in the event of a failure. Howe'
                            'ver, the HA relationship with the partner '
                            'is either not configured or not healthy.',
             'PossibleEffect': 'In the event that "$(cifs_ndo_node_resou'
                               'rce.node)" fails, its aggregates will be'
                               'come unavailable and open file state wil'
                               'l be lost, which will prevent CIFS clien'
                               'ts from recovering persistent open files'
                               ' and may result in a disruption to the '
                               'associated client applications.',
             'CorrectiveActions': 'This alert will persist while a node '
                                  'is in takeover state. If that is the '
                                  'case, issue a giveback to return the'
                                  ' aggregates to the partner once it is '
                                  'ready to accept them. Otherwise, verify'
                                  ' that there is a properly configured and'
                                  ' enabled HA relationship between "$(cifs'
                                  '_ndo_node_resource.node)" and its partner.'
                                  ' Alternatively volumes can be moved to a'
                                  'n aggregate on a node that is part of '
                                  'an operable HA pair.'},
        'IOM12ToIOM6SquarePortConnection_Alert':
            {'severityofAlert': 'Major',
             'probableCause': 'Cable_tamper',
             'description': 'Shelf-to-shelf connection between disk shelves'
                            ' $(storage_node_shelf_connector.shelf) and $(s'
                            'torage_node_shelf_connector.remote-shelf) have '
                            'IOM12E port cabled to IOM6 square port.',
             'PossibleEffect': 'Connection between disk shelves $(storage_'
                               'node_shelf_connector.shelf) and $(storage_'
                               'node_shelf_connector.remote-shelf) might '
                               'be inactive and cause controller $(LOCALHOST)'
                               ' to lose connectivity to the disk shelves.',
             'CorrectiveActions': '1. Consult the guide applicable to your '
                                  '$(storage_node_shelf_connector.module-ty'
                                  'pe) disk shelf to review cabling rules a'
                                  'nd complete the SAS cabling worksheet fo'
                                  'r your system.2. Connect IOM12E disk she'
                                  'lf port to IOM6 disk shelf circle port.3'
                                  '. Contact support personnel if the alert'
                                  ' persists.'},
        'InterconnectAdapterOfflineAlert':
            {'severityofAlert': 'Major',
             'probableCause': 'Cable_tamper',
             'description': 'Physical link on port $(mcc_nhm_fcvi_adapter.p'
                            'ort-no) is offline.',
             'PossibleEffect': 'DR protection of NVRAM mirror might be comp'
                               'romised.',
             'CorrectiveActions': '1. Ensure that the FC-VI link has not be'
                                  'en tampered with.2. Verify that the phys'
                                  'ical status of the FC-VI adapter is "Up"'
                                  ' by using the command "metrocluster inte'
                                  'rconnect adapter show".3. If the configu'
                                  'ration includes fabric switches, ensure t'
                                  'hat they are properly cabled and configur'
                                  'ed.'},
        'MixOfIOMAandIOMBConnection_Alert': {
            'severityofAlert': 'Major',
            'probableCause': 'Cable_tamper',
            'description': 'Mixed IOM A and IOM B connection between disk s'
                           'helves $(storage_node_shelf_connector.shelf) a'
                           'nd $(storage_node_shelf_connector.remote-shelf).',
            'PossibleEffect': 'Commands sent from the controller to all IO'
                              'M A or IOM B domain might cause unintended'
                              ' results.',
            'CorrectiveActions': '1. Consult the guide applicable to your '
                                 '$(storage_node_shelf_connector.module-typ'
                                 'e) disk shelf to review cabling rules and '
                                 'complete the SAS cabling worksheet for your'
                                 ' system.2. Connect IOM A of disk shelf '
                                 '$(storage_node_shelf_connector.shelf) to'
                                 ' IOM A of disk shelf $(storage_node_'
                                 'shelf_connector.remote-shelf).3. Connect '
                                 'IOM B of disk shelf $(storage_node_shelf_'
                                 'connector.shelf) to IOM B of disk shelf '
                                 '$(storage_node_shelf_connector.remote-shel'
                                 'f).4. Contact support personnel if the ale'
                                 'rt persists.'},
        'NchmTwoNodeMccAUSODisabled_Alert': {
            'severityofAlert': 'Major',
            'probableCause': 'Out_of_service',
            'description': '$(LOCALHOST) has automatic switchover disabled.',
            'PossibleEffect': "On a controller fault it's disaster-recovery "
                              "(DR) partner will not trigger an automatic "
                              "switchover to ensure Non-disruptive Operation."
                              "",
            'CorrectiveActions': 'Use "metrocluster modify -node-name $(LOCA'
                                 'LHOST) -automatic-switchover-onfailure tr'
                                 'ue" to enable automatic switchover.'},
        'NoPathToIOMA_Alert': {
            'severityofAlert': 'Major',
            'probableCause': 'Cable_tamper',
            'description': 'Controller $(LOCALHOST) is connected only to IOM '
                           'B of stack $(storage_node_stack.stack-id) through '
                           '$(storage_node_stack.initiator) ports.',
            'PossibleEffect': 'Access to disk shelves within stack $(storage_'
                              'node_stack.stack-id) might be lost with a sing'
                              'le IOM B failure or a shelf-to-shelf connect'
                              'ion cable failure.',
            'CorrectiveActions': '1. Consult the guide applicable to your $(s'
                                 'torage_node_stack.module-type) disk shelf '
                                 'to review cabling rules and complete the S'
                                 'AS cabling worksheet for your system.2. Co'
                                 'nnect controller $(LOCALHOST) to IOM A and'
                                 ' IOM B of stack $(storage_node_stack.stac'
                                 'k-id) using either a multipath or quad-pa'
                                 'th configuration.3. Contact support perso'
                                 'nnel if the alert persists.'},
        'NoPathToIOMB_Alert': {
            'severityofAlert': 'Major',
            'probableCause': 'Cable_tamper',
            'description': 'Controller $(LOCALHOST) is connected only to IOM'
                           'A of stack $(storage_node_stack.stack-id) through'
                           '$(storage_node_stack.initiator) ports.',
            'PossibleEffect': 'Access to disk shelves within stack $(storage_'
                              'node_stack.stack-id) might be lost with a fail'
                              'ure of a single IOM A or a shelf-to-shelf conn'
                              'ection cable failure.',
            'CorrectiveActions': '1. Consult the guide applicable to your $(s'
                                 'torage_node_stack.module-type disk shelf to'
                                 ' review cabling rules and complete the SAS '
                                 'cabling worksheet for your system.2 Connect'
                                 ' controller $(LOCALHOST) to IOM A and IOM B'
                                 'of stack $(storage_node_stack.stack-id) usi'
                                 'ng  either a multipath or quad-path '
                                 'configuration.3. Contact support personnel '
                                 'if the alert persists.'},
        'NoStandbyLifCifsNdo_Alert': {
            'severityofAlert': 'Minor',
            'probableCause': 'Configuration_error',
            'description': 'Vserver "$(cifs_ndo_node_vserver_resource.vserver'
                           ')" is actively serving data over CIFS through no'
                           'de "$(cifs_ndo_node_vserver_resource.node)", an'
                           'd there are CIFS files opened persistently over'
                           ' continuously available shares. However, its par'
                           'tner node "$(cifs_ndo_node_vserver_resource.par'
                           'tner)" is not exposing any active data L'
                           'IFs for the Vserver.',
            'PossibleEffect': 'In the event that node "$(cifs_ndo_node_vs'
                              'erver_resource.node)" fails, node "$(cifs_'
                              'ndo_node_vserver_resource.partner)" will '
                              'witness the condition very quickly. If a d'
                              'ata LIF for Vserver "$(cifs_ndo_node_vserve'
                              'r_resource.vserver)" existed on node "$(cif'
                              's_ndo_node_vserver_resource.partner)", tha'
                              't node would have the capability to bring '
                              'active connections away from node "$(cifs_'
                              'ndo_node_vserver_resource.node)" non-disru'
                              'ptively and faster than waiting for the da'
                              'ta LIF to fail over and the client to reco'
                              'ver on its own.',
            'CorrectiveActions': 'Create a data LIF on node "$(cifs_ndo_n'
                                 'ode_vserver_resource.partner)" for Vserv'
                                 'er "$(cifs_ndo_node_vserver_resource.vse'
                                 'rver)", or move an existing one to tha'
                                 't node.'},
        'SinglePathToDiskShelf_Alert': {
            'severityofAlert': 'Major',
            'probableCause': 'Cable_tamper',
            'description': 'Controller $(LOCALHOST) has only a single-pa'
                           'th configuration to disk shelf $(storage_nod'
                           'e_shelf.shelf). This might occur when the co'
                           'ntroller does not have dual-path configurati'
                           'on to stack $(storage_node_shelf.stack-id), a'
                           ' SAS HBA port on the controller connected to '
                           'the disk shelf is disabled, or shelf-to-shel'
                           'f cabling is incorrect.',
            'PossibleEffect': 'Access to disk shelf $(storage_node_shelf'
                              '.shelf) via controller $(LOCALHOST) might '
                              'be lost with a failure of controller $(st'
                              'orage_node_shelf.initiator) port, a singl'
                              'e shelf-to-shelf cable or a single disk '
                              'shelf IOM.',
            'CorrectiveActions': '1. Consult the guide applicable to you'
                                 'r $(storage_node_shelf.module-type) di'
                                 'sk shelf to review cabling rules and c'
                                 'omplete the SAS cabling worksheet for '
                                 'your system.2. Connect controller $(LO'
                                 'CALHOST) to the first and last disk sh'
                                 'elf of stack $(storage_node_shelf.stac'
                                 'k-id) using active SAS HBA ports.3. Ve'
                                 'rify that controller $(LOCALHOST) is c'
                                 'abled to IOM A at one end and IOM B at '
                                 'another end of stack $(storage_node_shel'
                                 'f.stack-id).4. If disk shelf $(storage_n'
                                 'ode_shelf.shelf) is located between two'
                                 ' disk shelves within stack $(storage_no'
                                 'de_shelf.stack-id), verify that IOM A a'
                                 'nd IOM B are properly cabled to their i'
                                 'ndependent domains.5. Contact support p'
                                 'ersonnel if the alert persists.'},
        'SinglePathToDisk_Alert': {
            'severityofAlert': 'Major',
            'probableCause': 'Cable_tamper',
            'description': 'Disk $(storage_node_disk.disk-name) does not ha'
                           've two paths to controller $(LOCALHOST) but the'
                           ' containing disk shelf $(storage_node_disk.shel'
                           'f) does have two paths. Disk $(storage_node_dis'
                           'k.disk-name) might be faulty.',
            'PossibleEffect': 'Access to disk $(storage_node_disk.disk-name'
                              ') via controller $(LOCALHOST) will be lost w'
                              'ith a single hardware component failure (e.g'
                              '. cable, HBA, or IOM failure).',
            'CorrectiveActions': '1. Reseat disk $(storage_node_disk.disk-n'
                                 'ame) following the rules in the Installat'
                                 'ion and Service Guide.2. Wait six minutes'
                                 ' for the alert condition to clear.3. If '
                                 'reseating disk $(storage_node_disk.disk-n'
                                 'ame) fails to clear the alert condition, '
                                 'replace disk $(storage_node_disk.disk-name'
                                 ').4. Wait six minutes for the alert condi'
                                 'tion to clear.5. Contact support personne'
                                 'l if the alert persists.'},
        'SqrToSqrOrCirToCirPortConnection_Alert': {
            'severityofAlert': 'Major',
            'probableCause': 'Cable_tamper',
            'description': 'Shelf-to-shelf connection between disk shelves'
                           ' $(storage_node_shelf_connector.shelf) and $(s'
                           'torage_node_shelf_connector.remote-shelf) have'
                           ' $(storage_node_shelf_connector.module-type) s'
                           'quare to square ports or circle to circle port'
                           's cabled together.',
            'PossibleEffect': 'Connection between disk shelves $(storage_n'
                              'ode_shelf_connector.shelf) and $(storage_no'
                              'de_shelf_connector.remote-shelf) might be i'
                              'nactive and cause controller $(LOCALHOST) t'
                              'o lose connectivity to the shelves.',
            'CorrectiveActions': '1. Consult the guide applicable to your '
                                 '$(storage_node_shelf_connector.module-ty'
                                 'pe) disk shelf to review cabling rules a'
                                 'nd complete the SAS cabling worksheet for'
                                 ' your system.2. Connect disk shelf $(sto'
                                 'rage_node_shelf_connector.shelf) square '
                                 'port to disk shelf $(storage_node_shelf'
                                 '_connector.remote-shelf) circle port.3.'
                                 ' Verify that IOM A of disk shelf $(stor'
                                 'age_node_shelf_connector.shelf) is conn'
                                 'ected to IOM A of disk shelf $(storage_'
                                 'node_shelf_connector.remote-shelf).4. V'
                                 'erify that IOM B of disk shelf $(storag'
                                 'e_node_shelf_connector.shelf) is connect'
                                 'ed to IOM B of disk shelf $(storage_nod'
                                 'e_shelf_connector.remote-shelf).5. Cont'
                                 'act support personnel if the alert pers'
                                 'ists.'},
        'StorageFCAdapterFault_Alert': {
            'severityofAlert': 'Major',
            'probableCause': 'Cable_tamper',
            'description': 'FC initiator adapter $(mcc_nhm_storage_fc_ada'
                           'pter.name) is at fault.',
            'PossibleEffect': 'Resiliency of backend storage is compromis'
                              'ed.',
            'CorrectiveActions': '1. Ensure that the FC initiator link ha'
                                 's not been tampered with.2. Verify the '
                                 'operational status of the FC initiator'
                                 ' adapter by using the command "system '
                                 'node run -node local -command storage'
                                 ' show adapter".'},
        'ThreePathToStack_Alert': {
            'severityofAlert': 'Major',
            'probableCause': 'Cable_tamper',
            'description': 'Controller $(LOCALHOST) has only $(storage_no'
                           'de_stack.path-count) paths to stack $(storage'
                           '_node_stack.stack-id).',
            'PossibleEffect': 'Only multipath or quad-path configurations'
                              ' are supported for IOM12 stacks.',
            'CorrectiveActions': '1. Consult the guide applicable to your'
                                 ' $(storage_node_stack.module-type) disk'
                                 ' shelf to review cabling rules and comp'
                                 'lete the SAS cabling worksheet for your'
                                 ' system.2. Connect controller $(LOCALHO'
                                 'ST) to stack $(storage_node_stack.stack-'
                                 'id) using a multipath or quad-path config'
                                 'uration.3. Contact support personnel if '
                                 'the alert persists.'},
        'UnsupportedMixOfIOM12andIOM6Shelves_Alert': {
            'severityofAlert': 'Major',
            'probableCause': 'Cable_tamper',
            'description': 'Cabling together disk shelves $(storage_node_'
                           'shelf_connector.shelf) of $(storage_node_shelf'
                           '_connector.module-type) and $(storage_node_she'
                           'lf_connector.remote-shelf) of $(storage_node_'
                           'shelf_connector.remote-module-type) is not su'
                           'pported.',
            'PossibleEffect': 'Devices might not be accessible by the cont'
                              'roller.',
            'CorrectiveActions': '1. Consult the guide applicable to your '
                                 '$(storage_node_shelf_connector.module-type) disk shelf to revi'
                                 'ew cabling rules and complete the SAS cab'
                                 'ling worksheet for your system.2. Connect'
                                 ' disk shelf $(storage_node_shelf_connector'
                                 '.shelf) only to other $(storage_node_shelf'
                                 '_connector.module-type) disk shelves in a '
                                 'stack.3. Connect disk shelf $(storage_node'
                                 '_shelf_connector.remote-shelf) only to ot'
                                 'her $(storage_node_shelf_connector.remote'
                                 '-module-type) disk shelves in a separate'
                                 ' stack.4. Contact support personnel if th'
                                 'e alert persists.'},
        'BootMediaMissingAlert': {
            'severityofAlert': 'Minor',
            'probableCause': 'Configuration_error',
            'description': 'Node"$(nphm_boot_media_count.display-name)" sup'
                           'ports 2 boot media devices, but less than 2 boo'
                           't media devices have been detected.',
            'PossibleEffect': 'Boot media is not currently redundant.',
            'CorrectiveActions': '1. Halt the node. 2. Verify that both b'
                                 'oot media devices are present and reseat them.3. Reboot the nod'
                                 'e.4. If the problem persists, contact techn'
                                 'ical support for further assistance.'},
        'BootmediaReplaceAlert': {
            'severityofAlert': 'Critical',
            'probableCause': 'hardware_degrading',
            'description': 'Bad sector count in the boot media has reached c'
                           'ritical level.',
            'PossibleEffect': 'Upgrading, downgrading, reverting, or applyin'
                              'g patches to Data ONTAP can damage the boot d'
                              'evice. If the boot device is damaged, the sto'
                              'rage system will not boot.',
            'CorrectiveActions': '1. Contact technical support to obtain a n'
                                 'ew boot device.2. If possible, perform a ta'
                                 'keover of this node and bring the node down'
                                 ' for maintenance.3. Refer to the "Boot medi'
                                 'a replacement guide for your given hardware'
                                 ' platform" to replace the boot device.4. Up'
                                 'date the boot device with the appropriate'
                                 ' Da'
                                 'ta ONTAP version. 5. Bring the storage syst'
                                 'em online.'},
        'BootmediaWarnAlert': {
            'severityofAlert': 'Major',
            'probableCause': 'hardware_degrading',
            'description': 'Boot device is wearing out due to write operatio'
                           'ns in the form of regular updates.',
            'PossibleEffect': 'Upgrading, downgrading, reverting, or applyi'
                              'ng patches to Data ONTAP can cause addition'
                              'al wear to the boot device. The boot device'
                              ' might enter critical condition due to the '
                              'additional wear.',
            'CorrectiveActions': '1. Contact technical support to obtain '
                                 'a new boot device.2. If possible, perfo'
                                 'rm a takeover of this node and bring th'
                                 'e node down for maintenance.3. Refer to'
                                 ' the "Boot media replacement guide for '
                                 'your given hardware platform" to replac'
                                 'e the boot device.4. Update the boot de'
                                 'vice with the appropriate Data ONTAP ver'
                                 'sion. 5. Bring the storage system online.'},
        'CriticalCECCCountMemErrAlert': {
            'severityofAlert': 'Critical',
            'probableCause': 'DIMM_Degraded',
            'description': 'The DIMM has degraded, leading to memory error'
                           's.',
            'PossibleEffect': 'Memory issues can lead to a catastrophic sy'
                              'stem panic, which can lead to data downtim'
                              'e on the node.',
            'CorrectiveActions': '1. Contact technical support to obtain '
                                 'a new DIMM of the same specification.2.'
                                 ' If possible, perform a takeover of this'
                                 ' node and bring the node down for maint'
                                 'enance.3. Refer to the DIMM replacement'
                                 ' guide for your given hardware platform'
                                 ' to replace the DIMM.4. Bring the stora'
                                 'ge system online.'},
        'IOXMBadPowerSignalAlert': {
            'severityofAlert': 'Major',
            'probableCause': 'hardware_degradation',
            'description': 'One or more power rails on the I/O expansion'
                           ' module (IOXM) deteriorated.',
            'PossibleEffect': 'Devices on the IOXM might not work when th'
                              'e IOXM is in degraded mode.',
            'CorrectiveActions': '1. Contact technical support to get new'
                                 ' IOXM that is compatible with your plat'
                                 'form.2. If possible, perform a takeove'
                                 'r of this node and bring the node down'
                                 ' for maintenance.3. Replace the IOXM. '
                                 'Refer to the Hardware specification g'
                                 'uide for more information on the posi'
                                 'tion of the FRU and ways to check or '
                                 'replace it.4. Bring the storage system'
                                 ' online.5. If the problem persists, c'
                                 'ontact technical support to get the c'
                                 'hassis replaced.'},
        'NodeClusFlapWarnAlert': {
            'severityofAlert': 'Major',
            'probableCause': 'Threshold_crossed',
            'description': 'The number of link flapping errors on port "$('
                           'nphm_clus_flaps_info.display-name)" is above  '
                           'the warning threshold of "$(nphm_clus_flaps_'
                           'info.threshold)" for the polling period.',
            'PossibleEffect': 'Communication from this node to the cluster '
                              'might be degraded.',
            'CorrectiveActions': '1) Migrate any cluster LIF that uses '
                                 'this link to another port connected '
                                 'to a cluster switch by using the '
                                 '"network interface migrate" command . 2) '
                                 'Replace the network cable with a  '
                                 'known-good cable.If errors are  '
                                 'corrected,  stop. No further action is '
                                 'required.Otherwise,  continue to Step '
                                 '3.3) Move the network cable  to another '
                                 'available port on the cluster switch(if '
                                 'available).If errors are corrected, '
                                 'stop. Contact technical support to '
                                 'troubleshoot the original switch port. '
                                 'Otherwise, continue to Step 4.4) If '
                                 'available, configure another port on '
                                 'the node for the cluster broadcast '
                                 'domain.Move the network cable to '
                                 'another available cluster switch '
                                 'port.Migrate the cluster LIF back to '
                                 'the original port.If errors are '
                                 'corrected, contact technical support to '
                                 'troubleshoot the original node port.If '
                                 'errors persist, contact technical '
                                 'support for further assistance.'},
    'NodeIfInErrorsWarnAlert': {
            'severityofAlert': 'Major',
            'probableCause': 'Threshold_crossed',
            'description': 'The percentage of inbound packet errors of'
                           ' node "$(nphm_node_analytics_info.device)" on '
                           'interface "$('
                           'nphm_node_analytics_info.interface-name)" is '
                           'above the warning threshold.',
            'PossibleEffect': 'Communication from this node to the cluster '
                              'might be degraded',
            'CorrectiveActions': '1) Migrate any cluster LIF that uses this '
                                 'connection to another port connected to '
                                 'a cluster switch.  For example, '
                                 'if cluster LIF "clus1" is on port e0a '
                                 'and the other LIF is on e0b, run the '
                                 'following command to move "clus1" to '
                                 'e0b: "network interface migrate '
                                 '-vserver vs1 -lif clus1 -sourcenode '
                                 'node1 -destnode node1 -dest-port e0b"2) '
                                 'Replace the network cable with a '
                                 'known-good cable.If errors are '
                                 'corrected, stop. No further action is '
                                 'required.Otherwise, continue to Step '
                                 '3.3) Move the network cable to another '
                                 'port on the node (if available).Migrate '
                                 'the cluster LIF to the new port.If '
                                 'errors are corrected, contact technical '
                                 'support to troubleshoot the original '
                                 'node port. Otherwise, continue to Step '
                                 '4.4) Move the network cable to another '
                                 'available cluster switch port.Migrate '
                                 'the cluster LIF back to the original '
                                 'port.If errors are corrected, contact '
                                 'technical support to troubleshoot the '
                                 'original switch port.If errors persist, '
                                 'contact technical support for further '
                                 'assistance.'},
        'NodeIfOutErrorsWarnAlert': {
            'severityofAlert': 'Major',
            'probableCause': 'Threshold_crossed',
            'description': 'The percentage of outbound packet errors of '
                           'node "$(nphm_node_analytics_info.device)" on interface '
                           '"$(nphm_node_analytics_info.interface-name)" '
                           'is above the warning threshold.',
            'PossibleEffect': 'Communication from this node to the cluster '
                              'might be degraded',
            'CorrectiveActions': '1) Migrate any cluster LIF that uses this '
                                 'connection to another port connected to a '
                                 'cluster switch.  For example, if cluster LIF '
                                 '"clus1" is on port e0a and the other '
                                 'LIF is on e0b, run the following '
                                 'command to move "clus1" to e0b: '
                                 '"network interface migrate -vserver vs1 '
                                 '-lif clus1 -sourcenode node1 -destnode '
                                 'node1 -dest-port e0b"2) Replace the '
                                 'network cable with a known-good '
                                 'cable.If errors are corrected, stop. No '
                                 'further action is required.Otherwise, '
                                 'continue to Step 3.3) Move the network '
                                 'cable to another port on the node (if '
                                 'available).Migrate the cluster LIF to '
                                 'the new port.If errors are corrected, '
                                 'contact technical support to '
                                 'troubleshoot the original node port. '
                                 'Otherwise, continue to Step 4.4) Move '
                                 'the network cable to another available '
                                 'cluster switch port.Migrate the cluster '
                                 'LIF back to the original port.If errors '
                                 'are corrected, contact technical '
                                 'support to troubleshoot the original '
                                 'switch port.If errors persist, contact '
                                 'technical support for further '
                                 'assistance.'},
        'NvramBadBlocksAlert': {
            'severityofAlert': 'Major',
            'probableCause': 'hardware_degrading',
            'description': 'The number of bad block errors on NVRAM module'
                           '  "$(nphm_nvram_fru.display-name)" is above  '
                           'the warning threshold of "$('
                           'nphm_nvram_bb_threshold.nvram-bb-threshold)".',
            'PossibleEffect': 'Potential data loss as the NVRAM becomes '
                              'degraded.',
            'CorrectiveActions': 'Contact technical support for assistance '
                                 'with NVRAM module replacement.'},
        'PCIeLaneErrorAlert': {
            'severityofAlert': 'Minor',
            'probableCause': 'Threshold_crossed',
            'description': 'One or more PCIe lanes for the device"$(nphm_io_'
                           'pcie_lane.location)" in slot "$('
                           'nphm_io_pcie_lane.slot)"are not operating '
                           'correctly.',
            'PossibleEffect': 'Functionality or performance of this device'
                              ' might be degraded.',
            'CorrectiveActions': 'Contact technical support for further'
                                 ' assistance.'},
        'PCIeRxErrorAlert': {
            'severityofAlert': 'Critical',
            'probableCause': 'hardware_degradation',
            'description': '1. The link between the PCIE endpoint and its'
                           ' root port is degraded.2. A physical layer '
                           'device (PHY) in the PCIe endpoint is no longer '
                           'working.3. A physical layer device (PHY) in '
                           'the switch to which the device in the PCIe '
                           'slot is connected is no longer working.',
            'PossibleEffect': 'The device connected to the PCIe slot will'
                              ' not function properly.',
            'CorrectiveActions': 'Contact technical support for assistance'
                                 ' in determining whether an I/O card or '
                                 'PCM replacement is required.'},
        'SPAutoUpgradeFailedMajorAlert': {
            'severityofAlert': 'Major',
            'probableCause': 'Configuration_error',
            'description': 'A Service Processor automatic firmware update'
                           ' failure was detected, which can result in '
                           'Service Processor not being updated to the '
                           'latest available compatible firmware package.',
            'PossibleEffect': 'Suboptimal system behavior can result from'
                              ' Service Processor not being updated to the '
                              'latest available compatible firmware package.',
            'CorrectiveActions': '1. Use the "system service-processor '
                                 'image show" command to display the '
                                 'firmware version that SP is currently '
                                 'booted from.2. Manually upgrade Service '
                                 'Processor by using the "system '
                                 'service-processor image update" '
                                 'command.3. Allow sufficient time for the '
                                 'system to update Service Processor '
                                 'firmware to the specified SP firmware '
                                 'package.4. Contact the technical support '
                                 'if the alert persists.'},
        'SPLinkDownAlert': {
            'severityofAlert': 'Major',
            'probableCause': 'Connection_establishment_error',
            'description': 'Service Processor in node $(LOCALHOST) has no'
                           ' network connectivity.The cable between the '
                           'Wrench port on the controller and the ethernet '
                           'switch is disconnected.',
            'PossibleEffect': 'You might not be able to use the Service '
                              'Processor to remotely access, monitor, '
                              'and troubleshoot your storage system.',
            'CorrectiveActions': '1. Check the connection between the Wrench'
                                 ' port and the ethernet switch.2. If the '
                                 'cable is properly connected, ensure that '
                                 'the Service Processor\'s ethernet '
                                 'interface is configured properly by '
                                 'executing the command "system '
                                 'service-processor network show".3. Check '
                                 'for network cable related issues. 4. '
                                 'Contact the technical support if the '
                                 'alert persists.'},
        'SPNewVersionAvailableAlert': {
            'severityofAlert': 'Major',
            'probableCause': 'Configuration_error',
            'description': 'A Service Processor on node $(LOCALHOST) is not '
                           'booted from the latest locally available '
                           'firmware package. A new compatible SP firmware '
                           'package is available.',
            'PossibleEffect': 'Suboptimal system behavior can result from'
                              ' Service Processor not being updated to the '
                              'latest available compatible firmware package.',
            'CorrectiveActions': '"system service-processor image modify'
                                 ' -node $(LOCALHOST) -autoupdate true".2. '
                                 'If SP auto-update must remain disabled ('
                                 'not recommended), download the latest '
                                 'compatible SP firmware package from the '
                                 'Support Site and trigger SP update using '
                                 'the "system service-processor image '
                                 'update" command.3. Use the "system '
                                 'service-processor image show" command to '
                                 'display the firmware version that SP is '
                                 'currently booted from.4. Allow '
                                 'sufficient time (up to 1 hour) for the '
                                 'system to update Service Processor '
                                 'firmware to the specified SP firmware '
                                 'package.5. Contact the technical support '
                                 'if the alert persists.'},
        'SPNotConfiguredAlert': {
            'severityofAlert': 'Major',
            'probableCause': 'Configuration_error',
            'description': 'Service Processor is not properly configured.',
            'PossibleEffect': 'You might not be able to use the Service'
                              ' Processor to remotely access, monitor, '
                              'and troubleshoot your storage system.',
            'CorrectiveActions': '1. Use the "system service-processor'
                                 ' network modify" command to configure '
                                 'the network interface of the Service '
                                 'Processor. 2. Use the "system '
                                 'service-processor image modify -node $('
                                 'LOCALHOST) -autoupdate true" to '
                                 'configure AutoUpdate feature of the '
                                 'Service Processor.3. Contact the '
                                 'technical support if the alert persists.'},
        'ClusterSeveredAllLinksAlert': {
            'severityofAlert': 'Major',
            'probableCause': 'Out_of_service',
            'description': 'FCVI adapters and intercluster LIFs have broken'
                           ' connections to the peered cluster or the '
                           'peered cluster is down.',
            'PossibleEffect': 'NVRAM mirroring to the peered cluster is '
                              'compromised and replication of '
                              'configuration between the clusters might stop.',
            'CorrectiveActions': '1) Ensure that the intercluster LIFs '
                                 'are up and running. Repair the '
                                 'intercluster LIFs if they are down.2) '
                                 'Verify that the peered cluster is up and '
                                 'running by using the command "cluster '
                                 'peer ping". Refer to the MetroCluster '
                                 'Disaster Recovery Guide if the peered '
                                 'cluster is down. 3) For fabric '
                                 'MetroCluster, verify that the backend '
                                 'fabric ISLs are up and running. Repair '
                                 'the backend fabric ISLs if they are '
                                 'down. 4) For non-fabric Metrocluster, '
                                 'verify that the cabling is correct '
                                 'between the FCVI adapters. Reconfigure '
                                 'the cabling if the links are down.'},
        'DualControllerHa_Alert': {
            'severityofAlert': 'Major',
            'probableCause': 'Configuration_error',
            'description': 'Disk shelf $(sschm_shelf_info.id) is not conne'
                           'cted to both controllers of the HA pair ($('
                           'sschm_node_info.owner-node), '
                           '$(sschm_node_info.ha-node)).',
            'PossibleEffect': 'Access to disk shelf $(sschm_shelf_info.id) '
                              'will be lost with a single controller '
                              'failure.',
            'CorrectiveActions': '1. Halt all controllers that are connected '
                                 'to disk shelf $(sschm_shelf_info.id).2.'
                                 ' Connect disk shelf $(sschm_shelf_info.'
                                 'id) to both HA controllers following the'
                                 ' rules in the Universal SAS and ACP '
                                 'Cabling Guide.3. Reboot the halted '
                                 'controllers.4. Contact support personnel '
                                 'if the alert persists.'},
        'DualControllerNonHa_Alert': {
            'severityofAlert': 'Major',
            'probableCause': 'Configuration_error',
            'description': 'Disk shelf $(sschm_shelf_info.id) is connected '
                           'to two controllers ($('
                           'sschm_shelf_info.connected-nodes)) that are '
                           'not an HA pair.',
            'PossibleEffect': 'Access to disk shelf $(sschm_shelf_info.id)'
                              ' may be lost with a single controller '
                              'failure.',
            'CorrectiveActions': '1. Halt all controllers that are connected'
                                 ' to disk shelf $(sschm_shelf_info.id).2. '
                                 'Connect disk shelf $('
                                 'sschm_shelf_info.id) to both HA '
                                 'controllers following the rules in the '
                                 'Universal SAS and ACP Cabling Guide.3. '
                                 'Reboot the halted controllers.4. Contact '
                                 'support personnel if the alert persists.'},
        'FabricSwitchFanFail_Alert': {
            'severityofAlert': 'Major',
            'probableCause': 'Fan_failure',
            'description': 'The fan "$(fhm_switch_errors.switch-component-'
                           'name)" on switch "$('
                           'fhm_switch_errors.switch-name)" has failed.',
            'PossibleEffect': 'Failure of the fan in the switch "$(fhm_sw'
                              'itch_errors.switch-name)" might affect its '
                              'cooling.',
            'CorrectiveActions': '1) Ensure that the fans in the switch '
                                 'are operating correctly by using the '
                                 'command "storage switch show '
                                 '-cooling".2) Ensure that the fan FRUs '
                                 'are properly inserted and operational.'},
        'FabricSwitchPowerFail_Alert': {
            'severityofAlert': 'Major',
            'probableCause': 'Power_supply_failure',
            'description': 'A power supply unit on the switch "$('
                           'fhm_switch_errors.switch-name)" is not '
                           'operational.',
            'PossibleEffect': 'Power supply redundancy on switch "$('
                              'fhm_switch_errors.switch-name)" is lost.',
            'CorrectiveActions': '1) Check the error details by using the '
                                 'command "storage switch show -error '
                                 '-switch-name $('
                                 'fhm_switch_errors.switch-name)".2) '
                                 'Identify the faulty power supply unit '
                                 'by using the command "storage switch '
                                 'show -power -switch-name $('
                                 'fhm_switch_errors.switch-name)".3) '
                                 'Ensure that the power supply unit "$('
                                 'fhm_switch_errors.switch-component-name)" '
                                 'is properly inserted into the chassis of '
                                 'the switch "$('
                                 'fhm_switch_errors.switch-name)" and '
                                 'fully operational.'},
        'FabricSwitchTempCritical_Alert': {
            'severityofAlert': 'Major',
            'probableCause': 'Temperature_unacceptable',
            'description': '"$(fhm_switch_errors.switch-component-name)" '
                           'temperature sensor on the FC switch "$('
                           'fhm_switch_errors.switch-name)" is reporting '
                           'critical temperature.',
            'PossibleEffect': '"$(fhm_switch_errors.switch-name)" switch '
                              'might shutdown if the temperature remains '
                              'at critical level.',
            'CorrectiveActions': '1) Check the operational status of the '
                                 'temperature sensors on the switch by '
                                 'using the command "storage switch show '
                                 '-cooling".2) Verify that the switch is '
                                 'operating under recommended temperature '
                                 'conditions.'},
        'FabricSwitchTempSensorFailed_Alert': {
            'severityofAlert': 'Major',
            'probableCause': 'Sensor_failure',
            'description': 'Sensor "$('
                           'fhm_switch_errors.switch-component-name)" on '
                           'the FC switch "$('
                           'fhm_switch_errors.switch-name)" has failed.',
            'PossibleEffect': 'Problems with the switch "$('
                              'fhm_switch_errors.switch-name)" '
                              'temperature might go undetected.',
            'CorrectiveActions': '1) Check the operational status of the '
                                 'temperature sensors on the switch by '
                                 'using the command "storage switch show '
                                 '-cooling".2) Verify that the switch is '
                                 'operating under recommended temperature '
                                 'conditions.'},
        'FabricSwitchUnreachable_Alert': {
            'severityofAlert': 'Major',
            'probableCause': 'Connection_establishment_error',
            'description': '"$(fhm_switch_errors.switch-component-name)" '
                           'switch is not reachable over the management '
                           'network.',
            'PossibleEffect': 'Switch "$('
                              'fhm_switch_errors.switch-component-name)" '
                              'cannot be monitored for alerts.',
            'CorrectiveActions': '1) Ensure that the node management LIF '
                                 'is up by using the command "network '
                                 'interface show".2) Ensure that the '
                                 'switch "$( '
                                 'fhm_switch_errors.switch-component-name)"'
                                 ' is alive by using the command "network '
                                 'ping".3) Ensure that the switch is '
                                 'reachable over SNMP by checking its SNMP '
                                 'settings after logging into the switch.'},
        'InterclusterBrokenConnectionAlert': {
            'severityofAlert': 'Major',
            'probableCause': 'Out_of_service',
            'description': 'Connectivity to peer cluster is broken.',
            'PossibleEffect': 'Communication to the peer cluster is '
                              'compromised and the replication of '
                              'configuration between the clusters might '
                              'stop.',
            'CorrectiveActions': '1) Ensure that the port is connected to '
                                 'the correct network/switch.2) Ensure '
                                 'that the intercluster LIF is connected '
                                 'with the peered cluster.3) Ensure that '
                                 'the peered cluster is up and running by '
                                 'using the command "cluster peer ping". '
                                 'Refer to the MetroCluster Disaster '
                                 'Recovery Guide if the peered cluster is '
                                 'down.'},
        'NoISLPresentAlert': {
            'severityofAlert': 'Major',
            'probableCause': 'Out_of_service',
            'description': 'All ISL links on $(mcchm_isl.display-name) are '
                           'down.',
            'PossibleEffect': 'Backend fabric might lose ISL redundancy.',
            'CorrectiveActions': '1) Repair the backend fabric ISLs on $('
                                 'mcchm_isl.display-name).2) Ensure that '
                                 'the peered cluster is up and running by '
                                 'using the command "cluster peer ping". '
                                 'Refer to the MetroCluster Disaster '
                                 'Recovery Guide if the peered cluster is '
                                 'down.'},
        'RaidDegradedMirrorAggrAlert': {
            'severityofAlert': 'Major',
            'probableCause': 'Out_of_service',
            'description': 'Mirrored aggregate $(mcchm_aggr.name) has a '
                           'failed plex.',
            'PossibleEffect': 'DR protection of backend storage is '
                              'compromised.',
            'CorrectiveActions': 'If a plex failed:1) Ensure that the ISLs '
                                 'are healthy if the configuration '
                                 'includes fabric switches.2) Locate the '
                                 'problematic shelf and address any '
                                 'issues if seen.3) Check if any disks '
                                 'are broken by using the command '
                                 '"storage disk show -container-type '
                                 'broken".'},
        'RaidLeftBehindAggrAlert': {
            'severityofAlert': 'Major',
            'probableCause': 'Out_of_service',
            'description': 'Aggregate $(mcchm_aggr.name) was left behind '
                           'during switchback.',
            'PossibleEffect': 'Loss of access to aggregate by the original '
                              'owner.',
            'CorrectiveActions': '1) Check the aggregate state by using '
                                 'the command "aggr show".2) If the '
                                 'aggregate is online, return it to its '
                                 'original owner by using the command '
                                 '"metrocluster switchback".'},
        'RaidLeftBehindSpareAlert': {
            'severityofAlert': 'Major',
            'probableCause': 'Out_of_service',
            'description': 'Spare disk $(mcchm_disk.name) was left behind '
                           'during switchback.',
            'PossibleEffect': 'Loss of a spare disk by the original owner.',
            'CorrectiveActions': 'If the disk is not failed, return it to '
                                 'its original owner by using the command '
                                 '"metrocluster switchback".'},
        'StorageBridgeInvalidConfiguration_Alert': {
            'severityofAlert': 'Major',
            'probableCause': 'Connection_establishment_error',
            'description': 'Bridge $(mcchm_bridge_errors.name) is '
                           'incorrectly configured.',
            'PossibleEffect': 'Loss of redundancy or access to storage.',
            'CorrectiveActions': '1) Check the bridge\'s port details by '
                                 'using the command "storage bridge show '
                                 '-ports -name $('
                                 'mcchm_bridge_errors.name)" and ensure '
                                 'that the bridge\'s second FC and SAS '
                                 'ports are not being used.2) Refer to '
                                 'the MetroCluster(tm) Installation and '
                                 'Configuration Guide for the recommended '
                                 'configuration settings.'},
        'StorageBridgePortDown_Alert': {
            'severityofAlert': 'Major',
            'probableCause': 'Cable_tamper',
            'description': 'The port "$(fhm_bridge_errors.component-name)" '
                           'on the bridge "$(fhm_bridge_errors.name)" is '
                           'offline.',
            'PossibleEffect': 'Failure of the port "$('
                              'fhm_bridge_errors.component-name)" in the '
                              'bridge "$(fhm_bridge_errors.name)" might '
                              'cause loss of redundancy.',
            'CorrectiveActions': '1) Check the operational status of the '
                                 'ports on the bridge by using the '
                                 'command "storage bridge show -ports".2) '
                                 'Verify logical and physical '
                                 'connectivity to the port.'},
        'StorageBridgeTempAboveCritical_Alert': {
            'severityofAlert': 'Major',
            'probableCause': 'Temperature_unacceptable',
            'description': 'Sensor "$(fhm_bridge_errors.component-name)" '
                           'on the FC bridge "$(fhm_bridge_errors.name)" '
                           'is reporting a temperature that is above the '
                           'critical threshold.',
            'PossibleEffect': 'FC Bridge "$(fhm_bridge_errors.name)" might '
                              'shut down if the bridge temperature '
                              'remains at this reading.',
            'CorrectiveActions': '1) Check the operational status of the '
                                 'chassis temperature sensor on the '
                                 'bridge using the command "storage '
                                 'bridge show -cooling".2) Verify that '
                                 'the bridge is operating under '
                                 'recommended temperature conditions.'},
        'StorageBridgeTempBelowCritical_Alert': {
            'severityofAlert': 'Major',
            'probableCause': 'Temperature_unacceptable',
            'description': 'Sensor "$(fhm_bridge_errors.component-name)" '
                           'on the FC bridge "$(fhm_bridge_errors.name)" '
                           'is reporting a temperature that is below the '
                           'critical threshold.',
            'PossibleEffect': 'FC Bridge "$(fhm_bridge_errors.name)" might '
                              'shut down if the bridge temperature '
                              'remains at this reading.',
            'CorrectiveActions': '1) Check the operational status of the '
                                 'fans on the bridge.2) Verify that the '
                                 'bridge is operating under recommended '
                                 'temperature conditions.'},
        'StorageBridgeUnreachable_Alert': {
            'severityofAlert': 'Major',
            'probableCause': 'Connection_establishment_error',
            'description': '"$(fhm_bridge_errors.name)" bridge is not '
                           'reachable over management network.',
            'PossibleEffect': 'Bridge "$(fhm_bridge_errors.name)" cannot '
                              'be monitored for alerts.',
            'CorrectiveActions': '1) Ensure that the node management LIF '
                                 'is up by using the command "network '
                                 'interface show".2) Ensure that the '
                                 'bridge "$(fhm_bridge_errors.name)" is '
                                 'alive by using the command "network '
                                 'ping".'},
        'CriticalFan1FruFaultAlert': {
            'severityofAlert': 'Critical',
            'probableCause': 'hardware_degradation',
            'description': '$(cenv_fru_info.fru-name) is faulty. The nodes '
                           'in this chassis are $('
                           'cenv_fru_info.connected-nodes1).',
            'PossibleEffect': 'The chassis can lose its cooling capability '
                              'and the temperature can increase. If the '
                              'temperature increases past the threshold '
                              'values, the system might shutdown.',
            'CorrectiveActions': '1. Check $(cenv_fru_info.fru-name) for '
                                 'failures. If necessary replace $('
                                 'cenv_fru_info.fru-name) as soon as '
                                 'possible.2. Refer to fan module '
                                 'replacement documentation for more '
                                 'information.'},
        'CriticalFan2FruFaultAlert': {
            'severityofAlert': 'Critical',
            'probableCause': 'hardware_degradation',
            'description': '$(cenv_fru_info.fru-name) is faulty. The nodes '
                           'in this chassis are $('
                           'cenv_fru_info.connected-nodes1).',
            'PossibleEffect': 'The chassis can lose its cooling capability '
                              'and the temperature can increase. If the '
                              'temperature increases past the threshold '
                              'values, the system might shutdown.',
            'CorrectiveActions': '1. Check $(cenv_fru_info.fru-name) for '
