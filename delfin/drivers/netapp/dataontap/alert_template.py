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
    
