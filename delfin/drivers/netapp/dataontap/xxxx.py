                                 'failures. If necessary replace $('
                                 'cenv_fru_info.fru-name) as soon as '
                                 'possible.2. Refer to fan module '
                                 'replacement documentation for more '
                                 'information.'},
        'CriticalFan3FruFaultAlert': {
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
        'CriticalFan4FruFaultAlert': {
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
        'CriticalFanCurrFaultAlert': {
            'severityofAlert': 'Critical',
            'probableCause': 'hardware_degradation',
            'description': '$(cenv_fru_info.fru-name) is faulty. The nodes '
                           'in this chassis are $('
                           'cenv_fru_info.connected-nodes1).',
            'PossibleEffect': 'The fan does not have current within the '
                              'normal range, and could potentially fail.A '
                              'fan failure could cause the chassis to '
                              'lose its cooling capability and the '
                              'temperature can increase. If the '
                              'temperature increases past the threshold '
                              'values, the system might shutdown.',
            'CorrectiveActions': '1. Check $(cenv_fru_info.fru-name) for '
                                 'failures. If necessary replace $('
                                 'cenv_fru_info.fru-name) as soon as '
                                 'possible.2. Refer to fan module '
                                 'replacement documentation for more '
                                 'information.'},
        'CriticalFanFruFaultAlert': {
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
                                 'possible.2. Refer to the Hardware '
                                 'specification guide for more '
                                 'information on the position of the fan '
                                 'and ways to check or replace it. 3. '
                                 'Contact support personnel if the alert '
                                 'persists.'},
        'CriticalFanVoltFaultAlert': {
            'severityofAlert': 'Critical',
            'probableCause': 'hardware_degradation',
            'description': '$(cenv_fru_info.fru-name) is faulty. The nodes '
                           'in this chassis are $('
                           'cenv_fru_info.connected-nodes1).',
            'PossibleEffect': 'The fan does not have voltage within the '
                              'normal range, and could potentially fail.A '
                              'fan failure could cause the chassis to '
                              'lose its cooling capability and the '
                              'temperature can increase. If the '
                              'temperature increases past the threshold '
                              'values, the system might shutdown.',
            'CorrectiveActions': '1. Check $(cenv_fru_info.fru-name) for '
                                 'failures. If necessary replace $('
                                 'cenv_fru_info.fru-name) as soon as '
                                 'possible.2. Refer to fan module '
                                 'replacement documentation for more '
                                 'information.'},
        'CriticalFruMultiFaultAlert': {
            'severityofAlert': 'Critical',
            'probableCause': 'Equipment_malfunction',
            'description': '$(cenv_fru_info.fru-name) has multiple faults. '
                           'The nodes in this chassis are $('
                           'cenv_fru_info.connected-nodes1).',
            'PossibleEffect': 'The FRU $(cenv_fru_info.fru-name) might '
                              'stop functioning soon. The nodes in the '
                              'chassis might not function effectively or '
                              'redundancy might be lost.',
            'CorrectiveActions': '1. Check $(cenv_fru_info.fru-name) for '
                                 'failures. If necessary replace $('
                                 'cenv_fru_info.fru-name) as soon as '
                                 'possible.2. Refer to the Hardware '
                                 'specification guide for more '
                                 'information on the position of the '
                                 'field-replaceable unit (FRU) and ways '
                                 'to check or replace it. 3. Contact '
                                 'support personnel if the alert persists.'},
        'CriticalFruNotPresentAlert': {
            'severityofAlert': 'Critical',
            'probableCause': 'Configuration_error',
            'description': '$(cenv_fru_info.fru-name) is not present in '
                           'the chassis $(cenv_fru_info.chassis-id). The '
                           'nodes in this chassis are $('
                           'cenv_fru_info.connected-nodes1).',
            'PossibleEffect': 'The nodes in the chassis might not function '
                              'effectively or redundancy might be lost.',
            'CorrectiveActions': '1. Plug in $(cenv_fru_info.fru-name) '
                                 'correctly into the slot.2. Refer to the '
                                 'Hardware specification guide for more '
                                 'information on the position of the '
                                 'field-replaceable unit (FRU) and ways '
                                 'to check or replace it. 3. Contact '
                                 'support personnel if the alert persists.'},
        'CriticalPSUFruFaultAlert': {
            'severityofAlert': 'Critical',
            'probableCause': 'Equipment_malfunction',
            'description': '$(cenv_fru_info.fru-name) is faulty. The nodes '
                           'in this chassis are $('
                           'cenv_fru_info.connected-nodes1).',
            'PossibleEffect': '$(cenv_fru_info.fru-name) is faulty and has '
                              'stopped functioning. The system might '
                              'switch off if the other redundant power '
                              'supply units (PSUs) become faulty.',
            'CorrectiveActions': '1. Check $(cenv_fru_info.fru-name) for '
                                 'failures. If necessary replace $('
                                 'cenv_fru_info.fru-name) as soon as '
                                 'possible.2. Refer to the Hardware '
                                 'specification guide for more '
                                 'information on the position of the '
                                 'power supply unit (PSU) and ways to '
                                 'check or replace it. 3. Contact support '
                                 'personnel if the alert persists.'},
        'CriticalPSUFruOffAlert': {
            'severityofAlert': 'Critical',
            'probableCause': 'Loss_of_redundancy',
            'description': '$(cenv_fru_info.fru-name) is off. The nodes in '
                           'this chassis are $('
                           'cenv_fru_info.connected-nodes1).',
            'PossibleEffect': 'The system might switch off if the other '
                              'redundant power supply units (PSUs) become '
                              'faulty.',
            'CorrectiveActions': '1. Check $(cenv_fru_info.fru-name) and '
                                 'switch it on. 2. Refer to the Hardware '
                                 'specification guide for more '
                                 'information on the position of the '
                                 'power supply unit (PSU) and ways to '
                                 'check or replace it. 3. Contact support '
                                 'personnel if the alert persists.'},
        'CriticalPSUFruOverCurrentAlert': {
            'severityofAlert': 'Critical',
            'probableCause': 'Equipment_malfunction',
            'description': 'The input current to the power supply unit $('
                           'cenv_fru_info.fru-name) is very high. The '
                           'nodes in this chassis are $('
                           'cenv_fru_info.connected-nodes1).',
            'PossibleEffect': 'The power supply unit $('
                              'cenv_fru_info.fru-name) might stop '
                              'functioning if the input current stays '
                              'high for a prolonged period. The system '
                              'can lose redundancy if this power supply '
                              'unit (PSU) stops functioning.',
            'CorrectiveActions': '1. Check $(cenv_fru_info.fru-name) and '
                                 'the supply power to it. 2. Refer to the '
                                 'Hardware specification guide for more '
                                 'information on the position of the '
                                 'power supply unit (PSU) and ways to '
                                 'check or replace it. 3. Contact support '
                                 'personnel if the alert persists.'},
        'CriticalPSUFruOverPowerAlert': {
            'severityofAlert': 'Critical',
            'probableCause': 'Equipment_malfunction',
            'description': 'The input voltage to the power supply unit $('
                           'cenv_fru_info.fru-name) is very high. The '
                           'nodes in this chassis are $('
                           'cenv_fru_info.connected-nodes1).',
            'PossibleEffect': 'The power supply unit $('
                              'cenv_fru_info.fru-name) might stop '
                              'functioning if the input voltage stays '
                              'high for a prolonged period. The system '
                              'can lose redundancy if this power supply '
                              'unit (PSU) stops functioning.',
            'CorrectiveActions': '1. Check $(cenv_fru_info.fru-name) and '
                                 'the supply power to it. 2. Refer to the '
                                 'Hardware specification guide for more '
                                 'information on the position of the '
                                 'power supply unit (PSU) and ways to '
                                 'check or replace it. 3. Contact support '
                                 'personnel if the alert persists.'},
        'CriticalPSUFruOverTemperatureAlert': {
            'severityofAlert': 'Critical',
            'probableCause': 'Equipment_malfunction',
            'description': 'The temperature of power supply unit $(cenv_fru_info.fru-name) is very high. The nodes in this chassis are $(cenv_fru_info.connected-nodes1).',
            'PossibleEffect': 'The power supply unit $(cenv_fru_info.fru-name) might stop functioning if the temperature stays high for a prolonged period. The system can lose redundancy if this power supply unit (PSU) stops functioning.',
            'CorrectiveActions': '1. Check $(cenv_fru_info.fru-name) and the fans associated with it. 2. Refer to the Hardware specification guide for more information on the position of the power supply unit (PSU) and ways to check or replace it. 3. Contact support personnel if the alert persists.'},
        'CriticalPSUFruOverVoltageAlert': {
            'severityofAlert': 'Critical',
            'probableCause': 'Equipment_malfunction',
            'description': 'The input voltage to the power supply unit $(cenv_fru_info.fru-name) is very high. The nodes in this chassis are $(cenv_fru_info.connected-nodes1).',
            'PossibleEffect': 'The power supply unit $(cenv_fru_info.fru-name) might stop functioning if the input voltage stays high for a prolonged period. The system can lose redundancy if this power supply unit (PSU) stops functioning.',
            'CorrectiveActions': '1. Check $(cenv_fru_info.fru-name) and the supply power to it. 2. Refer to the Hardware specification guide for more information on the position of the power supply unit (PSU) and ways to check or replace it. 3. Contact support personnel if the alert persists.'},
        'FanFruFan1MajorAlert': {
            'severityofAlert': 'Major',
            'probableCause': 'Equipment_malfunction',
            'description': 'A fan in the fan module $(cenv_fru_info.fru-name) is in critical state. The nodes connected to this fan are $(cenv_fru_info.connected-nodes1).',
            'PossibleEffect': 'The chassis can lose its cooling capability and the temperature can increase. If the temperature increases past the threshold values, the system might shutdown.',
            'CorrectiveActions': '1. Check $(cenv_fru_info.fru-name) for failures. If necessary replace $(cenv_fru_info.fru-name) as soon as possible. 2. Refer to the Hardware specification guide for more information on the position of the fan and ways to check or replace it. 3. Contact support personnel if the alert persists.'},
        'FanFruFan1MinorAlert': {
            'severityofAlert': 'Minor',
            'probableCause': 'Equipment_malfunction',
            'description': 'A fan in the fan module $(cenv_fru_info.fru-name) is in warning state. The nodes in this chassis are $(cenv_fru_info.connected-nodes1).',
            'PossibleEffect': 'Cooling of the system could be slightly degraded. The chassis can lose its cooling capability and the temperature can increase.',
            'CorrectiveActions': '1. Check $(cenv_fru_info.fru-name) for failures. If necessary replace $(cenv_fru_info.fru-name) as soon as possible.2. Refer to the Hardware specification guide for more information on the position of the fan and ways to check or replace it. 3. Contact support personnel if the alert persists.'},
        'FanFruFan2MajorAlert': {
            'severityofAlert': 'Major',
            'probableCause': 'Equipment_malfunction',
            'description': 'A fan in the fan module $(cenv_fru_info.fru-name) is in critical state. The nodes in this chassis are $(cenv_fru_info.connected-nodes1).',
            'PossibleEffect': 'The chassis can lose its cooling capability and the temperature can increase. If the temperature increases past the threshold values, the system might shutdown.',
            'CorrectiveActions': '1. Check $(cenv_fru_info.fru-name) for failures. If necessary replace $(cenv_fru_info.fru-name) as soon as possible. 2. Refer to the Hardware specification guide for more information on the position of the fan and ways to check or replace it.3. Contact support personnel if the alert persists.'},
        'FanFruFan2MinorAlert': {
            'severityofAlert': 'Minor',
            'probableCause': 'Equipment_malfunction',
            'description': 'A fan in the fan module $(cenv_fru_info.fru-name) is in warning state. The nodes in this chassis are $(cenv_fru_info.connected-nodes1).',
            'PossibleEffect': 'Cooling of the system could be slightly degraded. The chassis can lose its cooling capability and the temperature can increase.',
            'CorrectiveActions': '1. Check $(cenv_fru_info.fru-name) for failures. If necessary replace $(cenv_fru_info.fru-name) as soon as possible.2. Refer to the Hardware specification guide for more information on the position of the fan and ways to check or replace it.3. Contact support personnel if the alert persists.'},
        'PSUFruFanBadAlert': {
            'severityofAlert': 'Major',
            'probableCause': 'Equipment_malfunction',
            'description': 'Power Supply Unit $(cenv_fru_info.fru-name) has a major fan problem. The nodes in this chassis are $(cenv_fru_info.connected-nodes1).',
            'PossibleEffect': 'The power supply unit (PSU) might stop functioning if the temperature increases.',
            'CorrectiveActions': '1. Check $(cenv_fru_info.fru-name) and the fans associated with it. 2. Refer to the Hardware specification guide for more information on the position of the power supply unit (PSU) and ways to check or replace it. 3. Contact support personnel if the alert persists.'},
        'PSUFruFanCriticalAlert': {
            'severityofAlert': 'Critical',
            'probableCause': 'Equipment_malfunction',
            'description': 'Power Supply Unit $(cenv_fru_info.fru-name) has a critical fan problem. The nodes in this chassis are $(cenv_fru_info.connected-nodes1).',
            'PossibleEffect': 'The power supply unit (PSU) might stop functioning if the temperature increases.',
            'CorrectiveActions': '1. Check $(cenv_fru_info.fru-name) and the fans associated with it. 2. Refer to the Hardware specification guide for more information on the position of the power supply unit (PSU) and ways to check or replace it. 3. Contact support personnel if the alert persists.'},
        'PSUFruFanMinorAlert': {
            'severityofAlert': 'Minor',
            'probableCause': 'Equipment_malfunction',
            'description': 'Power Supply Unit $(cenv_fru_info.fru-name) has a fan problem. The nodes in this chassis are $(cenv_fru_info.connected-nodes1).',
            'PossibleEffect': 'The power supply unit (PSU) might stop functioning if the fan is not fixed.',
            'CorrectiveActions': '1. Check $(cenv_fru_info.fru-name) and the fans associated with it. 2. Refer to the Hardware specification guide for more information on the position of the power supply unit (PSU) and ways to check or replace it.3. Contact support personnel if the alert persists.'},
        'ClusterSwitchCN1610MTU_Alert': {
            'severityofAlert': 'Minor',
            'probableCause': 'Configuration_error',
            'description': 'MTU value "$(cluster_switch_interface.mtu)" on port "$(cluster_switch_interface.display-name)" of switch "$(cluster_switch_interface.device)" is too small. It should be 9216.',
            'PossibleEffect': 'Received Ethernet packets that are larger than the configured MTU are dropped, causing data transfer issues.',
            'CorrectiveActions': 'To modify the switch port MTU, consult the switch configuration guide.'},
        'ClusterSwitchConfig_Alert': {
            'severityofAlert': 'Major',
            'probableCause': 'Configuration_error',
            'description': 'One or more nodes are not connected to both cluster switches.',
            'PossibleEffect': 'If one cluster switch fails, "$(cluster_switch_connection.node)" might lose access to the cluster.',
            'CorrectiveActions': 'Ensure the switch "$(cluster_switch_connection.missing-switch)" is connectedto the node "$(cluster_switch_connection.node)".'},
        'ClusterSwitchMissing_Alert': {
            'severityofAlert': 'Major',
            'probableCause': 'Configuration_error',
            'description': 'Redundant configuration is missing for cluster switches.',
            'PossibleEffect': 'If the remaining cluster switch fails, you can no longer access the cluster.',
            'CorrectiveActions': '1) Ensure that a redundant pair of cluster switches exists in the network.2) Ensure that cluster ports are connected to both switches.3) Enable the Cisco Discovery Protocol (CDP)/Industy Standard Discovery Protocol(ISDP) on the switches, if you previously disabled it. CDP/ISDP is enabled by default. Refer to your switch documentation for instructions. 4) If Data ONTAP cannot automatically discover a switch, use the "system health cluster-switch create" command to configure discovery and monitoring of the switch.'},
        'ClusterSwitchNEXUS5596MTU_Alert': {
            'severityofAlert': 'Minor',
            'probableCause': 'Configuration_error',
            'description': 'MTU value "$(cluster_switch_interface.mtu)" on port "$(cluster_switch_interface.display-name)" of switch "$(cluster_switch_interface.device)" is too small. It should be 1500.',
            'PossibleEffect': 'Received Ethernet packets that are larger than the configured MTU are dropped, causing data transfer issues.',
            'CorrectiveActions': 'To modify the switch port MTU, consult the switch configuration guide.'},
        'NodeSwitchPortMTU_Alert': {
            'severityofAlert': 'Minor',
            'probableCause': 'Configuration_error',
            'description': 'MTU value "$(cluster_switch_interface.remote-port-mtu)" on port "$(cluster_switch_interface.remote-port-name)" of node "$(cluster_switch_interface.remote-device)" is improperly set. It should be 9000.',
            'PossibleEffect': 'Received Ethernet packets that are larger than the configured MTU are dropped, causing data transfer issues.',
            'CorrectiveActions': 'modify the MTU using the command "network port broadcast-domain modify -broadcast-domain <broadcast_domain_name> -mtu <MTU>". To find out the broadcast domain name of the port, execute the command "network port broadcast-domain show".'},
        'SwitchFanFail_Alert': {
            'severityofAlert': 'Major',
            'probableCause': 'Fan_failure',
            'description': 'The fan "$(cluster_switch_fan.fan-name)" on the switch "$(cluster_switch_fan.device)" has failed.',
            'PossibleEffect': 'Failure of the fan in the switch "$(cluster_switch_fan.device)" might affect it\'s cooling.',
            'CorrectiveActions': '1) Check if the fans in the switch are running properly.2) Ensure proper power supply to the fan FRU. 3) Contact technical support if the alert persists.'},
        'SwitchFanNotOperational_Alert': {
            'severityofAlert': 'Major',
            'probableCause': 'Out_of_service',
            'description': 'The fan "$(cluster_switch_fan.fan-name)" on switch "$(cluster_switch_fan.device)" is not functioning properly.',
            'PossibleEffect': 'Cooling of switch "$(cluster_switch_fan.device)" will be degraded.',
            'CorrectiveActions': '1) Verify that the fan is turned on through the switch CLI.2) Contact technical support if the alert persists.'},
        'SwitchFanNotPresent_Alert': {
            'severityofAlert': 'Major',
            'probableCause': 'Out_of_service',
            'description': 'The fan "$(cluster_switch_fan.fan-name)" is not inserted properly.',
            'PossibleEffect': 'Cooling of switch "$(cluster_switch_fan.device)" will be degraded.',
            'CorrectiveActions': '1) Verify that the fan module is inserted properly.'},
        'SwitchIfInErrorsWarn_Alert': {
            'severityofAlert': 'Major',
            'probableCause': 'Threshold_crossed',
            'description': 'The percentage of inbound packet errors of switch interface "$(cluster_switch_analytics.unique-name)" is above the warning threshold.',
            'PossibleEffect': 'Communication between nodes in the cluster might be degraded.',
            'CorrectiveActions': '1) Migrate any cluster LIF that uses this connection to another port connected to a cluster switch.For example, if cluster LIF "clus1" is on port e0a and the other LIF is on e0b,run the following command to move "clus1" to e0b:"network interface migrate -vserver vs1 -lif clus1 -sourcenode node1 -destnode node1 -dest-port e0b"2) Replace the network cable with a known-good cable.If errors are corrected, stop. No further action is required.Otherwise, continue to Step 3.3) Move the network cable to another port on the node (if available).Migrate the cluster LIF to the new port.If errors are corrected, contact technical support to troubleshoot the original node port.Otherwise, continue to Step 4.4) Move the network cable to another available cluster switch port.Migrate the cluster LIF back to the original port.If errors are corrected, contact technical support to troubleshoot the original switch port.If errors persist, contact technical support for further assistance.'},
        'SwitchIfIslDownWarn_Alert': {
            'severityofAlert': 'Major',
            'probableCause': 'Cable_tamper',
            'description': 'The cable used to connect switch "$(cluster_switch_interface.unique-name)" to the ISL port might be faulty.',
            'PossibleEffect': 'Cluster redundancy might be lost.',
            'CorrectiveActions': '1) Check whether the cable is fully inserted into the interface port on both ends. 2) Reconnect the ISL port using another cable. After reconnecting it, verify whether the link of the ISL port is up by executing the commands as per switch configuration guide or by checking whether the Link status LED is on.3) Contact technical support if the alert persists.'},
        'SwitchIfOutErrorsWarn_Alert': {
            'severityofAlert': 'Major',
            'probableCause': 'Threshold_crossed',
            'description': 'The percentage of outbound packet errors of switch interface "$(cluster_switch_analytics.unique-name)" is above the warning threshold.',
            'PossibleEffect': 'Communication between nodes in the cluster might be degraded.',
            'CorrectiveActions': '1) Migrate any cluster LIF that uses this connection to another port connected to a cluster switch.For example, if cluster LIF "clus1" is on port e0a and the other LIF is on e0b,run the following command to move "clus1" to e0b:"network interface migrate -vserver vs1 -lif clus1 -sourcenode node1 -destnode node1 -dest-port e0b"2) Replace the network cable with a known-good cable.If errors are corrected, stop. No further action is required.Otherwise, continue to Step 3.3) Move the network cable to another port on the node (if available).Migrate the cluster LIF to the new port.If errors are corrected, contact technical support to troubleshoot the original node port.Otherwise, continue to Step 4.4) Move the network cable to another available cluster switch port.Migrate the cluster LIF back to the original port.If errors are corrected, contact technical support to troubleshoot the original switch port.If errors persist, contact technical support for further assistance.'},
        'SwitchPowerFail_Alert': {
            'severityofAlert': 'Major',
            'probableCause': 'Power_supply_failure',
            'description': 'The power supply "$(cluster_switch_power.psu-name)" on the switch "$(cluster_switch_power.device)" is missing or is not operational.',
            'PossibleEffect': 'Power supply redundancy on switch "$(cluster_switch_power.device)" will be lost.',
            'CorrectiveActions': '1) Ensure that the power supply mains supplying power to the switch is turned on. 2) Ensure that the power cord is connected to the power supply of the switch. 3) Contact technical support if the alert persists.'},
        'SwitchPowerNotOperational_Alert': {
            'severityofAlert': 'Major',
            'probableCause': 'Out_of_service',
            'description': 'The power supply "$(cluster_switch_power.psu-name)" on switch "$(cluster_switch_power.device)" is not functioning properly.',
            'PossibleEffect': 'Switch "$(cluster_switch_power.device)" might shutdown if the dual power supply degrades to a non-operational state.',
            'CorrectiveActions': "1) Ensure that the power supply unit is turned on through switch CLI. 2) Run diagnostics on the switch to check the operational status of the power supply unit (PSU). For instructions about how to run switch diagnostics, see the switch's configuration guide. 3) Contact technical support if the alert persists."},
        'SwitchPowerNotPresent_Alert': {
            'severityofAlert': 'Major',
            'probableCause': 'Out_of_service',
            'description': 'The power supply "$(cluster_switch_power.psu-name)" on switch "$(cluster_switch_power.device)" is not functioning properly.',
            'PossibleEffect': 'The remaining power supply is a single point of failure. Switch "$(cluster_switch_power.device)" might shut down with the next PSU failure.',
            'CorrectiveActions': "1) Check whether the switch's power supply unit is properly inserted into the chassis of the switch."},
        'SwitchPsuFanNotOperational_Alert': {
            'severityofAlert': 'Major',
            'probableCause': 'Out_of_service',
            'description': 'The fan "$(cluster_switch_fan.fan-name)" on switch "$(cluster_switch_fan.device)" is not functioning properly.',
            'PossibleEffect': 'Cooling of switch "$(cluster_switch_fan.device)" will be degraded.',
            'CorrectiveActions': '1) Verify that the fan is turned on through the switch CLI.2) Contact technical support if the alert persists.'},
        'SwitchTemperatureCritical_Alert': {
            'severityofAlert': 'Major',
            'probableCause': 'Temperature_unacceptable',
            'description': 'Sensor "$(cluster_switch_temperature.sensor-name)" on switch "$(cluster_switch_temperature.device)" is reporting a temperature of $(cluster_switch_temperature.temperature) C, which is $(cluster_switch_temperature.cause-desc-var).',
            'PossibleEffect': 'Switch "$(cluster_switch_temperature.device)" might shut down if the switch temperature remains $(cluster_switch_temperature.effect-msg-var) the critical threshold.',
            'CorrectiveActions': "1) Check the fans on the switch.2) Maintain the switch's recommended operating environment.3) Check the front and rear panels of the switch to make sure they are clear of any obstructions.4) Contact technical support if the alert persists."},
        'SwitchTemperatureNotOperational_Alert': {
            'severityofAlert': 'Major',
            'probableCause': 'Sensor_failure',
            'description': 'The sensor "$(cluster_switch_temperature.sensor-name)" on the switch "$(cluster_switch_temperature.device)" is not functioning properly.',
            'PossibleEffect': 'Problems with the switch "$(cluster_switch_temperature.device)" temperature might go undetected.',
            'CorrectiveActions': "1) Run diagnostics on the switch to check the operational status of the temperature sensors. For instructions about how to run switch diagnostics, see the switch's configuration guide. 2) Contact technical support if the alert persists."},
        'SwitchTemperatureWarn_Alert': {
            'severityofAlert': 'Minor',
            'probableCause': 'Threshold_crossed',
            'description': 'Sensor "$(cluster_switch_temperature.sensor-name)" on switch "$(cluster_switch_temperature.device)" is reporting a temperature of $(cluster_switch_temperature.temperature) C, which is $(cluster_switch_temperature.cause-desc-var).',
            'PossibleEffect': 'Switch "$(cluster_switch_temperature.device)" might shut down if the switch temperature continues to $(cluster_switch_temperature.effect-msg-var).',
            'CorrectiveActions': "1) Check the fans on the switch.2) Maintain the switch's recommended operating environment.3) Check the front and rear panels of the switch to make sure they are clear of any obstructions."},
        'SwitchlessConfig_Alert': {
            'severityofAlert': 'Major',
            'probableCause': 'Configuration_error',
            'description': 'No cluster switch is detected and the switchless option is not enabled.',
            'PossibleEffect': 'Communication problems and cluster connectivity issues occur.',
            'CorrectiveActions': '1) If the cluster network is configured as a two-node switchless cluster (TNSC),enable the switchless option with the command "network options switchless-cluster modify -enabled true".No further action is required.2) If the cluster network is configured with cluster switches, the nodes fail to detect the switches.Ensure that the network interfaces on the cluster switches connected to the node cluster ports are enabled on both sides.If the errors are corrected, stop. No further action is required. Otherwise, continue to step 3.3) Check the physical connections between the nodes and the cluster switches. Replace network cables with known-good cables.If the errors are corrected, stop. No further action is required. Otherwise, continue to step 4.4) Ensure that either CDP (for Cisco switches) or ISDP (for NetApp CN1610) is enabled on the cluster switches.If the errors still persist, contact technical support for further assistance.'},
        'UnsupportedSwitch_Alert': {
            'severityofAlert': 'Major',
            'probableCause': 'Configuration_error',
            'description': 'Unsupported cluster switch is detected.',
            'PossibleEffect': 'Communication problems and cluster connectivity issues occur.',
            'CorrectiveActions': 'Unsupported cluster switch "$(cluster_switch_support.device)" found. Connect a supported cluster switch to cluster network.'},
        'DegradedOnlinePort_Alert': {
            'severityofAlert': 'Major',
            'probableCause': 'Cable_tamper',
            'description': 'SAS port $(storage_node_port.port) on controller $(LOCALHOST) has $(storage_node_port.inactive-phy-count) disabled PHYs.',
            'PossibleEffect': 'Inactive PHYs might cause degraded link performance.',
            'CorrectiveActions': '1. Verify that SAS port $(storage_node_port.port) has disabled PHYs by using the "storage port show -node $(LOCALHOST) -port $(storage_node_port.port)" command. '},
        'DegradedOnlineShelfPort_Alert': {
            'severityofAlert': 'Major',
            'probableCause': 'Cable_tamper',
            'description': 'Shelf-to-shelf connection between disk shelves '
                           '$(storage_node_shelf_connector.shelf) $('
                           'storage_node_shelf_connector.connector-designator)'
                           ' port and $('
                           'storage_node_shelf_connector.remote-shelf) $('
                           'storage_node_shelf_connector.remote-connector'
                           '-designator) port have $('
                           'storage_node_shelf_connector.inactive-phy-count'
                           ') inactive PHYs on IOM $('
                           'storage_node_shelf_connector.shelf-module-id).',
            'PossibleEffect': 'Inactive PHYs might cause degraded link '
                              'performance.',
            'CorrectiveActions': '1. Consult the guide applicable to your '
                                 '$(storage_node_shelf_connector.module-type)'
                                 ' disk shelf to review cabling rules and '
                                 'complete the SAS cabling worksheet for '
                                 'your system.2. Verify that disk shelf $('
                                 'storage_node_shelf_connector.shelf) has '
                                 'disabled PHYs by using the "storage '
                                 'shelf show -shelf $('
                                 'storage_node_shelf_connector.shelf) '
                                 '-port" command. 3. If the disk shelves '
                                 'have multiple paths to the node, reseat '
                                 'disk shelf $('
                                 'storage_node_shelf_connector.shelf) $('
                                 'storage_node_shelf_connector.connector-'
                                 'designator) port cable on IOM $('
                                 'storage_node_shelf_connector.shelf-modul'
                                 'e-id) and disk shelf $('
                                 'storage_node_shelf_connector.remote-shelf)'
                                 ' $(storage_node_shelf_connector.remote-c'
                                 'onnector-designator) port cable on IOM '
                                 '$(storage_node_shelf_connector.remote-shel'
                                 'f-module-id).4. Verify that the physical'
                                 ' cable connection is secure and operationa'
                                 'l, and replace the cable, if necessary.'},
        'MccIp_PortOfflineAlert': {
            'severityofAlert': 'Major',
            'probableCause': 'Cable_tamper',
            'description': 'Physical link on port $('
                           'mcc_nhm_ip_adapter.port-no) is offline.',
            'PossibleEffect': 'DR protection of NVRAM mirrors and remote '
                              'storage might be compromised.',
            'CorrectiveActions': '1. Ensure that the link has not been '
                                 'tampered with.2. Verify that the '
                                 'physical status of the '
                                 'adapter is "Up" by using the '
                                 '"metrocluster interconnect adapter '
                                 'show" command.'},
        'MultipleTransitionsInStack_Alert': {
            'severityofAlert': 'Major',
            'probableCause': 'Cable_tamper',
            'description': 'Stack $(storage_node_stack.stack-id) on '
                           'controller $(LOCALHOST) contains multiple '
                           'technology transitions between SAS shelves.',
            'PossibleEffect': 'Some SAS shelves might not be accessible. '
                              'Multiple technology transitions are not '
                              'supported.',
            'CorrectiveActions': '1. Consult the guide for hot-adding '
                                 'shelves with IOM12 modules to stacks of '
                                 'shelves with IOM6 modules.2. Connect '
                                 'controller $(LOCALHOST) to stack $('
                                 'storage_node_stack.stack-id) using a '
                                 'multipath configuration that does not '
                                 'contain multiple technology transitions.'},
        'NoPathToNSMA_Alert': {
            'severityofAlert': 'Major',
            'probableCause': 'Cable_tamper',
            'description': 'Controller $(LOCALHOST) is connected only to '
                           'module B of shelf $(storage_node_ns.shelf) '
                           'through port $('
                           'storage_node_ns.initiator-ports).',
            'PossibleEffect': 'You will lose access to shelf $('
                              'storage_node_ns.shelf) if module B fails.',
            'CorrectiveActions': '1. Consult the guide applicable to your '
                                 'NVMe storage shelf to review cabling '
                                 'rules for your '
                                 'system.2. Connect controller $('
                                 'LOCALHOST) to module A and module B of '
                                 'shelf $(storage_node_ns.shelf).'},
        'NoPathToNSMB_Alert': {
            'severityofAlert': 'Major',
            'probableCause': 'Cable_tamper',
            'description': 'Controller $(LOCALHOST) is connected only to '
                           'module A of shelf $(storage_node_ns.shelf) '
                           'through port $('
                           'storage_node_ns.initiator-ports).',
            'PossibleEffect': 'You will lose access to shelf $('
                              'storage_node_ns.shelf) if module A fails.',
            'CorrectiveActions': '1. Consult the guide applicable to your '
                                 'NVMe storage shelf to review cabling '
                                 'rules for your system.2. Connect '
                                 'controller $(LOCALHOST) to module A and '
                                 'module B of shelf $('
                                 'storage_node_ns.shelf).'},
        'PriPortToBPort_Alert': {
            'severityofAlert': 'Minor',
            'probableCause': 'Cable_tamper',
            'description': 'Port $(storage_port_ns.port) on controller $('
                           'LOCALHOST) is connected to port $('
                           'storage_port_ns.remote-port) on module $('
                           'storage_port_ns.shelf-module-id) of shelf $('
                           'storage_port_ns.shelf).',
            'PossibleEffect': 'This will affect upgrades to '
                              'switch-attached storage.',
            'CorrectiveActions': '1. Consult the guide applicable to your '
                                 'NVMe storage shelf to review cabling '
                                 'rules for your system.2. Connect $('
                                 'storage_port_ns.port) to e0a on either '
                                 'module of shelf $('
                                 'storage_port_ns.shelf).'},
        'SecPortToAPort_Alert': {
            'severityofAlert': 'Minor',
            'probableCause': 'Cable_tamper',
            'description': 'Port $(storage_port_ns.port) on controller $('
                           'LOCALHOST) is connected to port $('
                           'storage_port_ns.remote-port) on module $('
                           'storage_port_ns.shelf-module-id) of shelf $('
                           'storage_port_ns.shelf).',
            'PossibleEffect': 'This will affect upgrades to '
                              'switch-attached storage.',
            'CorrectiveActions': '1. Consult the guide applicable to your '
                                 'NVMe storage shelf to review cabling '
                                 'rules for your system.2. Connect $('
                                 'storage_port_ns.port) to e0b on either '
                                 'module of shelf $('
                                 'storage_port_ns.shelf).'},
        'SingleAdapterToShelf_Alert': {
            'severityofAlert': 'Major',
            'probableCause': 'Cable_tamper',
            'description': 'Controller $(LOCALHOST) is connected to shelf '
                           '$(storage_node_ns.shelf) using ports $('
                           'storage_node_ns.initiator-ports) on the same '
                           'adapter.',
            'PossibleEffect': 'Access to shelf $(storage_node_ns.shelf) '
                              'might be lost with an adapter failure.',
            'CorrectiveActions': '1. Consult the guide applicable to your '
                                 'NVMe storage shelf to review cabling '
                                 'rules for your system.2. Connect '
                                 'controller $(LOCALHOST) to module A and '
                                 'module B of shelf $('
                                 'storage_node_ns.shelf) using ports from '
                                 'different adapters.'},
        'SingleAdapterToSwitch_Alert': {
            'severityofAlert': 'Major',
            'probableCause': 'Cable_tamper',
            'description': 'Controller $(storage_node_switch.node) is '
                           'connected to switches $('
                           'storage_node_switch.switch-list) using ports '
                           'on the same adapter ($('
                           'storage_node_switch.initiator-ports)).',
            'PossibleEffect': 'You will lose access to shelves $('
                              'storage_node_switch.shelves) if a single '
                              'adapter fails.',
            'CorrectiveActions': '1. Consult the guide applicable to your '
                                 'NVMe storage shelf to review cabling '
                                 'rules for your system.2. Connect '
                                 'controller $(LOCALHOST) to storage '
                                 'switches using ports from two different '
                                 'adapters.'},
        'SingleSwitchToShelf_Alert': {
            'severityofAlert': 'Major',
            'probableCause': 'Cable_tamper',
            'description': 'Controller $(storage_node_switch.node) is '
                           'connected to NVMe storage shelves $('
                           'storage_node_switch.shelves) through only one '
                           'switch $(storage_node_switch.switch-list).',
            'PossibleEffect': 'You will lose access to shelves if switch $('
                              'storage_node_switch.switch-list) fails.',
            'CorrectiveActions': '1. Consult the guide applicable to your '
                                 'NVMe storage shelf to review cabling '
                                 'rules for your system.2. Connect '
                                 'controller $(LOCALHOST) to NVMe shelves '
                                 'through two storage switches.'},
        'DomainMismatchFromNodeToShelf_Alert': {
            'severityofAlert': 'Major',
            'probableCause': 'Configuration_error',
            'description': 'The storage domain between the nodes $('
                           'sschm_switch.node-list) and switch $('
                           'sschm_switch.switch-name) is different from '
                           'the domain between the switch and shelves $('
                           'sschm_switch.shelves).',
            'PossibleEffect': 'This issue will affect conversions to '
                              'direct-attached storage.',
            'CorrectiveActions': 'Connect the switch $('
                                 'sschm_switch.switch-name) to both the '
                                 'node and the shelves with the same '
                                 'storage domain, following the guide '
                                 'applicable to your shelf.'},
        'FabricSwitchNoISLPresentAlert': {
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
        'MissingPathFromSwitchToNSM_Alert': {
            'severityofAlert': 'Major',
            'probableCause': 'Configuration_error',
            'description': 'Shelf $(sschm_shelf_module.shelf-name) module'
                           ' $(sschm_shelf_module.module-id) is connected '
                           'to only one storage switch.',
            'PossibleEffect': 'Access to shelf $(sschm_shelf_module.'
                              'shelf-name) module $('
                              'sschm_shelf_module.module-id) can be lost '
                              'due to a switch failure.',
            'CorrectiveActions': 'Connect shelf $('
                                 'sschm_shelf_module.shelf-name) module $('
                                 'sschm_shelf_module.module-id) to two '
                                 'storage switches, following the guide '
                                 'applicable to your shelf.'},
        'MixedDomainFromNodeToSwitch_Alert': {
            'severityofAlert': 'Minor',
            'probableCause': 'Configuration_error',
            'description': 'Storage Switch $(sschm_switch.device) is '
                           'connected to nodes $(sschm_switch.node-'
                           'list) using ports $(sschm_switch.port-lis'
                           't). The storage ports belong to different'
                           ' storage domains.',
            'PossibleEffect': 'This issue will affect conversions to '
                              'direct-attached storage.',
            'CorrectiveActions': 'Connect the switch $(sschm_switch.'
                                 'device) using ports from the same'
                                 ' storage domain, following the '
                                 'guide applicable to your shelf.'},
        'MixedDomainFromSwitchToShelf_Alert': {
            'severityofAlert': 'Minor',
            'probableCause': 'Configuration_error',
            'description': 'Storage Switch $(sschm_switch.switch-name) is '
                           'connected to shelves $(sschm_switch.shelves) '
                           'with mixed domains.',
            'PossibleEffect': 'This issue will affect conversions to '
                              'direct-attached storage.',
            'CorrectiveActions': 'Connect the switch $(sschm_switch.swi'
                                 'tch-name) to both shelves with the '
                                 'same storage domain, following the '
                                 'guide applicable to your shelf.'},
        'NoPathFromSwitchToNSM_Alert': {
            'severityofAlert': 'Major',
            'probableCause': 'Configuration_error',
            'description': 'Storage shelf $(sschm_shelf_module.shelf-name) '
                           'module $(sschm_shelf_module.module-id) is not '
                           'connected to storage switches.',
            'PossibleEffect': 'Access to shelf $(sschm_shelf_module.shelf-'
                              'name) can be lost with a single shelf module '
                              'failure.',
            'CorrectiveActions': 'Connect shelf $(sschm_shelf_module.shelf-n'
                                 'ame) module $('
                                 'sschm_shelf_module.module-id) '
                                 'to two storage switches, following the '
                                 'guide'
                                 ' applicable to your shelf.'},
        'ShelfPSUFailure_Alert': {
            'severityofAlert': 'Major',
            'probableCause': 'Power_supply_failure',
            'description': 'Power Supply Units (PSU) on Shelf $(sschm_shelf'
                           '_psu.shelf-name) connected to controllers $('
                           'sschm_shelf_psu.nodes) are not operational.',
            'PossibleEffect': 'Some SAS or NVMe storage shelves might '
                              'not be accessible.',
            'CorrectiveActions': '1. Check the AC power distribution to '
                                 'the PSU and the PSU power switch.2. '
                                 'Switch off the PSU (if equipped). Remove '
                                 'the PSU. Wait one minute. Insert the '
                                 'PSU. Switch on the PSU (if equipped).'},
        'StorageBridgePowerSupplyFailed_Alert': {
            'severityofAlert': 'Major',
            'probableCause': 'Power_supply_failure',
            'description': '$(fhm_bridge_errors.component-name) '
                           '$(fhm_bridge_errors.component-unique-id) of "$('
                           'fhm_bridge_errors.name)" has failed.',
            'PossibleEffect': 'If the remaining power supply fails,'
                              ' "$(fhm_bridge_errors.name)" will go '
                              'offline, causing a loss of path redundancy '
                              'to storage.',
            'CorrectiveActions': '1) Check the power source for the'
                                 ' bridge, the power cords and fuses.2) If '
                                 'the problem cannot be corrected, replace '
                                 'the failed power supply.'},
        'CoredumpMissingAlert': {
            'severityofAlert': 'Major',
            'probableCause': 'Configuration_error',
            'description': 'Coredump device "$(nphm_coredump_info.displ'
                           'ay-name)" is missing from the system.',
            'PossibleEffect': 'Coredump files cannot be saved.',
            'CorrectiveActions': '1. Perform a takeover of this node an'
                                 'd bring the node down for maintenance. '
                                 '2. Verify that a coredump device is '
                                 'securely inserted in the system.3. Use '
                                 'the "bye" LOADER command to reboot the '
                                 'node, then perform a giveback.'},
        'CoredumpWarnAlert': {
            'severityofAlert': 'Major',
            'probableCause': 'hardware_degrading',
            'description': 'Coredump device is approaching the end of its '
                           'rated life.',
            'PossibleEffect': 'A coredump device that reaches the end of its '
                              'rated life might not be able to save or retain'
                              'coredumps.',
            'CorrectiveActions': '1. Plan a maintenance window to replace the '
                                 'coredump device.2. Perform a takeover of '
                                 'this node and bring the node down for '
                                 'maintenance.3. Replace the coredump '
                                 'device.4. Use the "bye" LOADER command '
                                 'to reboot the node, then perform a giveback.'},
        'NVDIMMBadHealthAlert': {
            'severityofAlert': 'Major',
            'probableCause': 'hardware_degrading',
            'description': 'NVDIMM "$(nphm_nvdimm_fru.display-name)" on node "$(nphm_nvdimm_fru.node-id)"is indicating a degraded status.',
            'PossibleEffect': 'Potential data loss as the NVDIMM becomes degraded.',
            'CorrectiveActions': 'Contact technical support for assistance with NVDIMM module replacement.'},
        'NVDIMMFailEndOfLifeAlert': {
            'severityofAlert': 'Critical',
            'probableCause': 'hardware_degradation',
            'description': 'Flash memory in NVDIMM "$(nphm_nvdimm_fru.'
                           'display-name)"on node "$('
                           'nphm_nvdimm_fru.node-id)" has reached its end '
                           'of life.',
            'PossibleEffect': 'Potential data loss because NVDIMM flash'
                              ' memory is not usable.',
            'CorrectiveActions': 'Contact technical support for assistance'
                                 ' with NVDIMM module replacement.'},
        'NVDIMMWarnLifeStatusAlert': {
            'severityofAlert': 'Minor',
            'probableCause': 'hardware_degrading',
            'description': 'Flash memory in NVDIMM "$(nphm_nvdimm_fru'
                           '.display-name)"on node "$('
                           'nphm_nvdimm_fru.node-id)" is nearing its end '
                           'of life.',
            'PossibleEffect': 'Potential data loss if NVDIMM flash'
                              ' memory becomes unusable.',
            'CorrectiveActions': 'Contact technical support for assistance.'},
        'ClusterIfInErrorsWarn_Alert': {
            'severityofAlert': 'Major',
            'probableCause': 'Threshold_crossed',
            'description': 'The percentage of inbound packet errors of '
                           'switch interface "$('
                           'cluster_switch_analytics.unique-name)" is '
                           'above the warning threshold.',
            'PossibleEffect': 'Communication between nodes in the cluster'
                              ' might be degraded.',
            'CorrectiveActions': '1) Migrate any cluster LIF that uses this '
                                 'connection to another port connected to '
                                 'a cluster switch.For example, if cluster '
                                 'LIF "clus1" is on port e0a and the other '
                                 'LIF is on e0b,run the following command '
                                 'to move "clus1" to e0b:"network '
                                 'interface migrate -vserver vs1 -lif '
                                 'clus1 -destination-node node1 '
                                 '-destination-port e0b"2) Replace the '
                                 'network cable with a known-good cable.If '
                                 'errors are corrected, stop. No further '
                                 'action is required.Otherwise, continue '
                                 'to Step 3.3) Move the network cable to '
                                 'another port on the node (if '
                                 'available).Migrate the cluster LIF to '
                                 'the new port.If errors are corrected, '
                                 'contact technical support to '
                                 'troubleshoot the original node '
                                 'port.Otherwise, continue to Step 4.4) '
                                 'Move the network cable to another '
                                 'available cluster switch port.Migrate '
                                 'the cluster LIF back to the original '
                                 'port.If errors are corrected, contact '
                                 'technical support to troubleshoot the '
                                 'original switch port.If errors persist, '
                                 'contact technical support for further '
                                 'assistance.'},
        'ClusterIfIslDownWarn_Alert': {
            'severityofAlert': 'Major',
            'probableCause': 'Cable_tamper',
            'description': 'The cable used to connect switch "$(clu'
                           'ster_switch_interface.unique-name)" to the ISL p'
                           'ort might be faulty. For the port-channel, please check each individual link.',
            'PossibleEffect': 'Cluster redundancy might be lost.',
            'CorrectiveActions': '1) Check whether the cable is ful'
                                 'ly inserted into the interface port on bot'
                                 'h ends. 2) Reconnect the ISL port using '
                                 'another cable. After reconnecting it, '
                                 'verify whether the link of the ISL port '
                                 'is up by executing the commands per the '
                                 'switch configuration guide or by '
                                 'checking whether the Link status LED is on.'},
        'ClusterIfOutErrorsWarn_Alert': {
            'severityofAlert': 'Major',
            'probableCause': 'Threshold_crossed',
            'description': 'The percentage of outbound packet error'
                           's of switch interface "$(cluster_switch_analytics.unique-name)" '
                           'is above the warning threshold.',
            'PossibleEffect': 'Communication between nodes in the c'
                              'luster might be degraded.',
            'CorrectiveActions': '1) Migrate any cluster LIF that u'
                                 'ses this connection to another port '
                                 'connected to a cluster switch.For examp'
                                 'le, if cluster LIF "clus1" is on port e0a '
                                 'and the other LIF is on e0b,'
                                 'run the following command to move "clus1" '
                                 'to e0b:"network interface migrate '
                                 '-vserver vs1 -lif clus1 -destination-node '
                                 'node1 -destination-port e0b"2) Replace '
                                 'the network cable with a known-good '
                                 'cable.If errors are corrected, stop. No '
                                 'further action is required.Otherwise, '
                                 'continue to Step 3.3) Move the network '
                                 'cable to another port on the node (if '
                                 'available).Migrate the cluster LIF to '
                                 'the new port.If errors are corrected, '
                                 'contact technical support to '
                                 'troubleshoot the original node '
                                 'port.Otherwise, continue to Step 4.4) '
                                 'Move the network cable to another '
                                 'available cluster switch port.Migrate '
                                 'the cluster LIF back to the original '
                                 'port.If errors are corrected, contact '
                                 'technical support to troubleshoot the '
                                 'original switch port.If errors persist, '
                                 'contact technical support for further '
                                 'assistance.'},
        'ClusterSwitchConnectivity_Alert': {
            'severityofAlert': 'Major',
            'probableCause': 'Configuration_error',
            'description': 'One or more nodes are not connected to b'
                           'oth cluster switches.',
            'PossibleEffect': 'If one cluster switch fails, "$(clust'
                              'er_switch_connection.node)" might lose access to the cluster.',
            'CorrectiveActions': 'Verify that the switch "$(cluster_'
                                 'switch_connection.missing-switch)" is connectedto the node "$(clus'
                                 'ter_switch_connection.node)".'},
        'ClusterSwitchlessConfig_Alert': {
            'severityofAlert': 'Major',
            'probableCause': 'Configuration_error',
            'description': 'No cluster switch is detected and the sw'
                           'itchless option is not enabled.',
            'PossibleEffect': 'Communication problems and cluster co'
                              'nnectivity issues occur.',
            'CorrectiveActions': '1) If the cluster network is confi'
                                 'gured as a two-node switchless cluster (TNSC),enable switchless de'
                                 'tection by using the "network options detect-switchless-cluster modify -enabled true" command.No further action is required.2) If the cluster network is configured with cluster switches, the nodes fail to detect the switches.Ensure that the network interfaces on the cluster switches connected to the node cluster ports are enabled on both sides.If the errors are corrected, stop. No further action is required. Otherwise, continue to step 3.3) Check the physical connections between the nodes and the cluster switches. Replace network cables with known-good cables.If the errors are corrected, stop. No further action is required. Otherwise, continue to step 4.4) Ensure that either CDP (for Cisco switches) or ISDP (for NetApp CN1610 and Broadcom BES-53248 switches) is enabled on the cluster switches.'},
        'StorageIfInErrorsWarn_Alert': {
            'severityofAlert': 'Major',
            'probableCause': 'Threshold_crossed',
            'description': 'The percentage of inbound packet errors'
                           ' of switch:port $(cluster_switch_analyt'
                           'ics.device):$(cluster_switch_analytics.'
                           'interface-name) is above the warning '
                           'threshold.',
            'PossibleEffect': 'Communication with storage shelves i'
                              'n the cluster might be degraded.',
            'CorrectiveActions': '1) Replace the network cable with'
                                 ' a known-good cable.If errors are'
                                 ' corrected, stop. No further actio'
                                 'n is required.Otherwise, continue '
                                 'to Step 2.2) Move the network cabl'
                                 'e to another port on the node (if '
                                 'available).Consult the guide appli'
                                 'cable to your NVMe storage shelf to '
                                 'review cabling rules for your system'
                                 '.If errors are corrected, contact te'
                                 'chnical support to troubleshoot the'
                                 'original node port.Otherwise, contin'
                                 'ue to Step 3.3) Move the network ca'
                                 'ble to another available storage sw'
                                 'itch port.If errors are corrected, '
                                 'contact technical support to troubl'
                                 'eshoot the original switch port.If '
                                 'errors persist, contact technical su'
                                 'pport for further assistance.'},
        'StorageIfOutErrorsWarn_Alert': {
            'severityofAlert': 'Major',
            'probableCause': 'Threshold_crossed',
            'description': 'The percentage of outbound packet errors of sw'
                           'itch:port $(cluster_switch_analytics.device):'
                           '$(cluster_switch_analytics.interface-name) '
                           'is above the warning threshold.',
            'PossibleEffect': 'Communication with storage shelves in the'
                              ' cluster might be degraded.',
            'CorrectiveActions': '1) Replace the network cable with a kn'
                                 'own-good cable.If errors are corrected,'
                                 ' stop. No further action is required.O'
                                 'therwise, continue to Step 2.2) Move t'
                                 'he network cable to another port on th'
                                 'e node (if available).Consult the guid'
                                 'e applicable to your NVMe storage shel'
                                 'f to review cabling rules for your sys'
                                 'tem.If errors are corrected, contact t'
                                 'echnical support to troubleshoot the o'
                                 'riginal node port.Otherwise, continue '
                                 'to Step 3.3) Move the network cable to '
                                 'another available storage switch port.I'
                                 'f errors are corrected, contact techni'
                                 'cal support to troubleshoot the origin'
                                 'al switch port.If errors persist, conta'
                                 'ct technical support for further assist'
                                 'ance.'},
        'StorageSwitchIfIslConfig_Alert': {
            'severityofAlert': 'Major',
            'probableCause': 'Configuration_error',
            'description': 'An ISL link has been detected between storaqe '
                           'switch:port $(cluster_switch_interface.device)'
                           ':$(cluster_switch_interface.interface-name) and '
                           'switch:port $(cluster_switch_interface.remote-'
                           'device):$(cluster_switch_interface.remote-por'
                           't-name)"',
            'PossibleEffect': 'Poor storage performance could result.',
            'CorrectiveActions': 'Disconnect the ISL cable connections'
                                 ' between the two switches.'},
        'StorageSwitchMissing_Alert': {
            'severityofAlert': 'Major',
            'probableCause': 'Configuration_error',
            'description': 'Redundant configuration is missing for sto'
                           'rage switches.',
            'PossibleEffect': 'If the remaining storage switch fails,'
                              ' you will no longer be able to access t'
                              'he storage shelves.',
            'CorrectiveActions': '1) Ensure that a redundant pair of s'
                                 'torage switches exists in the networ'
                                 'k.2) Ensure that cluster ports are '
                                 'connected to both switches.3) Enable'
                                 ' the Cisco Discovery Protocol (CDP)'
                                 '/Industry Standard Discovery Protocol'
                                 ' (ISDP) on switches, if you previousl'
                                 'y disabled it. CDP/ISDP is enabled by'
                                 ' default. Refer to your switch documen'
                                 'tation for instructions. 4) If ONTAP(R)'
                                 ' software cannot automatically discov'
                                 'er a switch, use the "system switch e'
                                 'thernet create" command to configure '
                                 'discovery and monitoring of the switch'
                                 '.'},
        'SwitchAccess_Alert': {
            'severityofAlert': 'Minor',
            'probableCause': 'Login_attempts_failed',
            'description': 'Login failed to Ethernet switch "$(cluste'
                           'r_switch_information.unique-name)". Canno'
                           't collect tech-support logs.',
            'PossibleEffect': 'Ethernet switch tech-support logs are '
                              'not available in AutoSupport(R) messag'
                              'es for troubleshooting.',
            'CorrectiveActions': '1) To set up public SSH key authent'
                                 'ication on the Ethernet switch,run '
                                 'the "system switch ethernet log set'
                                 'up-password" command. ONTAP(R) sof'
                                 'tware requires one-time use of the '
                                 'Ethernet switch\'s administrative l'
                                 'ogin credentialsto set up the publ'
                                 'ic SSH key for ONTAP access. The a'
                                 'dministrative credentials will be di'
                                 'scarded after the setup command is '
                                 'complete. 2) If public SSH key authe'
                                 'ntication is already configured, log'
                                 ' in to the Ethernet switch with adm'
                                 'inistrative credentials from an SSH'
                                 ' host or serial console to investiga'
                                 'te the login failures. 3) To disable'
                                 ' tech-support log collection, run th'
                                 'e "system switch ethernet log disabl'
                                 'e-collection" command.'},
        'SwitchCommunityString_Alert': {
            'severityofAlert': 'Major',
            'probableCause': 'Configuration_error',
            'description': 'Ethernet switch "$(cluster_switch_support'
                           '.device)" with IP address "$(cluster_swit'
                           'ch_support.ip-address)" is not reachable '
                           'via SNMP. Incorrect SNMP community string'
                           ' might be configured on the Ethernet switch.',
            'PossibleEffect': 'Ethernet switch communication problems'
                              ' and accessibility issues.',
            'CorrectiveActions': 'Check the SNMP community string on '
                                 'the Ethernet switch to verify that'
                                 ' the expected community string is '
                                 'configured. Use the "system switch'
                                 ' ethernet show -snmp-config" comma'
                                 'nd to view the expected community '
                                 'string.'},
        'SwitchFanUnknown_Alert': {
            'severityofAlert': 'Major',
            'probableCause': 'Fan_failure',
            'description': 'The status of "$(cluster_switch_fan.fan-'
                           'name)" on switch "$(cluster_switch_fan.d'
                           'evice)" is unknown.',
            'PossibleEffect': 'Unknown fan status in switch "$(clust'
                              'er_switch_fan.device)" might affect '
                              'cooling performance.',
            'CorrectiveActions': '1) Verify that the fans on the sw'
                                 'itch are running properly.2) Repl'
                                 'ace the fan, if it is not operatio'
                                 'nal.'},
        'SwitchPortMTU_Alert': {
            'severityofAlert': 'Minor',
            'probableCause': 'Configuration_error',
            'description': 'MTU value "$(cluster_switch_interface.rem'
                           'ote-port-mtu)" on port "$(cluster_switch_i'
                           'nterface.remote-port-name)" of node "$(clu'
                           'ster_switch_interface.remote-device)" is '
                           'improperly set. It should be 9000.',
            'PossibleEffect': 'Received Ethernet packets that are larg'
                              'er than the configured MTU are dropped,'
                              ' causing data transfer issues.',
            'CorrectiveActions': 'Modify the MTU by using the "network'
                                 ' port broadcast-domain modify -ipspace'
                                 ' Cluster -broadcast-domain Cluster -mtu'
                                 ' <MTU>" command. To find out the broad'
                                 'cast domain name of the port, run the '
                                 '"network port broadcast-domain show" '
                                 'command.'},
        'SwitchPowerUnknown_Alert': {
            'severityofAlert': 'Major',
            'probableCause': 'Power_supply_failure',
            'description': 'The status of "$(cluster_switch_power.psu'
                           '-name)" on switch "$(cluster_switch_power'
                           '.device)" is unknown.',
            'PossibleEffect': 'Power supply redundancy on switch "$(c'
                              'luster_switch_power.device)" might be '
                              'lost.',
            'CorrectiveActions': '1) Ensure that the power supply uni'
                                 'ts supplying power to the switch are'
                                 ' turned on. 2) Ensure that the powe'
                                 'r cord is securely connected to the'
                                 ' power supply of the switch.'},
        'SwitchReboot_Alert': {
            'severityofAlert': 'Minor',
            'probableCause': 'Out_of_service',
            'description': 'The Ethernet switch "$(cluster_switch_in'
                           'formation.unique-name)" has recently reb'
                           'ooted.',
            'PossibleEffect': 'Communication problems and network co'
                              'nnectivity issues might occur.',
            'CorrectiveActions': 'If the Ethernet switch was not re'
                                 'booted on purpose, then check the'
                                 ' switch to ensure that it is oper'
                                 'ating normally.'},
        'SwitchTemperatureUnknown_Alert': {
            'severityofAlert': 'Major',
            'probableCause': 'Sensor_failure',
            'description': 'The status of "$(cluster_switch_temperature'
                           '.sensor-name)" on switch "$(cluster_switch_'
                           'temperature.device)" is unknown.',
            'PossibleEffect': 'Problems with the switch "$(cluster_swit'
                              'ch_temperature.device)" temperature mig'
                              'ht go undetected.',
            'CorrectiveActions': "Run diagnostics on the switch to check the"
                                 " operational status of the temperature s"
                                 "ensors.For instructions about how to run "
                                 "switch diagnostics, see the switch'"
                                 "s configuration guide."}}
