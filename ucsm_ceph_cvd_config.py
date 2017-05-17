#!/usr/bin/env python


# README
# ------
# fw download, disk zoning needed up front
# run script
# modify cfp to exclude all components, associate chassis profile
# modify hfp to exclude all components, sp from template
#
import sys
import json

if len(sys.argv) < 2:
    print "Usage: %s <JSON settings file>" % sys.argv[0]
    sys.exit(0)
f = open(sys.argv[1], 'r')
settings_file = json.load(f)
is_secure = True
if settings_file['secure'] == "False":
    is_secure = False
#
# -----
# end README

from ucsmsdk.ucshandle import UcsHandle

handle = UcsHandle(ip=settings_file['ip'], username=settings_file['user'], password=settings_file['pw'], secure=is_secure)
handle.login()

from ucsmsdk.mometa.compute.ComputeChassisConnPolicy import ComputeChassisConnPolicy
from ucsmsdk.mometa.cpmaint.CpmaintMaintPolicy import CpmaintMaintPolicy
from ucsmsdk.mometa.lstorage.LstorageDiskZoningPolicy import LstorageDiskZoningPolicy
from ucsmsdk.mometa.lstorage.LstorageDiskSlot import LstorageDiskSlot
from ucsmsdk.mometa.lstorage.LstorageControllerRef import LstorageControllerRef
from ucsmsdk.mometa.lstorage.LstorageDiskGroupConfigPolicy import LstorageDiskGroupConfigPolicy
from ucsmsdk.mometa.lstorage.LstorageVirtualDriveDef import LstorageVirtualDriveDef
from ucsmsdk.mometa.lstorage.LstorageLocalDiskConfigRef import LstorageLocalDiskConfigRef
from ucsmsdk.mometa.firmware.FirmwareChassisPack import FirmwareChassisPack
from ucsmsdk.mometa.firmware.FirmwarePackItem import FirmwarePackItem
from ucsmsdk.mometa.firmware.FirmwareExcludeChassisComponent import FirmwareExcludeChassisComponent
from ucsmsdk.mometa.uuidpool.UuidpoolPool import UuidpoolPool
from ucsmsdk.mometa.uuidpool.UuidpoolBlock import UuidpoolBlock
from ucsmsdk.mometa.ippool.IppoolPool import IppoolPool
from ucsmsdk.mometa.compute.ComputeQual import ComputeQual
from ucsmsdk.mometa.compute.ComputeChassisQual import ComputeChassisQual
from ucsmsdk.mometa.adaptor.AdaptorHostEthIfProfile import AdaptorHostEthIfProfile
from ucsmsdk.mometa.adaptor.AdaptorEthInterruptScalingProfile import AdaptorEthInterruptScalingProfile
from ucsmsdk.mometa.adaptor.AdaptorEthAdvFilterProfile import AdaptorEthAdvFilterProfile
from ucsmsdk.mometa.adaptor.AdaptorEthFailoverProfile import AdaptorEthFailoverProfile
from ucsmsdk.mometa.adaptor.AdaptorEthOffloadProfile import AdaptorEthOffloadProfile
from ucsmsdk.mometa.adaptor.AdaptorEthWorkQueueProfile import AdaptorEthWorkQueueProfile
from ucsmsdk.mometa.adaptor.AdaptorEthCompQueueProfile import AdaptorEthCompQueueProfile
from ucsmsdk.mometa.adaptor.AdaptorEthRecvQueueProfile import AdaptorEthRecvQueueProfile
from ucsmsdk.mometa.adaptor.AdaptorEthVxLANProfile import AdaptorEthVxLANProfile
from ucsmsdk.mometa.adaptor.AdaptorEthNVGREProfile import AdaptorEthNVGREProfile
from ucsmsdk.mometa.adaptor.AdaptorEthArfsProfile import AdaptorEthArfsProfile
from ucsmsdk.mometa.adaptor.AdaptorEthRoCEProfile import AdaptorEthRoCEProfile
from ucsmsdk.mometa.adaptor.AdaptorEthInterruptProfile import AdaptorEthInterruptProfile
from ucsmsdk.mometa.adaptor.AdaptorRssProfile import AdaptorRssProfile
from ucsmsdk.mometa.macpool.MacpoolPool import MacpoolPool
from ucsmsdk.mometa.macpool.MacpoolBlock import MacpoolBlock
from ucsmsdk.mometa.compute.ComputePool import ComputePool
from ucsmsdk.mometa.compute.ComputePooledRackUnit import ComputePooledRackUnit
from ucsmsdk.mometa.vnic.VnicLanConnTempl import VnicLanConnTempl
from ucsmsdk.mometa.vnic.VnicEtherIf import VnicEtherIf
from ucsmsdk.mometa.ls.LsServer import LsServer
from ucsmsdk.mometa.ls.LsVConAssign import LsVConAssign
from ucsmsdk.mometa.lstorage.LstorageProfileBinding import LstorageProfileBinding
from ucsmsdk.mometa.vnic.VnicEther import VnicEther
from ucsmsdk.mometa.vnic.VnicDefBeh import VnicDefBeh
from ucsmsdk.mometa.ls.LsVersionBeh import LsVersionBeh
from ucsmsdk.mometa.ls.LsServerExtension import LsServerExtension
from ucsmsdk.mometa.vnic.VnicConnDef import VnicConnDef
from ucsmsdk.mometa.vnic.VnicFcNode import VnicFcNode
from ucsmsdk.mometa.fabric.FabricVCon import FabricVCon
from ucsmsdk.mometa.ls.LsPower import LsPower
from ucsmsdk.mometa.storage.StorageLocalDiskConfigPolicy import StorageLocalDiskConfigPolicy
from ucsmsdk.mometa.power.PowerPolicy import PowerPolicy
from ucsmsdk.mometa.mgmt.MgmtBackupPolicy import MgmtBackupPolicy
from ucsmsdk.mometa.compute.ComputePooledSlot import ComputePooledSlot
from ucsmsdk.mometa.compute.ComputeKvmMgmtPolicy import ComputeKvmMgmtPolicy
from ucsmsdk.mometa.firmware.FirmwareCatalogPack import FirmwareCatalogPack
from ucsmsdk.mometa.adaptor.AdaptorHostFcIfProfile import AdaptorHostFcIfProfile
from ucsmsdk.mometa.adaptor.AdaptorFcCdbWorkQueueProfile import AdaptorFcCdbWorkQueueProfile
from ucsmsdk.mometa.adaptor.AdaptorFcPortPLogiProfile import AdaptorFcPortPLogiProfile
from ucsmsdk.mometa.adaptor.AdaptorFcPortFLogiProfile import AdaptorFcPortFLogiProfile
from ucsmsdk.mometa.adaptor.AdaptorFcErrorRecoveryProfile import AdaptorFcErrorRecoveryProfile
from ucsmsdk.mometa.adaptor.AdaptorFcWorkQueueProfile import AdaptorFcWorkQueueProfile
from ucsmsdk.mometa.adaptor.AdaptorFcRecvQueueProfile import AdaptorFcRecvQueueProfile
from ucsmsdk.mometa.adaptor.AdaptorFcPortProfile import AdaptorFcPortProfile
from ucsmsdk.mometa.adaptor.AdaptorFcFnicProfile import AdaptorFcFnicProfile
from ucsmsdk.mometa.adaptor.AdaptorFcInterruptProfile import AdaptorFcInterruptProfile
from ucsmsdk.mometa.mgmt.MgmtCfgExportPolicy import MgmtCfgExportPolicy
from ucsmsdk.mometa.lstorage.LstorageProfile import LstorageProfile
from ucsmsdk.mometa.lstorage.LstorageDasScsiLun import LstorageDasScsiLun
from ucsmsdk.mometa.fcpool.FcpoolInitiators import FcpoolInitiators
from ucsmsdk.mometa.adaptor.AdaptorHostIscsiIfProfile import AdaptorHostIscsiIfProfile
from ucsmsdk.mometa.adaptor.AdaptorProtocolProfile import AdaptorProtocolProfile
from ucsmsdk.mometa.compute.ComputeMemoryConfigPolicy import ComputeMemoryConfigPolicy
from ucsmsdk.mometa.lsboot.LsbootPolicy import LsbootPolicy
from ucsmsdk.mometa.lsboot.LsbootVirtualMedia import LsbootVirtualMedia
from ucsmsdk.mometa.lsboot.LsbootStorage import LsbootStorage
from ucsmsdk.mometa.lsboot.LsbootLocalStorage import LsbootLocalStorage
from ucsmsdk.mometa.lsboot.LsbootLocalHddImage import LsbootLocalHddImage
from ucsmsdk.mometa.lsboot.LsbootLan import LsbootLan
from ucsmsdk.mometa.lsboot.LsbootLanImagePath import LsbootLanImagePath
from ucsmsdk.mometa.vnic.VnicUsnicConPolicy import VnicUsnicConPolicy
from ucsmsdk.mometa.lsboot.LsbootDefaultLocalImage import LsbootDefaultLocalImage
from ucsmsdk.mometa.compute.ComputeServerMgmtPolicy import ComputeServerMgmtPolicy
from ucsmsdk.mometa.lsmaint.LsmaintMaintPolicy import LsmaintMaintPolicy
from ucsmsdk.mometa.stats.StatsThresholdPolicy import StatsThresholdPolicy
from ucsmsdk.mometa.compute.ComputePowerSyncPolicy import ComputePowerSyncPolicy
from ucsmsdk.mometa.compute.ComputeChassisDiscPolicy import ComputeChassisDiscPolicy
from ucsmsdk.mometa.fabric.FabricMulticastPolicy import FabricMulticastPolicy
from ucsmsdk.mometa.nwctrl.NwctrlDefinition import NwctrlDefinition
from ucsmsdk.mometa.dpsec.DpsecMac import DpsecMac
from ucsmsdk.mometa.ls.LsRequirement import LsRequirement
from ucsmsdk.mometa.compute.ComputeServerDiscPolicy import ComputeServerDiscPolicy
from ucsmsdk.mometa.ippool.IppoolBlock import IppoolBlock
from ucsmsdk.mometa.iqnpool.IqnpoolPool import IqnpoolPool
from ucsmsdk.mometa.compute.ComputeScrubPolicy import ComputeScrubPolicy
from ucsmsdk.mometa.power.PowerMgmtPolicy import PowerMgmtPolicy
from ucsmsdk.mometa.fabric.FabricOrgVlanPolicy import FabricOrgVlanPolicy
from ucsmsdk.mometa.epqos.EpqosDefinition import EpqosDefinition
from ucsmsdk.mometa.epqos.EpqosEgress import EpqosEgress
from ucsmsdk.mometa.bios.BiosVProfile import BiosVProfile
from ucsmsdk.mometa.bios.BiosVfUSBSystemIdlePowerOptimizingSetting import BiosVfUSBSystemIdlePowerOptimizingSetting
from ucsmsdk.mometa.bios.BiosVfIntelTrustedExecutionTechnology import BiosVfIntelTrustedExecutionTechnology
from ucsmsdk.mometa.bios.BiosVfIntegratedGraphicsApertureSize import BiosVfIntegratedGraphicsApertureSize
from ucsmsdk.mometa.bios.BiosVfIntelVirtualizationTechnology import BiosVfIntelVirtualizationTechnology
from ucsmsdk.mometa.bios.BiosVfOSBootWatchdogTimerTimeout import BiosVfOSBootWatchdogTimerTimeout
from ucsmsdk.mometa.bios.BiosVfSelectMemoryRASConfiguration import BiosVfSelectMemoryRASConfiguration
from ucsmsdk.mometa.bios.BiosVfProcessorEnergyConfiguration import BiosVfProcessorEnergyConfiguration
from ucsmsdk.mometa.bios.BiosVfConsistentDeviceNameControl import BiosVfConsistentDeviceNameControl
from ucsmsdk.mometa.bios.BiosVfOSBootWatchdogTimerPolicy import BiosVfOSBootWatchdogTimerPolicy
from ucsmsdk.mometa.bios.BiosVfEnhancedPowerCappingSupport import BiosVfEnhancedPowerCappingSupport
from ucsmsdk.mometa.bios.BiosVfCPUHardwarePowerManagement import BiosVfCPUHardwarePowerManagement
from ucsmsdk.mometa.bios.BiosVfEnhancedIntelSpeedStepTech import BiosVfEnhancedIntelSpeedStepTech
from ucsmsdk.mometa.bios.BiosVfPCILOMPortsConfiguration import BiosVfPCILOMPortsConfiguration
from ucsmsdk.mometa.bios.BiosVfUSBFrontPanelAccessLock import BiosVfUSBFrontPanelAccessLock
from ucsmsdk.mometa.bios.BiosVfIntelEntrySASRAIDModule import BiosVfIntelEntrySASRAIDModule
from ucsmsdk.mometa.bios.BiosVfRedirectionAfterBIOSPOST import BiosVfRedirectionAfterBIOSPOST
from ucsmsdk.mometa.bios.BiosVfMemoryMappedIOAbove4GB import BiosVfMemoryMappedIOAbove4GB
from ucsmsdk.mometa.bios.BiosVfQPILinkFrequencySelect import BiosVfQPILinkFrequencySelect
from ucsmsdk.mometa.bios.BiosVfIntelHyperThreadingTech import BiosVfIntelHyperThreadingTech
from ucsmsdk.mometa.bios.BiosVfEnergyPerformanceTuning import BiosVfEnergyPerformanceTuning
from ucsmsdk.mometa.bios.BiosVfProcessorPrefetchConfig import BiosVfProcessorPrefetchConfig
from ucsmsdk.mometa.bios.BiosVfMaxVariableMTRRSetting import BiosVfMaxVariableMTRRSetting
from ucsmsdk.mometa.bios.BiosVfUEFIOSUseLegacyVideo import BiosVfUEFIOSUseLegacyVideo
from ucsmsdk.mometa.bios.BiosVfInterleaveConfiguration import BiosVfInterleaveConfiguration
from ucsmsdk.mometa.bios.BiosVfFrequencyFloorOverride import BiosVfFrequencyFloorOverride
from ucsmsdk.mometa.bios.BiosVfIntelVTForDirectedIO import BiosVfIntelVTForDirectedIO
from ucsmsdk.mometa.bios.BiosVfMaximumMemoryBelow4GB import BiosVfMaximumMemoryBelow4GB
from ucsmsdk.mometa.bios.BiosVfResumeOnACPowerLoss import BiosVfResumeOnACPowerLoss
from ucsmsdk.mometa.bios.BiosVfTrustedPlatformModule import BiosVfTrustedPlatformModule
from ucsmsdk.mometa.bios.BiosVfOutOfBandManagement import BiosVfOutOfBandManagement
from ucsmsdk.mometa.bios.BiosVfOSBootWatchdogTimer import BiosVfOSBootWatchdogTimer
from ucsmsdk.mometa.bios.BiosVfUSBPortConfiguration import BiosVfUSBPortConfiguration
from ucsmsdk.mometa.bios.BiosVfWorkloadConfiguration import BiosVfWorkloadConfiguration
from ucsmsdk.mometa.bios.BiosVfDDR3VoltageSelection import BiosVfDDR3VoltageSelection
from ucsmsdk.mometa.bios.BiosVfIntelTurboBoostTech import BiosVfIntelTurboBoostTech
from ucsmsdk.mometa.bios.BiosVfPackageCStateLimit import BiosVfPackageCStateLimit
from ucsmsdk.mometa.bios.BiosVfDRAMClockThrottling import BiosVfDRAMClockThrottling
from ucsmsdk.mometa.bios.BiosVfPSTATECoordination import BiosVfPSTATECoordination
from ucsmsdk.mometa.bios.BiosVfCoreMultiProcessing import BiosVfCoreMultiProcessing
from ucsmsdk.mometa.bios.BiosVfSerialPortAEnable import BiosVfSerialPortAEnable
from ucsmsdk.mometa.bios.BiosVfProcessorC3Report import BiosVfProcessorC3Report
from ucsmsdk.mometa.bios.BiosVfProcessorC7Report import BiosVfProcessorC7Report
from ucsmsdk.mometa.bios.BiosVfProcessorC6Report import BiosVfProcessorC6Report
from ucsmsdk.mometa.bios.BiosVfExecuteDisableBit import BiosVfExecuteDisableBit
from ucsmsdk.mometa.bios.BiosVfFrontPanelLockout import BiosVfFrontPanelLockout
from ucsmsdk.mometa.bios.BiosVfIntegratedGraphics import BiosVfIntegratedGraphics
from ucsmsdk.mometa.bios.BiosVfDirectCacheAccess import BiosVfDirectCacheAccess
from ucsmsdk.mometa.bios.BiosVfConsoleRedirection import BiosVfConsoleRedirection
from ucsmsdk.mometa.bios.BiosVfPCISlotLinkSpeed import BiosVfPCISlotLinkSpeed
from ucsmsdk.mometa.bios.BiosVfAssertNMIOnSERR import BiosVfAssertNMIOnSERR
from ucsmsdk.mometa.bios.BiosVfAssertNMIOnPERR import BiosVfAssertNMIOnPERR
from ucsmsdk.mometa.bios.BiosVfIOENVMe1OptionROM import BiosVfIOENVMe1OptionROM
from ucsmsdk.mometa.bios.BiosVfIOENVMe2OptionROM import BiosVfIOENVMe2OptionROM
from ucsmsdk.mometa.bios.BiosVfIOESlot1OptionROM import BiosVfIOESlot1OptionROM
from ucsmsdk.mometa.bios.BiosVfIOESlot2OptionROM import BiosVfIOESlot2OptionROM
from ucsmsdk.mometa.bios.BiosVfIOEMezz1OptionROM import BiosVfIOEMezz1OptionROM
from ucsmsdk.mometa.bios.BiosVfBootOptionRetry import BiosVfBootOptionRetry
from ucsmsdk.mometa.bios.BiosVfUSBConfiguration import BiosVfUSBConfiguration
from ucsmsdk.mometa.bios.BiosVfDramRefreshRate import BiosVfDramRefreshRate
from ucsmsdk.mometa.bios.BiosVfProcessorCState import BiosVfProcessorCState
from ucsmsdk.mometa.bios.BiosVfSBNVMe1OptionROM import BiosVfSBNVMe1OptionROM
from ucsmsdk.mometa.bios.BiosVfSBMezz1OptionROM import BiosVfSBMezz1OptionROM
from ucsmsdk.mometa.bios.BiosVfOnboardGraphics import BiosVfOnboardGraphics
from ucsmsdk.mometa.bios.BiosVfPOSTErrorPause import BiosVfPOSTErrorPause
from ucsmsdk.mometa.bios.BiosVfAllUSBDevices import BiosVfAllUSBDevices
from ucsmsdk.mometa.bios.BiosVfUSBBootConfig import BiosVfUSBBootConfig
from ucsmsdk.mometa.bios.BiosVfOnboardStorage import BiosVfOnboardStorage
from ucsmsdk.mometa.bios.BiosVfCPUPerformance import BiosVfCPUPerformance
from ucsmsdk.mometa.bios.BiosVfSIOC1OptionROM import BiosVfSIOC1OptionROM
from ucsmsdk.mometa.bios.BiosVfSIOC2OptionROM import BiosVfSIOC2OptionROM
from ucsmsdk.mometa.bios.BiosVfACPI10Support import BiosVfACPI10Support
from ucsmsdk.mometa.bios.BiosVfLvDIMMSupport import BiosVfLvDIMMSupport
from ucsmsdk.mometa.bios.BiosVfScrubPolicies import BiosVfScrubPolicies
from ucsmsdk.mometa.bios.BiosVfMirroringMode import BiosVfMirroringMode
from ucsmsdk.mometa.bios.BiosVfQPISnoopMode import BiosVfQPISnoopMode
from ucsmsdk.mometa.bios.BiosVfNUMAOptimized import BiosVfNUMAOptimized
from ucsmsdk.mometa.bios.BiosVfProcessorCMCI import BiosVfProcessorCMCI
from ucsmsdk.mometa.bios.BiosVfLocalX2Apic import BiosVfLocalX2Apic
from ucsmsdk.mometa.bios.BiosVfProcessorC1E import BiosVfProcessorC1E
from ucsmsdk.mometa.bios.BiosVfVGAPriority import BiosVfVGAPriority
from ucsmsdk.mometa.bios.BiosVfASPMSupport import BiosVfASPMSupport
from ucsmsdk.mometa.bios.BiosVfSparingMode import BiosVfSparingMode
from ucsmsdk.mometa.bios.BiosVfFRB2Timer import BiosVfFRB2Timer
from ucsmsdk.mometa.bios.BiosVfPCIROMCLP import BiosVfPCIROMCLP
from ucsmsdk.mometa.bios.BiosVfQuietBoot import BiosVfQuietBoot
from ucsmsdk.mometa.bios.BiosVfAltitude import BiosVfAltitude
from ucsmsdk.mometa.equipment.EquipmentChassisProfile import EquipmentChassisProfile
from ucsmsdk.mometa.vm.VmLifeCyclePolicy import VmLifeCyclePolicy
from ucsmsdk.mometa.fabric.FabricLacpPolicy import FabricLacpPolicy
from ucsmsdk.mometa.firmware.FirmwareAutoSyncPolicy import FirmwareAutoSyncPolicy
from ucsmsdk.mometa.fabric.FabricUdldPolicy import FabricUdldPolicy
from ucsmsdk.mometa.compute.ComputePsuPolicy import ComputePsuPolicy
from ucsmsdk.mometa.vnic.VnicVnicBehPolicy import VnicVnicBehPolicy
from ucsmsdk.mometa.vnic.VnicVhbaBehPolicy import VnicVhbaBehPolicy
from ucsmsdk.mometa.sysdebug.SysdebugBackupBehavior import SysdebugBackupBehavior
from ucsmsdk.mometa.fabric.FabricVlan import FabricVlan
from ucsmsdk.mometa.fabric.FabricVsan import FabricVsan
from ucsmsdk.mometa.stats.StatsThresholdClass import StatsThresholdClass
from ucsmsdk.mometa.stats.StatsThr64Definition import StatsThr64Definition
from ucsmsdk.mometa.stats.StatsThr64Value import StatsThr64Value
from ucsmsdk.mometa.fabric.FabricDceSwSrvEp import FabricDceSwSrvEp
from ucsmsdk.mometa.fabric.FabricLanCloud import FabricLanCloud
from ucsmsdk.mometa.fabric.FabricEthLinkProfile import FabricEthLinkProfile
from ucsmsdk.mometa.fabric.FabricUdldLinkPolicy import FabricUdldLinkPolicy
from ucsmsdk.mometa.fabric.FabricNetGroup import FabricNetGroup
from ucsmsdk.mometa.fabric.FabricEthVlanPc import FabricEthVlanPc
from ucsmsdk.mometa.fabric.FabricPooledVlan import FabricPooledVlan
from ucsmsdk.mometa.mgmt.MgmtInbandProfile import MgmtInbandProfile
from ucsmsdk.mometa.flowctrl.FlowctrlDefinition import FlowctrlDefinition
from ucsmsdk.mometa.flowctrl.FlowctrlItem import FlowctrlItem
from ucsmsdk.mometa.qosclass.QosclassDefinition import QosclassDefinition
from ucsmsdk.mometa.qosclass.QosclassEthBE import QosclassEthBE
from ucsmsdk.mometa.qosclass.QosclassEthClassified import QosclassEthClassified
from ucsmsdk.mometa.qosclass.QosclassFc import QosclassFc
from ucsmsdk.mometa.fabric.FabricEthLanPc import FabricEthLanPc
from ucsmsdk.mometa.fabric.FabricEthLanPcEp import FabricEthLanPcEp
from ucsmsdk.mometa.fabric.FabricSanCloud import FabricSanCloud
from ucsmsdk.mometa.fabric.FabricFcSan import FabricFcSan
from ucsmsdk.mometa.fault.FaultPolicy import FaultPolicy
from ucsmsdk.mometa.stats.StatsCollectionPolicy import StatsCollectionPolicy
from ucsmsdk.mometa.extmgmt.ExtmgmtIfMonPolicy import ExtmgmtIfMonPolicy
from ucsmsdk.mometa.extmgmt.ExtmgmtNdiscTargets import ExtmgmtNdiscTargets
from ucsmsdk.mometa.extmgmt.ExtmgmtArpTargets import ExtmgmtArpTargets
from ucsmsdk.mometa.extmgmt.ExtmgmtMiiStatus import ExtmgmtMiiStatus
from ucsmsdk.mometa.trig.TrigSched import TrigSched
from ucsmsdk.mometa.trig.TrigLocalSched import TrigLocalSched
from ucsmsdk.mometa.controller.ControllerHaController import ControllerHaController
from ucsmsdk.mometa.top.TopInfoPolicy import TopInfoPolicy
from ucsmsdk.mometa.vm.VmSwitch import VmSwitch
from ucsmsdk.mometa.extvmm.ExtvmmMasterExtKey import ExtvmmMasterExtKey
from ucsmsdk.mometa.comm.CommWebSvcLimits import CommWebSvcLimits
from ucsmsdk.mometa.comm.CommDateTime import CommDateTime
from ucsmsdk.mometa.comm.CommNtpProvider import CommNtpProvider
from ucsmsdk.mometa.comm.CommTelnet import CommTelnet
from ucsmsdk.mometa.comm.CommCimxml import CommCimxml
from ucsmsdk.mometa.comm.CommHttps import CommHttps
from ucsmsdk.mometa.comm.CommSnmp import CommSnmp
from ucsmsdk.mometa.comm.CommHttp import CommHttp
from ucsmsdk.mometa.comm.CommDns import CommDns
from ucsmsdk.mometa.comm.CommDnsProvider import CommDnsProvider
from ucsmsdk.mometa.comm.CommSyslog import CommSyslog
from ucsmsdk.mometa.comm.CommSyslogClient import CommSyslogClient
from ucsmsdk.mometa.comm.CommSyslogMonitor import CommSyslogMonitor
from ucsmsdk.mometa.comm.CommSyslogConsole import CommSyslogConsole
from ucsmsdk.mometa.comm.CommSyslogSource import CommSyslogSource
from ucsmsdk.mometa.comm.CommSyslogFile import CommSyslogFile



obj = handle.query_dn("org-root")
mo = handle.query_dn("org-root/chassis-conn-policy-chassis-2-fabric-A")
mo.policy_owner = "local"
mo.backplane_speed_pref = "global"
mo.admin_state = "global"
handle.set_mo(mo)
handle.commit()

obj = handle.query_dn("org-root")
mo = handle.query_dn("org-root/chassis-conn-policy-chassis-1-fabric-A")
mo.policy_owner = "local"
mo.backplane_speed_pref = "global"
mo.admin_state = "global"
handle.set_mo(mo)
handle.commit()

obj = handle.query_dn("org-root")
mo = handle.query_dn("org-root/chassis-conn-policy-chassis-4-fabric-A")
mo.policy_owner = "local"
mo.backplane_speed_pref = "global"
mo.admin_state = "global"
handle.set_mo(mo)
handle.commit()

obj = handle.query_dn("org-root")
mo = CpmaintMaintPolicy(parent_mo_or_dn=obj, policy_owner="local", uptime_disr="user-ack", name="UCS-S3260-Main", descr="Maintenance Policy for UCS S3260")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = LstorageDiskZoningPolicy(parent_mo_or_dn=obj, preserve_config="no", policy_owner="local", descr="Disk Zoning for UCS S3260", name="UCS-S3260-Zoning")
mo_1 = LstorageDiskSlot(parent_mo_or_dn=mo, id="49", ownership="dedicated")
mo_2 = LstorageControllerRef(parent_mo_or_dn=mo_1, controller_type="SAS", server_id="2", controller_id="1")
mo_3 = LstorageDiskSlot(parent_mo_or_dn=mo, id="39", ownership="dedicated")
mo_4 = LstorageControllerRef(parent_mo_or_dn=mo_3, controller_type="SAS", server_id="2", controller_id="1")
mo_5 = LstorageDiskSlot(parent_mo_or_dn=mo, id="29", ownership="dedicated")
mo_6 = LstorageControllerRef(parent_mo_or_dn=mo_5, controller_type="SAS", server_id="1", controller_id="1")
mo_7 = LstorageDiskSlot(parent_mo_or_dn=mo, id="19", ownership="dedicated")
mo_8 = LstorageControllerRef(parent_mo_or_dn=mo_7, controller_type="SAS", server_id="1", controller_id="1")
mo_9 = LstorageDiskSlot(parent_mo_or_dn=mo, id="48", ownership="dedicated")
mo_10 = LstorageControllerRef(parent_mo_or_dn=mo_9, controller_type="SAS", server_id="2", controller_id="1")
mo_11 = LstorageDiskSlot(parent_mo_or_dn=mo, id="38", ownership="dedicated")
mo_12 = LstorageControllerRef(parent_mo_or_dn=mo_11, controller_type="SAS", server_id="2", controller_id="1")
mo_13 = LstorageDiskSlot(parent_mo_or_dn=mo, id="28", ownership="dedicated")
mo_14 = LstorageControllerRef(parent_mo_or_dn=mo_13, controller_type="SAS", server_id="1", controller_id="1")
mo_15 = LstorageDiskSlot(parent_mo_or_dn=mo, id="18", ownership="dedicated")
mo_16 = LstorageControllerRef(parent_mo_or_dn=mo_15, controller_type="SAS", server_id="1", controller_id="1")
mo_17 = LstorageDiskSlot(parent_mo_or_dn=mo, id="47", ownership="dedicated")
mo_18 = LstorageControllerRef(parent_mo_or_dn=mo_17, controller_type="SAS", server_id="2", controller_id="1")
mo_19 = LstorageDiskSlot(parent_mo_or_dn=mo, id="37", ownership="dedicated")
mo_20 = LstorageControllerRef(parent_mo_or_dn=mo_19, controller_type="SAS", server_id="2", controller_id="1")
mo_21 = LstorageDiskSlot(parent_mo_or_dn=mo, id="27", ownership="dedicated")
mo_22 = LstorageControllerRef(parent_mo_or_dn=mo_21, controller_type="SAS", server_id="1", controller_id="1")
mo_23 = LstorageDiskSlot(parent_mo_or_dn=mo, id="17", ownership="dedicated")
mo_24 = LstorageControllerRef(parent_mo_or_dn=mo_23, controller_type="SAS", server_id="1", controller_id="1")
mo_25 = LstorageDiskSlot(parent_mo_or_dn=mo, id="56", ownership="dedicated")
mo_26 = LstorageControllerRef(parent_mo_or_dn=mo_25, controller_type="SAS", server_id="2", controller_id="1")
mo_27 = LstorageDiskSlot(parent_mo_or_dn=mo, id="46", ownership="dedicated")
mo_28 = LstorageControllerRef(parent_mo_or_dn=mo_27, controller_type="SAS", server_id="2", controller_id="1")
mo_29 = LstorageDiskSlot(parent_mo_or_dn=mo, id="36", ownership="dedicated")
mo_30 = LstorageControllerRef(parent_mo_or_dn=mo_29, controller_type="SAS", server_id="2", controller_id="1")
mo_31 = LstorageDiskSlot(parent_mo_or_dn=mo, id="26", ownership="dedicated")
mo_32 = LstorageControllerRef(parent_mo_or_dn=mo_31, controller_type="SAS", server_id="1", controller_id="1")
mo_33 = LstorageDiskSlot(parent_mo_or_dn=mo, id="16", ownership="dedicated")
mo_34 = LstorageControllerRef(parent_mo_or_dn=mo_33, controller_type="SAS", server_id="1", controller_id="1")
mo_35 = LstorageDiskSlot(parent_mo_or_dn=mo, id="55", ownership="dedicated")
mo_36 = LstorageControllerRef(parent_mo_or_dn=mo_35, controller_type="SAS", server_id="2", controller_id="1")
mo_37 = LstorageDiskSlot(parent_mo_or_dn=mo, id="45", ownership="dedicated")
mo_38 = LstorageControllerRef(parent_mo_or_dn=mo_37, controller_type="SAS", server_id="2", controller_id="1")
mo_39 = LstorageDiskSlot(parent_mo_or_dn=mo, id="35", ownership="dedicated")
mo_40 = LstorageControllerRef(parent_mo_or_dn=mo_39, controller_type="SAS", server_id="2", controller_id="1")
mo_41 = LstorageDiskSlot(parent_mo_or_dn=mo, id="25", ownership="dedicated")
mo_42 = LstorageControllerRef(parent_mo_or_dn=mo_41, controller_type="SAS", server_id="1", controller_id="1")
mo_43 = LstorageDiskSlot(parent_mo_or_dn=mo, id="15", ownership="dedicated")
mo_44 = LstorageControllerRef(parent_mo_or_dn=mo_43, controller_type="SAS", server_id="1", controller_id="1")
mo_45 = LstorageDiskSlot(parent_mo_or_dn=mo, id="54", ownership="dedicated")
mo_46 = LstorageControllerRef(parent_mo_or_dn=mo_45, controller_type="SAS", server_id="2", controller_id="1")
mo_47 = LstorageDiskSlot(parent_mo_or_dn=mo, id="44", ownership="dedicated")
mo_48 = LstorageControllerRef(parent_mo_or_dn=mo_47, controller_type="SAS", server_id="2", controller_id="1")
mo_49 = LstorageDiskSlot(parent_mo_or_dn=mo, id="34", ownership="dedicated")
mo_50 = LstorageControllerRef(parent_mo_or_dn=mo_49, controller_type="SAS", server_id="2", controller_id="1")
mo_51 = LstorageDiskSlot(parent_mo_or_dn=mo, id="24", ownership="dedicated")
mo_52 = LstorageControllerRef(parent_mo_or_dn=mo_51, controller_type="SAS", server_id="1", controller_id="1")
mo_53 = LstorageDiskSlot(parent_mo_or_dn=mo, id="14", ownership="dedicated")
mo_54 = LstorageControllerRef(parent_mo_or_dn=mo_53, controller_type="SAS", server_id="1", controller_id="1")
mo_55 = LstorageDiskSlot(parent_mo_or_dn=mo, id="53", ownership="dedicated")
mo_56 = LstorageControllerRef(parent_mo_or_dn=mo_55, controller_type="SAS", server_id="2", controller_id="1")
mo_57 = LstorageDiskSlot(parent_mo_or_dn=mo, id="43", ownership="dedicated")
mo_58 = LstorageControllerRef(parent_mo_or_dn=mo_57, controller_type="SAS", server_id="2", controller_id="1")
mo_59 = LstorageDiskSlot(parent_mo_or_dn=mo, id="33", ownership="dedicated")
mo_60 = LstorageControllerRef(parent_mo_or_dn=mo_59, controller_type="SAS", server_id="2", controller_id="1")
mo_61 = LstorageDiskSlot(parent_mo_or_dn=mo, id="23", ownership="dedicated")
mo_62 = LstorageControllerRef(parent_mo_or_dn=mo_61, controller_type="SAS", server_id="1", controller_id="1")
mo_63 = LstorageDiskSlot(parent_mo_or_dn=mo, id="13", ownership="dedicated")
mo_64 = LstorageControllerRef(parent_mo_or_dn=mo_63, controller_type="SAS", server_id="1", controller_id="1")
mo_65 = LstorageDiskSlot(parent_mo_or_dn=mo, id="52", ownership="dedicated")
mo_66 = LstorageControllerRef(parent_mo_or_dn=mo_65, controller_type="SAS", server_id="2", controller_id="1")
mo_67 = LstorageDiskSlot(parent_mo_or_dn=mo, id="42", ownership="dedicated")
mo_68 = LstorageControllerRef(parent_mo_or_dn=mo_67, controller_type="SAS", server_id="2", controller_id="1")
mo_69 = LstorageDiskSlot(parent_mo_or_dn=mo, id="32", ownership="dedicated")
mo_70 = LstorageControllerRef(parent_mo_or_dn=mo_69, controller_type="SAS", server_id="1", controller_id="1")
mo_71 = LstorageDiskSlot(parent_mo_or_dn=mo, id="22", ownership="dedicated")
mo_72 = LstorageControllerRef(parent_mo_or_dn=mo_71, controller_type="SAS", server_id="1", controller_id="1")
mo_73 = LstorageDiskSlot(parent_mo_or_dn=mo, id="12", ownership="dedicated")
mo_74 = LstorageControllerRef(parent_mo_or_dn=mo_73, controller_type="SAS", server_id="1", controller_id="1")
mo_75 = LstorageDiskSlot(parent_mo_or_dn=mo, id="51", ownership="dedicated")
mo_76 = LstorageControllerRef(parent_mo_or_dn=mo_75, controller_type="SAS", server_id="2", controller_id="1")
mo_77 = LstorageDiskSlot(parent_mo_or_dn=mo, id="41", ownership="dedicated")
mo_78 = LstorageControllerRef(parent_mo_or_dn=mo_77, controller_type="SAS", server_id="2", controller_id="1")
mo_79 = LstorageDiskSlot(parent_mo_or_dn=mo, id="31", ownership="dedicated")
mo_80 = LstorageControllerRef(parent_mo_or_dn=mo_79, controller_type="SAS", server_id="1", controller_id="1")
mo_81 = LstorageDiskSlot(parent_mo_or_dn=mo, id="21", ownership="dedicated")
mo_82 = LstorageControllerRef(parent_mo_or_dn=mo_81, controller_type="SAS", server_id="1", controller_id="1")
mo_83 = LstorageDiskSlot(parent_mo_or_dn=mo, id="11", ownership="dedicated")
mo_84 = LstorageControllerRef(parent_mo_or_dn=mo_83, controller_type="SAS", server_id="1", controller_id="1")
mo_85 = LstorageDiskSlot(parent_mo_or_dn=mo, id="50", ownership="dedicated")
mo_86 = LstorageControllerRef(parent_mo_or_dn=mo_85, controller_type="SAS", server_id="2", controller_id="1")
mo_87 = LstorageDiskSlot(parent_mo_or_dn=mo, id="40", ownership="dedicated")
mo_88 = LstorageControllerRef(parent_mo_or_dn=mo_87, controller_type="SAS", server_id="2", controller_id="1")
mo_89 = LstorageDiskSlot(parent_mo_or_dn=mo, id="30", ownership="dedicated")
mo_90 = LstorageControllerRef(parent_mo_or_dn=mo_89, controller_type="SAS", server_id="1", controller_id="1")
mo_91 = LstorageDiskSlot(parent_mo_or_dn=mo, id="20", ownership="dedicated")
mo_92 = LstorageControllerRef(parent_mo_or_dn=mo_91, controller_type="SAS", server_id="1", controller_id="1")
mo_93 = LstorageDiskSlot(parent_mo_or_dn=mo, id="10", ownership="dedicated")
mo_94 = LstorageControllerRef(parent_mo_or_dn=mo_93, controller_type="SAS", server_id="1", controller_id="1")
mo_95 = LstorageDiskSlot(parent_mo_or_dn=mo, id="9", ownership="dedicated")
mo_96 = LstorageControllerRef(parent_mo_or_dn=mo_95, controller_type="SAS", server_id="1", controller_id="1")
mo_97 = LstorageDiskSlot(parent_mo_or_dn=mo, id="8", ownership="dedicated")
mo_98 = LstorageControllerRef(parent_mo_or_dn=mo_97, controller_type="SAS", server_id="2", controller_id="1")
mo_99 = LstorageDiskSlot(parent_mo_or_dn=mo, id="7", ownership="dedicated")
mo_100 = LstorageControllerRef(parent_mo_or_dn=mo_99, controller_type="SAS", server_id="2", controller_id="1")
mo_101 = LstorageDiskSlot(parent_mo_or_dn=mo, id="6", ownership="dedicated")
mo_102 = LstorageControllerRef(parent_mo_or_dn=mo_101, controller_type="SAS", server_id="2", controller_id="1")
mo_103 = LstorageDiskSlot(parent_mo_or_dn=mo, id="5", ownership="dedicated")
mo_104 = LstorageControllerRef(parent_mo_or_dn=mo_103, controller_type="SAS", server_id="2", controller_id="1")
mo_105 = LstorageDiskSlot(parent_mo_or_dn=mo, id="4", ownership="dedicated")
mo_106 = LstorageControllerRef(parent_mo_or_dn=mo_105, controller_type="SAS", server_id="1", controller_id="1")
mo_107 = LstorageDiskSlot(parent_mo_or_dn=mo, id="3", ownership="dedicated")
mo_108 = LstorageControllerRef(parent_mo_or_dn=mo_107, controller_type="SAS", server_id="1", controller_id="1")
mo_109 = LstorageDiskSlot(parent_mo_or_dn=mo, id="2", ownership="dedicated")
mo_110 = LstorageControllerRef(parent_mo_or_dn=mo_109, controller_type="SAS", server_id="1", controller_id="1")
mo_111 = LstorageDiskSlot(parent_mo_or_dn=mo, id="1", ownership="dedicated")
mo_112 = LstorageControllerRef(parent_mo_or_dn=mo_111, controller_type="SAS", server_id="1", controller_id="1")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = LstorageDiskGroupConfigPolicy(parent_mo_or_dn=obj, policy_owner="local", raid_level="mirror", name="C220M4S-MRAID")
mo_1 = LstorageVirtualDriveDef(parent_mo_or_dn=mo, read_policy="platform-default", drive_cache="platform-default", strip_size="platform-default", io_policy="platform-default", write_cache_policy="platform-default", access_policy="platform-default")
mo_2 = LstorageLocalDiskConfigRef(parent_mo_or_dn=mo, role="normal", slot_num="2", span_id="unspecified")
mo_3 = LstorageLocalDiskConfigRef(parent_mo_or_dn=mo, role="normal", slot_num="1", span_id="unspecified")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = LstorageDiskGroupConfigPolicy(parent_mo_or_dn=obj, policy_owner="local", raid_level="stripe", name="S3260-Boot-R0")
mo_1 = LstorageVirtualDriveDef(parent_mo_or_dn=mo, read_policy="platform-default", drive_cache="platform-default", strip_size="platform-default", io_policy="platform-default", write_cache_policy="platform-default", access_policy="platform-default")
mo_2 = LstorageLocalDiskConfigRef(parent_mo_or_dn=mo, role="normal", slot_num="201", span_id="unspecified")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = FirmwareChassisPack(parent_mo_or_dn=obj, chassis_bundle_version="3.1(2f)C", name="UCS-S3260-Firm", descr="Firmware Package for UCS S3260", stage_size="0", update_trigger="immediate", force_deploy="no", policy_owner="local", mode="staged", override_default_exclusion="yes")
mo_1 = FirmwarePackItem(parent_mo_or_dn=mo, hw_model="UCSC-C3260-SIOC", version="1.0.14", type="chassis-board-controller", hw_vendor="Cisco Systems Inc")
mo_2 = FirmwarePackItem(parent_mo_or_dn=mo, hw_model="UCSC-C3X60-BASE", version="04.08.01.B073", type="sas-expander", hw_vendor="Cisco Systems Inc")
mo_3 = FirmwarePackItem(parent_mo_or_dn=mo, hw_model="UCS-C460-M4", version="65.10.40.00", type="sas-expander", hw_vendor="Cisco Systems Inc")
mo_4 = FirmwarePackItem(parent_mo_or_dn=mo, hw_model="UCS-C240-M4", version="65.10.40.00", type="sas-expander", hw_vendor="Cisco Systems Inc")
mo_5 = FirmwarePackItem(parent_mo_or_dn=mo, hw_model="UCSC-C3260-SIOC", version="4.1(2d)", type="iocard", hw_vendor="Cisco Systems Inc")
mo_6 = FirmwarePackItem(parent_mo_or_dn=mo, hw_model="UCSC-C3260-SIOC", version="2.0(13j)", type="cmc", hw_vendor="Cisco Systems Inc")
mo_7 = FirmwareExcludeChassisComponent(parent_mo_or_dn=mo, chassis_component="local-disk")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = CpmaintMaintPolicy(parent_mo_or_dn=obj, policy_owner="local", uptime_disr="user-ack", name="default")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = handle.query_dn("org-root/chassis-qualifier-all-chassis")
mo_1 = handle.query_dn("org-root/chassis-qualifier-all-chassis/chassis-from-1-to-40")
handle.commit()

obj = handle.query_dn("org-root")
mo = LstorageDiskGroupConfigPolicy(parent_mo_or_dn=obj, policy_owner="local", raid_level="mirror", name="C220M4S-LSI")
mo_1 = LstorageVirtualDriveDef(parent_mo_or_dn=mo, read_policy="platform-default", drive_cache="platform-default", strip_size="platform-default", io_policy="platform-default", write_cache_policy="platform-default", access_policy="platform-default")
mo_2 = LstorageLocalDiskConfigRef(parent_mo_or_dn=mo, role="normal", slot_num="10", span_id="unspecified")
mo_3 = LstorageLocalDiskConfigRef(parent_mo_or_dn=mo, role="normal", slot_num="6", span_id="unspecified")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = LstorageDiskGroupConfigPolicy(parent_mo_or_dn=obj, policy_owner="local", raid_level="mirror", name="S3260-Boot")
mo_1 = LstorageVirtualDriveDef(parent_mo_or_dn=mo, read_policy="platform-default", drive_cache="platform-default", strip_size="platform-default", io_policy="platform-default", write_cache_policy="platform-default", access_policy="platform-default")
mo_2 = LstorageLocalDiskConfigRef(parent_mo_or_dn=mo, role="normal", slot_num="202", span_id="unspecified")
mo_3 = LstorageLocalDiskConfigRef(parent_mo_or_dn=mo, role="normal", slot_num="201", span_id="unspecified")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = UuidpoolPool(parent_mo_or_dn=obj, name="UCS-Ceph-UUID-Pool", prefix="17C349D0-C5E9-11E6", policy_owner="local", descr="UUID Pool for S3260 and C220 M4S", assignment_order="sequential")
mo_1 = UuidpoolBlock(parent_mo_or_dn=mo, to="0000-111122221123", r_from="0000-111122221110")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = IppoolPool(parent_mo_or_dn=obj, is_net_bios_enabled="disabled", name="iscsi-initiator-pool", policy_owner="local", ext_managed="internal", supports_dhcp="disabled", guid="00000000-0000-0000-0000-000000000000", assignment_order="default")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = ComputeQual(parent_mo_or_dn=obj, policy_owner="local", name="all-chassis")
mo_1 = ComputeChassisQual(parent_mo_or_dn=mo, min_id="1", max_id="40")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = LstorageDiskGroupConfigPolicy(parent_mo_or_dn=obj, policy_owner="local", raid_level="stripe", descr="RAID 0 Disk Group for Disk ID 49", name="R0_HDD_49")
mo_1 = LstorageVirtualDriveDef(parent_mo_or_dn=mo, read_policy="read-ahead", drive_cache="disable", strip_size="platform-default", io_policy="direct", write_cache_policy="always-write-back", access_policy="platform-default")
mo_2 = LstorageLocalDiskConfigRef(parent_mo_or_dn=mo, role="normal", slot_num="49", span_id="unspecified")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = LstorageDiskGroupConfigPolicy(parent_mo_or_dn=obj, policy_owner="local", raid_level="stripe", descr="RAID 0 Disk Group for Disk ID 39", name="R0_HDD_39")
mo_1 = LstorageVirtualDriveDef(parent_mo_or_dn=mo, read_policy="read-ahead", drive_cache="disable", strip_size="platform-default", io_policy="direct", write_cache_policy="always-write-back", access_policy="platform-default")
mo_2 = LstorageLocalDiskConfigRef(parent_mo_or_dn=mo, role="normal", slot_num="39", span_id="unspecified")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = LstorageDiskGroupConfigPolicy(parent_mo_or_dn=obj, policy_owner="local", raid_level="stripe", descr="RAID 0 Disk Group for Disk ID 29", name="R0_HDD_29")
mo_1 = LstorageVirtualDriveDef(parent_mo_or_dn=mo, read_policy="read-ahead", drive_cache="disable", strip_size="platform-default", io_policy="direct", write_cache_policy="always-write-back", access_policy="platform-default")
mo_2 = LstorageLocalDiskConfigRef(parent_mo_or_dn=mo, role="normal", slot_num="29", span_id="unspecified")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = LstorageDiskGroupConfigPolicy(parent_mo_or_dn=obj, policy_owner="local", raid_level="stripe", descr="RAID 0 Disk Group for Disk ID 19", name="R0_HDD_19")
mo_1 = LstorageVirtualDriveDef(parent_mo_or_dn=mo, read_policy="read-ahead", drive_cache="disable", strip_size="platform-default", io_policy="direct", write_cache_policy="always-write-back", access_policy="platform-default")
mo_2 = LstorageLocalDiskConfigRef(parent_mo_or_dn=mo, role="normal", slot_num="19", span_id="unspecified")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = LstorageDiskGroupConfigPolicy(parent_mo_or_dn=obj, policy_owner="local", raid_level="stripe", descr="RAID 0 Disk Group for Disk ID 48", name="R0_HDD_48")
mo_1 = LstorageVirtualDriveDef(parent_mo_or_dn=mo, read_policy="read-ahead", drive_cache="disable", strip_size="platform-default", io_policy="direct", write_cache_policy="always-write-back", access_policy="platform-default")
mo_2 = LstorageLocalDiskConfigRef(parent_mo_or_dn=mo, role="normal", slot_num="48", span_id="unspecified")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = LstorageDiskGroupConfigPolicy(parent_mo_or_dn=obj, policy_owner="local", raid_level="stripe", descr="RAID 0 Disk Group for Disk ID 38", name="R0_HDD_38")
mo_1 = LstorageVirtualDriveDef(parent_mo_or_dn=mo, read_policy="read-ahead", drive_cache="disable", strip_size="platform-default", io_policy="direct", write_cache_policy="always-write-back", access_policy="platform-default")
mo_2 = LstorageLocalDiskConfigRef(parent_mo_or_dn=mo, role="normal", slot_num="38", span_id="unspecified")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = LstorageDiskGroupConfigPolicy(parent_mo_or_dn=obj, policy_owner="local", raid_level="stripe", descr="RAID 0 Disk Group for Disk ID 28", name="R0_HDD_28")
mo_1 = LstorageVirtualDriveDef(parent_mo_or_dn=mo, read_policy="read-ahead", drive_cache="disable", strip_size="platform-default", io_policy="direct", write_cache_policy="always-write-back", access_policy="platform-default")
mo_2 = LstorageLocalDiskConfigRef(parent_mo_or_dn=mo, role="normal", slot_num="28", span_id="unspecified")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = LstorageDiskGroupConfigPolicy(parent_mo_or_dn=obj, policy_owner="local", raid_level="stripe", descr="RAID 0 Disk Group for Disk ID 18", name="R0_HDD_18")
mo_1 = LstorageVirtualDriveDef(parent_mo_or_dn=mo, read_policy="read-ahead", drive_cache="disable", strip_size="platform-default", io_policy="direct", write_cache_policy="always-write-back", access_policy="platform-default")
mo_2 = LstorageLocalDiskConfigRef(parent_mo_or_dn=mo, role="normal", slot_num="18", span_id="unspecified")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = LstorageDiskGroupConfigPolicy(parent_mo_or_dn=obj, policy_owner="local", raid_level="stripe", descr="RAID 0 Disk Group for Disk ID 47", name="R0_HDD_47")
mo_1 = LstorageVirtualDriveDef(parent_mo_or_dn=mo, read_policy="read-ahead", drive_cache="disable", strip_size="platform-default", io_policy="direct", write_cache_policy="always-write-back", access_policy="platform-default")
mo_2 = LstorageLocalDiskConfigRef(parent_mo_or_dn=mo, role="normal", slot_num="47", span_id="unspecified")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = LstorageDiskGroupConfigPolicy(parent_mo_or_dn=obj, policy_owner="local", raid_level="stripe", descr="RAID 0 Disk Group for Disk ID 37", name="R0_HDD_37")
mo_1 = LstorageVirtualDriveDef(parent_mo_or_dn=mo, read_policy="read-ahead", drive_cache="disable", strip_size="platform-default", io_policy="direct", write_cache_policy="always-write-back", access_policy="platform-default")
mo_2 = LstorageLocalDiskConfigRef(parent_mo_or_dn=mo, role="normal", slot_num="37", span_id="unspecified")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = LstorageDiskGroupConfigPolicy(parent_mo_or_dn=obj, policy_owner="local", raid_level="stripe", descr="RAID 0 Disk Group for Disk ID 27", name="R0_HDD_27")
mo_1 = LstorageVirtualDriveDef(parent_mo_or_dn=mo, read_policy="read-ahead", drive_cache="disable", strip_size="platform-default", io_policy="direct", write_cache_policy="always-write-back", access_policy="platform-default")
mo_2 = LstorageLocalDiskConfigRef(parent_mo_or_dn=mo, role="normal", slot_num="27", span_id="unspecified")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = LstorageDiskGroupConfigPolicy(parent_mo_or_dn=obj, policy_owner="local", raid_level="stripe", descr="RAID 0 Disk Group for Disk ID 17", name="R0_HDD_17")
mo_1 = LstorageVirtualDriveDef(parent_mo_or_dn=mo, read_policy="read-ahead", drive_cache="disable", strip_size="platform-default", io_policy="direct", write_cache_policy="always-write-back", access_policy="platform-default")
mo_2 = LstorageLocalDiskConfigRef(parent_mo_or_dn=mo, role="normal", slot_num="17", span_id="unspecified")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = LstorageDiskGroupConfigPolicy(parent_mo_or_dn=obj, policy_owner="local", raid_level="stripe", descr="RAID 0 Disk Group for Disk ID 56", name="R0_HDD_56")
mo_1 = LstorageVirtualDriveDef(parent_mo_or_dn=mo, read_policy="read-ahead", drive_cache="disable", strip_size="platform-default", io_policy="direct", write_cache_policy="always-write-back", access_policy="platform-default")
mo_2 = LstorageLocalDiskConfigRef(parent_mo_or_dn=mo, role="normal", slot_num="56", span_id="unspecified")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = LstorageDiskGroupConfigPolicy(parent_mo_or_dn=obj, policy_owner="local", raid_level="stripe", descr="RAID 0 Disk Group for Disk ID 46", name="R0_HDD_46")
mo_1 = LstorageVirtualDriveDef(parent_mo_or_dn=mo, read_policy="read-ahead", drive_cache="disable", strip_size="platform-default", io_policy="direct", write_cache_policy="always-write-back", access_policy="platform-default")
mo_2 = LstorageLocalDiskConfigRef(parent_mo_or_dn=mo, role="normal", slot_num="46", span_id="unspecified")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = LstorageDiskGroupConfigPolicy(parent_mo_or_dn=obj, policy_owner="local", raid_level="stripe", descr="RAID 0 Disk Group for Disk ID 36", name="R0_HDD_36")
mo_1 = LstorageVirtualDriveDef(parent_mo_or_dn=mo, read_policy="read-ahead", drive_cache="disable", strip_size="platform-default", io_policy="direct", write_cache_policy="always-write-back", access_policy="platform-default")
mo_2 = LstorageLocalDiskConfigRef(parent_mo_or_dn=mo, role="normal", slot_num="36", span_id="unspecified")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = LstorageDiskGroupConfigPolicy(parent_mo_or_dn=obj, policy_owner="local", raid_level="stripe", descr="RAID 0 Disk Group for Disk ID 26", name="R0_HDD_26")
mo_1 = LstorageVirtualDriveDef(parent_mo_or_dn=mo, read_policy="read-ahead", drive_cache="disable", strip_size="platform-default", io_policy="direct", write_cache_policy="always-write-back", access_policy="platform-default")
mo_2 = LstorageLocalDiskConfigRef(parent_mo_or_dn=mo, role="normal", slot_num="26", span_id="unspecified")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = LstorageDiskGroupConfigPolicy(parent_mo_or_dn=obj, policy_owner="local", raid_level="stripe", descr="RAID 0 Disk Group for Disk ID 16", name="R0_HDD_16")
mo_1 = LstorageVirtualDriveDef(parent_mo_or_dn=mo, read_policy="read-ahead", drive_cache="disable", strip_size="platform-default", io_policy="direct", write_cache_policy="always-write-back", access_policy="platform-default")
mo_2 = LstorageLocalDiskConfigRef(parent_mo_or_dn=mo, role="normal", slot_num="16", span_id="unspecified")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = LstorageDiskGroupConfigPolicy(parent_mo_or_dn=obj, policy_owner="local", raid_level="stripe", descr="RAID 0 Disk Group for Disk ID 55", name="R0_HDD_55")
mo_1 = LstorageVirtualDriveDef(parent_mo_or_dn=mo, read_policy="read-ahead", drive_cache="disable", strip_size="platform-default", io_policy="direct", write_cache_policy="always-write-back", access_policy="platform-default")
mo_2 = LstorageLocalDiskConfigRef(parent_mo_or_dn=mo, role="normal", slot_num="55", span_id="unspecified")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = LstorageDiskGroupConfigPolicy(parent_mo_or_dn=obj, policy_owner="local", raid_level="stripe", descr="RAID 0 Disk Group for Disk ID 45", name="R0_HDD_45")
mo_1 = LstorageVirtualDriveDef(parent_mo_or_dn=mo, read_policy="read-ahead", drive_cache="disable", strip_size="platform-default", io_policy="direct", write_cache_policy="always-write-back", access_policy="platform-default")
mo_2 = LstorageLocalDiskConfigRef(parent_mo_or_dn=mo, role="normal", slot_num="45", span_id="unspecified")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = LstorageDiskGroupConfigPolicy(parent_mo_or_dn=obj, policy_owner="local", raid_level="stripe", descr="RAID 0 Disk Group for Disk ID 35", name="R0_HDD_35")
mo_1 = LstorageVirtualDriveDef(parent_mo_or_dn=mo, read_policy="read-ahead", drive_cache="disable", strip_size="platform-default", io_policy="direct", write_cache_policy="always-write-back", access_policy="platform-default")
mo_2 = LstorageLocalDiskConfigRef(parent_mo_or_dn=mo, role="normal", slot_num="35", span_id="unspecified")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = LstorageDiskGroupConfigPolicy(parent_mo_or_dn=obj, policy_owner="local", raid_level="stripe", descr="RAID 0 Disk Group for Disk ID 25", name="R0_HDD_25")
mo_1 = LstorageVirtualDriveDef(parent_mo_or_dn=mo, read_policy="read-ahead", drive_cache="disable", strip_size="platform-default", io_policy="direct", write_cache_policy="always-write-back", access_policy="platform-default")
mo_2 = LstorageLocalDiskConfigRef(parent_mo_or_dn=mo, role="normal", slot_num="25", span_id="unspecified")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = LstorageDiskGroupConfigPolicy(parent_mo_or_dn=obj, policy_owner="local", raid_level="stripe", descr="RAID 0 Disk Group for Disk ID 15", name="R0_HDD_15")
mo_1 = LstorageVirtualDriveDef(parent_mo_or_dn=mo, read_policy="read-ahead", drive_cache="disable", strip_size="platform-default", io_policy="direct", write_cache_policy="always-write-back", access_policy="platform-default")
mo_2 = LstorageLocalDiskConfigRef(parent_mo_or_dn=mo, role="normal", slot_num="15", span_id="unspecified")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = LstorageDiskGroupConfigPolicy(parent_mo_or_dn=obj, policy_owner="local", raid_level="stripe", descr="RAID 0 Disk Group for Disk ID 54", name="R0_HDD_54")
mo_1 = LstorageVirtualDriveDef(parent_mo_or_dn=mo, read_policy="read-ahead", drive_cache="disable", strip_size="platform-default", io_policy="direct", write_cache_policy="always-write-back", access_policy="platform-default")
mo_2 = LstorageLocalDiskConfigRef(parent_mo_or_dn=mo, role="normal", slot_num="54", span_id="unspecified")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = LstorageDiskGroupConfigPolicy(parent_mo_or_dn=obj, policy_owner="local", raid_level="stripe", descr="RAID 0 Disk Group for Disk ID 44", name="R0_HDD_44")
mo_1 = LstorageVirtualDriveDef(parent_mo_or_dn=mo, read_policy="read-ahead", drive_cache="disable", strip_size="platform-default", io_policy="direct", write_cache_policy="always-write-back", access_policy="platform-default")
mo_2 = LstorageLocalDiskConfigRef(parent_mo_or_dn=mo, role="normal", slot_num="44", span_id="unspecified")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = LstorageDiskGroupConfigPolicy(parent_mo_or_dn=obj, policy_owner="local", raid_level="stripe", descr="RAID 0 Disk Group for Disk ID 34", name="R0_HDD_34")
mo_1 = LstorageVirtualDriveDef(parent_mo_or_dn=mo, read_policy="read-ahead", drive_cache="disable", strip_size="platform-default", io_policy="direct", write_cache_policy="always-write-back", access_policy="platform-default")
mo_2 = LstorageLocalDiskConfigRef(parent_mo_or_dn=mo, role="normal", slot_num="34", span_id="unspecified")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = LstorageDiskGroupConfigPolicy(parent_mo_or_dn=obj, policy_owner="local", raid_level="stripe", descr="RAID 0 Disk Group for Disk ID 24", name="R0_HDD_24")
mo_1 = LstorageVirtualDriveDef(parent_mo_or_dn=mo, read_policy="read-ahead", drive_cache="disable", strip_size="platform-default", io_policy="direct", write_cache_policy="always-write-back", access_policy="platform-default")
mo_2 = LstorageLocalDiskConfigRef(parent_mo_or_dn=mo, role="normal", slot_num="24", span_id="unspecified")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = LstorageDiskGroupConfigPolicy(parent_mo_or_dn=obj, policy_owner="local", raid_level="stripe", descr="RAID 0 Disk Group for Disk ID 14", name="R0_HDD_14")
mo_1 = LstorageVirtualDriveDef(parent_mo_or_dn=mo, read_policy="read-ahead", drive_cache="disable", strip_size="platform-default", io_policy="direct", write_cache_policy="always-write-back", access_policy="platform-default")
mo_2 = LstorageLocalDiskConfigRef(parent_mo_or_dn=mo, role="normal", slot_num="14", span_id="unspecified")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = LstorageDiskGroupConfigPolicy(parent_mo_or_dn=obj, policy_owner="local", raid_level="stripe", descr="RAID 0 Disk Group for Disk ID 53", name="R0_HDD_53")
mo_1 = LstorageVirtualDriveDef(parent_mo_or_dn=mo, read_policy="read-ahead", drive_cache="disable", strip_size="platform-default", io_policy="direct", write_cache_policy="always-write-back", access_policy="platform-default")
mo_2 = LstorageLocalDiskConfigRef(parent_mo_or_dn=mo, role="normal", slot_num="53", span_id="unspecified")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = LstorageDiskGroupConfigPolicy(parent_mo_or_dn=obj, policy_owner="local", raid_level="stripe", descr="RAID 0 Disk Group for Disk ID 43", name="R0_HDD_43")
mo_1 = LstorageVirtualDriveDef(parent_mo_or_dn=mo, read_policy="read-ahead", drive_cache="disable", strip_size="platform-default", io_policy="direct", write_cache_policy="always-write-back", access_policy="platform-default")
mo_2 = LstorageLocalDiskConfigRef(parent_mo_or_dn=mo, role="normal", slot_num="43", span_id="unspecified")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = LstorageDiskGroupConfigPolicy(parent_mo_or_dn=obj, policy_owner="local", raid_level="stripe", descr="RAID 0 Disk Group for Disk ID 33", name="R0_HDD_33")
mo_1 = LstorageVirtualDriveDef(parent_mo_or_dn=mo, read_policy="read-ahead", drive_cache="disable", strip_size="platform-default", io_policy="direct", write_cache_policy="always-write-back", access_policy="platform-default")
mo_2 = LstorageLocalDiskConfigRef(parent_mo_or_dn=mo, role="normal", slot_num="33", span_id="unspecified")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = LstorageDiskGroupConfigPolicy(parent_mo_or_dn=obj, policy_owner="local", raid_level="stripe", descr="RAID 0 Disk Group for Disk ID 23", name="R0_HDD_23")
mo_1 = LstorageVirtualDriveDef(parent_mo_or_dn=mo, read_policy="read-ahead", drive_cache="disable", strip_size="platform-default", io_policy="direct", write_cache_policy="always-write-back", access_policy="platform-default")
mo_2 = LstorageLocalDiskConfigRef(parent_mo_or_dn=mo, role="normal", slot_num="23", span_id="unspecified")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = LstorageDiskGroupConfigPolicy(parent_mo_or_dn=obj, policy_owner="local", raid_level="stripe", descr="RAID 0 Disk Group for Disk ID 13", name="R0_HDD_13")
mo_1 = LstorageVirtualDriveDef(parent_mo_or_dn=mo, read_policy="read-ahead", drive_cache="disable", strip_size="platform-default", io_policy="direct", write_cache_policy="always-write-back", access_policy="platform-default")
mo_2 = LstorageLocalDiskConfigRef(parent_mo_or_dn=mo, role="normal", slot_num="13", span_id="unspecified")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = LstorageDiskGroupConfigPolicy(parent_mo_or_dn=obj, policy_owner="local", raid_level="stripe", descr="RAID 0 Disk Group for Disk ID 52", name="R0_HDD_52")
mo_1 = LstorageVirtualDriveDef(parent_mo_or_dn=mo, read_policy="read-ahead", drive_cache="disable", strip_size="platform-default", io_policy="direct", write_cache_policy="always-write-back", access_policy="platform-default")
mo_2 = LstorageLocalDiskConfigRef(parent_mo_or_dn=mo, role="normal", slot_num="52", span_id="unspecified")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = LstorageDiskGroupConfigPolicy(parent_mo_or_dn=obj, policy_owner="local", raid_level="stripe", descr="RAID 0 Disk Group for Disk ID 42", name="R0_HDD_42")
mo_1 = LstorageVirtualDriveDef(parent_mo_or_dn=mo, read_policy="read-ahead", drive_cache="disable", strip_size="platform-default", io_policy="direct", write_cache_policy="always-write-back", access_policy="platform-default")
mo_2 = LstorageLocalDiskConfigRef(parent_mo_or_dn=mo, role="normal", slot_num="42", span_id="unspecified")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = LstorageDiskGroupConfigPolicy(parent_mo_or_dn=obj, policy_owner="local", raid_level="stripe", descr="RAID 0 Disk Group for Disk ID 32", name="R0_HDD_32")
mo_1 = LstorageVirtualDriveDef(parent_mo_or_dn=mo, read_policy="read-ahead", drive_cache="disable", strip_size="platform-default", io_policy="direct", write_cache_policy="always-write-back", access_policy="platform-default")
mo_2 = LstorageLocalDiskConfigRef(parent_mo_or_dn=mo, role="normal", slot_num="32", span_id="unspecified")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = LstorageDiskGroupConfigPolicy(parent_mo_or_dn=obj, policy_owner="local", raid_level="stripe", descr="RAID 0 Disk Group for Disk ID 22", name="R0_HDD_22")
mo_1 = LstorageVirtualDriveDef(parent_mo_or_dn=mo, read_policy="read-ahead", drive_cache="disable", strip_size="platform-default", io_policy="direct", write_cache_policy="always-write-back", access_policy="platform-default")
mo_2 = LstorageLocalDiskConfigRef(parent_mo_or_dn=mo, role="normal", slot_num="22", span_id="unspecified")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = LstorageDiskGroupConfigPolicy(parent_mo_or_dn=obj, policy_owner="local", raid_level="stripe", descr="RAID 0 Disk Group for Disk ID 12", name="R0_HDD_12")
mo_1 = LstorageVirtualDriveDef(parent_mo_or_dn=mo, read_policy="read-ahead", drive_cache="disable", strip_size="platform-default", io_policy="direct", write_cache_policy="always-write-back", access_policy="platform-default")
mo_2 = LstorageLocalDiskConfigRef(parent_mo_or_dn=mo, role="normal", slot_num="12", span_id="unspecified")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = LstorageDiskGroupConfigPolicy(parent_mo_or_dn=obj, policy_owner="local", raid_level="stripe", descr="RAID 0 Disk Group for Disk ID 51", name="R0_HDD_51")
mo_1 = LstorageVirtualDriveDef(parent_mo_or_dn=mo, read_policy="read-ahead", drive_cache="disable", strip_size="platform-default", io_policy="direct", write_cache_policy="always-write-back", access_policy="platform-default")
mo_2 = LstorageLocalDiskConfigRef(parent_mo_or_dn=mo, role="normal", slot_num="51", span_id="unspecified")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = LstorageDiskGroupConfigPolicy(parent_mo_or_dn=obj, policy_owner="local", raid_level="stripe", descr="RAID 0 Disk Group for Disk ID 41", name="R0_HDD_41")
mo_1 = LstorageVirtualDriveDef(parent_mo_or_dn=mo, read_policy="read-ahead", drive_cache="disable", strip_size="platform-default", io_policy="direct", write_cache_policy="always-write-back", access_policy="platform-default")
mo_2 = LstorageLocalDiskConfigRef(parent_mo_or_dn=mo, role="normal", slot_num="41", span_id="unspecified")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = LstorageDiskGroupConfigPolicy(parent_mo_or_dn=obj, policy_owner="local", raid_level="stripe", descr="RAID 0 Disk Group for Disk ID 31", name="R0_HDD_31")
mo_1 = LstorageVirtualDriveDef(parent_mo_or_dn=mo, read_policy="read-ahead", drive_cache="disable", strip_size="platform-default", io_policy="direct", write_cache_policy="always-write-back", access_policy="platform-default")
mo_2 = LstorageLocalDiskConfigRef(parent_mo_or_dn=mo, role="normal", slot_num="31", span_id="unspecified")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = LstorageDiskGroupConfigPolicy(parent_mo_or_dn=obj, policy_owner="local", raid_level="stripe", descr="RAID 0 Disk Group for Disk ID 21", name="R0_HDD_21")
mo_1 = LstorageVirtualDriveDef(parent_mo_or_dn=mo, read_policy="read-ahead", drive_cache="disable", strip_size="platform-default", io_policy="direct", write_cache_policy="always-write-back", access_policy="platform-default")
mo_2 = LstorageLocalDiskConfigRef(parent_mo_or_dn=mo, role="normal", slot_num="21", span_id="unspecified")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = LstorageDiskGroupConfigPolicy(parent_mo_or_dn=obj, policy_owner="local", raid_level="stripe", descr="RAID 0 Disk Group for Disk ID 11", name="R0_HDD_11")
mo_1 = LstorageVirtualDriveDef(parent_mo_or_dn=mo, read_policy="read-ahead", drive_cache="disable", strip_size="platform-default", io_policy="direct", write_cache_policy="always-write-back", access_policy="platform-default")
mo_2 = LstorageLocalDiskConfigRef(parent_mo_or_dn=mo, role="normal", slot_num="11", span_id="unspecified")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = LstorageDiskGroupConfigPolicy(parent_mo_or_dn=obj, policy_owner="local", raid_level="stripe", descr="RAID 0 Disk Group for Disk ID 50", name="R0_HDD_50")
mo_1 = LstorageVirtualDriveDef(parent_mo_or_dn=mo, read_policy="read-ahead", drive_cache="disable", strip_size="platform-default", io_policy="direct", write_cache_policy="always-write-back", access_policy="platform-default")
mo_2 = LstorageLocalDiskConfigRef(parent_mo_or_dn=mo, role="normal", slot_num="50", span_id="unspecified")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = LstorageDiskGroupConfigPolicy(parent_mo_or_dn=obj, policy_owner="local", raid_level="stripe", descr="RAID 0 Disk Group for Disk ID 40", name="R0_HDD_40")
mo_1 = LstorageVirtualDriveDef(parent_mo_or_dn=mo, read_policy="read-ahead", drive_cache="disable", strip_size="platform-default", io_policy="direct", write_cache_policy="always-write-back", access_policy="platform-default")
mo_2 = LstorageLocalDiskConfigRef(parent_mo_or_dn=mo, role="normal", slot_num="40", span_id="unspecified")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = LstorageDiskGroupConfigPolicy(parent_mo_or_dn=obj, policy_owner="local", raid_level="stripe", descr="RAID 0 Disk Group for Disk ID 30", name="R0_HDD_30")
mo_1 = LstorageVirtualDriveDef(parent_mo_or_dn=mo, read_policy="read-ahead", drive_cache="disable", strip_size="platform-default", io_policy="direct", write_cache_policy="always-write-back", access_policy="platform-default")
mo_2 = LstorageLocalDiskConfigRef(parent_mo_or_dn=mo, role="normal", slot_num="30", span_id="unspecified")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = LstorageDiskGroupConfigPolicy(parent_mo_or_dn=obj, policy_owner="local", raid_level="stripe", descr="RAID 0 Disk Group for Disk ID 20", name="R0_HDD_20")
mo_1 = LstorageVirtualDriveDef(parent_mo_or_dn=mo, read_policy="read-ahead", drive_cache="disable", strip_size="platform-default", io_policy="direct", write_cache_policy="always-write-back", access_policy="platform-default")
mo_2 = LstorageLocalDiskConfigRef(parent_mo_or_dn=mo, role="normal", slot_num="20", span_id="unspecified")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = LstorageDiskGroupConfigPolicy(parent_mo_or_dn=obj, policy_owner="local", raid_level="stripe", descr="RAID 0 Disk Group for Disk ID 10", name="R0_HDD_10")
mo_1 = LstorageVirtualDriveDef(parent_mo_or_dn=mo, read_policy="read-ahead", drive_cache="disable", strip_size="platform-default", io_policy="direct", write_cache_policy="always-write-back", access_policy="platform-default")
mo_2 = LstorageLocalDiskConfigRef(parent_mo_or_dn=mo, role="normal", slot_num="10", span_id="unspecified")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = AdaptorHostEthIfProfile(parent_mo_or_dn=obj, policy_owner="local", name="VMWarePassThru", descr="Recommended adapter settings for VMWare pass-thru (dynamic vNIC)")
mo_1 = AdaptorEthInterruptScalingProfile(parent_mo_or_dn=mo, admin_state="disabled")
mo_2 = handle.query_dn("org-root/eth-profile-VMWarePassThru/ext-ipv6-rss-hash")
mo_3 = AdaptorEthAdvFilterProfile(parent_mo_or_dn=mo, admin_state="disabled")
mo_4 = handle.query_dn("org-root/eth-profile-VMWarePassThru/ipv6-rss-hash")
mo_5 = handle.query_dn("org-root/eth-profile-VMWarePassThru/ipv4-rss-hash")
mo_6 = AdaptorEthFailoverProfile(parent_mo_or_dn=mo, timeout="5")
mo_7 = AdaptorEthOffloadProfile(parent_mo_or_dn=mo, tcp_segment="enabled", large_receive="enabled", tcp_rx_checksum="enabled", tcp_tx_checksum="enabled")
mo_8 = AdaptorEthWorkQueueProfile(parent_mo_or_dn=mo, count="4", ring_size="256")
mo_9 = AdaptorEthCompQueueProfile(parent_mo_or_dn=mo, count="8")
mo_10 = AdaptorEthRecvQueueProfile(parent_mo_or_dn=mo, count="4", ring_size="512")
mo_11 = AdaptorEthVxLANProfile(parent_mo_or_dn=mo, admin_state="disabled")
mo_12 = AdaptorEthNVGREProfile(parent_mo_or_dn=mo, admin_state="disabled")
mo_13 = AdaptorEthArfsProfile(parent_mo_or_dn=mo, accelarated_rfs="disabled")
mo_14 = AdaptorEthRoCEProfile(parent_mo_or_dn=mo, admin_state="disabled", resource_groups="32", memory_regions="131072", queue_pairs="256")
mo_15 = AdaptorEthInterruptProfile(parent_mo_or_dn=mo, count="12", coalescing_type="min", mode="msi", coalescing_time="125")
mo_16 = AdaptorRssProfile(parent_mo_or_dn=mo, receive_side_scaling="enabled")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = LstorageDiskZoningPolicy(parent_mo_or_dn=obj, preserve_config="yes", policy_owner="local", name="default")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = MacpoolPool(parent_mo_or_dn=obj, policy_owner="local", assignment_order="sequential", descr="MAC Pool for S3260 and C220M4S", name="UCS-Ceph-MAC-Pool")
mo_1 = MacpoolBlock(parent_mo_or_dn=mo, to="00:25:B5:00:00:63", r_from="00:25:B5:00:00:00")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = ComputePool(parent_mo_or_dn=obj, policy_owner="local", name="C220M4S-MRAID")
mo_1 = ComputePooledRackUnit(parent_mo_or_dn=mo, id="7")
mo_2 = ComputePooledRackUnit(parent_mo_or_dn=mo, id="6")
mo_3 = ComputePooledRackUnit(parent_mo_or_dn=mo, id="5")
mo_4 = ComputePooledRackUnit(parent_mo_or_dn=mo, id="4")
mo_5 = ComputePooledRackUnit(parent_mo_or_dn=mo, id="2")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = VnicLanConnTempl(parent_mo_or_dn=obj, redundancy_pair_type="none", name="Default-NIC", descr="Default NIC Template", stats_policy_name="default", switch_id="A-B", mtu="1500", policy_owner="local", templ_type="initial-template", qos_policy_name="QoS-Ceph", target="adaptor", ident_pool_name="UCS-Ceph-MAC-Pool", cdn_source="vnic-name", nw_ctrl_policy_name="Enable-CDP")
mo_1 = VnicEtherIf(parent_mo_or_dn=mo, default_net="yes", name="default")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = VnicLanConnTempl(parent_mo_or_dn=obj, redundancy_pair_type="none", name="Cluster-NIC", descr="Cluster NIC Template", stats_policy_name="default", switch_id="B-A", mtu="9000", policy_owner="local", templ_type="initial-template", qos_policy_name="QoS-Ceph", target="adaptor", ident_pool_name="UCS-Ceph-MAC-Pool", cdn_source="vnic-name", nw_ctrl_policy_name="Enable-CDP")
mo_1 = VnicEtherIf(parent_mo_or_dn=mo, default_net="no", name="Cluster")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = AdaptorHostEthIfProfile(parent_mo_or_dn=obj, policy_owner="local", name="usNICOracleRAC", descr="Recommended adapter settings for usNIC Oracle RAC Connection")
mo_1 = AdaptorEthInterruptScalingProfile(parent_mo_or_dn=mo, admin_state="enabled")
mo_2 = handle.query_dn("org-root/eth-profile-usNICOracleRAC/ext-ipv6-rss-hash")
mo_3 = AdaptorEthAdvFilterProfile(parent_mo_or_dn=mo, admin_state="disabled")
mo_4 = handle.query_dn("org-root/eth-profile-usNICOracleRAC/ipv6-rss-hash")
mo_5 = handle.query_dn("org-root/eth-profile-usNICOracleRAC/ipv4-rss-hash")
mo_6 = AdaptorEthFailoverProfile(parent_mo_or_dn=mo, timeout="0")
mo_7 = AdaptorEthOffloadProfile(parent_mo_or_dn=mo, tcp_segment="enabled", large_receive="enabled", tcp_rx_checksum="enabled", tcp_tx_checksum="enabled")
mo_8 = AdaptorEthWorkQueueProfile(parent_mo_or_dn=mo, count="1000", ring_size="256")
mo_9 = AdaptorEthCompQueueProfile(parent_mo_or_dn=mo, count="2000")
mo_10 = AdaptorEthRecvQueueProfile(parent_mo_or_dn=mo, count="1000", ring_size="512")
mo_11 = AdaptorEthVxLANProfile(parent_mo_or_dn=mo, admin_state="disabled")
mo_12 = AdaptorEthNVGREProfile(parent_mo_or_dn=mo, admin_state="disabled")
mo_13 = AdaptorEthArfsProfile(parent_mo_or_dn=mo, accelarated_rfs="disabled")
mo_14 = AdaptorEthRoCEProfile(parent_mo_or_dn=mo, admin_state="disabled", resource_groups="32", memory_regions="131072", queue_pairs="256")
mo_15 = AdaptorEthInterruptProfile(parent_mo_or_dn=mo, count="1024", coalescing_type="min", mode="msi-x", coalescing_time="125")
mo_16 = AdaptorRssProfile(parent_mo_or_dn=mo, receive_side_scaling="enabled")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = VnicLanConnTempl(parent_mo_or_dn=obj, redundancy_pair_type="none", name="PublicB-NIC", descr="Public NIC Template for FI-B", stats_policy_name="default", switch_id="B-A", mtu="9000", policy_owner="local", templ_type="initial-template", qos_policy_name="QoS-Ceph", target="adaptor", ident_pool_name="UCS-Ceph-MAC-Pool", cdn_source="vnic-name", nw_ctrl_policy_name="Enable-CDP")
mo_1 = VnicEtherIf(parent_mo_or_dn=mo, default_net="no", name="Public")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = VnicLanConnTempl(parent_mo_or_dn=obj, redundancy_pair_type="none", name="PublicA-NIC", descr="Public NIC Template for FI-A", stats_policy_name="default", switch_id="A-B", mtu="9000", policy_owner="local", templ_type="initial-template", qos_policy_name="QoS-Ceph", target="adaptor", ident_pool_name="UCS-Ceph-MAC-Pool", cdn_source="vnic-name", nw_ctrl_policy_name="Enable-CDP")
mo_1 = VnicEtherIf(parent_mo_or_dn=mo, default_net="no", name="Public")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = LstorageDiskGroupConfigPolicy(parent_mo_or_dn=obj, policy_owner="local", raid_level="stripe", descr="RAID 0 Disk Group for Disk ID 9", name="R0_HDD_9")
mo_1 = LstorageVirtualDriveDef(parent_mo_or_dn=mo, read_policy="read-ahead", drive_cache="disable", strip_size="platform-default", io_policy="direct", write_cache_policy="always-write-back", access_policy="platform-default")
mo_2 = LstorageLocalDiskConfigRef(parent_mo_or_dn=mo, role="normal", slot_num="9", span_id="unspecified")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = LsServer(parent_mo_or_dn=obj, src_templ_name="C220M4S-MRAID", uuid="17c349d0-c5e9-11e6-0000-11112222111d", maint_policy_name="Server-Maint", stats_policy_name="default", ext_ip_state="none", bios_profile_name="Ceph", power_policy_name="No-Power-Cap", boot_policy_name="PXE-Boot", policy_owner="local", ext_ip_pool_name="ext-mgmt", scrub_policy_name="Disk-Scrub", ident_pool_name="UCS-Ceph-UUID-Pool", resolve_remote="yes", type="instance", name="UCS-Mon-C220M4S-MRAID-2")
mo_1 = LsVConAssign(parent_mo_or_dn=mo, admin_vcon="1", vnic_name="Default", order="1", transport="ethernet", admin_host_port="ANY")
mo_2 = LsVConAssign(parent_mo_or_dn=mo, admin_vcon="1", vnic_name="Public", order="2", transport="ethernet", admin_host_port="ANY")
mo_3 = handle.query_dn("org-root/ls-UCS-Mon-C220M4S-MRAID-2/ls-identity-info")
mo_4 = handle.query_dn("org-root/ls-UCS-Mon-C220M4S-MRAID-2/vdrive-ref-Boot")
mo_5 = LstorageProfileBinding(parent_mo_or_dn=mo, storage_profile_name="C220M4S-MRAID")
mo_6 = VnicEther(parent_mo_or_dn=mo, nw_ctrl_policy_name="Enable-CDP", admin_host_port="ANY", admin_vcon="1", stats_policy_name="default", cdn_prop_in_sync="yes", switch_id="A-B", name="Default", order="1", qos_policy_name="QoS-Ceph", adaptor_profile_name="RHEL", ident_pool_name="UCS-Ceph-MAC-Pool", cdn_source="vnic-name", mtu="1500", nw_templ_name="Default-NIC", addr="00:25:B5:00:00:24")
mo_7 = VnicEtherIf(parent_mo_or_dn=mo_6, default_net="yes", name="default")
mo_8 = VnicEther(parent_mo_or_dn=mo, nw_ctrl_policy_name="Enable-CDP", admin_host_port="ANY", admin_vcon="1", stats_policy_name="default", cdn_prop_in_sync="yes", switch_id="A-B", name="Public", order="2", qos_policy_name="QoS-Ceph", adaptor_profile_name="RHEL", ident_pool_name="UCS-Ceph-MAC-Pool", cdn_source="vnic-name", mtu="9000", nw_templ_name="Public-NIC", addr="00:25:B5:00:00:25")
mo_9 = VnicEtherIf(parent_mo_or_dn=mo_8, default_net="no", name="Public")
mo_10 = VnicDefBeh(parent_mo_or_dn=mo, action="none", policy_owner="local", type="vhba")
mo_11 = LsVersionBeh(parent_mo_or_dn=mo, pci_enum="static-zero-func", vcon_map="round-robin", vnic_order="dynamic-all-last", vnic_map="physical-cap-first")
mo_12 = LsServerExtension(parent_mo_or_dn=mo, guid="dfe19896-2eb6-48ce-88cc-295e215b8f93")
mo_13 = VnicConnDef(parent_mo_or_dn=mo, )
mo_14 = VnicFcNode(parent_mo_or_dn=mo, ident_pool_name="node-default", addr="pool-derived")
mo_15 = FabricVCon(parent_mo_or_dn=mo, placement="physical", fabric="NONE", share="shared", select="all", transport="ethernet,fc", id="4", inst_type="manual")
mo_16 = FabricVCon(parent_mo_or_dn=mo, placement="physical", fabric="NONE", share="shared", select="all", transport="ethernet,fc", id="3", inst_type="manual")
mo_17 = FabricVCon(parent_mo_or_dn=mo, placement="physical", fabric="NONE", share="shared", select="all", transport="ethernet,fc", id="2", inst_type="manual")
mo_18 = FabricVCon(parent_mo_or_dn=mo, placement="physical", fabric="NONE", share="shared", select="all", transport="ethernet,fc", id="1", inst_type="manual")
mo_19 = LsPower(parent_mo_or_dn=mo, state="up")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = LsServer(parent_mo_or_dn=obj, src_templ_name="C220M4S-MRAID", uuid="17c349d0-c5e9-11e6-0000-11112222111c", maint_policy_name="Server-Maint", stats_policy_name="default", ext_ip_state="none", bios_profile_name="Ceph", power_policy_name="No-Power-Cap", boot_policy_name="PXE-Boot", policy_owner="local", ext_ip_pool_name="ext-mgmt", scrub_policy_name="Disk-Scrub", ident_pool_name="UCS-Ceph-UUID-Pool", resolve_remote="yes", type="instance", name="UCS-Mon-C220M4S-MRAID-1")
mo_1 = LsVConAssign(parent_mo_or_dn=mo, admin_vcon="1", vnic_name="Default", order="1", transport="ethernet", admin_host_port="ANY")
mo_2 = LsVConAssign(parent_mo_or_dn=mo, admin_vcon="1", vnic_name="Public", order="2", transport="ethernet", admin_host_port="ANY")
mo_3 = handle.query_dn("org-root/ls-UCS-Mon-C220M4S-MRAID-1/ls-identity-info")
mo_4 = handle.query_dn("org-root/ls-UCS-Mon-C220M4S-MRAID-1/vdrive-ref-Boot")
mo_5 = LstorageProfileBinding(parent_mo_or_dn=mo, storage_profile_name="C220M4S-MRAID")
mo_6 = VnicEther(parent_mo_or_dn=mo, nw_ctrl_policy_name="Enable-CDP", admin_host_port="ANY", admin_vcon="1", stats_policy_name="default", cdn_prop_in_sync="yes", switch_id="A-B", name="Default", order="1", qos_policy_name="QoS-Ceph", adaptor_profile_name="RHEL", ident_pool_name="UCS-Ceph-MAC-Pool", cdn_source="vnic-name", mtu="1500", nw_templ_name="Default-NIC", addr="00:25:B5:00:00:22")
mo_7 = VnicEtherIf(parent_mo_or_dn=mo_6, default_net="yes", name="default")
mo_8 = VnicEther(parent_mo_or_dn=mo, nw_ctrl_policy_name="Enable-CDP", admin_host_port="ANY", admin_vcon="1", stats_policy_name="default", cdn_prop_in_sync="yes", switch_id="A-B", name="Public", order="2", qos_policy_name="QoS-Ceph", adaptor_profile_name="RHEL", ident_pool_name="UCS-Ceph-MAC-Pool", cdn_source="vnic-name", mtu="9000", nw_templ_name="Public-NIC", addr="00:25:B5:00:00:23")
mo_9 = VnicEtherIf(parent_mo_or_dn=mo_8, default_net="no", name="Public")
mo_10 = VnicDefBeh(parent_mo_or_dn=mo, action="none", policy_owner="local", type="vhba")
mo_11 = LsVersionBeh(parent_mo_or_dn=mo, pci_enum="static-zero-func", vcon_map="round-robin", vnic_order="dynamic-all-last", vnic_map="physical-cap-first")
mo_12 = LsServerExtension(parent_mo_or_dn=mo, guid="8d5fca02-6b9a-4f17-b8c6-2b96a47b4696")
mo_13 = VnicConnDef(parent_mo_or_dn=mo, )
mo_14 = VnicFcNode(parent_mo_or_dn=mo, ident_pool_name="node-default", addr="pool-derived")
mo_15 = FabricVCon(parent_mo_or_dn=mo, placement="physical", fabric="NONE", share="shared", select="all", transport="ethernet,fc", id="4", inst_type="manual")
mo_16 = FabricVCon(parent_mo_or_dn=mo, placement="physical", fabric="NONE", share="shared", select="all", transport="ethernet,fc", id="3", inst_type="manual")
mo_17 = FabricVCon(parent_mo_or_dn=mo, placement="physical", fabric="NONE", share="shared", select="all", transport="ethernet,fc", id="2", inst_type="manual")
mo_18 = FabricVCon(parent_mo_or_dn=mo, placement="physical", fabric="NONE", share="shared", select="all", transport="ethernet,fc", id="1", inst_type="manual")
mo_19 = LsPower(parent_mo_or_dn=mo, state="up")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = StorageLocalDiskConfigPolicy(parent_mo_or_dn=obj, protect_config="yes", name="default", flex_flash_raid_reporting_state="disable", flex_flash_state="disable", policy_owner="local", mode="any-configuration")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = PowerPolicy(parent_mo_or_dn=obj, fan_speed="any", descr="Power Cap Policy for Ceph", policy_owner="local", prio="no-cap", name="No-Power-Cap")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = VnicLanConnTempl(parent_mo_or_dn=obj, redundancy_pair_type="none", name="Public-NIC", descr="Public NIC Template", stats_policy_name="default", switch_id="A-B", mtu="9000", policy_owner="local", templ_type="initial-template", qos_policy_name="QoS-Ceph", target="adaptor", ident_pool_name="UCS-Ceph-MAC-Pool", cdn_source="vnic-name", nw_ctrl_policy_name="Enable-CDP")
mo_1 = VnicEtherIf(parent_mo_or_dn=mo, default_net="no", name="Public")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = handle.query_dn("org-root/db-backup-policy-default")
mo.descr = "Database Backup Policy"
mo.schedule = "1day"
mo.proto = "scp"
mo.host = "172.25.206.202"
mo.policy_owner = "local"
mo.admin_state = "enable"
mo.user = "owalsdor"
mo.pwd = "ZwfC4M24NZ/q"
mo.remote_file = "/home/owalsdor/FI6332backup/"
handle.set_mo(mo)
handle.commit()

obj = handle.query_dn("org-root")
mo = ComputePool(parent_mo_or_dn=obj, policy_owner="local", name="C220M4S-LSI")
mo_1 = ComputePooledRackUnit(parent_mo_or_dn=mo, id="3")
mo_2 = ComputePooledRackUnit(parent_mo_or_dn=mo, id="1")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = LsServer(parent_mo_or_dn=obj, src_templ_name="C220M4S-LSI", uuid="17c349d0-c5e9-11e6-0000-11112222111b", maint_policy_name="Server-Maint", stats_policy_name="default", ext_ip_state="none", bios_profile_name="Ceph", power_policy_name="No-Power-Cap", boot_policy_name="PXE-Boot", policy_owner="local", ext_ip_pool_name="ext-mgmt", scrub_policy_name="Disk-Scrub", ident_pool_name="UCS-Ceph-UUID-Pool", resolve_remote="yes", type="instance", name="UCS-Mon-C220M4S-LSI-2")
mo_1 = LsVConAssign(parent_mo_or_dn=mo, admin_vcon="1", vnic_name="Default", order="1", transport="ethernet", admin_host_port="ANY")
mo_2 = LsVConAssign(parent_mo_or_dn=mo, admin_vcon="1", vnic_name="Public", order="2", transport="ethernet", admin_host_port="ANY")
mo_3 = handle.query_dn("org-root/ls-UCS-Mon-C220M4S-LSI-2/ls-identity-info")
mo_4 = handle.query_dn("org-root/ls-UCS-Mon-C220M4S-LSI-2/vdrive-ref-Boot")
mo_5 = LstorageProfileBinding(parent_mo_or_dn=mo, storage_profile_name="C220M4S-LSI")
mo_6 = VnicEther(parent_mo_or_dn=mo, nw_ctrl_policy_name="Enable-CDP", admin_host_port="ANY", admin_vcon="1", stats_policy_name="default", cdn_prop_in_sync="yes", switch_id="A-B", name="Default", order="1", qos_policy_name="QoS-Ceph", adaptor_profile_name="RHEL", ident_pool_name="UCS-Ceph-MAC-Pool", cdn_source="vnic-name", mtu="1500", nw_templ_name="Default-NIC", addr="00:25:B5:00:00:20")
mo_7 = VnicEtherIf(parent_mo_or_dn=mo_6, default_net="yes", name="default")
mo_8 = VnicEther(parent_mo_or_dn=mo, nw_ctrl_policy_name="Enable-CDP", admin_host_port="ANY", admin_vcon="1", stats_policy_name="default", cdn_prop_in_sync="yes", switch_id="A-B", name="Public", order="2", qos_policy_name="QoS-Ceph", adaptor_profile_name="RHEL", ident_pool_name="UCS-Ceph-MAC-Pool", cdn_source="vnic-name", mtu="9000", nw_templ_name="Public-NIC", addr="00:25:B5:00:00:21")
mo_9 = VnicEtherIf(parent_mo_or_dn=mo_8, default_net="no", name="Public")
mo_10 = VnicDefBeh(parent_mo_or_dn=mo, action="none", policy_owner="local", type="vhba")
mo_11 = LsVersionBeh(parent_mo_or_dn=mo, pci_enum="static-zero-func", vcon_map="round-robin", vnic_order="dynamic-all-last", vnic_map="physical-cap-first")
mo_12 = LsServerExtension(parent_mo_or_dn=mo, guid="220f71f6-9a3f-469f-8f47-aedbf19704a9")
mo_13 = VnicConnDef(parent_mo_or_dn=mo, )
mo_14 = VnicFcNode(parent_mo_or_dn=mo, ident_pool_name="node-default", addr="pool-derived")
mo_15 = FabricVCon(parent_mo_or_dn=mo, placement="physical", fabric="NONE", share="shared", select="all", transport="ethernet,fc", id="4", inst_type="manual")
mo_16 = FabricVCon(parent_mo_or_dn=mo, placement="physical", fabric="NONE", share="shared", select="all", transport="ethernet,fc", id="3", inst_type="manual")
mo_17 = FabricVCon(parent_mo_or_dn=mo, placement="physical", fabric="NONE", share="shared", select="all", transport="ethernet,fc", id="2", inst_type="manual")
mo_18 = FabricVCon(parent_mo_or_dn=mo, placement="physical", fabric="NONE", share="shared", select="all", transport="ethernet,fc", id="1", inst_type="manual")
mo_19 = LsPower(parent_mo_or_dn=mo, state="up")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = ComputePool(parent_mo_or_dn=obj, policy_owner="local", name="S3260-Node2", descr="Cisco UCS S3260 Bottom Node Server Pool")
mo_1 = ComputePooledSlot(parent_mo_or_dn=mo, slot_id="2", chassis_id="1")
mo_2 = ComputePooledSlot(parent_mo_or_dn=mo, slot_id="2", chassis_id="2")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = LsServer(parent_mo_or_dn=obj, src_templ_name="C220M4S-LSI", uuid="17c349d0-c5e9-11e6-0000-11112222111a", maint_policy_name="Server-Maint", stats_policy_name="default", ext_ip_state="none", bios_profile_name="Ceph", power_policy_name="No-Power-Cap", boot_policy_name="PXE-Boot", policy_owner="local", ext_ip_pool_name="ext-mgmt", scrub_policy_name="Disk-Scrub", ident_pool_name="UCS-Ceph-UUID-Pool", resolve_remote="yes", type="instance", name="UCS-Mon-C220M4S-LSI-1")
mo_1 = LsVConAssign(parent_mo_or_dn=mo, admin_vcon="1", vnic_name="Default", order="1", transport="ethernet", admin_host_port="ANY")
mo_2 = LsVConAssign(parent_mo_or_dn=mo, admin_vcon="1", vnic_name="Public", order="2", transport="ethernet", admin_host_port="ANY")
mo_3 = handle.query_dn("org-root/ls-UCS-Mon-C220M4S-LSI-1/ls-identity-info")
mo_4 = handle.query_dn("org-root/ls-UCS-Mon-C220M4S-LSI-1/vdrive-ref-Boot")
mo_5 = LstorageProfileBinding(parent_mo_or_dn=mo, storage_profile_name="C220M4S-LSI")
mo_6 = VnicEther(parent_mo_or_dn=mo, nw_ctrl_policy_name="Enable-CDP", admin_host_port="ANY", admin_vcon="1", stats_policy_name="default", cdn_prop_in_sync="yes", switch_id="A-B", name="Default", order="1", qos_policy_name="QoS-Ceph", adaptor_profile_name="RHEL", ident_pool_name="UCS-Ceph-MAC-Pool", cdn_source="vnic-name", mtu="1500", nw_templ_name="Default-NIC", addr="00:25:B5:00:00:1E")
mo_7 = VnicEtherIf(parent_mo_or_dn=mo_6, default_net="yes", name="default")
mo_8 = VnicEther(parent_mo_or_dn=mo, nw_ctrl_policy_name="Enable-CDP", admin_host_port="ANY", admin_vcon="1", stats_policy_name="default", cdn_prop_in_sync="yes", switch_id="A-B", name="Public", order="2", qos_policy_name="QoS-Ceph", adaptor_profile_name="RHEL", ident_pool_name="UCS-Ceph-MAC-Pool", cdn_source="vnic-name", mtu="9000", nw_templ_name="Public-NIC", addr="00:25:B5:00:00:1F")
mo_9 = VnicEtherIf(parent_mo_or_dn=mo_8, default_net="no", name="Public")
mo_10 = VnicDefBeh(parent_mo_or_dn=mo, action="none", policy_owner="local", type="vhba")
mo_11 = LsVersionBeh(parent_mo_or_dn=mo, pci_enum="static-zero-func", vcon_map="round-robin", vnic_order="dynamic-all-last", vnic_map="physical-cap-first")
mo_12 = LsServerExtension(parent_mo_or_dn=mo, guid="5385291f-27dd-4aeb-95be-268ae4b358cb")
mo_13 = VnicConnDef(parent_mo_or_dn=mo, )
mo_14 = VnicFcNode(parent_mo_or_dn=mo, ident_pool_name="node-default", addr="pool-derived")
mo_15 = FabricVCon(parent_mo_or_dn=mo, placement="physical", fabric="NONE", share="shared", select="all", transport="ethernet,fc", id="4", inst_type="manual")
mo_16 = FabricVCon(parent_mo_or_dn=mo, placement="physical", fabric="NONE", share="shared", select="all", transport="ethernet,fc", id="3", inst_type="manual")
mo_17 = FabricVCon(parent_mo_or_dn=mo, placement="physical", fabric="NONE", share="shared", select="all", transport="ethernet,fc", id="2", inst_type="manual")
mo_18 = FabricVCon(parent_mo_or_dn=mo, placement="physical", fabric="NONE", share="shared", select="all", transport="ethernet,fc", id="1", inst_type="manual")
mo_19 = LsPower(parent_mo_or_dn=mo, state="up")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = ComputePool(parent_mo_or_dn=obj, policy_owner="local", name="S3260-Node1", descr="Cisco UCS S3260 Top Node Server Pool")
mo_1 = ComputePooledSlot(parent_mo_or_dn=mo, slot_id="1", chassis_id="1")
mo_2 = ComputePooledSlot(parent_mo_or_dn=mo, slot_id="1", chassis_id="2")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = ComputeKvmMgmtPolicy(parent_mo_or_dn=obj, policy_owner="local", name="default", vmedia_encryption="disable")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = FirmwareChassisPack(parent_mo_or_dn=obj, name="default", descr="Chassis Firmware Pack", stage_size="0", update_trigger="immediate", force_deploy="no", policy_owner="local", mode="staged", override_default_exclusion="no")
mo_1 = FirmwareExcludeChassisComponent(parent_mo_or_dn=mo, chassis_component="local-disk")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = handle.query_dn("org-root/fw-catalog-pack-default")
mo.update_trigger = "immediate"
mo.policy_owner = "local"
mo.stage_size = "0"
mo.mode = "staged"
mo.descr = "Catalog Pack"
handle.set_mo(mo)
handle.commit()

obj = handle.query_dn("org-root")
mo = AdaptorHostFcIfProfile(parent_mo_or_dn=obj, policy_owner="local", name="WindowsBoot", descr="Recommended adapter settings for Windows SAN Boot")
mo_1 = AdaptorFcCdbWorkQueueProfile(parent_mo_or_dn=mo, count="1", ring_size="512")
mo_2 = AdaptorFcPortPLogiProfile(parent_mo_or_dn=mo, retries="8", timeout="4000")
mo_3 = AdaptorFcPortFLogiProfile(parent_mo_or_dn=mo, retries="8", timeout="4000")
mo_4 = AdaptorFcErrorRecoveryProfile(parent_mo_or_dn=mo, port_down_timeout="5000", link_down_timeout="30000", fcp_error_recovery="disabled", port_down_io_retry_count="30")
mo_5 = AdaptorFcWorkQueueProfile(parent_mo_or_dn=mo, ring_size="64")
mo_6 = AdaptorFcRecvQueueProfile(parent_mo_or_dn=mo, ring_size="64")
mo_7 = AdaptorFcPortProfile(parent_mo_or_dn=mo, io_throttle_count="256", luns_per_target="1024")
mo_8 = AdaptorFcFnicProfile(parent_mo_or_dn=mo, lun_queue_depth="20", io_retry_timeout="5")
mo_9 = AdaptorFcInterruptProfile(parent_mo_or_dn=mo, mode="msi-x")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = handle.query_dn("org-root/equipment-pool-default")
handle.commit()

obj = handle.query_dn("org-root")
mo = handle.query_dn("org-root/cfg-exp-policy-default")
mo.descr = "Configuration Export Policy"
mo.schedule = "1day"
mo.proto = "scp"
mo.host = "172.25.206.202"
mo.policy_owner = "local"
mo.admin_state = "enable"
mo.user = "owalsdor"
mo.pwd = "ZwfC4M24NZ/q"
mo.remote_file = "/home/owalsdor/FI6332backup/"
handle.set_mo(mo)
handle.commit()

obj = handle.query_dn("org-root")
mo = VnicLanConnTempl(parent_mo_or_dn=obj, redundancy_pair_type="none", name="PublicB", stats_policy_name="default", switch_id="B-A", mtu="9000", policy_owner="local", templ_type="initial-template", qos_policy_name="QoS-Ceph", target="adaptor", ident_pool_name="UCS-Ceph-MAC-Pool", cdn_source="vnic-name", nw_ctrl_policy_name="Enable-CDP")
mo_1 = VnicEtherIf(parent_mo_or_dn=mo, default_net="no", name="Public")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = LsServer(parent_mo_or_dn=obj, uuid="derived", maint_policy_name="Server-Maint", stats_policy_name="default", ext_ip_state="none", bios_profile_name="Ceph", power_policy_name="No-Power-Cap", boot_policy_name="PXE-Boot", policy_owner="local", ext_ip_pool_name="ext-mgmt", scrub_policy_name="Disk-Scrub", ident_pool_name="UCS-Ceph-UUID-Pool", resolve_remote="yes", type="initial-template", name="UCS-S3260-OSD-Node2")
mo_1 = LsVConAssign(parent_mo_or_dn=mo, admin_vcon="1", vnic_name="OSD-Cluster", order="3", transport="ethernet", admin_host_port="ANY")
mo_2 = LsVConAssign(parent_mo_or_dn=mo, admin_vcon="1", vnic_name="Default", order="1", transport="ethernet", admin_host_port="ANY")
mo_3 = LsVConAssign(parent_mo_or_dn=mo, admin_vcon="1", vnic_name="Public", order="2", transport="ethernet", admin_host_port="ANY")
mo_4 = handle.query_dn("org-root/ls-UCS-S3260-OSD-Node2/vdrive-ref-R0-LUN-49")
mo_5 = handle.query_dn("org-root/ls-UCS-S3260-OSD-Node2/vdrive-ref-R0-LUN-39")
mo_6 = handle.query_dn("org-root/ls-UCS-S3260-OSD-Node2/vdrive-ref-R0-LUN-48")
mo_7 = handle.query_dn("org-root/ls-UCS-S3260-OSD-Node2/vdrive-ref-R0-LUN-38")
mo_8 = handle.query_dn("org-root/ls-UCS-S3260-OSD-Node2/vdrive-ref-R0-LUN-47")
mo_9 = handle.query_dn("org-root/ls-UCS-S3260-OSD-Node2/vdrive-ref-R0-LUN-37")
mo_10 = handle.query_dn("org-root/ls-UCS-S3260-OSD-Node2/vdrive-ref-R0-LUN-56")
mo_11 = handle.query_dn("org-root/ls-UCS-S3260-OSD-Node2/vdrive-ref-R0-LUN-46")
mo_12 = handle.query_dn("org-root/ls-UCS-S3260-OSD-Node2/vdrive-ref-R0-LUN-36")
mo_13 = handle.query_dn("org-root/ls-UCS-S3260-OSD-Node2/vdrive-ref-R0-LUN-55")
mo_14 = handle.query_dn("org-root/ls-UCS-S3260-OSD-Node2/vdrive-ref-R0-LUN-45")
mo_15 = handle.query_dn("org-root/ls-UCS-S3260-OSD-Node2/vdrive-ref-R0-LUN-35")
mo_16 = handle.query_dn("org-root/ls-UCS-S3260-OSD-Node2/vdrive-ref-R0-LUN-54")
mo_17 = handle.query_dn("org-root/ls-UCS-S3260-OSD-Node2/vdrive-ref-R0-LUN-44")
mo_18 = handle.query_dn("org-root/ls-UCS-S3260-OSD-Node2/vdrive-ref-R0-LUN-34")
mo_19 = handle.query_dn("org-root/ls-UCS-S3260-OSD-Node2/vdrive-ref-R0-LUN-53")
mo_20 = handle.query_dn("org-root/ls-UCS-S3260-OSD-Node2/vdrive-ref-R0-LUN-43")
mo_21 = handle.query_dn("org-root/ls-UCS-S3260-OSD-Node2/vdrive-ref-R0-LUN-33")
mo_22 = handle.query_dn("org-root/ls-UCS-S3260-OSD-Node2/vdrive-ref-R0-LUN-52")
mo_23 = handle.query_dn("org-root/ls-UCS-S3260-OSD-Node2/vdrive-ref-R0-LUN-42")
mo_24 = handle.query_dn("org-root/ls-UCS-S3260-OSD-Node2/vdrive-ref-R0-LUN-51")
mo_25 = handle.query_dn("org-root/ls-UCS-S3260-OSD-Node2/vdrive-ref-R0-LUN-41")
mo_26 = handle.query_dn("org-root/ls-UCS-S3260-OSD-Node2/vdrive-ref-R0-LUN-50")
mo_27 = handle.query_dn("org-root/ls-UCS-S3260-OSD-Node2/vdrive-ref-R0-LUN-40")
mo_28 = VnicEther(parent_mo_or_dn=mo, nw_ctrl_policy_name="Enable-CDP", admin_host_port="ANY", admin_vcon="1", stats_policy_name="default", cdn_prop_in_sync="yes", switch_id="B-A", name="OSD-Cluster", order="3", qos_policy_name="QoS-Ceph", adaptor_profile_name="RHEL", ident_pool_name="UCS-Ceph-MAC-Pool", cdn_source="vnic-name", mtu="9000", nw_templ_name="Cluster-NIC", addr="derived")
mo_29 = VnicEtherIf(parent_mo_or_dn=mo_28, default_net="no", name="Cluster")
mo_30 = handle.query_dn("org-root/ls-UCS-S3260-OSD-Node2/vdrive-ref-Boot")
mo_31 = LstorageProfileBinding(parent_mo_or_dn=mo, storage_profile_name="S3260-Node2")
mo_32 = VnicEther(parent_mo_or_dn=mo, nw_ctrl_policy_name="Enable-CDP", admin_host_port="ANY", admin_vcon="1", stats_policy_name="default", cdn_prop_in_sync="yes", switch_id="A-B", name="Default", order="1", qos_policy_name="QoS-Ceph", adaptor_profile_name="RHEL", ident_pool_name="UCS-Ceph-MAC-Pool", cdn_source="vnic-name", mtu="1500", nw_templ_name="Default-NIC", addr="derived")
mo_33 = VnicEtherIf(parent_mo_or_dn=mo_32, default_net="yes", name="default")
mo_34 = VnicEther(parent_mo_or_dn=mo, nw_ctrl_policy_name="Enable-CDP", admin_host_port="ANY", admin_vcon="1", stats_policy_name="default", cdn_prop_in_sync="yes", switch_id="B-A", name="Public", order="2", qos_policy_name="QoS-Ceph", adaptor_profile_name="RHEL", ident_pool_name="UCS-Ceph-MAC-Pool", cdn_source="vnic-name", mtu="9000", nw_templ_name="PublicB-NIC", addr="derived")
mo_35 = VnicEtherIf(parent_mo_or_dn=mo_34, default_net="no", name="Public")
mo_36 = VnicDefBeh(parent_mo_or_dn=mo, action="none", policy_owner="local", type="vhba")
mo_37 = VnicConnDef(parent_mo_or_dn=mo, )
mo_38 = VnicFcNode(parent_mo_or_dn=mo, ident_pool_name="node-default", addr="pool-derived")
mo_39 = FabricVCon(parent_mo_or_dn=mo, placement="physical", fabric="NONE", share="shared", select="all", transport="ethernet,fc", id="4", inst_type="manual")
mo_40 = FabricVCon(parent_mo_or_dn=mo, placement="physical", fabric="NONE", share="shared", select="all", transport="ethernet,fc", id="3", inst_type="manual")
mo_41 = FabricVCon(parent_mo_or_dn=mo, placement="physical", fabric="NONE", share="shared", select="all", transport="ethernet,fc", id="2", inst_type="manual")
mo_42 = FabricVCon(parent_mo_or_dn=mo, placement="physical", fabric="NONE", share="shared", select="all", transport="ethernet,fc", id="1", inst_type="manual")
mo_43 = LsPower(parent_mo_or_dn=mo, state="up")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = LsServer(parent_mo_or_dn=obj, uuid="derived", maint_policy_name="Server-Maint", stats_policy_name="default", ext_ip_state="none", bios_profile_name="Ceph", power_policy_name="No-Power-Cap", boot_policy_name="PXE-Boot", policy_owner="local", ext_ip_pool_name="ext-mgmt", scrub_policy_name="Disk-Scrub", ident_pool_name="UCS-Ceph-UUID-Pool", resolve_remote="yes", type="initial-template", name="UCS-S3260-OSD-Node1")
mo_1 = LsVConAssign(parent_mo_or_dn=mo, admin_vcon="1", vnic_name="OSD-Cluster", order="3", transport="ethernet", admin_host_port="ANY")
mo_2 = LsVConAssign(parent_mo_or_dn=mo, admin_vcon="1", vnic_name="Default", order="1", transport="ethernet", admin_host_port="ANY")
mo_3 = LsVConAssign(parent_mo_or_dn=mo, admin_vcon="1", vnic_name="Public", order="2", transport="ethernet", admin_host_port="ANY")
mo_4 = handle.query_dn("org-root/ls-UCS-S3260-OSD-Node1/vdrive-ref-R0-LUN-29")
mo_5 = handle.query_dn("org-root/ls-UCS-S3260-OSD-Node1/vdrive-ref-R0-LUN-19")
mo_6 = handle.query_dn("org-root/ls-UCS-S3260-OSD-Node1/vdrive-ref-R0-LUN-28")
mo_7 = handle.query_dn("org-root/ls-UCS-S3260-OSD-Node1/vdrive-ref-R0-LUN-18")
mo_8 = handle.query_dn("org-root/ls-UCS-S3260-OSD-Node1/vdrive-ref-R0-LUN-27")
mo_9 = handle.query_dn("org-root/ls-UCS-S3260-OSD-Node1/vdrive-ref-R0-LUN-17")
mo_10 = handle.query_dn("org-root/ls-UCS-S3260-OSD-Node1/vdrive-ref-R0-LUN-26")
mo_11 = handle.query_dn("org-root/ls-UCS-S3260-OSD-Node1/vdrive-ref-R0-LUN-16")
mo_12 = handle.query_dn("org-root/ls-UCS-S3260-OSD-Node1/vdrive-ref-R0-LUN-25")
mo_13 = handle.query_dn("org-root/ls-UCS-S3260-OSD-Node1/vdrive-ref-R0-LUN-15")
mo_14 = handle.query_dn("org-root/ls-UCS-S3260-OSD-Node1/vdrive-ref-R0-LUN-24")
mo_15 = handle.query_dn("org-root/ls-UCS-S3260-OSD-Node1/vdrive-ref-R0-LUN-14")
mo_16 = handle.query_dn("org-root/ls-UCS-S3260-OSD-Node1/vdrive-ref-R0-LUN-23")
mo_17 = handle.query_dn("org-root/ls-UCS-S3260-OSD-Node1/vdrive-ref-R0-LUN-13")
mo_18 = handle.query_dn("org-root/ls-UCS-S3260-OSD-Node1/vdrive-ref-R0-LUN-32")
mo_19 = handle.query_dn("org-root/ls-UCS-S3260-OSD-Node1/vdrive-ref-R0-LUN-22")
mo_20 = handle.query_dn("org-root/ls-UCS-S3260-OSD-Node1/vdrive-ref-R0-LUN-12")
mo_21 = handle.query_dn("org-root/ls-UCS-S3260-OSD-Node1/vdrive-ref-R0-LUN-31")
mo_22 = handle.query_dn("org-root/ls-UCS-S3260-OSD-Node1/vdrive-ref-R0-LUN-21")
mo_23 = handle.query_dn("org-root/ls-UCS-S3260-OSD-Node1/vdrive-ref-R0-LUN-11")
mo_24 = handle.query_dn("org-root/ls-UCS-S3260-OSD-Node1/vdrive-ref-R0-LUN-30")
mo_25 = handle.query_dn("org-root/ls-UCS-S3260-OSD-Node1/vdrive-ref-R0-LUN-20")
mo_26 = handle.query_dn("org-root/ls-UCS-S3260-OSD-Node1/vdrive-ref-R0-LUN-10")
mo_27 = handle.query_dn("org-root/ls-UCS-S3260-OSD-Node1/vdrive-ref-R0-LUN-9")
mo_28 = VnicEther(parent_mo_or_dn=mo, nw_ctrl_policy_name="Enable-CDP", admin_host_port="ANY", admin_vcon="1", stats_policy_name="default", cdn_prop_in_sync="yes", switch_id="B-A", name="OSD-Cluster", order="3", qos_policy_name="QoS-Ceph", adaptor_profile_name="RHEL", ident_pool_name="UCS-Ceph-MAC-Pool", cdn_source="vnic-name", mtu="9000", nw_templ_name="Cluster-NIC", addr="derived")
mo_29 = VnicEtherIf(parent_mo_or_dn=mo_28, default_net="no", name="Cluster")
mo_30 = handle.query_dn("org-root/ls-UCS-S3260-OSD-Node1/vdrive-ref-Boot")
mo_31 = LstorageProfileBinding(parent_mo_or_dn=mo, storage_profile_name="S3260-Node1")
mo_32 = VnicEther(parent_mo_or_dn=mo, nw_ctrl_policy_name="Enable-CDP", admin_host_port="ANY", admin_vcon="1", stats_policy_name="default", cdn_prop_in_sync="yes", switch_id="A-B", name="Default", order="1", qos_policy_name="QoS-Ceph", adaptor_profile_name="RHEL", ident_pool_name="UCS-Ceph-MAC-Pool", cdn_source="vnic-name", mtu="1500", nw_templ_name="Default-NIC", addr="derived")
mo_33 = VnicEtherIf(parent_mo_or_dn=mo_32, default_net="yes", name="default")
mo_34 = VnicEther(parent_mo_or_dn=mo, nw_ctrl_policy_name="Enable-CDP", admin_host_port="ANY", admin_vcon="1", stats_policy_name="default", cdn_prop_in_sync="yes", switch_id="A-B", name="Public", order="2", qos_policy_name="QoS-Ceph", adaptor_profile_name="RHEL", ident_pool_name="UCS-Ceph-MAC-Pool", cdn_source="vnic-name", mtu="9000", nw_templ_name="PublicA-NIC", addr="derived")
mo_35 = VnicEtherIf(parent_mo_or_dn=mo_34, default_net="no", name="Public")
mo_36 = VnicDefBeh(parent_mo_or_dn=mo, action="none", policy_owner="local", type="vhba")
mo_37 = VnicConnDef(parent_mo_or_dn=mo, )
mo_38 = VnicFcNode(parent_mo_or_dn=mo, ident_pool_name="node-default", addr="pool-derived")
mo_39 = FabricVCon(parent_mo_or_dn=mo, placement="physical", fabric="NONE", share="shared", select="all", transport="ethernet,fc", id="4", inst_type="manual")
mo_40 = FabricVCon(parent_mo_or_dn=mo, placement="physical", fabric="NONE", share="shared", select="all", transport="ethernet,fc", id="3", inst_type="manual")
mo_41 = FabricVCon(parent_mo_or_dn=mo, placement="physical", fabric="NONE", share="shared", select="all", transport="ethernet,fc", id="2", inst_type="manual")
mo_42 = FabricVCon(parent_mo_or_dn=mo, placement="physical", fabric="NONE", share="shared", select="all", transport="ethernet,fc", id="1", inst_type="manual")
mo_43 = LsPower(parent_mo_or_dn=mo, state="up")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = LstorageProfile(parent_mo_or_dn=obj, policy_owner="local", name="S3260-Node1-R0")
mo_1 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_29", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-29")
mo_2 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_19", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-19")
mo_3 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_28", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-28")
mo_4 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_18", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-18")
mo_5 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_27", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-27")
mo_6 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_17", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-17")
mo_7 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_26", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-26")
mo_8 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_16", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-16")
mo_9 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_25", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-25")
mo_10 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_15", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-15")
mo_11 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_24", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-24")
mo_12 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_14", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-14")
mo_13 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_23", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-23")
mo_14 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_13", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-13")
mo_15 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_32", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-32")
mo_16 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_22", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-22")
mo_17 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_12", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-12")
mo_18 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_31", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-31")
mo_19 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_21", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-21")
mo_20 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_11", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-11")
mo_21 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_30", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-30")
mo_22 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_20", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-20")
mo_23 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_10", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-10")
mo_24 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_9", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-9")
mo_25 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="S3260-Boot-R0", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="Boot")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = LstorageProfile(parent_mo_or_dn=obj, policy_owner="local", name="S3260-Node2-R0")
mo_1 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_49", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-49")
mo_2 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_39", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-39")
mo_3 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_48", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-48")
mo_4 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_38", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-38")
mo_5 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_47", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-47")
mo_6 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_37", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-37")
mo_7 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_56", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-56")
mo_8 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_46", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-46")
mo_9 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_36", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-36")
mo_10 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_55", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-55")
mo_11 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_45", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-45")
mo_12 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_35", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-35")
mo_13 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_54", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-54")
mo_14 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_44", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-44")
mo_15 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_34", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-34")
mo_16 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_53", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-53")
mo_17 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_43", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-43")
mo_18 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_33", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-33")
mo_19 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_52", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-52")
mo_20 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_42", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-42")
mo_21 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_51", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-51")
mo_22 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_41", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-41")
mo_23 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_50", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-50")
mo_24 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_40", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-40")
mo_25 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="S3260-Boot-R0", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="Boot")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = AdaptorHostEthIfProfile(parent_mo_or_dn=obj, policy_owner="local", name="SMBClient", descr="Recommended adapter settings for SMB Client")
mo_1 = AdaptorEthInterruptScalingProfile(parent_mo_or_dn=mo, admin_state="disabled")
mo_2 = handle.query_dn("org-root/eth-profile-SMBClient/ext-ipv6-rss-hash")
mo_3 = AdaptorEthAdvFilterProfile(parent_mo_or_dn=mo, admin_state="disabled")
mo_4 = handle.query_dn("org-root/eth-profile-SMBClient/ipv6-rss-hash")
mo_5 = handle.query_dn("org-root/eth-profile-SMBClient/ipv4-rss-hash")
mo_6 = AdaptorEthFailoverProfile(parent_mo_or_dn=mo, timeout="5")
mo_7 = AdaptorEthOffloadProfile(parent_mo_or_dn=mo, tcp_segment="enabled", large_receive="enabled", tcp_rx_checksum="enabled", tcp_tx_checksum="enabled")
mo_8 = AdaptorEthWorkQueueProfile(parent_mo_or_dn=mo, count="1", ring_size="256")
mo_9 = AdaptorEthCompQueueProfile(parent_mo_or_dn=mo, count="5")
mo_10 = AdaptorEthRecvQueueProfile(parent_mo_or_dn=mo, count="4", ring_size="512")
mo_11 = AdaptorEthVxLANProfile(parent_mo_or_dn=mo, admin_state="disabled")
mo_12 = AdaptorEthNVGREProfile(parent_mo_or_dn=mo, admin_state="disabled")
mo_13 = AdaptorEthArfsProfile(parent_mo_or_dn=mo, accelarated_rfs="disabled")
mo_14 = AdaptorEthRoCEProfile(parent_mo_or_dn=mo, admin_state="enabled", resource_groups="32", memory_regions="131072", queue_pairs="256")
mo_15 = AdaptorEthInterruptProfile(parent_mo_or_dn=mo, count="8", coalescing_type="min", mode="msi-x", coalescing_time="125")
mo_16 = AdaptorRssProfile(parent_mo_or_dn=mo, receive_side_scaling="enabled")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = FcpoolInitiators(parent_mo_or_dn=obj, policy_owner="local", max_ports_per_node="upto3", purpose="node-wwn-assignment", assignment_order="default", name="node-default")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = AdaptorHostIscsiIfProfile(parent_mo_or_dn=obj, policy_owner="local", name="default", descr="default issci adapter policy")
mo_1 = AdaptorProtocolProfile(parent_mo_or_dn=mo, boot_to_target="no", tcp_time_stamp="no", connection_time_out="0", dhcp_time_out="60", lun_busy_retry_count="0", hba_mode="no")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = handle.query_dn("org-root/memory-config-default")
mo.black_listing = "enabled"
mo.policy_owner = "local"
handle.set_mo(mo)
handle.commit()

obj = handle.query_dn("org-root")
mo = AdaptorHostEthIfProfile(parent_mo_or_dn=obj, policy_owner="local", name="SMBServer", descr="Recommended adapter settings for SMB server")
mo_1 = AdaptorEthInterruptScalingProfile(parent_mo_or_dn=mo, admin_state="disabled")
mo_2 = handle.query_dn("org-root/eth-profile-SMBServer/ext-ipv6-rss-hash")
mo_3 = AdaptorEthAdvFilterProfile(parent_mo_or_dn=mo, admin_state="disabled")
mo_4 = handle.query_dn("org-root/eth-profile-SMBServer/ipv6-rss-hash")
mo_5 = handle.query_dn("org-root/eth-profile-SMBServer/ipv4-rss-hash")
mo_6 = AdaptorEthFailoverProfile(parent_mo_or_dn=mo, timeout="5")
mo_7 = AdaptorEthOffloadProfile(parent_mo_or_dn=mo, tcp_segment="enabled", large_receive="enabled", tcp_rx_checksum="enabled", tcp_tx_checksum="enabled")
mo_8 = AdaptorEthWorkQueueProfile(parent_mo_or_dn=mo, count="1", ring_size="256")
mo_9 = AdaptorEthCompQueueProfile(parent_mo_or_dn=mo, count="5")
mo_10 = AdaptorEthRecvQueueProfile(parent_mo_or_dn=mo, count="4", ring_size="512")
mo_11 = AdaptorEthVxLANProfile(parent_mo_or_dn=mo, admin_state="disabled")
mo_12 = AdaptorEthNVGREProfile(parent_mo_or_dn=mo, admin_state="disabled")
mo_13 = AdaptorEthArfsProfile(parent_mo_or_dn=mo, accelarated_rfs="disabled")
mo_14 = AdaptorEthRoCEProfile(parent_mo_or_dn=mo, admin_state="enabled", resource_groups="32", memory_regions="131072", queue_pairs="2048")
mo_15 = AdaptorEthInterruptProfile(parent_mo_or_dn=mo, count="8", coalescing_type="min", mode="msi-x", coalescing_time="125")
mo_16 = AdaptorRssProfile(parent_mo_or_dn=mo, receive_side_scaling="enabled")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = LstorageProfile(parent_mo_or_dn=obj, policy_owner="local", name="C220M4S-MRAID")
mo_1 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="C220M4S-MRAID", auto_deploy="auto-deploy", expand_to_avail="no", lun_map_type="non-shared", size="100", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="Boot")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = PowerPolicy(parent_mo_or_dn=obj, fan_speed="any", policy_owner="local", prio="5", name="default")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = LsbootPolicy(parent_mo_or_dn=obj, name="PXE-Boot", descr="Ceph Boot Policy", reboot_on_update="no", policy_owner="local", purpose="operational", enforce_vnic_name="yes", boot_mode="legacy")
mo_1 = LsbootVirtualMedia(parent_mo_or_dn=mo, access="read-only-local", lun_id="0", order="2")
mo_2 = LsbootStorage(parent_mo_or_dn=mo, order="1")
mo_3 = LsbootLocalStorage(parent_mo_or_dn=mo_2, )
mo_4 = LsbootLocalHddImage(parent_mo_or_dn=mo_3, order="1")
mo_5 = LsbootLan(parent_mo_or_dn=mo, prot="pxe", order="3")
mo_6 = LsbootLanImagePath(parent_mo_or_dn=mo_5, type="primary", vnic_name="Default")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = ComputePool(parent_mo_or_dn=obj, policy_owner="local", name="default")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = handle.query_dn("org-root/agent-policy-default")
handle.commit()

obj = handle.query_dn("org-root")
mo = VnicUsnicConPolicy(parent_mo_or_dn=obj, usnic_count="4", policy_owner="local", name="oracle-rac", descr="usnic connection policy for Oracle RAC", adaptor_profile_name="usNICOracleRAC")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = LsServer(parent_mo_or_dn=obj, src_templ_name="C220M4S-MRAID", uuid="17c349d0-c5e9-11e6-0000-111122221120", maint_policy_name="Server-Maint", stats_policy_name="default", ext_ip_state="none", bios_profile_name="Ceph", power_policy_name="No-Power-Cap", boot_policy_name="PXE-Boot", policy_owner="local", ext_ip_pool_name="ext-mgmt", scrub_policy_name="Disk-Scrub", ident_pool_name="UCS-Ceph-UUID-Pool", resolve_remote="yes", type="instance", name="UCS-RGW-C220M4S-3")
mo_1 = LsVConAssign(parent_mo_or_dn=mo, admin_vcon="1", vnic_name="Default", order="1", transport="ethernet", admin_host_port="ANY")
mo_2 = LsVConAssign(parent_mo_or_dn=mo, admin_vcon="1", vnic_name="Public", order="2", transport="ethernet", admin_host_port="ANY")
mo_3 = handle.query_dn("org-root/ls-UCS-RGW-C220M4S-3/ls-identity-info")
mo_4 = handle.query_dn("org-root/ls-UCS-RGW-C220M4S-3/vdrive-ref-Boot")
mo_5 = LstorageProfileBinding(parent_mo_or_dn=mo, storage_profile_name="C220M4S-MRAID")
mo_6 = VnicEther(parent_mo_or_dn=mo, nw_ctrl_policy_name="Enable-CDP", admin_host_port="ANY", admin_vcon="1", stats_policy_name="default", cdn_prop_in_sync="yes", switch_id="A-B", name="Default", order="1", qos_policy_name="QoS-Ceph", adaptor_profile_name="RHEL", ident_pool_name="UCS-Ceph-MAC-Pool", cdn_source="vnic-name", mtu="1500", nw_templ_name="Default-NIC", addr="00:25:B5:00:00:2A")
mo_7 = VnicEtherIf(parent_mo_or_dn=mo_6, default_net="yes", name="default")
mo_8 = VnicEther(parent_mo_or_dn=mo, nw_ctrl_policy_name="Enable-CDP", admin_host_port="ANY", admin_vcon="1", stats_policy_name="default", cdn_prop_in_sync="yes", switch_id="A-B", name="Public", order="2", qos_policy_name="QoS-Ceph", adaptor_profile_name="RHEL", ident_pool_name="UCS-Ceph-MAC-Pool", cdn_source="vnic-name", mtu="9000", nw_templ_name="Public-NIC", addr="00:25:B5:00:00:2B")
mo_9 = VnicEtherIf(parent_mo_or_dn=mo_8, default_net="no", name="Public")
mo_10 = VnicDefBeh(parent_mo_or_dn=mo, action="none", policy_owner="local", type="vhba")
mo_11 = LsVersionBeh(parent_mo_or_dn=mo, pci_enum="static-zero-func", vcon_map="round-robin", vnic_order="dynamic-all-last", vnic_map="physical-cap-first")
mo_12 = LsServerExtension(parent_mo_or_dn=mo, guid="94ba2051-699d-4aa4-a9b3-a7710dd62564")
mo_13 = VnicConnDef(parent_mo_or_dn=mo, )
mo_14 = VnicFcNode(parent_mo_or_dn=mo, ident_pool_name="node-default", addr="pool-derived")
mo_15 = FabricVCon(parent_mo_or_dn=mo, placement="physical", fabric="NONE", share="shared", select="all", transport="ethernet,fc", id="4", inst_type="manual")
mo_16 = FabricVCon(parent_mo_or_dn=mo, placement="physical", fabric="NONE", share="shared", select="all", transport="ethernet,fc", id="3", inst_type="manual")
mo_17 = FabricVCon(parent_mo_or_dn=mo, placement="physical", fabric="NONE", share="shared", select="all", transport="ethernet,fc", id="2", inst_type="manual")
mo_18 = FabricVCon(parent_mo_or_dn=mo, placement="physical", fabric="NONE", share="shared", select="all", transport="ethernet,fc", id="1", inst_type="manual")
mo_19 = LsPower(parent_mo_or_dn=mo, state="up")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = LsServer(parent_mo_or_dn=obj, src_templ_name="C220M4S-MRAID", uuid="17c349d0-c5e9-11e6-0000-11112222111f", maint_policy_name="Server-Maint", stats_policy_name="default", ext_ip_state="none", bios_profile_name="Ceph", power_policy_name="No-Power-Cap", boot_policy_name="PXE-Boot", policy_owner="local", ext_ip_pool_name="ext-mgmt", scrub_policy_name="Disk-Scrub", ident_pool_name="UCS-Ceph-UUID-Pool", resolve_remote="yes", type="instance", name="UCS-RGW-C220M4S-2")
mo_1 = LsVConAssign(parent_mo_or_dn=mo, admin_vcon="1", vnic_name="Default", order="1", transport="ethernet", admin_host_port="ANY")
mo_2 = LsVConAssign(parent_mo_or_dn=mo, admin_vcon="1", vnic_name="Public", order="2", transport="ethernet", admin_host_port="ANY")
mo_3 = handle.query_dn("org-root/ls-UCS-RGW-C220M4S-2/ls-identity-info")
mo_4 = handle.query_dn("org-root/ls-UCS-RGW-C220M4S-2/vdrive-ref-Boot")
mo_5 = LstorageProfileBinding(parent_mo_or_dn=mo, storage_profile_name="C220M4S-MRAID")
mo_6 = VnicEther(parent_mo_or_dn=mo, nw_ctrl_policy_name="Enable-CDP", admin_host_port="ANY", admin_vcon="1", stats_policy_name="default", cdn_prop_in_sync="yes", switch_id="A-B", name="Default", order="1", qos_policy_name="QoS-Ceph", adaptor_profile_name="RHEL", ident_pool_name="UCS-Ceph-MAC-Pool", cdn_source="vnic-name", mtu="1500", nw_templ_name="Default-NIC", addr="00:25:B5:00:00:28")
mo_7 = VnicEtherIf(parent_mo_or_dn=mo_6, default_net="yes", name="default")
mo_8 = VnicEther(parent_mo_or_dn=mo, nw_ctrl_policy_name="Enable-CDP", admin_host_port="ANY", admin_vcon="1", stats_policy_name="default", cdn_prop_in_sync="yes", switch_id="A-B", name="Public", order="2", qos_policy_name="QoS-Ceph", adaptor_profile_name="RHEL", ident_pool_name="UCS-Ceph-MAC-Pool", cdn_source="vnic-name", mtu="9000", nw_templ_name="Public-NIC", addr="00:25:B5:00:00:29")
mo_9 = VnicEtherIf(parent_mo_or_dn=mo_8, default_net="no", name="Public")
mo_10 = VnicDefBeh(parent_mo_or_dn=mo, action="none", policy_owner="local", type="vhba")
mo_11 = LsVersionBeh(parent_mo_or_dn=mo, pci_enum="static-zero-func", vcon_map="round-robin", vnic_order="dynamic-all-last", vnic_map="physical-cap-first")
mo_12 = LsServerExtension(parent_mo_or_dn=mo, guid="ce15911d-4378-435a-b52b-26931336ad07")
mo_13 = VnicConnDef(parent_mo_or_dn=mo, )
mo_14 = VnicFcNode(parent_mo_or_dn=mo, ident_pool_name="node-default", addr="pool-derived")
mo_15 = FabricVCon(parent_mo_or_dn=mo, placement="physical", fabric="NONE", share="shared", select="all", transport="ethernet,fc", id="4", inst_type="manual")
mo_16 = FabricVCon(parent_mo_or_dn=mo, placement="physical", fabric="NONE", share="shared", select="all", transport="ethernet,fc", id="3", inst_type="manual")
mo_17 = FabricVCon(parent_mo_or_dn=mo, placement="physical", fabric="NONE", share="shared", select="all", transport="ethernet,fc", id="2", inst_type="manual")
mo_18 = FabricVCon(parent_mo_or_dn=mo, placement="physical", fabric="NONE", share="shared", select="all", transport="ethernet,fc", id="1", inst_type="manual")
mo_19 = LsPower(parent_mo_or_dn=mo, state="up")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = LsServer(parent_mo_or_dn=obj, src_templ_name="C220M4S-MRAID", uuid="17c349d0-c5e9-11e6-0000-11112222111e", maint_policy_name="Server-Maint", stats_policy_name="default", ext_ip_state="none", bios_profile_name="Ceph", power_policy_name="No-Power-Cap", boot_policy_name="PXE-Boot", policy_owner="local", ext_ip_pool_name="ext-mgmt", scrub_policy_name="Disk-Scrub", ident_pool_name="UCS-Ceph-UUID-Pool", resolve_remote="yes", type="instance", name="UCS-RGW-C220M4S-1")
mo_1 = LsVConAssign(parent_mo_or_dn=mo, admin_vcon="1", vnic_name="Default", order="1", transport="ethernet", admin_host_port="ANY")
mo_2 = LsVConAssign(parent_mo_or_dn=mo, admin_vcon="1", vnic_name="Public", order="2", transport="ethernet", admin_host_port="ANY")
mo_3 = handle.query_dn("org-root/ls-UCS-RGW-C220M4S-1/ls-identity-info")
mo_4 = handle.query_dn("org-root/ls-UCS-RGW-C220M4S-1/vdrive-ref-Boot")
mo_5 = LstorageProfileBinding(parent_mo_or_dn=mo, storage_profile_name="C220M4S-MRAID")
mo_6 = VnicEther(parent_mo_or_dn=mo, nw_ctrl_policy_name="Enable-CDP", admin_host_port="ANY", admin_vcon="1", stats_policy_name="default", cdn_prop_in_sync="yes", switch_id="A-B", name="Default", order="1", qos_policy_name="QoS-Ceph", adaptor_profile_name="RHEL", ident_pool_name="UCS-Ceph-MAC-Pool", cdn_source="vnic-name", mtu="1500", nw_templ_name="Default-NIC", addr="00:25:B5:00:00:26")
mo_7 = VnicEtherIf(parent_mo_or_dn=mo_6, default_net="yes", name="default")
mo_8 = VnicEther(parent_mo_or_dn=mo, nw_ctrl_policy_name="Enable-CDP", admin_host_port="ANY", admin_vcon="1", stats_policy_name="default", cdn_prop_in_sync="yes", switch_id="A-B", name="Public", order="2", qos_policy_name="QoS-Ceph", adaptor_profile_name="RHEL", ident_pool_name="UCS-Ceph-MAC-Pool", cdn_source="vnic-name", mtu="9000", nw_templ_name="Public-NIC", addr="00:25:B5:00:00:27")
mo_9 = VnicEtherIf(parent_mo_or_dn=mo_8, default_net="no", name="Public")
mo_10 = VnicDefBeh(parent_mo_or_dn=mo, action="none", policy_owner="local", type="vhba")
mo_11 = LsVersionBeh(parent_mo_or_dn=mo, pci_enum="static-zero-func", vcon_map="round-robin", vnic_order="dynamic-all-last", vnic_map="physical-cap-first")
mo_12 = LsServerExtension(parent_mo_or_dn=mo, guid="c8ccf274-dab9-4e3d-81a1-d52daff4b990")
mo_13 = VnicConnDef(parent_mo_or_dn=mo, )
mo_14 = VnicFcNode(parent_mo_or_dn=mo, ident_pool_name="node-default", addr="pool-derived")
mo_15 = FabricVCon(parent_mo_or_dn=mo, placement="physical", fabric="NONE", share="shared", select="all", transport="ethernet,fc", id="4", inst_type="manual")
mo_16 = FabricVCon(parent_mo_or_dn=mo, placement="physical", fabric="NONE", share="shared", select="all", transport="ethernet,fc", id="3", inst_type="manual")
mo_17 = FabricVCon(parent_mo_or_dn=mo, placement="physical", fabric="NONE", share="shared", select="all", transport="ethernet,fc", id="2", inst_type="manual")
mo_18 = FabricVCon(parent_mo_or_dn=mo, placement="physical", fabric="NONE", share="shared", select="all", transport="ethernet,fc", id="1", inst_type="manual")
mo_19 = LsPower(parent_mo_or_dn=mo, state="up")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = LsbootPolicy(parent_mo_or_dn=obj, name="utility", reboot_on_update="no", policy_owner="local", purpose="utility", enforce_vnic_name="no", boot_mode="legacy")
mo_1 = LsbootLan(parent_mo_or_dn=mo, prot="pxe", order="1")
mo_2 = LsbootLanImagePath(parent_mo_or_dn=mo_1, type="primary", vnic_name="default")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = LsbootPolicy(parent_mo_or_dn=obj, name="default", reboot_on_update="no", policy_owner="local", purpose="operational", enforce_vnic_name="no", boot_mode="legacy")
mo_1 = LsbootVirtualMedia(parent_mo_or_dn=mo, access="read-write", lun_id="unspecified", order="4")
mo_2 = LsbootVirtualMedia(parent_mo_or_dn=mo, access="read-only", lun_id="unspecified", order="3")
mo_3 = LsbootStorage(parent_mo_or_dn=mo, order="1")
mo_4 = LsbootLocalStorage(parent_mo_or_dn=mo_3, )
mo_5 = LsbootDefaultLocalImage(parent_mo_or_dn=mo_4, order="1")
mo_6 = LsbootLan(parent_mo_or_dn=mo, prot="pxe", order="2")
mo_7 = LsbootLanImagePath(parent_mo_or_dn=mo_6, type="primary", vnic_name="default")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = AdaptorHostEthIfProfile(parent_mo_or_dn=obj, policy_owner="local", name="default", descr="default adapter policy")
mo_1 = AdaptorEthInterruptScalingProfile(parent_mo_or_dn=mo, admin_state="disabled")
mo_2 = handle.query_dn("org-root/eth-profile-default/ext-ipv6-rss-hash")
mo_3 = AdaptorEthAdvFilterProfile(parent_mo_or_dn=mo, admin_state="disabled")
mo_4 = handle.query_dn("org-root/eth-profile-default/ipv6-rss-hash")
mo_5 = handle.query_dn("org-root/eth-profile-default/ipv4-rss-hash")
mo_6 = AdaptorEthFailoverProfile(parent_mo_or_dn=mo, timeout="5")
mo_7 = AdaptorEthOffloadProfile(parent_mo_or_dn=mo, tcp_segment="enabled", large_receive="enabled", tcp_rx_checksum="enabled", tcp_tx_checksum="enabled")
mo_8 = AdaptorEthWorkQueueProfile(parent_mo_or_dn=mo, count="1", ring_size="256")
mo_9 = AdaptorEthCompQueueProfile(parent_mo_or_dn=mo, count="2")
mo_10 = AdaptorEthRecvQueueProfile(parent_mo_or_dn=mo, count="1", ring_size="512")
mo_11 = AdaptorEthVxLANProfile(parent_mo_or_dn=mo, admin_state="disabled")
mo_12 = AdaptorEthNVGREProfile(parent_mo_or_dn=mo, admin_state="disabled")
mo_13 = AdaptorEthArfsProfile(parent_mo_or_dn=mo, accelarated_rfs="disabled")
mo_14 = AdaptorEthRoCEProfile(parent_mo_or_dn=mo, admin_state="disabled", resource_groups="32", memory_regions="131072", queue_pairs="256")
mo_15 = AdaptorEthInterruptProfile(parent_mo_or_dn=mo, count="4", coalescing_type="min", mode="msi-x", coalescing_time="125")
mo_16 = AdaptorRssProfile(parent_mo_or_dn=mo, receive_side_scaling="disabled")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = AdaptorHostEthIfProfile(parent_mo_or_dn=obj, policy_owner="local", name="Windows", descr="Recommended adapter settings for Windows")
mo_1 = AdaptorEthInterruptScalingProfile(parent_mo_or_dn=mo, admin_state="disabled")
mo_2 = handle.query_dn("org-root/eth-profile-Windows/ext-ipv6-rss-hash")
mo_3 = AdaptorEthAdvFilterProfile(parent_mo_or_dn=mo, admin_state="disabled")
mo_4 = handle.query_dn("org-root/eth-profile-Windows/ipv6-rss-hash")
mo_5 = handle.query_dn("org-root/eth-profile-Windows/ipv4-rss-hash")
mo_6 = AdaptorEthFailoverProfile(parent_mo_or_dn=mo, timeout="5")
mo_7 = AdaptorEthOffloadProfile(parent_mo_or_dn=mo, tcp_segment="enabled", large_receive="enabled", tcp_rx_checksum="enabled", tcp_tx_checksum="enabled")
mo_8 = AdaptorEthWorkQueueProfile(parent_mo_or_dn=mo, count="1", ring_size="256")
mo_9 = AdaptorEthCompQueueProfile(parent_mo_or_dn=mo, count="5")
mo_10 = AdaptorEthRecvQueueProfile(parent_mo_or_dn=mo, count="4", ring_size="512")
mo_11 = AdaptorEthVxLANProfile(parent_mo_or_dn=mo, admin_state="disabled")
mo_12 = AdaptorEthNVGREProfile(parent_mo_or_dn=mo, admin_state="disabled")
mo_13 = AdaptorEthArfsProfile(parent_mo_or_dn=mo, accelarated_rfs="disabled")
mo_14 = AdaptorEthRoCEProfile(parent_mo_or_dn=mo, admin_state="disabled", resource_groups="32", memory_regions="131072", queue_pairs="256")
mo_15 = AdaptorEthInterruptProfile(parent_mo_or_dn=mo, count="8", coalescing_type="min", mode="msi-x", coalescing_time="125")
mo_16 = AdaptorRssProfile(parent_mo_or_dn=mo, receive_side_scaling="enabled")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = AdaptorHostEthIfProfile(parent_mo_or_dn=obj, policy_owner="local", name="Solaris", descr="Recommended adapter settings for Solaris")
mo_1 = AdaptorEthInterruptScalingProfile(parent_mo_or_dn=mo, admin_state="disabled")
mo_2 = handle.query_dn("org-root/eth-profile-Solaris/ext-ipv6-rss-hash")
mo_3 = AdaptorEthAdvFilterProfile(parent_mo_or_dn=mo, admin_state="disabled")
mo_4 = handle.query_dn("org-root/eth-profile-Solaris/ipv6-rss-hash")
mo_5 = handle.query_dn("org-root/eth-profile-Solaris/ipv4-rss-hash")
mo_6 = AdaptorEthFailoverProfile(parent_mo_or_dn=mo, timeout="5")
mo_7 = AdaptorEthOffloadProfile(parent_mo_or_dn=mo, tcp_segment="enabled", large_receive="enabled", tcp_rx_checksum="enabled", tcp_tx_checksum="enabled")
mo_8 = AdaptorEthWorkQueueProfile(parent_mo_or_dn=mo, count="1", ring_size="256")
mo_9 = AdaptorEthCompQueueProfile(parent_mo_or_dn=mo, count="2")
mo_10 = AdaptorEthRecvQueueProfile(parent_mo_or_dn=mo, count="1", ring_size="512")
mo_11 = AdaptorEthVxLANProfile(parent_mo_or_dn=mo, admin_state="disabled")
mo_12 = AdaptorEthNVGREProfile(parent_mo_or_dn=mo, admin_state="disabled")
mo_13 = AdaptorEthArfsProfile(parent_mo_or_dn=mo, accelarated_rfs="disabled")
mo_14 = AdaptorEthRoCEProfile(parent_mo_or_dn=mo, admin_state="disabled", resource_groups="32", memory_regions="131072", queue_pairs="256")
mo_15 = AdaptorEthInterruptProfile(parent_mo_or_dn=mo, count="4", coalescing_type="min", mode="msi-x", coalescing_time="125")
mo_16 = AdaptorRssProfile(parent_mo_or_dn=mo, receive_side_scaling="disabled")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = LstorageProfile(parent_mo_or_dn=obj, policy_owner="local", name="C220M4S-LSI")
mo_1 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="C220M4S-LSI", auto_deploy="auto-deploy", expand_to_avail="no", lun_map_type="non-shared", size="100", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="Boot")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = LstorageProfile(parent_mo_or_dn=obj, policy_owner="local", name="S3260-Node2")
mo_1 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_49", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-49")
mo_2 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_39", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-39")
mo_3 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_48", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-48")
mo_4 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_38", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-38")
mo_5 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_47", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-47")
mo_6 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_37", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-37")
mo_7 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_56", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-56")
mo_8 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_46", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-46")
mo_9 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_36", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-36")
mo_10 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_55", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-55")
mo_11 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_45", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-45")
mo_12 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_35", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-35")
mo_13 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_54", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-54")
mo_14 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_44", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-44")
mo_15 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_34", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-34")
mo_16 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_53", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-53")
mo_17 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_43", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-43")
mo_18 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_33", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-33")
mo_19 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_52", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-52")
mo_20 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_42", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-42")
mo_21 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_51", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-51")
mo_22 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_41", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-41")
mo_23 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_50", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-50")
mo_24 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_40", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-40")
mo_25 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="S3260-Boot", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="Boot")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = LsServer(parent_mo_or_dn=obj, src_templ_name="UCS-S3260-OSD-Node2", uuid="17c349d0-c5e9-11e6-0000-111122221116", maint_policy_name="Server-Maint", stats_policy_name="default", ext_ip_state="none", bios_profile_name="Ceph", power_policy_name="No-Power-Cap", boot_policy_name="PXE-Boot", policy_owner="local", ext_ip_pool_name="ext-mgmt", scrub_policy_name="Disk-Scrub", ident_pool_name="UCS-Ceph-UUID-Pool", resolve_remote="yes", type="instance", name="Ceph-OSD-Node2-2")
mo_1 = LsVConAssign(parent_mo_or_dn=mo, admin_vcon="1", vnic_name="OSD-Cluster", order="3", transport="ethernet", admin_host_port="ANY")
mo_2 = LsVConAssign(parent_mo_or_dn=mo, admin_vcon="1", vnic_name="Default", order="1", transport="ethernet", admin_host_port="ANY")
mo_3 = LsVConAssign(parent_mo_or_dn=mo, admin_vcon="1", vnic_name="Public", order="2", transport="ethernet", admin_host_port="ANY")
mo_4 = handle.query_dn("org-root/ls-Ceph-OSD-Node2-2/vdrive-ref-R0-LUN-49")
mo_5 = handle.query_dn("org-root/ls-Ceph-OSD-Node2-2/vdrive-ref-R0-LUN-39")
mo_6 = handle.query_dn("org-root/ls-Ceph-OSD-Node2-2/vdrive-ref-R0-LUN-48")
mo_7 = handle.query_dn("org-root/ls-Ceph-OSD-Node2-2/vdrive-ref-R0-LUN-38")
mo_8 = handle.query_dn("org-root/ls-Ceph-OSD-Node2-2/vdrive-ref-R0-LUN-47")
mo_9 = handle.query_dn("org-root/ls-Ceph-OSD-Node2-2/vdrive-ref-R0-LUN-37")
mo_10 = handle.query_dn("org-root/ls-Ceph-OSD-Node2-2/vdrive-ref-R0-LUN-56")
mo_11 = handle.query_dn("org-root/ls-Ceph-OSD-Node2-2/vdrive-ref-R0-LUN-46")
mo_12 = handle.query_dn("org-root/ls-Ceph-OSD-Node2-2/vdrive-ref-R0-LUN-36")
mo_13 = handle.query_dn("org-root/ls-Ceph-OSD-Node2-2/vdrive-ref-R0-LUN-55")
mo_14 = handle.query_dn("org-root/ls-Ceph-OSD-Node2-2/vdrive-ref-R0-LUN-45")
mo_15 = handle.query_dn("org-root/ls-Ceph-OSD-Node2-2/vdrive-ref-R0-LUN-35")
mo_16 = handle.query_dn("org-root/ls-Ceph-OSD-Node2-2/vdrive-ref-R0-LUN-54")
mo_17 = handle.query_dn("org-root/ls-Ceph-OSD-Node2-2/vdrive-ref-R0-LUN-44")
mo_18 = handle.query_dn("org-root/ls-Ceph-OSD-Node2-2/vdrive-ref-R0-LUN-34")
mo_19 = handle.query_dn("org-root/ls-Ceph-OSD-Node2-2/vdrive-ref-R0-LUN-53")
mo_20 = handle.query_dn("org-root/ls-Ceph-OSD-Node2-2/vdrive-ref-R0-LUN-43")
mo_21 = handle.query_dn("org-root/ls-Ceph-OSD-Node2-2/vdrive-ref-R0-LUN-33")
mo_22 = handle.query_dn("org-root/ls-Ceph-OSD-Node2-2/vdrive-ref-R0-LUN-52")
mo_23 = handle.query_dn("org-root/ls-Ceph-OSD-Node2-2/vdrive-ref-R0-LUN-42")
mo_24 = handle.query_dn("org-root/ls-Ceph-OSD-Node2-2/vdrive-ref-R0-LUN-51")
mo_25 = handle.query_dn("org-root/ls-Ceph-OSD-Node2-2/vdrive-ref-R0-LUN-41")
mo_26 = handle.query_dn("org-root/ls-Ceph-OSD-Node2-2/vdrive-ref-R0-LUN-50")
mo_27 = handle.query_dn("org-root/ls-Ceph-OSD-Node2-2/vdrive-ref-R0-LUN-40")
mo_28 = VnicEther(parent_mo_or_dn=mo, nw_ctrl_policy_name="Enable-CDP", admin_host_port="ANY", admin_vcon="1", stats_policy_name="default", cdn_prop_in_sync="yes", switch_id="B-A", name="OSD-Cluster", order="3", qos_policy_name="QoS-Ceph", adaptor_profile_name="RHEL", ident_pool_name="UCS-Ceph-MAC-Pool", cdn_source="vnic-name", mtu="9000", nw_templ_name="Cluster-NIC", addr="00:25:B5:00:00:14")
mo_29 = VnicEtherIf(parent_mo_or_dn=mo_28, default_net="no", name="Cluster")
mo_30 = handle.query_dn("org-root/ls-Ceph-OSD-Node2-2/ls-identity-info")
mo_31 = handle.query_dn("org-root/ls-Ceph-OSD-Node2-2/vdrive-ref-Boot")
mo_32 = LstorageProfileBinding(parent_mo_or_dn=mo, storage_profile_name="S3260-Node2")
mo_33 = VnicEther(parent_mo_or_dn=mo, nw_ctrl_policy_name="Enable-CDP", admin_host_port="ANY", admin_vcon="1", stats_policy_name="default", cdn_prop_in_sync="yes", switch_id="A-B", name="Default", order="1", qos_policy_name="QoS-Ceph", adaptor_profile_name="RHEL", ident_pool_name="UCS-Ceph-MAC-Pool", cdn_source="vnic-name", mtu="1500", nw_templ_name="Default-NIC", addr="00:25:B5:00:00:12")
mo_34 = VnicEtherIf(parent_mo_or_dn=mo_33, default_net="yes", name="default")
mo_35 = VnicEther(parent_mo_or_dn=mo, nw_ctrl_policy_name="Enable-CDP", admin_host_port="ANY", admin_vcon="1", stats_policy_name="default", cdn_prop_in_sync="yes", switch_id="B-A", name="Public", order="2", qos_policy_name="QoS-Ceph", adaptor_profile_name="RHEL", ident_pool_name="UCS-Ceph-MAC-Pool", cdn_source="vnic-name", mtu="9000", nw_templ_name="PublicB-NIC", addr="00:25:B5:00:00:13")
mo_36 = VnicEtherIf(parent_mo_or_dn=mo_35, default_net="no", name="Public")
mo_37 = VnicDefBeh(parent_mo_or_dn=mo, action="none", policy_owner="local", type="vhba")
mo_38 = LsVersionBeh(parent_mo_or_dn=mo, pci_enum="static-zero-func", vcon_map="round-robin", vnic_order="dynamic-all-last", vnic_map="physical-cap-first")
mo_39 = LsServerExtension(parent_mo_or_dn=mo, guid="843b4cac-0fef-4ccf-b73a-07478f91ef4a")
mo_40 = VnicConnDef(parent_mo_or_dn=mo, )
mo_41 = VnicFcNode(parent_mo_or_dn=mo, ident_pool_name="node-default", addr="pool-derived")
mo_42 = FabricVCon(parent_mo_or_dn=mo, placement="physical", fabric="NONE", share="shared", select="all", transport="ethernet,fc", id="4", inst_type="manual")
mo_43 = FabricVCon(parent_mo_or_dn=mo, placement="physical", fabric="NONE", share="shared", select="all", transport="ethernet,fc", id="3", inst_type="manual")
mo_44 = FabricVCon(parent_mo_or_dn=mo, placement="physical", fabric="NONE", share="shared", select="all", transport="ethernet,fc", id="2", inst_type="manual")
mo_45 = FabricVCon(parent_mo_or_dn=mo, placement="physical", fabric="NONE", share="shared", select="all", transport="ethernet,fc", id="1", inst_type="manual")
mo_46 = LsPower(parent_mo_or_dn=mo, state="up")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = LsServer(parent_mo_or_dn=obj, src_templ_name="UCS-S3260-OSD-Node1", uuid="17c349d0-c5e9-11e6-0000-111122221111", maint_policy_name="Server-Maint", stats_policy_name="default", ext_ip_state="none", bios_profile_name="Ceph", power_policy_name="No-Power-Cap", boot_policy_name="PXE-Boot", policy_owner="local", ext_ip_pool_name="ext-mgmt", scrub_policy_name="Disk-Scrub", ident_pool_name="UCS-Ceph-UUID-Pool", resolve_remote="yes", type="instance", name="Ceph-OSD-Node1-2")
mo_1 = LsVConAssign(parent_mo_or_dn=mo, admin_vcon="1", vnic_name="OSD-Cluster", order="3", transport="ethernet", admin_host_port="ANY")
mo_2 = LsVConAssign(parent_mo_or_dn=mo, admin_vcon="1", vnic_name="Default", order="1", transport="ethernet", admin_host_port="ANY")
mo_3 = LsVConAssign(parent_mo_or_dn=mo, admin_vcon="1", vnic_name="Public", order="2", transport="ethernet", admin_host_port="ANY")
mo_4 = handle.query_dn("org-root/ls-Ceph-OSD-Node1-2/vdrive-ref-R0-LUN-29")
mo_5 = handle.query_dn("org-root/ls-Ceph-OSD-Node1-2/vdrive-ref-R0-LUN-19")
mo_6 = handle.query_dn("org-root/ls-Ceph-OSD-Node1-2/vdrive-ref-R0-LUN-28")
mo_7 = handle.query_dn("org-root/ls-Ceph-OSD-Node1-2/vdrive-ref-R0-LUN-18")
mo_8 = handle.query_dn("org-root/ls-Ceph-OSD-Node1-2/vdrive-ref-R0-LUN-27")
mo_9 = handle.query_dn("org-root/ls-Ceph-OSD-Node1-2/vdrive-ref-R0-LUN-17")
mo_10 = handle.query_dn("org-root/ls-Ceph-OSD-Node1-2/vdrive-ref-R0-LUN-26")
mo_11 = handle.query_dn("org-root/ls-Ceph-OSD-Node1-2/vdrive-ref-R0-LUN-16")
mo_12 = handle.query_dn("org-root/ls-Ceph-OSD-Node1-2/vdrive-ref-R0-LUN-25")
mo_13 = handle.query_dn("org-root/ls-Ceph-OSD-Node1-2/vdrive-ref-R0-LUN-15")
mo_14 = handle.query_dn("org-root/ls-Ceph-OSD-Node1-2/vdrive-ref-R0-LUN-24")
mo_15 = handle.query_dn("org-root/ls-Ceph-OSD-Node1-2/vdrive-ref-R0-LUN-14")
mo_16 = handle.query_dn("org-root/ls-Ceph-OSD-Node1-2/vdrive-ref-R0-LUN-23")
mo_17 = handle.query_dn("org-root/ls-Ceph-OSD-Node1-2/vdrive-ref-R0-LUN-13")
mo_18 = handle.query_dn("org-root/ls-Ceph-OSD-Node1-2/vdrive-ref-R0-LUN-32")
mo_19 = handle.query_dn("org-root/ls-Ceph-OSD-Node1-2/vdrive-ref-R0-LUN-22")
mo_20 = handle.query_dn("org-root/ls-Ceph-OSD-Node1-2/vdrive-ref-R0-LUN-12")
mo_21 = handle.query_dn("org-root/ls-Ceph-OSD-Node1-2/vdrive-ref-R0-LUN-31")
mo_22 = handle.query_dn("org-root/ls-Ceph-OSD-Node1-2/vdrive-ref-R0-LUN-21")
mo_23 = handle.query_dn("org-root/ls-Ceph-OSD-Node1-2/vdrive-ref-R0-LUN-11")
mo_24 = handle.query_dn("org-root/ls-Ceph-OSD-Node1-2/vdrive-ref-R0-LUN-30")
mo_25 = handle.query_dn("org-root/ls-Ceph-OSD-Node1-2/vdrive-ref-R0-LUN-20")
mo_26 = handle.query_dn("org-root/ls-Ceph-OSD-Node1-2/vdrive-ref-R0-LUN-10")
mo_27 = handle.query_dn("org-root/ls-Ceph-OSD-Node1-2/vdrive-ref-R0-LUN-9")
mo_28 = VnicEther(parent_mo_or_dn=mo, nw_ctrl_policy_name="Enable-CDP", admin_host_port="ANY", admin_vcon="1", stats_policy_name="default", cdn_prop_in_sync="yes", switch_id="B-A", name="OSD-Cluster", order="3", qos_policy_name="QoS-Ceph", adaptor_profile_name="RHEL", ident_pool_name="UCS-Ceph-MAC-Pool", cdn_source="vnic-name", mtu="9000", nw_templ_name="Cluster-NIC", addr="00:25:B5:00:00:05")
mo_29 = VnicEtherIf(parent_mo_or_dn=mo_28, default_net="no", name="Cluster")
mo_30 = handle.query_dn("org-root/ls-Ceph-OSD-Node1-2/ls-identity-info")
mo_31 = handle.query_dn("org-root/ls-Ceph-OSD-Node1-2/vdrive-ref-Boot")
mo_32 = LstorageProfileBinding(parent_mo_or_dn=mo, storage_profile_name="S3260-Node1")
mo_33 = VnicEther(parent_mo_or_dn=mo, nw_ctrl_policy_name="Enable-CDP", admin_host_port="ANY", admin_vcon="1", stats_policy_name="default", cdn_prop_in_sync="yes", switch_id="A-B", name="Default", order="1", qos_policy_name="QoS-Ceph", adaptor_profile_name="RHEL", ident_pool_name="UCS-Ceph-MAC-Pool", cdn_source="vnic-name", mtu="1500", nw_templ_name="Default-NIC", addr="00:25:B5:00:00:03")
mo_34 = VnicEtherIf(parent_mo_or_dn=mo_33, default_net="yes", name="default")
mo_35 = VnicEther(parent_mo_or_dn=mo, nw_ctrl_policy_name="Enable-CDP", admin_host_port="ANY", admin_vcon="1", stats_policy_name="default", cdn_prop_in_sync="yes", switch_id="A-B", name="Public", order="2", qos_policy_name="QoS-Ceph", adaptor_profile_name="RHEL", ident_pool_name="UCS-Ceph-MAC-Pool", cdn_source="vnic-name", mtu="9000", nw_templ_name="Public-NIC", addr="00:25:B5:00:00:04")
mo_36 = VnicEtherIf(parent_mo_or_dn=mo_35, default_net="no", name="Public")
mo_37 = VnicDefBeh(parent_mo_or_dn=mo, action="none", policy_owner="local", type="vhba")
mo_38 = LsVersionBeh(parent_mo_or_dn=mo, pci_enum="static-zero-func", vcon_map="round-robin", vnic_order="dynamic-all-last", vnic_map="physical-cap-first")
mo_39 = LsServerExtension(parent_mo_or_dn=mo, guid="1f7af514-7de9-40c3-b410-0d605c30768a")
mo_40 = VnicConnDef(parent_mo_or_dn=mo, )
mo_41 = VnicFcNode(parent_mo_or_dn=mo, ident_pool_name="node-default", addr="pool-derived")
mo_42 = FabricVCon(parent_mo_or_dn=mo, placement="physical", fabric="NONE", share="shared", select="all", transport="ethernet,fc", id="4", inst_type="manual")
mo_43 = FabricVCon(parent_mo_or_dn=mo, placement="physical", fabric="NONE", share="shared", select="all", transport="ethernet,fc", id="3", inst_type="manual")
mo_44 = FabricVCon(parent_mo_or_dn=mo, placement="physical", fabric="NONE", share="shared", select="all", transport="ethernet,fc", id="2", inst_type="manual")
mo_45 = FabricVCon(parent_mo_or_dn=mo, placement="physical", fabric="NONE", share="shared", select="all", transport="ethernet,fc", id="1", inst_type="manual")
mo_46 = LsPower(parent_mo_or_dn=mo, state="up")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = LstorageProfile(parent_mo_or_dn=obj, policy_owner="local", name="S3260-Node1")
mo_1 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_29", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-29")
mo_2 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_19", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-19")
mo_3 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_28", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-28")
mo_4 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_18", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-18")
mo_5 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_27", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-27")
mo_6 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_17", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-17")
mo_7 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_26", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-26")
mo_8 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_16", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-16")
mo_9 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_25", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-25")
mo_10 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_15", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-15")
mo_11 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_24", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-24")
mo_12 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_14", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-14")
mo_13 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_23", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-23")
mo_14 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_13", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-13")
mo_15 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_32", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-32")
mo_16 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_22", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-22")
mo_17 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_12", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-12")
mo_18 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_31", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-31")
mo_19 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_21", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-21")
mo_20 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_11", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-11")
mo_21 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_30", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-30")
mo_22 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_20", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-20")
mo_23 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_10", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-10")
mo_24 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="R0_HDD_9", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="R0-LUN-9")
mo_25 = LstorageDasScsiLun(parent_mo_or_dn=mo, local_disk_policy_name="S3260-Boot", auto_deploy="auto-deploy", expand_to_avail="yes", lun_map_type="non-shared", size="1", fractional_size="0", admin_state="online", deferred_naming="no", order="not-applicable", name="Boot")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = LsServer(parent_mo_or_dn=obj, src_templ_name="UCS-S3260-OSD-Node2", uuid="17c349d0-c5e9-11e6-0000-111122221115", maint_policy_name="Server-Maint", stats_policy_name="default", ext_ip_state="none", bios_profile_name="Ceph", power_policy_name="No-Power-Cap", boot_policy_name="PXE-Boot", policy_owner="local", ext_ip_pool_name="ext-mgmt", scrub_policy_name="Disk-Scrub", ident_pool_name="UCS-Ceph-UUID-Pool", resolve_remote="yes", type="instance", name="Ceph-OSD-Node2-1")
mo_1 = LsVConAssign(parent_mo_or_dn=mo, admin_vcon="1", vnic_name="OSD-Cluster", order="3", transport="ethernet", admin_host_port="ANY")
mo_2 = LsVConAssign(parent_mo_or_dn=mo, admin_vcon="1", vnic_name="Default", order="1", transport="ethernet", admin_host_port="ANY")
mo_3 = LsVConAssign(parent_mo_or_dn=mo, admin_vcon="1", vnic_name="Public", order="2", transport="ethernet", admin_host_port="ANY")
mo_4 = handle.query_dn("org-root/ls-Ceph-OSD-Node2-1/vdrive-ref-R0-LUN-49")
mo_5 = handle.query_dn("org-root/ls-Ceph-OSD-Node2-1/vdrive-ref-R0-LUN-39")
mo_6 = handle.query_dn("org-root/ls-Ceph-OSD-Node2-1/vdrive-ref-R0-LUN-48")
mo_7 = handle.query_dn("org-root/ls-Ceph-OSD-Node2-1/vdrive-ref-R0-LUN-38")
mo_8 = handle.query_dn("org-root/ls-Ceph-OSD-Node2-1/vdrive-ref-R0-LUN-47")
mo_9 = handle.query_dn("org-root/ls-Ceph-OSD-Node2-1/vdrive-ref-R0-LUN-37")
mo_10 = handle.query_dn("org-root/ls-Ceph-OSD-Node2-1/vdrive-ref-R0-LUN-56")
mo_11 = handle.query_dn("org-root/ls-Ceph-OSD-Node2-1/vdrive-ref-R0-LUN-46")
mo_12 = handle.query_dn("org-root/ls-Ceph-OSD-Node2-1/vdrive-ref-R0-LUN-36")
mo_13 = handle.query_dn("org-root/ls-Ceph-OSD-Node2-1/vdrive-ref-R0-LUN-55")
mo_14 = handle.query_dn("org-root/ls-Ceph-OSD-Node2-1/vdrive-ref-R0-LUN-45")
mo_15 = handle.query_dn("org-root/ls-Ceph-OSD-Node2-1/vdrive-ref-R0-LUN-35")
mo_16 = handle.query_dn("org-root/ls-Ceph-OSD-Node2-1/vdrive-ref-R0-LUN-54")
mo_17 = handle.query_dn("org-root/ls-Ceph-OSD-Node2-1/vdrive-ref-R0-LUN-44")
mo_18 = handle.query_dn("org-root/ls-Ceph-OSD-Node2-1/vdrive-ref-R0-LUN-34")
mo_19 = handle.query_dn("org-root/ls-Ceph-OSD-Node2-1/vdrive-ref-R0-LUN-53")
mo_20 = handle.query_dn("org-root/ls-Ceph-OSD-Node2-1/vdrive-ref-R0-LUN-43")
mo_21 = handle.query_dn("org-root/ls-Ceph-OSD-Node2-1/vdrive-ref-R0-LUN-33")
mo_22 = handle.query_dn("org-root/ls-Ceph-OSD-Node2-1/vdrive-ref-R0-LUN-52")
mo_23 = handle.query_dn("org-root/ls-Ceph-OSD-Node2-1/vdrive-ref-R0-LUN-42")
mo_24 = handle.query_dn("org-root/ls-Ceph-OSD-Node2-1/vdrive-ref-R0-LUN-51")
mo_25 = handle.query_dn("org-root/ls-Ceph-OSD-Node2-1/vdrive-ref-R0-LUN-41")
mo_26 = handle.query_dn("org-root/ls-Ceph-OSD-Node2-1/vdrive-ref-R0-LUN-50")
mo_27 = handle.query_dn("org-root/ls-Ceph-OSD-Node2-1/vdrive-ref-R0-LUN-40")
mo_28 = VnicEther(parent_mo_or_dn=mo, nw_ctrl_policy_name="Enable-CDP", admin_host_port="ANY", admin_vcon="1", stats_policy_name="default", cdn_prop_in_sync="yes", switch_id="B-A", name="OSD-Cluster", order="3", qos_policy_name="QoS-Ceph", adaptor_profile_name="RHEL", ident_pool_name="UCS-Ceph-MAC-Pool", cdn_source="vnic-name", mtu="9000", nw_templ_name="Cluster-NIC", addr="00:25:B5:00:00:11")
mo_29 = VnicEtherIf(parent_mo_or_dn=mo_28, default_net="no", name="Cluster")
mo_30 = handle.query_dn("org-root/ls-Ceph-OSD-Node2-1/ls-identity-info")
mo_31 = handle.query_dn("org-root/ls-Ceph-OSD-Node2-1/vdrive-ref-Boot")
mo_32 = LstorageProfileBinding(parent_mo_or_dn=mo, storage_profile_name="S3260-Node2")
mo_33 = VnicEther(parent_mo_or_dn=mo, nw_ctrl_policy_name="Enable-CDP", admin_host_port="ANY", admin_vcon="1", stats_policy_name="default", cdn_prop_in_sync="yes", switch_id="A-B", name="Default", order="1", qos_policy_name="QoS-Ceph", adaptor_profile_name="RHEL", ident_pool_name="UCS-Ceph-MAC-Pool", cdn_source="vnic-name", mtu="1500", nw_templ_name="Default-NIC", addr="00:25:B5:00:00:0F")
mo_34 = VnicEtherIf(parent_mo_or_dn=mo_33, default_net="yes", name="default")
mo_35 = VnicEther(parent_mo_or_dn=mo, nw_ctrl_policy_name="Enable-CDP", admin_host_port="ANY", admin_vcon="1", stats_policy_name="default", cdn_prop_in_sync="yes", switch_id="B-A", name="Public", order="2", qos_policy_name="QoS-Ceph", adaptor_profile_name="RHEL", ident_pool_name="UCS-Ceph-MAC-Pool", cdn_source="vnic-name", mtu="9000", nw_templ_name="PublicB-NIC", addr="00:25:B5:00:00:10")
mo_36 = VnicEtherIf(parent_mo_or_dn=mo_35, default_net="no", name="Public")
mo_37 = VnicDefBeh(parent_mo_or_dn=mo, action="none", policy_owner="local", type="vhba")
mo_38 = LsVersionBeh(parent_mo_or_dn=mo, pci_enum="static-zero-func", vcon_map="round-robin", vnic_order="dynamic-all-last", vnic_map="physical-cap-first")
mo_39 = LsServerExtension(parent_mo_or_dn=mo, guid="006ec7fd-f3a2-4e16-adb1-f41eea0c3f6d")
mo_40 = VnicConnDef(parent_mo_or_dn=mo, )
mo_41 = VnicFcNode(parent_mo_or_dn=mo, ident_pool_name="node-default", addr="pool-derived")
mo_42 = FabricVCon(parent_mo_or_dn=mo, placement="physical", fabric="NONE", share="shared", select="all", transport="ethernet,fc", id="4", inst_type="manual")
mo_43 = FabricVCon(parent_mo_or_dn=mo, placement="physical", fabric="NONE", share="shared", select="all", transport="ethernet,fc", id="3", inst_type="manual")
mo_44 = FabricVCon(parent_mo_or_dn=mo, placement="physical", fabric="NONE", share="shared", select="all", transport="ethernet,fc", id="2", inst_type="manual")
mo_45 = FabricVCon(parent_mo_or_dn=mo, placement="physical", fabric="NONE", share="shared", select="all", transport="ethernet,fc", id="1", inst_type="manual")
mo_46 = LsPower(parent_mo_or_dn=mo, state="up")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = LsServer(parent_mo_or_dn=obj, src_templ_name="UCS-S3260-OSD-Node1", uuid="17c349d0-c5e9-11e6-0000-111122221110", maint_policy_name="Server-Maint", stats_policy_name="default", ext_ip_state="none", bios_profile_name="Ceph", power_policy_name="No-Power-Cap", boot_policy_name="PXE-Boot", policy_owner="local", ext_ip_pool_name="ext-mgmt", scrub_policy_name="Disk-Scrub", ident_pool_name="UCS-Ceph-UUID-Pool", resolve_remote="yes", type="instance", name="Ceph-OSD-Node1-1")
mo_1 = LsVConAssign(parent_mo_or_dn=mo, admin_vcon="1", vnic_name="OSD-Cluster", order="3", transport="ethernet", admin_host_port="ANY")
mo_2 = LsVConAssign(parent_mo_or_dn=mo, admin_vcon="1", vnic_name="Default", order="1", transport="ethernet", admin_host_port="ANY")
mo_3 = LsVConAssign(parent_mo_or_dn=mo, admin_vcon="1", vnic_name="Public", order="2", transport="ethernet", admin_host_port="ANY")
mo_4 = handle.query_dn("org-root/ls-Ceph-OSD-Node1-1/vdrive-ref-R0-LUN-29")
mo_5 = handle.query_dn("org-root/ls-Ceph-OSD-Node1-1/vdrive-ref-R0-LUN-19")
mo_6 = handle.query_dn("org-root/ls-Ceph-OSD-Node1-1/vdrive-ref-R0-LUN-28")
mo_7 = handle.query_dn("org-root/ls-Ceph-OSD-Node1-1/vdrive-ref-R0-LUN-18")
mo_8 = handle.query_dn("org-root/ls-Ceph-OSD-Node1-1/vdrive-ref-R0-LUN-27")
mo_9 = handle.query_dn("org-root/ls-Ceph-OSD-Node1-1/vdrive-ref-R0-LUN-17")
mo_10 = handle.query_dn("org-root/ls-Ceph-OSD-Node1-1/vdrive-ref-R0-LUN-26")
mo_11 = handle.query_dn("org-root/ls-Ceph-OSD-Node1-1/vdrive-ref-R0-LUN-16")
mo_12 = handle.query_dn("org-root/ls-Ceph-OSD-Node1-1/vdrive-ref-R0-LUN-25")
mo_13 = handle.query_dn("org-root/ls-Ceph-OSD-Node1-1/vdrive-ref-R0-LUN-15")
mo_14 = handle.query_dn("org-root/ls-Ceph-OSD-Node1-1/vdrive-ref-R0-LUN-24")
mo_15 = handle.query_dn("org-root/ls-Ceph-OSD-Node1-1/vdrive-ref-R0-LUN-14")
mo_16 = handle.query_dn("org-root/ls-Ceph-OSD-Node1-1/vdrive-ref-R0-LUN-23")
mo_17 = handle.query_dn("org-root/ls-Ceph-OSD-Node1-1/vdrive-ref-R0-LUN-13")
mo_18 = handle.query_dn("org-root/ls-Ceph-OSD-Node1-1/vdrive-ref-R0-LUN-32")
mo_19 = handle.query_dn("org-root/ls-Ceph-OSD-Node1-1/vdrive-ref-R0-LUN-22")
mo_20 = handle.query_dn("org-root/ls-Ceph-OSD-Node1-1/vdrive-ref-R0-LUN-12")
mo_21 = handle.query_dn("org-root/ls-Ceph-OSD-Node1-1/vdrive-ref-R0-LUN-31")
mo_22 = handle.query_dn("org-root/ls-Ceph-OSD-Node1-1/vdrive-ref-R0-LUN-21")
mo_23 = handle.query_dn("org-root/ls-Ceph-OSD-Node1-1/vdrive-ref-R0-LUN-11")
mo_24 = handle.query_dn("org-root/ls-Ceph-OSD-Node1-1/vdrive-ref-R0-LUN-30")
mo_25 = handle.query_dn("org-root/ls-Ceph-OSD-Node1-1/vdrive-ref-R0-LUN-20")
mo_26 = handle.query_dn("org-root/ls-Ceph-OSD-Node1-1/vdrive-ref-R0-LUN-10")
mo_27 = handle.query_dn("org-root/ls-Ceph-OSD-Node1-1/vdrive-ref-R0-LUN-9")
mo_28 = VnicEther(parent_mo_or_dn=mo, nw_ctrl_policy_name="Enable-CDP", admin_host_port="ANY", admin_vcon="1", stats_policy_name="default", cdn_prop_in_sync="yes", switch_id="B-A", name="OSD-Cluster", order="3", qos_policy_name="QoS-Ceph", adaptor_profile_name="RHEL", ident_pool_name="UCS-Ceph-MAC-Pool", cdn_source="vnic-name", mtu="9000", nw_templ_name="Cluster-NIC", addr="00:25:B5:00:00:02")
mo_29 = VnicEtherIf(parent_mo_or_dn=mo_28, default_net="no", name="Cluster")
mo_30 = handle.query_dn("org-root/ls-Ceph-OSD-Node1-1/ls-identity-info")
mo_31 = handle.query_dn("org-root/ls-Ceph-OSD-Node1-1/vdrive-ref-Boot")
mo_32 = LstorageProfileBinding(parent_mo_or_dn=mo, storage_profile_name="S3260-Node1")
mo_33 = VnicEther(parent_mo_or_dn=mo, nw_ctrl_policy_name="Enable-CDP", admin_host_port="ANY", admin_vcon="1", stats_policy_name="default", cdn_prop_in_sync="yes", switch_id="A-B", name="Default", order="1", qos_policy_name="QoS-Ceph", adaptor_profile_name="RHEL", ident_pool_name="UCS-Ceph-MAC-Pool", cdn_source="vnic-name", mtu="1500", nw_templ_name="Default-NIC", addr="00:25:B5:00:00:00")
mo_34 = VnicEtherIf(parent_mo_or_dn=mo_33, default_net="yes", name="default")
mo_35 = VnicEther(parent_mo_or_dn=mo, nw_ctrl_policy_name="Enable-CDP", admin_host_port="ANY", admin_vcon="1", stats_policy_name="default", cdn_prop_in_sync="yes", switch_id="A-B", name="Public", order="2", qos_policy_name="QoS-Ceph", adaptor_profile_name="RHEL", ident_pool_name="UCS-Ceph-MAC-Pool", cdn_source="vnic-name", mtu="9000", nw_templ_name="Public-NIC", addr="00:25:B5:00:00:01")
mo_36 = VnicEtherIf(parent_mo_or_dn=mo_35, default_net="no", name="Public")
mo_37 = VnicDefBeh(parent_mo_or_dn=mo, action="none", policy_owner="local", type="vhba")
mo_38 = LsVersionBeh(parent_mo_or_dn=mo, pci_enum="static-zero-func", vcon_map="round-robin", vnic_order="dynamic-all-last", vnic_map="physical-cap-first")
mo_39 = LsServerExtension(parent_mo_or_dn=mo, guid="7e93f0a9-a846-4265-a81f-2ebe3a1f8313")
mo_40 = VnicConnDef(parent_mo_or_dn=mo, )
mo_41 = VnicFcNode(parent_mo_or_dn=mo, ident_pool_name="node-default", addr="pool-derived")
mo_42 = FabricVCon(parent_mo_or_dn=mo, placement="physical", fabric="NONE", share="shared", select="all", transport="ethernet,fc", id="4", inst_type="manual")
mo_43 = FabricVCon(parent_mo_or_dn=mo, placement="physical", fabric="NONE", share="shared", select="all", transport="ethernet,fc", id="3", inst_type="manual")
mo_44 = FabricVCon(parent_mo_or_dn=mo, placement="physical", fabric="NONE", share="shared", select="all", transport="ethernet,fc", id="2", inst_type="manual")
mo_45 = FabricVCon(parent_mo_or_dn=mo, placement="physical", fabric="NONE", share="shared", select="all", transport="ethernet,fc", id="1", inst_type="manual")
mo_46 = LsPower(parent_mo_or_dn=mo, state="up")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = handle.query_dn("org-root/server-mgmt-policy")
mo.action = "auto-acknowledged"
mo.policy_owner = "local"
mo.name = "default"
handle.set_mo(mo)
handle.commit()

obj = handle.query_dn("org-root")
mo = LsmaintMaintPolicy(parent_mo_or_dn=obj, uptime_disr="user-ack", policy_owner="local", soft_shutdown_timer="150-secs", name="Server-Maint", descr="UCS Server Maintenance Policy for Ceph")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = StatsThresholdPolicy(parent_mo_or_dn=obj, policy_owner="local", name="default")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = AdaptorHostFcIfProfile(parent_mo_or_dn=obj, policy_owner="local", name="default", descr="default adapter policy")
mo_1 = AdaptorFcCdbWorkQueueProfile(parent_mo_or_dn=mo, count="1", ring_size="512")
mo_2 = AdaptorFcPortPLogiProfile(parent_mo_or_dn=mo, retries="8", timeout="20000")
mo_3 = AdaptorFcPortFLogiProfile(parent_mo_or_dn=mo, retries="8", timeout="4000")
mo_4 = AdaptorFcErrorRecoveryProfile(parent_mo_or_dn=mo, port_down_timeout="30000", link_down_timeout="30000", fcp_error_recovery="disabled", port_down_io_retry_count="30")
mo_5 = AdaptorFcWorkQueueProfile(parent_mo_or_dn=mo, ring_size="64")
mo_6 = AdaptorFcRecvQueueProfile(parent_mo_or_dn=mo, ring_size="64")
mo_7 = AdaptorFcPortProfile(parent_mo_or_dn=mo, io_throttle_count="256", luns_per_target="1024")
mo_8 = AdaptorFcFnicProfile(parent_mo_or_dn=mo, lun_queue_depth="20", io_retry_timeout="5")
mo_9 = AdaptorFcInterruptProfile(parent_mo_or_dn=mo, mode="msi-x")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = ComputePowerSyncPolicy(parent_mo_or_dn=obj, policy_owner="local", sync_option="default", name="default")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = AdaptorHostFcIfProfile(parent_mo_or_dn=obj, policy_owner="local", name="Solaris", descr="Recommended adapter settings for Solaris")
mo_1 = AdaptorFcCdbWorkQueueProfile(parent_mo_or_dn=mo, count="1", ring_size="512")
mo_2 = AdaptorFcPortPLogiProfile(parent_mo_or_dn=mo, retries="8", timeout="20000")
mo_3 = AdaptorFcPortFLogiProfile(parent_mo_or_dn=mo, retries="8", timeout="4000")
mo_4 = AdaptorFcErrorRecoveryProfile(parent_mo_or_dn=mo, port_down_timeout="30000", link_down_timeout="30000", fcp_error_recovery="disabled", port_down_io_retry_count="30")
mo_5 = AdaptorFcWorkQueueProfile(parent_mo_or_dn=mo, ring_size="64")
mo_6 = AdaptorFcRecvQueueProfile(parent_mo_or_dn=mo, ring_size="64")
mo_7 = AdaptorFcPortProfile(parent_mo_or_dn=mo, io_throttle_count="256", luns_per_target="1024")
mo_8 = AdaptorFcFnicProfile(parent_mo_or_dn=mo, lun_queue_depth="20", io_retry_timeout="5")
mo_9 = AdaptorFcInterruptProfile(parent_mo_or_dn=mo, mode="msi-x")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = AdaptorHostFcIfProfile(parent_mo_or_dn=obj, policy_owner="local", name="Windows", descr="Recommended adapter settings for Windows")
mo_1 = AdaptorFcCdbWorkQueueProfile(parent_mo_or_dn=mo, count="1", ring_size="512")
mo_2 = AdaptorFcPortPLogiProfile(parent_mo_or_dn=mo, retries="8", timeout="20000")
mo_3 = AdaptorFcPortFLogiProfile(parent_mo_or_dn=mo, retries="8", timeout="4000")
mo_4 = AdaptorFcErrorRecoveryProfile(parent_mo_or_dn=mo, port_down_timeout="30000", link_down_timeout="30000", fcp_error_recovery="disabled", port_down_io_retry_count="30")
mo_5 = AdaptorFcWorkQueueProfile(parent_mo_or_dn=mo, ring_size="64")
mo_6 = AdaptorFcRecvQueueProfile(parent_mo_or_dn=mo, ring_size="64")
mo_7 = AdaptorFcPortProfile(parent_mo_or_dn=mo, io_throttle_count="256", luns_per_target="1024")
mo_8 = AdaptorFcFnicProfile(parent_mo_or_dn=mo, lun_queue_depth="20", io_retry_timeout="5")
mo_9 = AdaptorFcInterruptProfile(parent_mo_or_dn=mo, mode="msi-x")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = AdaptorHostEthIfProfile(parent_mo_or_dn=obj, policy_owner="local", name="VMWare", descr="Recommended adapter settings for VMWare")
mo_1 = AdaptorEthInterruptScalingProfile(parent_mo_or_dn=mo, admin_state="disabled")
mo_2 = handle.query_dn("org-root/eth-profile-VMWare/ext-ipv6-rss-hash")
mo_3 = AdaptorEthAdvFilterProfile(parent_mo_or_dn=mo, admin_state="disabled")
mo_4 = handle.query_dn("org-root/eth-profile-VMWare/ipv6-rss-hash")
mo_5 = handle.query_dn("org-root/eth-profile-VMWare/ipv4-rss-hash")
mo_6 = AdaptorEthFailoverProfile(parent_mo_or_dn=mo, timeout="5")
mo_7 = AdaptorEthOffloadProfile(parent_mo_or_dn=mo, tcp_segment="enabled", large_receive="enabled", tcp_rx_checksum="enabled", tcp_tx_checksum="enabled")
mo_8 = AdaptorEthWorkQueueProfile(parent_mo_or_dn=mo, count="1", ring_size="256")
mo_9 = AdaptorEthCompQueueProfile(parent_mo_or_dn=mo, count="2")
mo_10 = AdaptorEthRecvQueueProfile(parent_mo_or_dn=mo, count="1", ring_size="512")
mo_11 = AdaptorEthVxLANProfile(parent_mo_or_dn=mo, admin_state="disabled")
mo_12 = AdaptorEthNVGREProfile(parent_mo_or_dn=mo, admin_state="disabled")
mo_13 = AdaptorEthArfsProfile(parent_mo_or_dn=mo, accelarated_rfs="disabled")
mo_14 = AdaptorEthRoCEProfile(parent_mo_or_dn=mo, admin_state="disabled", resource_groups="32", memory_regions="131072", queue_pairs="256")
mo_15 = AdaptorEthInterruptProfile(parent_mo_or_dn=mo, count="4", coalescing_type="min", mode="msi-x", coalescing_time="125")
mo_16 = AdaptorRssProfile(parent_mo_or_dn=mo, receive_side_scaling="disabled")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = handle.query_dn("org-root/chassis-discovery")
mo.multicast_hw_hash = "disabled"
mo.backplane_speed_pref = "40G"
mo.policy_owner = "local"
mo.action = "platform-max"
mo.rebalance = "user-acknowledged"
mo.link_aggregation_pref = "port-channel"
handle.set_mo(mo)
handle.commit()

obj = handle.query_dn("org-root")
mo = AdaptorHostEthIfProfile(parent_mo_or_dn=obj, policy_owner="local", name="Linux", descr="Recommended adapter settings for linux")
mo_1 = AdaptorEthInterruptScalingProfile(parent_mo_or_dn=mo, admin_state="disabled")
mo_2 = handle.query_dn("org-root/eth-profile-Linux/ext-ipv6-rss-hash")
mo_3 = AdaptorEthAdvFilterProfile(parent_mo_or_dn=mo, admin_state="disabled")
mo_4 = handle.query_dn("org-root/eth-profile-Linux/ipv6-rss-hash")
mo_5 = handle.query_dn("org-root/eth-profile-Linux/ipv4-rss-hash")
mo_6 = AdaptorEthFailoverProfile(parent_mo_or_dn=mo, timeout="5")
mo_7 = AdaptorEthOffloadProfile(parent_mo_or_dn=mo, tcp_segment="enabled", large_receive="enabled", tcp_rx_checksum="enabled", tcp_tx_checksum="enabled")
mo_8 = AdaptorEthWorkQueueProfile(parent_mo_or_dn=mo, count="1", ring_size="256")
mo_9 = AdaptorEthCompQueueProfile(parent_mo_or_dn=mo, count="2")
mo_10 = AdaptorEthRecvQueueProfile(parent_mo_or_dn=mo, count="1", ring_size="512")
mo_11 = AdaptorEthVxLANProfile(parent_mo_or_dn=mo, admin_state="disabled")
mo_12 = AdaptorEthNVGREProfile(parent_mo_or_dn=mo, admin_state="disabled")
mo_13 = AdaptorEthArfsProfile(parent_mo_or_dn=mo, accelarated_rfs="disabled")
mo_14 = AdaptorEthRoCEProfile(parent_mo_or_dn=mo, admin_state="disabled", resource_groups="32", memory_regions="131072", queue_pairs="256")
mo_15 = AdaptorEthInterruptProfile(parent_mo_or_dn=mo, count="4", coalescing_type="min", mode="msi-x", coalescing_time="125")
mo_16 = AdaptorRssProfile(parent_mo_or_dn=mo, receive_side_scaling="disabled")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = FabricMulticastPolicy(parent_mo_or_dn=obj, querier_ip_addr="0.0.0.0", name="default", querier_ip_addr_peer="0.0.0.0", querier_state="disabled", snooping_state="enabled", policy_owner="local")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = VnicUsnicConPolicy(parent_mo_or_dn=obj, usnic_count="58", policy_owner="local", name="default", descr="default usnic connection policy", adaptor_profile_name="usNIC")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = UuidpoolPool(parent_mo_or_dn=obj, prefix="17C349D0-C5E9-11E6", policy_owner="local", assignment_order="default", name="default")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = AdaptorHostFcIfProfile(parent_mo_or_dn=obj, policy_owner="local", name="VMWare", descr="Recommended adapter settings for VMWare")
mo_1 = AdaptorFcCdbWorkQueueProfile(parent_mo_or_dn=mo, count="1", ring_size="512")
mo_2 = AdaptorFcPortPLogiProfile(parent_mo_or_dn=mo, retries="8", timeout="20000")
mo_3 = AdaptorFcPortFLogiProfile(parent_mo_or_dn=mo, retries="8", timeout="4000")
mo_4 = AdaptorFcErrorRecoveryProfile(parent_mo_or_dn=mo, port_down_timeout="10000", link_down_timeout="30000", fcp_error_recovery="disabled", port_down_io_retry_count="30")
mo_5 = AdaptorFcWorkQueueProfile(parent_mo_or_dn=mo, ring_size="64")
mo_6 = AdaptorFcRecvQueueProfile(parent_mo_or_dn=mo, ring_size="64")
mo_7 = AdaptorFcPortProfile(parent_mo_or_dn=mo, io_throttle_count="256", luns_per_target="1024")
mo_8 = AdaptorFcFnicProfile(parent_mo_or_dn=mo, lun_queue_depth="20", io_retry_timeout="5")
mo_9 = AdaptorFcInterruptProfile(parent_mo_or_dn=mo, mode="msi-x")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = AdaptorHostEthIfProfile(parent_mo_or_dn=obj, policy_owner="local", name="SRIOV", descr="Recommended adapter settings for Win8 SRIOV-VMFEX PF")
mo_1 = AdaptorEthInterruptScalingProfile(parent_mo_or_dn=mo, admin_state="disabled")
mo_2 = handle.query_dn("org-root/eth-profile-SRIOV/ext-ipv6-rss-hash")
mo_3 = AdaptorEthAdvFilterProfile(parent_mo_or_dn=mo, admin_state="disabled")
mo_4 = handle.query_dn("org-root/eth-profile-SRIOV/ipv6-rss-hash")
mo_5 = handle.query_dn("org-root/eth-profile-SRIOV/ipv4-rss-hash")
mo_6 = AdaptorEthFailoverProfile(parent_mo_or_dn=mo, timeout="5")
mo_7 = AdaptorEthOffloadProfile(parent_mo_or_dn=mo, tcp_segment="enabled", large_receive="enabled", tcp_rx_checksum="enabled", tcp_tx_checksum="enabled")
mo_8 = AdaptorEthWorkQueueProfile(parent_mo_or_dn=mo, count="1", ring_size="256")
mo_9 = AdaptorEthCompQueueProfile(parent_mo_or_dn=mo, count="5")
mo_10 = AdaptorEthRecvQueueProfile(parent_mo_or_dn=mo, count="4", ring_size="512")
mo_11 = AdaptorEthVxLANProfile(parent_mo_or_dn=mo, admin_state="disabled")
mo_12 = AdaptorEthNVGREProfile(parent_mo_or_dn=mo, admin_state="disabled")
mo_13 = AdaptorEthArfsProfile(parent_mo_or_dn=mo, accelarated_rfs="disabled")
mo_14 = AdaptorEthRoCEProfile(parent_mo_or_dn=mo, admin_state="disabled", resource_groups="32", memory_regions="131072", queue_pairs="256")
mo_15 = AdaptorEthInterruptProfile(parent_mo_or_dn=mo, count="32", coalescing_type="min", mode="msi-x", coalescing_time="125")
mo_16 = AdaptorRssProfile(parent_mo_or_dn=mo, receive_side_scaling="enabled")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = NwctrlDefinition(parent_mo_or_dn=obj, lldp_transmit="disabled", name="Enable-CDP", lldp_receive="disabled", mac_register_mode="all-host-vlans", policy_owner="local", cdp="enabled", uplink_fail_action="link-down", descr="Cisco Discovery Protocol (CDP) is enabled")
mo_1 = DpsecMac(parent_mo_or_dn=mo, forge="allow", policy_owner="local")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = AdaptorHostEthIfProfile(parent_mo_or_dn=obj, policy_owner="local", name="usNIC", descr="Recommended adapter settings for usNIC Connection")
mo_1 = AdaptorEthInterruptScalingProfile(parent_mo_or_dn=mo, admin_state="disabled")
mo_2 = handle.query_dn("org-root/eth-profile-usNIC/ext-ipv6-rss-hash")
mo_3 = AdaptorEthAdvFilterProfile(parent_mo_or_dn=mo, admin_state="disabled")
mo_4 = handle.query_dn("org-root/eth-profile-usNIC/ipv6-rss-hash")
mo_5 = handle.query_dn("org-root/eth-profile-usNIC/ipv4-rss-hash")
mo_6 = AdaptorEthFailoverProfile(parent_mo_or_dn=mo, timeout="0")
mo_7 = AdaptorEthOffloadProfile(parent_mo_or_dn=mo, tcp_segment="enabled", large_receive="enabled", tcp_rx_checksum="enabled", tcp_tx_checksum="enabled")
mo_8 = AdaptorEthWorkQueueProfile(parent_mo_or_dn=mo, count="6", ring_size="256")
mo_9 = AdaptorEthCompQueueProfile(parent_mo_or_dn=mo, count="6")
mo_10 = AdaptorEthRecvQueueProfile(parent_mo_or_dn=mo, count="6", ring_size="512")
mo_11 = AdaptorEthVxLANProfile(parent_mo_or_dn=mo, admin_state="disabled")
mo_12 = AdaptorEthNVGREProfile(parent_mo_or_dn=mo, admin_state="disabled")
mo_13 = AdaptorEthArfsProfile(parent_mo_or_dn=mo, accelarated_rfs="disabled")
mo_14 = AdaptorEthRoCEProfile(parent_mo_or_dn=mo, admin_state="disabled", resource_groups="32", memory_regions="131072", queue_pairs="256")
mo_15 = AdaptorEthInterruptProfile(parent_mo_or_dn=mo, count="6", coalescing_type="min", mode="msi-x", coalescing_time="125")
mo_16 = AdaptorRssProfile(parent_mo_or_dn=mo, receive_side_scaling="enabled")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = LsServer(parent_mo_or_dn=obj, uuid="derived", maint_policy_name="Server-Maint", stats_policy_name="default", ext_ip_state="none", bios_profile_name="Ceph", power_policy_name="No-Power-Cap", boot_policy_name="PXE-Boot", policy_owner="local", ext_ip_pool_name="ext-mgmt", scrub_policy_name="Disk-Scrub", ident_pool_name="UCS-Ceph-UUID-Pool", resolve_remote="yes", type="initial-template", name="S3260-Node1-R0")
mo_1 = LsVConAssign(parent_mo_or_dn=mo, admin_vcon="1", vnic_name="OSD-Cluster", order="3", transport="ethernet", admin_host_port="ANY")
mo_2 = LsVConAssign(parent_mo_or_dn=mo, admin_vcon="1", vnic_name="Default", order="1", transport="ethernet", admin_host_port="ANY")
mo_3 = LsVConAssign(parent_mo_or_dn=mo, admin_vcon="1", vnic_name="Public", order="2", transport="ethernet", admin_host_port="ANY")
mo_4 = handle.query_dn("org-root/ls-S3260-Node1-R0/vdrive-ref-R0-LUN-29")
mo_5 = handle.query_dn("org-root/ls-S3260-Node1-R0/vdrive-ref-R0-LUN-19")
mo_6 = handle.query_dn("org-root/ls-S3260-Node1-R0/vdrive-ref-R0-LUN-28")
mo_7 = handle.query_dn("org-root/ls-S3260-Node1-R0/vdrive-ref-R0-LUN-18")
mo_8 = handle.query_dn("org-root/ls-S3260-Node1-R0/vdrive-ref-R0-LUN-27")
mo_9 = handle.query_dn("org-root/ls-S3260-Node1-R0/vdrive-ref-R0-LUN-17")
mo_10 = handle.query_dn("org-root/ls-S3260-Node1-R0/vdrive-ref-R0-LUN-26")
mo_11 = handle.query_dn("org-root/ls-S3260-Node1-R0/vdrive-ref-R0-LUN-16")
mo_12 = handle.query_dn("org-root/ls-S3260-Node1-R0/vdrive-ref-R0-LUN-25")
mo_13 = handle.query_dn("org-root/ls-S3260-Node1-R0/vdrive-ref-R0-LUN-15")
mo_14 = handle.query_dn("org-root/ls-S3260-Node1-R0/vdrive-ref-R0-LUN-24")
mo_15 = handle.query_dn("org-root/ls-S3260-Node1-R0/vdrive-ref-R0-LUN-14")
mo_16 = handle.query_dn("org-root/ls-S3260-Node1-R0/vdrive-ref-R0-LUN-23")
mo_17 = handle.query_dn("org-root/ls-S3260-Node1-R0/vdrive-ref-R0-LUN-13")
mo_18 = handle.query_dn("org-root/ls-S3260-Node1-R0/vdrive-ref-R0-LUN-32")
mo_19 = handle.query_dn("org-root/ls-S3260-Node1-R0/vdrive-ref-R0-LUN-22")
mo_20 = handle.query_dn("org-root/ls-S3260-Node1-R0/vdrive-ref-R0-LUN-12")
mo_21 = handle.query_dn("org-root/ls-S3260-Node1-R0/vdrive-ref-R0-LUN-31")
mo_22 = handle.query_dn("org-root/ls-S3260-Node1-R0/vdrive-ref-R0-LUN-21")
mo_23 = handle.query_dn("org-root/ls-S3260-Node1-R0/vdrive-ref-R0-LUN-11")
mo_24 = handle.query_dn("org-root/ls-S3260-Node1-R0/vdrive-ref-R0-LUN-30")
mo_25 = handle.query_dn("org-root/ls-S3260-Node1-R0/vdrive-ref-R0-LUN-20")
mo_26 = handle.query_dn("org-root/ls-S3260-Node1-R0/vdrive-ref-R0-LUN-10")
mo_27 = handle.query_dn("org-root/ls-S3260-Node1-R0/vdrive-ref-R0-LUN-9")
mo_28 = VnicEther(parent_mo_or_dn=mo, nw_ctrl_policy_name="Enable-CDP", admin_host_port="ANY", admin_vcon="1", stats_policy_name="default", cdn_prop_in_sync="yes", switch_id="B-A", name="OSD-Cluster", order="3", qos_policy_name="QoS-Ceph", adaptor_profile_name="RHEL", ident_pool_name="UCS-Ceph-MAC-Pool", cdn_source="vnic-name", mtu="9000", nw_templ_name="Cluster-NIC", addr="derived")
mo_29 = VnicEtherIf(parent_mo_or_dn=mo_28, default_net="no", name="Cluster")
mo_30 = handle.query_dn("org-root/ls-S3260-Node1-R0/vdrive-ref-Boot")
mo_31 = LstorageProfileBinding(parent_mo_or_dn=mo, storage_profile_name="S3260-Node1-R0")
mo_32 = VnicEther(parent_mo_or_dn=mo, nw_ctrl_policy_name="Enable-CDP", admin_host_port="ANY", admin_vcon="1", stats_policy_name="default", cdn_prop_in_sync="yes", switch_id="A-B", name="Default", order="1", qos_policy_name="QoS-Ceph", adaptor_profile_name="RHEL", ident_pool_name="UCS-Ceph-MAC-Pool", cdn_source="vnic-name", mtu="1500", nw_templ_name="Default-NIC", addr="derived")
mo_33 = VnicEtherIf(parent_mo_or_dn=mo_32, default_net="yes", name="default")
mo_34 = VnicEther(parent_mo_or_dn=mo, nw_ctrl_policy_name="Enable-CDP", admin_host_port="ANY", admin_vcon="1", stats_policy_name="default", cdn_prop_in_sync="yes", switch_id="A-B", name="Public", order="2", qos_policy_name="QoS-Ceph", adaptor_profile_name="RHEL", ident_pool_name="UCS-Ceph-MAC-Pool", cdn_source="vnic-name", mtu="9000", nw_templ_name="PublicA-NIC", addr="derived")
mo_35 = VnicEtherIf(parent_mo_or_dn=mo_34, default_net="no", name="Public")
mo_36 = VnicDefBeh(parent_mo_or_dn=mo, action="none", policy_owner="local", type="vhba")
mo_37 = VnicConnDef(parent_mo_or_dn=mo, )
mo_38 = VnicFcNode(parent_mo_or_dn=mo, ident_pool_name="node-default", addr="pool-derived")
mo_39 = LsRequirement(parent_mo_or_dn=mo, restrict_migration="no", name="S3260-Node1")
mo_40 = FabricVCon(parent_mo_or_dn=mo, placement="physical", fabric="NONE", share="shared", select="all", transport="ethernet,fc", id="4", inst_type="manual")
mo_41 = FabricVCon(parent_mo_or_dn=mo, placement="physical", fabric="NONE", share="shared", select="all", transport="ethernet,fc", id="3", inst_type="manual")
mo_42 = FabricVCon(parent_mo_or_dn=mo, placement="physical", fabric="NONE", share="shared", select="all", transport="ethernet,fc", id="2", inst_type="manual")
mo_43 = FabricVCon(parent_mo_or_dn=mo, placement="physical", fabric="NONE", share="shared", select="all", transport="ethernet,fc", id="1", inst_type="manual")
mo_44 = LsPower(parent_mo_or_dn=mo, state="up")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = LsServer(parent_mo_or_dn=obj, uuid="derived", maint_policy_name="Server-Maint", stats_policy_name="default", ext_ip_state="none", bios_profile_name="Ceph", power_policy_name="No-Power-Cap", boot_policy_name="PXE-Boot", policy_owner="local", ext_ip_pool_name="ext-mgmt", scrub_policy_name="Disk-Scrub", ident_pool_name="UCS-Ceph-UUID-Pool", resolve_remote="yes", type="initial-template", name="S3260-Node2-R0")
mo_1 = LsVConAssign(parent_mo_or_dn=mo, admin_vcon="1", vnic_name="OSD-Cluster", order="3", transport="ethernet", admin_host_port="ANY")
mo_2 = LsVConAssign(parent_mo_or_dn=mo, admin_vcon="1", vnic_name="Default", order="1", transport="ethernet", admin_host_port="ANY")
mo_3 = LsVConAssign(parent_mo_or_dn=mo, admin_vcon="1", vnic_name="Public", order="2", transport="ethernet", admin_host_port="ANY")
mo_4 = handle.query_dn("org-root/ls-S3260-Node2-R0/vdrive-ref-R0-LUN-49")
mo_5 = handle.query_dn("org-root/ls-S3260-Node2-R0/vdrive-ref-R0-LUN-39")
mo_6 = handle.query_dn("org-root/ls-S3260-Node2-R0/vdrive-ref-R0-LUN-48")
mo_7 = handle.query_dn("org-root/ls-S3260-Node2-R0/vdrive-ref-R0-LUN-38")
mo_8 = handle.query_dn("org-root/ls-S3260-Node2-R0/vdrive-ref-R0-LUN-47")
mo_9 = handle.query_dn("org-root/ls-S3260-Node2-R0/vdrive-ref-R0-LUN-37")
mo_10 = handle.query_dn("org-root/ls-S3260-Node2-R0/vdrive-ref-R0-LUN-56")
mo_11 = handle.query_dn("org-root/ls-S3260-Node2-R0/vdrive-ref-R0-LUN-46")
mo_12 = handle.query_dn("org-root/ls-S3260-Node2-R0/vdrive-ref-R0-LUN-36")
mo_13 = handle.query_dn("org-root/ls-S3260-Node2-R0/vdrive-ref-R0-LUN-55")
mo_14 = handle.query_dn("org-root/ls-S3260-Node2-R0/vdrive-ref-R0-LUN-45")
mo_15 = handle.query_dn("org-root/ls-S3260-Node2-R0/vdrive-ref-R0-LUN-35")
mo_16 = handle.query_dn("org-root/ls-S3260-Node2-R0/vdrive-ref-R0-LUN-54")
mo_17 = handle.query_dn("org-root/ls-S3260-Node2-R0/vdrive-ref-R0-LUN-44")
mo_18 = handle.query_dn("org-root/ls-S3260-Node2-R0/vdrive-ref-R0-LUN-34")
mo_19 = handle.query_dn("org-root/ls-S3260-Node2-R0/vdrive-ref-R0-LUN-53")
mo_20 = handle.query_dn("org-root/ls-S3260-Node2-R0/vdrive-ref-R0-LUN-43")
mo_21 = handle.query_dn("org-root/ls-S3260-Node2-R0/vdrive-ref-R0-LUN-33")
mo_22 = handle.query_dn("org-root/ls-S3260-Node2-R0/vdrive-ref-R0-LUN-52")
mo_23 = handle.query_dn("org-root/ls-S3260-Node2-R0/vdrive-ref-R0-LUN-42")
mo_24 = handle.query_dn("org-root/ls-S3260-Node2-R0/vdrive-ref-R0-LUN-51")
mo_25 = handle.query_dn("org-root/ls-S3260-Node2-R0/vdrive-ref-R0-LUN-41")
mo_26 = handle.query_dn("org-root/ls-S3260-Node2-R0/vdrive-ref-R0-LUN-50")
mo_27 = handle.query_dn("org-root/ls-S3260-Node2-R0/vdrive-ref-R0-LUN-40")
mo_28 = VnicEther(parent_mo_or_dn=mo, nw_ctrl_policy_name="Enable-CDP", admin_host_port="ANY", admin_vcon="1", stats_policy_name="default", cdn_prop_in_sync="yes", switch_id="B-A", name="OSD-Cluster", order="3", qos_policy_name="QoS-Ceph", adaptor_profile_name="RHEL", ident_pool_name="UCS-Ceph-MAC-Pool", cdn_source="vnic-name", mtu="9000", nw_templ_name="Cluster-NIC", addr="derived")
mo_29 = VnicEtherIf(parent_mo_or_dn=mo_28, default_net="no", name="Cluster")
mo_30 = handle.query_dn("org-root/ls-S3260-Node2-R0/vdrive-ref-Boot")
mo_31 = LstorageProfileBinding(parent_mo_or_dn=mo, storage_profile_name="S3260-Node2-R0")
mo_32 = VnicEther(parent_mo_or_dn=mo, nw_ctrl_policy_name="Enable-CDP", admin_host_port="ANY", admin_vcon="1", stats_policy_name="default", cdn_prop_in_sync="yes", switch_id="A-B", name="Default", order="1", qos_policy_name="QoS-Ceph", adaptor_profile_name="RHEL", ident_pool_name="UCS-Ceph-MAC-Pool", cdn_source="vnic-name", mtu="1500", nw_templ_name="Default-NIC", addr="derived")
mo_33 = VnicEtherIf(parent_mo_or_dn=mo_32, default_net="yes", name="default")
mo_34 = VnicEther(parent_mo_or_dn=mo, nw_ctrl_policy_name="Enable-CDP", admin_host_port="ANY", admin_vcon="1", stats_policy_name="default", cdn_prop_in_sync="yes", switch_id="B-A", name="Public", order="2", qos_policy_name="QoS-Ceph", adaptor_profile_name="RHEL", ident_pool_name="UCS-Ceph-MAC-Pool", cdn_source="vnic-name", mtu="9000", nw_templ_name="PublicB-NIC", addr="derived")
mo_35 = VnicEtherIf(parent_mo_or_dn=mo_34, default_net="no", name="Public")
mo_36 = VnicDefBeh(parent_mo_or_dn=mo, action="none", policy_owner="local", type="vhba")
mo_37 = VnicConnDef(parent_mo_or_dn=mo, )
mo_38 = VnicFcNode(parent_mo_or_dn=mo, ident_pool_name="node-default", addr="pool-derived")
mo_39 = LsRequirement(parent_mo_or_dn=mo, restrict_migration="no", name="S3260-Node2")
mo_40 = FabricVCon(parent_mo_or_dn=mo, placement="physical", fabric="NONE", share="shared", select="all", transport="ethernet,fc", id="4", inst_type="manual")
mo_41 = FabricVCon(parent_mo_or_dn=mo, placement="physical", fabric="NONE", share="shared", select="all", transport="ethernet,fc", id="3", inst_type="manual")
mo_42 = FabricVCon(parent_mo_or_dn=mo, placement="physical", fabric="NONE", share="shared", select="all", transport="ethernet,fc", id="2", inst_type="manual")
mo_43 = FabricVCon(parent_mo_or_dn=mo, placement="physical", fabric="NONE", share="shared", select="all", transport="ethernet,fc", id="1", inst_type="manual")
mo_44 = LsPower(parent_mo_or_dn=mo, state="up")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = handle.query_dn("org-root/server-discovery")
mo.action = "immediate"
mo.policy_owner = "local"
mo.name = "default"
handle.set_mo(mo)
handle.commit()

obj = handle.query_dn("org-root")
mo = handle.query_dn("org-root/info-sync-policy")
handle.commit()

obj = handle.query_dn("org-root")
mo = AdaptorHostFcIfProfile(parent_mo_or_dn=obj, policy_owner="local", name="Linux", descr="Recommended adapter settings for Linux")
mo_1 = AdaptorFcCdbWorkQueueProfile(parent_mo_or_dn=mo, count="1", ring_size="512")
mo_2 = AdaptorFcPortPLogiProfile(parent_mo_or_dn=mo, retries="8", timeout="20000")
mo_3 = AdaptorFcPortFLogiProfile(parent_mo_or_dn=mo, retries="8", timeout="4000")
mo_4 = AdaptorFcErrorRecoveryProfile(parent_mo_or_dn=mo, port_down_timeout="30000", link_down_timeout="30000", fcp_error_recovery="disabled", port_down_io_retry_count="30")
mo_5 = AdaptorFcWorkQueueProfile(parent_mo_or_dn=mo, ring_size="64")
mo_6 = AdaptorFcRecvQueueProfile(parent_mo_or_dn=mo, ring_size="64")
mo_7 = AdaptorFcPortProfile(parent_mo_or_dn=mo, io_throttle_count="256", luns_per_target="1024")
mo_8 = AdaptorFcFnicProfile(parent_mo_or_dn=mo, lun_queue_depth="20", io_retry_timeout="5")
mo_9 = AdaptorFcInterruptProfile(parent_mo_or_dn=mo, mode="msi-x")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = IppoolPool(parent_mo_or_dn=obj, is_net_bios_enabled="disabled", name="ext-mgmt", policy_owner="local", ext_managed="internal", supports_dhcp="disabled", guid="00000000-0000-0000-0000-000000000000", assignment_order="default")
mo_1 = IppoolBlock(parent_mo_or_dn=mo, subnet="255.255.255.0", sec_dns="0.0.0.0", r_from="172.25.206.50", def_gw="172.25.206.1", to="172.25.206.69", prim_dns="173.36.131.10")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = IqnpoolPool(parent_mo_or_dn=obj, policy_owner="local", name="default", assignment_order="default")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = MacpoolPool(parent_mo_or_dn=obj, policy_owner="local", name="default", assignment_order="default")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = FcpoolInitiators(parent_mo_or_dn=obj, policy_owner="local", max_ports_per_node="upto3", purpose="port-wwn-assignment", assignment_order="default", name="default")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = LsbootPolicy(parent_mo_or_dn=obj, name="diag", reboot_on_update="no", policy_owner="local", purpose="utility", enforce_vnic_name="no", boot_mode="legacy")
mo_1 = LsbootVirtualMedia(parent_mo_or_dn=mo, access="read-write", lun_id="unspecified", order="2")
mo_2 = LsbootVirtualMedia(parent_mo_or_dn=mo, access="read-only", lun_id="unspecified", order="1")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = ComputeScrubPolicy(parent_mo_or_dn=obj, flex_flash_scrub="no", name="Disk-Scrub", descr="Scrub all disks after removing the profile", policy_owner="local", bios_settings_scrub="no", disk_scrub="yes")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = AdaptorHostEthIfProfile(parent_mo_or_dn=obj, policy_owner="local", name="RHEL", descr="Adapter Policy for RHEL")
mo_1 = AdaptorEthInterruptScalingProfile(parent_mo_or_dn=mo, admin_state="disabled")
mo_2 = handle.query_dn("org-root/eth-profile-RHEL/ext-ipv6-rss-hash")
mo_3 = AdaptorEthAdvFilterProfile(parent_mo_or_dn=mo, admin_state="disabled")
mo_4 = handle.query_dn("org-root/eth-profile-RHEL/ipv6-rss-hash")
mo_5 = handle.query_dn("org-root/eth-profile-RHEL/ipv4-rss-hash")
mo_6 = AdaptorEthFailoverProfile(parent_mo_or_dn=mo, timeout="5")
mo_7 = AdaptorEthOffloadProfile(parent_mo_or_dn=mo, tcp_segment="enabled", large_receive="enabled", tcp_rx_checksum="enabled", tcp_tx_checksum="enabled")
mo_8 = AdaptorEthWorkQueueProfile(parent_mo_or_dn=mo, count="8", ring_size="4096")
mo_9 = AdaptorEthCompQueueProfile(parent_mo_or_dn=mo, count="16")
mo_10 = AdaptorEthRecvQueueProfile(parent_mo_or_dn=mo, count="8", ring_size="4096")
mo_11 = AdaptorEthVxLANProfile(parent_mo_or_dn=mo, admin_state="disabled")
mo_12 = AdaptorEthNVGREProfile(parent_mo_or_dn=mo, admin_state="disabled")
mo_13 = AdaptorEthArfsProfile(parent_mo_or_dn=mo, accelarated_rfs="disabled")
mo_14 = AdaptorEthRoCEProfile(parent_mo_or_dn=mo, admin_state="disabled", resource_groups="32", memory_regions="131072", queue_pairs="256")
mo_15 = AdaptorEthInterruptProfile(parent_mo_or_dn=mo, count="32", coalescing_type="min", mode="msi-x", coalescing_time="125")
mo_16 = AdaptorRssProfile(parent_mo_or_dn=mo, receive_side_scaling="enabled")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = LsServer(parent_mo_or_dn=obj, uuid="derived", maint_policy_name="Server-Maint", stats_policy_name="default", ext_ip_state="none", bios_profile_name="Ceph", power_policy_name="No-Power-Cap", boot_policy_name="PXE-Boot", policy_owner="local", ext_ip_pool_name="ext-mgmt", scrub_policy_name="Disk-Scrub", ident_pool_name="UCS-Ceph-UUID-Pool", resolve_remote="yes", type="initial-template", name="C220M4S-MRAID")
mo_1 = LsVConAssign(parent_mo_or_dn=mo, admin_vcon="1", vnic_name="Default", order="1", transport="ethernet", admin_host_port="ANY")
mo_2 = LsVConAssign(parent_mo_or_dn=mo, admin_vcon="1", vnic_name="Public", order="2", transport="ethernet", admin_host_port="ANY")
mo_3 = handle.query_dn("org-root/ls-C220M4S-MRAID/vdrive-ref-Boot")
mo_4 = LstorageProfileBinding(parent_mo_or_dn=mo, storage_profile_name="C220M4S-MRAID")
mo_5 = VnicEther(parent_mo_or_dn=mo, nw_ctrl_policy_name="Enable-CDP", admin_host_port="ANY", admin_vcon="1", stats_policy_name="default", cdn_prop_in_sync="yes", switch_id="A-B", name="Default", order="1", qos_policy_name="QoS-Ceph", adaptor_profile_name="RHEL", ident_pool_name="UCS-Ceph-MAC-Pool", cdn_source="vnic-name", mtu="1500", nw_templ_name="Default-NIC", addr="derived")
mo_6 = VnicEtherIf(parent_mo_or_dn=mo_5, default_net="yes", name="default")
mo_7 = VnicEther(parent_mo_or_dn=mo, nw_ctrl_policy_name="Enable-CDP", admin_host_port="ANY", admin_vcon="1", stats_policy_name="default", cdn_prop_in_sync="yes", switch_id="A-B", name="Public", order="2", qos_policy_name="QoS-Ceph", adaptor_profile_name="RHEL", ident_pool_name="UCS-Ceph-MAC-Pool", cdn_source="vnic-name", mtu="9000", nw_templ_name="Public-NIC", addr="derived")
mo_8 = VnicEtherIf(parent_mo_or_dn=mo_7, default_net="no", name="Public")
mo_9 = VnicDefBeh(parent_mo_or_dn=mo, action="none", policy_owner="local", type="vhba")
mo_10 = VnicConnDef(parent_mo_or_dn=mo, )
mo_11 = VnicFcNode(parent_mo_or_dn=mo, ident_pool_name="node-default", addr="pool-derived")
mo_12 = LsRequirement(parent_mo_or_dn=mo, restrict_migration="no", name="C220M4S-MRAID")
mo_13 = FabricVCon(parent_mo_or_dn=mo, placement="physical", fabric="NONE", share="shared", select="all", transport="ethernet,fc", id="4", inst_type="manual")
mo_14 = FabricVCon(parent_mo_or_dn=mo, placement="physical", fabric="NONE", share="shared", select="all", transport="ethernet,fc", id="3", inst_type="manual")
mo_15 = FabricVCon(parent_mo_or_dn=mo, placement="physical", fabric="NONE", share="shared", select="all", transport="ethernet,fc", id="2", inst_type="manual")
mo_16 = FabricVCon(parent_mo_or_dn=mo, placement="physical", fabric="NONE", share="shared", select="all", transport="ethernet,fc", id="1", inst_type="manual")
mo_17 = LsPower(parent_mo_or_dn=mo, state="up")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = handle.query_dn("org-root/pwr-mgmt-policy")
mo.style = "intelligent-policy-driven"
mo.profiling = "no"
mo.name = "default"
mo.skip_power_deploy_check = "no"
mo.policy_owner = "local"
mo.skip_power_check = "no"
handle.set_mo(mo)
handle.commit()

obj = handle.query_dn("org-root")
mo = handle.query_dn("org-root/org-vlan-policy")
mo.admin_state = "disabled"
handle.set_mo(mo)
handle.commit()

obj = handle.query_dn("org-root")
mo = EpqosDefinition(parent_mo_or_dn=obj, policy_owner="local", name="QoS-Ceph")
mo_1 = EpqosEgress(parent_mo_or_dn=mo, rate="line-rate", host_control="none", prio="best-effort", burst="10240")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = BiosVProfile(parent_mo_or_dn=obj, policy_owner="local", name="SRIOV", descr="Recommended bios settings for SRIOV vNICs", reboot_on_update="no")
mo_1 = BiosVfUSBSystemIdlePowerOptimizingSetting(parent_mo_or_dn=mo, vp_usb_idle_power_optimizing="platform-default")
mo_2 = BiosVfIntelTrustedExecutionTechnology(parent_mo_or_dn=mo, vp_intel_trusted_execution_technology_support="platform-default")
mo_3 = BiosVfIntegratedGraphicsApertureSize(parent_mo_or_dn=mo, vp_integrated_graphics_aperture_size="platform-default")
mo_4 = BiosVfIntelVirtualizationTechnology(parent_mo_or_dn=mo, vp_intel_virtualization_technology="enabled")
mo_5 = BiosVfOSBootWatchdogTimerTimeout(parent_mo_or_dn=mo, vp_os_boot_watchdog_timer_timeout="platform-default")
mo_6 = BiosVfSelectMemoryRASConfiguration(parent_mo_or_dn=mo, vp_select_memory_ras_configuration="platform-default")
mo_7 = BiosVfProcessorEnergyConfiguration(parent_mo_or_dn=mo, vp_power_technology="platform-default", vp_energy_performance="platform-default")
mo_8 = BiosVfConsistentDeviceNameControl(parent_mo_or_dn=mo, vp_cdn_control="platform-default")
mo_9 = BiosVfOSBootWatchdogTimerPolicy(parent_mo_or_dn=mo, vp_os_boot_watchdog_timer_policy="platform-default")
mo_10 = BiosVfEnhancedPowerCappingSupport(parent_mo_or_dn=mo, vp_enhanced_power_capping="platform-default")
mo_11 = BiosVfCPUHardwarePowerManagement(parent_mo_or_dn=mo, vp_cpu_hardware_power_management="platform-default")
mo_12 = BiosVfEnhancedIntelSpeedStepTech(parent_mo_or_dn=mo, vp_enhanced_intel_speed_step_tech="platform-default")
mo_13 = BiosVfPCILOMPortsConfiguration(parent_mo_or_dn=mo, vp_pc_ie10_glo_m2_link="platform-default")
mo_14 = BiosVfUSBFrontPanelAccessLock(parent_mo_or_dn=mo, vp_usb_front_panel_lock="platform-default")
mo_15 = BiosVfIntelEntrySASRAIDModule(parent_mo_or_dn=mo, vp_sasraid="platform-default", vp_sasraid_module="platform-default")
mo_16 = BiosVfRedirectionAfterBIOSPOST(parent_mo_or_dn=mo, vp_redirection_after_post="platform-default")
mo_17 = BiosVfMemoryMappedIOAbove4GB(parent_mo_or_dn=mo, vp_memory_mapped_io_above4_gb="platform-default")
mo_18 = BiosVfQPILinkFrequencySelect(parent_mo_or_dn=mo, vp_qpi_link_frequency_select="platform-default")
mo_19 = BiosVfIntelHyperThreadingTech(parent_mo_or_dn=mo, vp_intel_hyper_threading_tech="platform-default")
mo_20 = BiosVfEnergyPerformanceTuning(parent_mo_or_dn=mo, vp_pwr_perf_tuning="platform-default")
mo_21 = BiosVfProcessorPrefetchConfig(parent_mo_or_dn=mo, vp_dcuip_prefetcher="platform-default", vp_adjacent_cache_line_prefetcher="platform-default", vp_hardware_prefetcher="platform-default", vp_dcu_streamer_prefetch="platform-default")
mo_22 = BiosVfMaxVariableMTRRSetting(parent_mo_or_dn=mo, vp_processor_mtrr="platform-default")
mo_23 = handle.query_dn("org-root/bios-prof-SRIOV/PCI-Slot-OptionROM-Enable")
mo_24 = BiosVfUEFIOSUseLegacyVideo(parent_mo_or_dn=mo, vp_uefios_use_legacy_video="platform-default")
mo_25 = BiosVfInterleaveConfiguration(parent_mo_or_dn=mo, vp_channel_interleaving="platform-default", vp_rank_interleaving="platform-default", vp_memory_interleaving="platform-default")
mo_26 = BiosVfFrequencyFloorOverride(parent_mo_or_dn=mo, vp_frequency_floor_override="platform-default")
mo_27 = BiosVfIntelVTForDirectedIO(parent_mo_or_dn=mo, vp_intel_vtd_pass_through_dma_support="platform-default", vp_intel_vtdats_support="platform-default", vp_intel_vtd_interrupt_remapping="enabled", vp_intel_vtd_coherency_support="disabled", vp_intel_vt_for_directed_io="enabled")
mo_28 = BiosVfMaximumMemoryBelow4GB(parent_mo_or_dn=mo, vp_maximum_memory_below4_gb="platform-default")
mo_29 = BiosVfResumeOnACPowerLoss(parent_mo_or_dn=mo, vp_resume_on_ac_power_loss="platform-default")
mo_30 = handle.query_dn("org-root/bios-prof-SRIOV/Onboard-SATA-controller")
mo_31 = BiosVfTrustedPlatformModule(parent_mo_or_dn=mo, vp_trusted_platform_module_support="platform-default")
mo_32 = BiosVfOutOfBandManagement(parent_mo_or_dn=mo, vp_com_spcr_enable="platform-default")
mo_33 = BiosVfOSBootWatchdogTimer(parent_mo_or_dn=mo, vp_os_boot_watchdog_timer="platform-default")
mo_34 = BiosVfUSBPortConfiguration(parent_mo_or_dn=mo, vp_usb_port_front="platform-default", vp_usb_port_v_media="platform-default", vp_usb_port_kvm="platform-default", vp_port6064_emulation="platform-default", vp_usb_port_rear="platform-default", vp_usb_port_internal="platform-default", vp_usb_port_sd_card="platform-default")
mo_35 = BiosVfWorkloadConfiguration(parent_mo_or_dn=mo, vp_workload_configuration="platform-default")
mo_36 = BiosVfDDR3VoltageSelection(parent_mo_or_dn=mo, vp_dd_r3_voltage_selection="platform-default")
mo_37 = handle.query_dn("org-root/bios-prof-SRIOV/UCSM-Boot-Mode-Control")
mo_38 = BiosVfIntelTurboBoostTech(parent_mo_or_dn=mo, vp_intel_turbo_boost_tech="platform-default")
mo_39 = BiosVfPackageCStateLimit(parent_mo_or_dn=mo, vp_package_c_state_limit="platform-default")
mo_40 = handle.query_dn("org-root/bios-prof-SRIOV/TPM-Pending-Operation")
mo_41 = BiosVfDRAMClockThrottling(parent_mo_or_dn=mo, vp_dram_clock_throttling="platform-default")
mo_42 = handle.query_dn("org-root/bios-prof-SRIOV/CPU-Power-Management")
mo_43 = BiosVfPSTATECoordination(parent_mo_or_dn=mo, vp_pstate_coordination="platform-default")
mo_44 = BiosVfCoreMultiProcessing(parent_mo_or_dn=mo, vp_core_multi_processing="platform-default")
mo_45 = BiosVfSerialPortAEnable(parent_mo_or_dn=mo, vp_serial_port_a_enable="platform-default")
mo_46 = BiosVfProcessorC3Report(parent_mo_or_dn=mo, vp_processor_c3_report="platform-default")
mo_47 = BiosVfProcessorC7Report(parent_mo_or_dn=mo, vp_processor_c7_report="platform-default")
mo_48 = BiosVfProcessorC6Report(parent_mo_or_dn=mo, vp_processor_c6_report="platform-default")
mo_49 = BiosVfExecuteDisableBit(parent_mo_or_dn=mo, vp_execute_disable_bit="platform-default")
mo_50 = BiosVfFrontPanelLockout(parent_mo_or_dn=mo, vp_front_panel_lockout="platform-default")
mo_51 = BiosVfIntegratedGraphics(parent_mo_or_dn=mo, vp_integrated_graphics="platform-default")
mo_52 = BiosVfDirectCacheAccess(parent_mo_or_dn=mo, vp_direct_cache_access="enabled")
mo_53 = BiosVfConsoleRedirection(parent_mo_or_dn=mo, vp_terminal_type="platform-default", vp_flow_control="platform-default", vp_baud_rate="platform-default", vp_putty_key_pad="platform-default", vp_console_redirection="platform-default", vp_legacy_os_redirection="platform-default")
mo_54 = BiosVfPCISlotLinkSpeed(parent_mo_or_dn=mo, vp_pc_ie_slot4_link_speed="platform-default", vp_pc_ie_slot3_link_speed="platform-default", vp_pc_ie_slot10_link_speed="platform-default", vp_pc_ie_slot9_link_speed="platform-default", vp_pc_ie_slot2_link_speed="platform-default", vp_pc_ie_slot8_link_speed="platform-default", vp_pc_ie_slot6_link_speed="platform-default", vp_pc_ie_slot5_link_speed="platform-default", vp_pc_ie_slot1_link_speed="platform-default", vp_pc_ie_slot7_link_speed="platform-default")
mo_55 = BiosVfAssertNMIOnSERR(parent_mo_or_dn=mo, vp_assert_nmi_on_serr="platform-default")
mo_56 = BiosVfAssertNMIOnPERR(parent_mo_or_dn=mo, vp_assert_nmi_on_perr="platform-default")
mo_57 = BiosVfIOENVMe1OptionROM(parent_mo_or_dn=mo, vp_ioenv_me1_option_rom="platform-default")
mo_58 = BiosVfIOENVMe2OptionROM(parent_mo_or_dn=mo, vp_ioenv_me2_option_rom="platform-default")
mo_59 = BiosVfIOESlot1OptionROM(parent_mo_or_dn=mo, vp_ioe_slot1_option_rom="platform-default")
mo_60 = BiosVfIOESlot2OptionROM(parent_mo_or_dn=mo, vp_ioe_slot2_option_rom="platform-default")
mo_61 = BiosVfIOEMezz1OptionROM(parent_mo_or_dn=mo, vp_ioe_mezz1_option_rom="platform-default")
mo_62 = BiosVfBootOptionRetry(parent_mo_or_dn=mo, vp_boot_option_retry="platform-default")
mo_63 = BiosVfUSBConfiguration(parent_mo_or_dn=mo, vp_xhci_mode="platform-default", vp_legacy_usb_support="platform-default")
mo_64 = BiosVfDramRefreshRate(parent_mo_or_dn=mo, vp_dram_refresh_rate="platform-default")
mo_65 = BiosVfProcessorCState(parent_mo_or_dn=mo, vp_processor_c_state="platform-default")
mo_66 = BiosVfSBNVMe1OptionROM(parent_mo_or_dn=mo, vp_sbnv_me1_option_rom="platform-default")
mo_67 = BiosVfSBMezz1OptionROM(parent_mo_or_dn=mo, vp_sb_mezz1_option_rom="platform-default")
mo_68 = BiosVfOnboardGraphics(parent_mo_or_dn=mo, vp_onboard_graphics="platform-default")
mo_69 = handle.query_dn("org-root/bios-prof-SRIOV/OptionROM-Enable")
mo_70 = BiosVfPOSTErrorPause(parent_mo_or_dn=mo, vp_post_error_pause="platform-default")
mo_71 = BiosVfAllUSBDevices(parent_mo_or_dn=mo, vp_all_usb_devices="platform-default")
mo_72 = BiosVfUSBBootConfig(parent_mo_or_dn=mo, vp_legacy_usb_support="platform-default", vp_make_device_non_bootable="platform-default")
mo_73 = BiosVfOnboardStorage(parent_mo_or_dn=mo, vp_onboard_scu_storage_support="platform-default")
mo_74 = BiosVfCPUPerformance(parent_mo_or_dn=mo, vp_cpu_performance="platform-default")
mo_75 = BiosVfSIOC1OptionROM(parent_mo_or_dn=mo, vp_sio_c1_option_rom="platform-default")
mo_76 = BiosVfSIOC2OptionROM(parent_mo_or_dn=mo, vp_sio_c2_option_rom="platform-default")
mo_77 = BiosVfACPI10Support(parent_mo_or_dn=mo, vp_acp_i10_support="platform-default")
mo_78 = BiosVfLvDIMMSupport(parent_mo_or_dn=mo, vp_lv_ddr_mode="platform-default")
mo_79 = BiosVfScrubPolicies(parent_mo_or_dn=mo, vp_patrol_scrub="platform-default", vp_demand_scrub="platform-default")
mo_80 = BiosVfMirroringMode(parent_mo_or_dn=mo, vp_mirroring_mode="platform-default")
mo_81 = BiosVfQPISnoopMode(parent_mo_or_dn=mo, vp_qpi_snoop_mode="platform-default")
mo_82 = BiosVfNUMAOptimized(parent_mo_or_dn=mo, vp_numa_optimized="platform-default")
mo_83 = BiosVfProcessorCMCI(parent_mo_or_dn=mo, vp_processor_cmci="platform-default")
mo_84 = handle.query_dn("org-root/bios-prof-SRIOV/PCH-SATA-Mode")
mo_85 = BiosVfLocalX2Apic(parent_mo_or_dn=mo, vp_local_x2_apic="platform-default")
mo_86 = BiosVfProcessorC1E(parent_mo_or_dn=mo, vp_processor_c1_e="platform-default")
mo_87 = BiosVfVGAPriority(parent_mo_or_dn=mo, vp_vga_priority="platform-default")
mo_88 = BiosVfASPMSupport(parent_mo_or_dn=mo, vp_aspm_support="platform-default")
mo_89 = handle.query_dn("org-root/bios-prof-SRIOV/Sriov-Config")
mo_90 = BiosVfSparingMode(parent_mo_or_dn=mo, vp_sparing_mode="platform-default")
mo_91 = handle.query_dn("org-root/bios-prof-SRIOV/TPM-Support")
mo_92 = BiosVfFRB2Timer(parent_mo_or_dn=mo, vp_fr_b2_timer="platform-default")
mo_93 = BiosVfPCIROMCLP(parent_mo_or_dn=mo, vp_pciromclp="platform-default")
mo_94 = BiosVfQuietBoot(parent_mo_or_dn=mo, vp_quiet_boot="platform-default")
mo_95 = BiosVfAltitude(parent_mo_or_dn=mo, vp_altitude="platform-default")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = BiosVProfile(parent_mo_or_dn=obj, policy_owner="local", name="usNIC", descr="Recommended bios settings for usNIC vNICs", reboot_on_update="no")
mo_1 = BiosVfUSBSystemIdlePowerOptimizingSetting(parent_mo_or_dn=mo, vp_usb_idle_power_optimizing="platform-default")
mo_2 = BiosVfIntelTrustedExecutionTechnology(parent_mo_or_dn=mo, vp_intel_trusted_execution_technology_support="platform-default")
mo_3 = BiosVfIntegratedGraphicsApertureSize(parent_mo_or_dn=mo, vp_integrated_graphics_aperture_size="platform-default")
mo_4 = BiosVfIntelVirtualizationTechnology(parent_mo_or_dn=mo, vp_intel_virtualization_technology="enabled")
mo_5 = BiosVfOSBootWatchdogTimerTimeout(parent_mo_or_dn=mo, vp_os_boot_watchdog_timer_timeout="platform-default")
mo_6 = BiosVfSelectMemoryRASConfiguration(parent_mo_or_dn=mo, vp_select_memory_ras_configuration="maximum-performance")
mo_7 = BiosVfProcessorEnergyConfiguration(parent_mo_or_dn=mo, vp_power_technology="platform-default", vp_energy_performance="platform-default")
mo_8 = BiosVfConsistentDeviceNameControl(parent_mo_or_dn=mo, vp_cdn_control="platform-default")
mo_9 = BiosVfOSBootWatchdogTimerPolicy(parent_mo_or_dn=mo, vp_os_boot_watchdog_timer_policy="platform-default")
mo_10 = BiosVfEnhancedPowerCappingSupport(parent_mo_or_dn=mo, vp_enhanced_power_capping="platform-default")
mo_11 = BiosVfCPUHardwarePowerManagement(parent_mo_or_dn=mo, vp_cpu_hardware_power_management="platform-default")
mo_12 = BiosVfEnhancedIntelSpeedStepTech(parent_mo_or_dn=mo, vp_enhanced_intel_speed_step_tech="enabled")
mo_13 = BiosVfPCILOMPortsConfiguration(parent_mo_or_dn=mo, vp_pc_ie10_glo_m2_link="platform-default")
mo_14 = BiosVfUSBFrontPanelAccessLock(parent_mo_or_dn=mo, vp_usb_front_panel_lock="platform-default")
mo_15 = BiosVfIntelEntrySASRAIDModule(parent_mo_or_dn=mo, vp_sasraid="platform-default", vp_sasraid_module="platform-default")
mo_16 = BiosVfRedirectionAfterBIOSPOST(parent_mo_or_dn=mo, vp_redirection_after_post="platform-default")
mo_17 = BiosVfMemoryMappedIOAbove4GB(parent_mo_or_dn=mo, vp_memory_mapped_io_above4_gb="disabled")
mo_18 = BiosVfQPILinkFrequencySelect(parent_mo_or_dn=mo, vp_qpi_link_frequency_select="platform-default")
mo_19 = BiosVfIntelHyperThreadingTech(parent_mo_or_dn=mo, vp_intel_hyper_threading_tech="disabled")
mo_20 = BiosVfEnergyPerformanceTuning(parent_mo_or_dn=mo, vp_pwr_perf_tuning="platform-default")
mo_21 = BiosVfProcessorPrefetchConfig(parent_mo_or_dn=mo, vp_dcuip_prefetcher="platform-default", vp_adjacent_cache_line_prefetcher="platform-default", vp_hardware_prefetcher="platform-default", vp_dcu_streamer_prefetch="platform-default")
mo_22 = BiosVfMaxVariableMTRRSetting(parent_mo_or_dn=mo, vp_processor_mtrr="platform-default")
mo_23 = handle.query_dn("org-root/bios-prof-usNIC/PCI-Slot-OptionROM-Enable")
mo_24 = BiosVfUEFIOSUseLegacyVideo(parent_mo_or_dn=mo, vp_uefios_use_legacy_video="platform-default")
mo_25 = BiosVfInterleaveConfiguration(parent_mo_or_dn=mo, vp_channel_interleaving="platform-default", vp_rank_interleaving="platform-default", vp_memory_interleaving="platform-default")
mo_26 = BiosVfFrequencyFloorOverride(parent_mo_or_dn=mo, vp_frequency_floor_override="platform-default")
mo_27 = BiosVfIntelVTForDirectedIO(parent_mo_or_dn=mo, vp_intel_vtd_pass_through_dma_support="platform-default", vp_intel_vtdats_support="enabled", vp_intel_vtd_interrupt_remapping="platform-default", vp_intel_vtd_coherency_support="enabled", vp_intel_vt_for_directed_io="enabled")
mo_28 = BiosVfMaximumMemoryBelow4GB(parent_mo_or_dn=mo, vp_maximum_memory_below4_gb="platform-default")
mo_29 = BiosVfResumeOnACPowerLoss(parent_mo_or_dn=mo, vp_resume_on_ac_power_loss="platform-default")
mo_30 = handle.query_dn("org-root/bios-prof-usNIC/Onboard-SATA-controller")
mo_31 = BiosVfTrustedPlatformModule(parent_mo_or_dn=mo, vp_trusted_platform_module_support="platform-default")
mo_32 = BiosVfOutOfBandManagement(parent_mo_or_dn=mo, vp_com_spcr_enable="platform-default")
mo_33 = BiosVfOSBootWatchdogTimer(parent_mo_or_dn=mo, vp_os_boot_watchdog_timer="platform-default")
mo_34 = BiosVfUSBPortConfiguration(parent_mo_or_dn=mo, vp_usb_port_front="platform-default", vp_usb_port_v_media="platform-default", vp_usb_port_kvm="platform-default", vp_port6064_emulation="platform-default", vp_usb_port_rear="platform-default", vp_usb_port_internal="platform-default", vp_usb_port_sd_card="platform-default")
mo_35 = BiosVfWorkloadConfiguration(parent_mo_or_dn=mo, vp_workload_configuration="platform-default")
mo_36 = BiosVfDDR3VoltageSelection(parent_mo_or_dn=mo, vp_dd_r3_voltage_selection="platform-default")
mo_37 = handle.query_dn("org-root/bios-prof-usNIC/UCSM-Boot-Mode-Control")
mo_38 = BiosVfIntelTurboBoostTech(parent_mo_or_dn=mo, vp_intel_turbo_boost_tech="enabled")
mo_39 = BiosVfPackageCStateLimit(parent_mo_or_dn=mo, vp_package_c_state_limit="platform-default")
mo_40 = handle.query_dn("org-root/bios-prof-usNIC/TPM-Pending-Operation")
mo_41 = BiosVfDRAMClockThrottling(parent_mo_or_dn=mo, vp_dram_clock_throttling="platform-default")
mo_42 = handle.query_dn("org-root/bios-prof-usNIC/CPU-Power-Management")
mo_43 = BiosVfPSTATECoordination(parent_mo_or_dn=mo, vp_pstate_coordination="platform-default")
mo_44 = BiosVfCoreMultiProcessing(parent_mo_or_dn=mo, vp_core_multi_processing="all")
mo_45 = BiosVfSerialPortAEnable(parent_mo_or_dn=mo, vp_serial_port_a_enable="platform-default")
mo_46 = BiosVfProcessorC3Report(parent_mo_or_dn=mo, vp_processor_c3_report="platform-default")
mo_47 = BiosVfProcessorC7Report(parent_mo_or_dn=mo, vp_processor_c7_report="platform-default")
mo_48 = BiosVfProcessorC6Report(parent_mo_or_dn=mo, vp_processor_c6_report="disabled")
mo_49 = BiosVfExecuteDisableBit(parent_mo_or_dn=mo, vp_execute_disable_bit="disabled")
mo_50 = BiosVfFrontPanelLockout(parent_mo_or_dn=mo, vp_front_panel_lockout="platform-default")
mo_51 = BiosVfIntegratedGraphics(parent_mo_or_dn=mo, vp_integrated_graphics="platform-default")
mo_52 = BiosVfDirectCacheAccess(parent_mo_or_dn=mo, vp_direct_cache_access="enabled")
mo_53 = BiosVfConsoleRedirection(parent_mo_or_dn=mo, vp_terminal_type="platform-default", vp_flow_control="platform-default", vp_baud_rate="platform-default", vp_putty_key_pad="platform-default", vp_console_redirection="platform-default", vp_legacy_os_redirection="platform-default")
mo_54 = BiosVfPCISlotLinkSpeed(parent_mo_or_dn=mo, vp_pc_ie_slot4_link_speed="platform-default", vp_pc_ie_slot3_link_speed="platform-default", vp_pc_ie_slot10_link_speed="platform-default", vp_pc_ie_slot9_link_speed="platform-default", vp_pc_ie_slot2_link_speed="platform-default", vp_pc_ie_slot8_link_speed="platform-default", vp_pc_ie_slot6_link_speed="platform-default", vp_pc_ie_slot5_link_speed="platform-default", vp_pc_ie_slot1_link_speed="platform-default", vp_pc_ie_slot7_link_speed="platform-default")
mo_55 = BiosVfAssertNMIOnSERR(parent_mo_or_dn=mo, vp_assert_nmi_on_serr="platform-default")
mo_56 = BiosVfAssertNMIOnPERR(parent_mo_or_dn=mo, vp_assert_nmi_on_perr="platform-default")
mo_57 = BiosVfIOENVMe1OptionROM(parent_mo_or_dn=mo, vp_ioenv_me1_option_rom="platform-default")
mo_58 = BiosVfIOENVMe2OptionROM(parent_mo_or_dn=mo, vp_ioenv_me2_option_rom="platform-default")
mo_59 = BiosVfIOESlot1OptionROM(parent_mo_or_dn=mo, vp_ioe_slot1_option_rom="platform-default")
mo_60 = BiosVfIOESlot2OptionROM(parent_mo_or_dn=mo, vp_ioe_slot2_option_rom="platform-default")
mo_61 = BiosVfIOEMezz1OptionROM(parent_mo_or_dn=mo, vp_ioe_mezz1_option_rom="platform-default")
mo_62 = BiosVfBootOptionRetry(parent_mo_or_dn=mo, vp_boot_option_retry="platform-default")
mo_63 = BiosVfUSBConfiguration(parent_mo_or_dn=mo, vp_xhci_mode="platform-default", vp_legacy_usb_support="platform-default")
mo_64 = BiosVfDramRefreshRate(parent_mo_or_dn=mo, vp_dram_refresh_rate="platform-default")
mo_65 = BiosVfProcessorCState(parent_mo_or_dn=mo, vp_processor_c_state="platform-default")
mo_66 = BiosVfSBNVMe1OptionROM(parent_mo_or_dn=mo, vp_sbnv_me1_option_rom="platform-default")
mo_67 = BiosVfSBMezz1OptionROM(parent_mo_or_dn=mo, vp_sb_mezz1_option_rom="platform-default")
mo_68 = BiosVfOnboardGraphics(parent_mo_or_dn=mo, vp_onboard_graphics="platform-default")
mo_69 = handle.query_dn("org-root/bios-prof-usNIC/OptionROM-Enable")
mo_70 = BiosVfPOSTErrorPause(parent_mo_or_dn=mo, vp_post_error_pause="platform-default")
mo_71 = BiosVfAllUSBDevices(parent_mo_or_dn=mo, vp_all_usb_devices="platform-default")
mo_72 = BiosVfUSBBootConfig(parent_mo_or_dn=mo, vp_legacy_usb_support="platform-default", vp_make_device_non_bootable="platform-default")
mo_73 = BiosVfOnboardStorage(parent_mo_or_dn=mo, vp_onboard_scu_storage_support="platform-default")
mo_74 = BiosVfCPUPerformance(parent_mo_or_dn=mo, vp_cpu_performance="platform-default")
mo_75 = BiosVfSIOC1OptionROM(parent_mo_or_dn=mo, vp_sio_c1_option_rom="platform-default")
mo_76 = BiosVfSIOC2OptionROM(parent_mo_or_dn=mo, vp_sio_c2_option_rom="platform-default")
mo_77 = BiosVfACPI10Support(parent_mo_or_dn=mo, vp_acp_i10_support="platform-default")
mo_78 = BiosVfLvDIMMSupport(parent_mo_or_dn=mo, vp_lv_ddr_mode="performance-mode")
mo_79 = BiosVfScrubPolicies(parent_mo_or_dn=mo, vp_patrol_scrub="platform-default", vp_demand_scrub="platform-default")
mo_80 = BiosVfMirroringMode(parent_mo_or_dn=mo, vp_mirroring_mode="platform-default")
mo_81 = BiosVfQPISnoopMode(parent_mo_or_dn=mo, vp_qpi_snoop_mode="platform-default")
mo_82 = BiosVfNUMAOptimized(parent_mo_or_dn=mo, vp_numa_optimized="enabled")
mo_83 = BiosVfProcessorCMCI(parent_mo_or_dn=mo, vp_processor_cmci="platform-default")
mo_84 = handle.query_dn("org-root/bios-prof-usNIC/PCH-SATA-Mode")
mo_85 = BiosVfLocalX2Apic(parent_mo_or_dn=mo, vp_local_x2_apic="platform-default")
mo_86 = BiosVfProcessorC1E(parent_mo_or_dn=mo, vp_processor_c1_e="disabled")
mo_87 = BiosVfVGAPriority(parent_mo_or_dn=mo, vp_vga_priority="platform-default")
mo_88 = BiosVfASPMSupport(parent_mo_or_dn=mo, vp_aspm_support="platform-default")
mo_89 = handle.query_dn("org-root/bios-prof-usNIC/Sriov-Config")
mo_90 = BiosVfSparingMode(parent_mo_or_dn=mo, vp_sparing_mode="platform-default")
mo_91 = handle.query_dn("org-root/bios-prof-usNIC/TPM-Support")
mo_92 = BiosVfFRB2Timer(parent_mo_or_dn=mo, vp_fr_b2_timer="platform-default")
mo_93 = BiosVfPCIROMCLP(parent_mo_or_dn=mo, vp_pciromclp="platform-default")
mo_94 = BiosVfQuietBoot(parent_mo_or_dn=mo, vp_quiet_boot="platform-default")
mo_95 = BiosVfAltitude(parent_mo_or_dn=mo, vp_altitude="platform-default")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = EquipmentChassisProfile(parent_mo_or_dn=obj, src_templ_name="UCS-S3260", name="S3260-Dual-4", maint_policy_name="UCS-S3260-Main", policy_owner="local", chassis_fw_policy_name="UCS-S3260-Firm", resolve_remote="yes", type="instance", disk_zoning_policy_name="UCS-S3260-Zoning")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = EquipmentChassisProfile(parent_mo_or_dn=obj, src_templ_name="UCS-S3260", name="S3260-Dual-2", maint_policy_name="UCS-S3260-Main", policy_owner="local", chassis_fw_policy_name="UCS-S3260-Firm", resolve_remote="yes", type="instance", disk_zoning_policy_name="UCS-S3260-Zoning")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = EquipmentChassisProfile(parent_mo_or_dn=obj, src_templ_name="UCS-S3260", name="S3260-Dual-1", maint_policy_name="UCS-S3260-Main", policy_owner="local", chassis_fw_policy_name="UCS-S3260-Firm", resolve_remote="yes", type="instance", disk_zoning_policy_name="UCS-S3260-Zoning")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = NwctrlDefinition(parent_mo_or_dn=obj, lldp_transmit="disabled", name="default", lldp_receive="disabled", mac_register_mode="only-native-vlan", policy_owner="local", cdp="disabled", uplink_fail_action="link-down")
mo_1 = DpsecMac(parent_mo_or_dn=mo, forge="allow", policy_owner="local")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = BiosVProfile(parent_mo_or_dn=obj, policy_owner="local", name="Ceph", descr="BIOS Policy for Ceph", reboot_on_update="no")
mo_1 = BiosVfUSBSystemIdlePowerOptimizingSetting(parent_mo_or_dn=mo, vp_usb_idle_power_optimizing="platform-default")
mo_2 = BiosVfIntelTrustedExecutionTechnology(parent_mo_or_dn=mo, vp_intel_trusted_execution_technology_support="platform-default")
mo_3 = BiosVfIntegratedGraphicsApertureSize(parent_mo_or_dn=mo, vp_integrated_graphics_aperture_size="platform-default")
mo_4 = BiosVfIntelVirtualizationTechnology(parent_mo_or_dn=mo, vp_intel_virtualization_technology="disabled")
mo_5 = BiosVfOSBootWatchdogTimerTimeout(parent_mo_or_dn=mo, vp_os_boot_watchdog_timer_timeout="platform-default")
mo_6 = BiosVfSelectMemoryRASConfiguration(parent_mo_or_dn=mo, vp_select_memory_ras_configuration="maximum-performance")
mo_7 = BiosVfProcessorEnergyConfiguration(parent_mo_or_dn=mo, vp_power_technology="performance", vp_energy_performance="performance")
mo_8 = BiosVfConsistentDeviceNameControl(parent_mo_or_dn=mo, vp_cdn_control="platform-default")
mo_9 = BiosVfOSBootWatchdogTimerPolicy(parent_mo_or_dn=mo, vp_os_boot_watchdog_timer_policy="platform-default")
mo_10 = BiosVfEnhancedPowerCappingSupport(parent_mo_or_dn=mo, vp_enhanced_power_capping="platform-default")
mo_11 = BiosVfCPUHardwarePowerManagement(parent_mo_or_dn=mo, vp_cpu_hardware_power_management="platform-default")
mo_12 = BiosVfEnhancedIntelSpeedStepTech(parent_mo_or_dn=mo, vp_enhanced_intel_speed_step_tech="enabled")
mo_13 = BiosVfPCILOMPortsConfiguration(parent_mo_or_dn=mo, vp_pc_ie10_glo_m2_link="platform-default")
mo_14 = BiosVfUSBFrontPanelAccessLock(parent_mo_or_dn=mo, vp_usb_front_panel_lock="platform-default")
mo_15 = BiosVfIntelEntrySASRAIDModule(parent_mo_or_dn=mo, vp_sasraid="platform-default", vp_sasraid_module="platform-default")
mo_16 = BiosVfRedirectionAfterBIOSPOST(parent_mo_or_dn=mo, vp_redirection_after_post="platform-default")
mo_17 = BiosVfMemoryMappedIOAbove4GB(parent_mo_or_dn=mo, vp_memory_mapped_io_above4_gb="platform-default")
mo_18 = BiosVfQPILinkFrequencySelect(parent_mo_or_dn=mo, vp_qpi_link_frequency_select="platform-default")
mo_19 = BiosVfIntelHyperThreadingTech(parent_mo_or_dn=mo, vp_intel_hyper_threading_tech="enabled")
mo_20 = BiosVfEnergyPerformanceTuning(parent_mo_or_dn=mo, vp_pwr_perf_tuning="os")
mo_21 = BiosVfProcessorPrefetchConfig(parent_mo_or_dn=mo, vp_dcuip_prefetcher="enabled", vp_adjacent_cache_line_prefetcher="enabled", vp_hardware_prefetcher="enabled", vp_dcu_streamer_prefetch="enabled")
mo_22 = BiosVfMaxVariableMTRRSetting(parent_mo_or_dn=mo, vp_processor_mtrr="platform-default")
mo_23 = handle.query_dn("org-root/bios-prof-Ceph/PCI-Slot-OptionROM-Enable")
mo_24 = BiosVfUEFIOSUseLegacyVideo(parent_mo_or_dn=mo, vp_uefios_use_legacy_video="platform-default")
mo_25 = BiosVfInterleaveConfiguration(parent_mo_or_dn=mo, vp_channel_interleaving="platform-default", vp_rank_interleaving="platform-default", vp_memory_interleaving="platform-default")
mo_26 = BiosVfFrequencyFloorOverride(parent_mo_or_dn=mo, vp_frequency_floor_override="enabled")
mo_27 = BiosVfIntelVTForDirectedIO(parent_mo_or_dn=mo, vp_intel_vtd_pass_through_dma_support="platform-default", vp_intel_vtdats_support="platform-default", vp_intel_vtd_interrupt_remapping="platform-default", vp_intel_vtd_coherency_support="platform-default", vp_intel_vt_for_directed_io="platform-default")
mo_28 = BiosVfMaximumMemoryBelow4GB(parent_mo_or_dn=mo, vp_maximum_memory_below4_gb="platform-default")
mo_29 = BiosVfResumeOnACPowerLoss(parent_mo_or_dn=mo, vp_resume_on_ac_power_loss="platform-default")
mo_30 = handle.query_dn("org-root/bios-prof-Ceph/Onboard-SATA-controller")
mo_31 = BiosVfTrustedPlatformModule(parent_mo_or_dn=mo, vp_trusted_platform_module_support="platform-default")
mo_32 = BiosVfOutOfBandManagement(parent_mo_or_dn=mo, vp_com_spcr_enable="platform-default")
mo_33 = BiosVfOSBootWatchdogTimer(parent_mo_or_dn=mo, vp_os_boot_watchdog_timer="platform-default")
mo_34 = BiosVfUSBPortConfiguration(parent_mo_or_dn=mo, vp_usb_port_front="platform-default", vp_usb_port_v_media="platform-default", vp_usb_port_kvm="platform-default", vp_port6064_emulation="platform-default", vp_usb_port_rear="platform-default", vp_usb_port_internal="platform-default", vp_usb_port_sd_card="platform-default")
mo_35 = BiosVfWorkloadConfiguration(parent_mo_or_dn=mo, vp_workload_configuration="io-sensitive")
mo_36 = BiosVfDDR3VoltageSelection(parent_mo_or_dn=mo, vp_dd_r3_voltage_selection="platform-default")
mo_37 = handle.query_dn("org-root/bios-prof-Ceph/UCSM-Boot-Mode-Control")
mo_38 = BiosVfIntelTurboBoostTech(parent_mo_or_dn=mo, vp_intel_turbo_boost_tech="enabled")
mo_39 = BiosVfPackageCStateLimit(parent_mo_or_dn=mo, vp_package_c_state_limit="auto")
mo_40 = handle.query_dn("org-root/bios-prof-Ceph/TPM-Pending-Operation")
mo_41 = BiosVfDRAMClockThrottling(parent_mo_or_dn=mo, vp_dram_clock_throttling="performance")
mo_42 = handle.query_dn("org-root/bios-prof-Ceph/CPU-Power-Management")
mo_43 = BiosVfPSTATECoordination(parent_mo_or_dn=mo, vp_pstate_coordination="hw-all")
mo_44 = BiosVfCoreMultiProcessing(parent_mo_or_dn=mo, vp_core_multi_processing="all")
mo_45 = BiosVfSerialPortAEnable(parent_mo_or_dn=mo, vp_serial_port_a_enable="platform-default")
mo_46 = BiosVfProcessorC3Report(parent_mo_or_dn=mo, vp_processor_c3_report="disabled")
mo_47 = BiosVfProcessorC7Report(parent_mo_or_dn=mo, vp_processor_c7_report="disabled")
mo_48 = BiosVfProcessorC6Report(parent_mo_or_dn=mo, vp_processor_c6_report="disabled")
mo_49 = BiosVfExecuteDisableBit(parent_mo_or_dn=mo, vp_execute_disable_bit="platform-default")
mo_50 = BiosVfFrontPanelLockout(parent_mo_or_dn=mo, vp_front_panel_lockout="platform-default")
mo_51 = BiosVfIntegratedGraphics(parent_mo_or_dn=mo, vp_integrated_graphics="platform-default")
mo_52 = BiosVfDirectCacheAccess(parent_mo_or_dn=mo, vp_direct_cache_access="enabled")
mo_53 = BiosVfConsoleRedirection(parent_mo_or_dn=mo, vp_terminal_type="platform-default", vp_flow_control="platform-default", vp_baud_rate="platform-default", vp_putty_key_pad="platform-default", vp_console_redirection="platform-default", vp_legacy_os_redirection="platform-default")
mo_54 = BiosVfPCISlotLinkSpeed(parent_mo_or_dn=mo, vp_pc_ie_slot4_link_speed="platform-default", vp_pc_ie_slot3_link_speed="platform-default", vp_pc_ie_slot10_link_speed="platform-default", vp_pc_ie_slot9_link_speed="platform-default", vp_pc_ie_slot2_link_speed="platform-default", vp_pc_ie_slot8_link_speed="platform-default", vp_pc_ie_slot6_link_speed="platform-default", vp_pc_ie_slot5_link_speed="platform-default", vp_pc_ie_slot1_link_speed="platform-default", vp_pc_ie_slot7_link_speed="platform-default")
mo_55 = BiosVfAssertNMIOnSERR(parent_mo_or_dn=mo, vp_assert_nmi_on_serr="platform-default")
mo_56 = BiosVfAssertNMIOnPERR(parent_mo_or_dn=mo, vp_assert_nmi_on_perr="platform-default")
mo_57 = BiosVfIOENVMe1OptionROM(parent_mo_or_dn=mo, vp_ioenv_me1_option_rom="platform-default")
mo_58 = BiosVfIOENVMe2OptionROM(parent_mo_or_dn=mo, vp_ioenv_me2_option_rom="platform-default")
mo_59 = BiosVfIOESlot1OptionROM(parent_mo_or_dn=mo, vp_ioe_slot1_option_rom="platform-default")
mo_60 = BiosVfIOESlot2OptionROM(parent_mo_or_dn=mo, vp_ioe_slot2_option_rom="platform-default")
mo_61 = BiosVfIOEMezz1OptionROM(parent_mo_or_dn=mo, vp_ioe_mezz1_option_rom="platform-default")
mo_62 = BiosVfBootOptionRetry(parent_mo_or_dn=mo, vp_boot_option_retry="platform-default")
mo_63 = BiosVfUSBConfiguration(parent_mo_or_dn=mo, vp_xhci_mode="platform-default", vp_legacy_usb_support="platform-default")
mo_64 = BiosVfDramRefreshRate(parent_mo_or_dn=mo, vp_dram_refresh_rate="1x")
mo_65 = BiosVfProcessorCState(parent_mo_or_dn=mo, vp_processor_c_state="disabled")
mo_66 = BiosVfSBNVMe1OptionROM(parent_mo_or_dn=mo, vp_sbnv_me1_option_rom="platform-default")
mo_67 = BiosVfSBMezz1OptionROM(parent_mo_or_dn=mo, vp_sb_mezz1_option_rom="platform-default")
mo_68 = BiosVfOnboardGraphics(parent_mo_or_dn=mo, vp_onboard_graphics="platform-default")
mo_69 = handle.query_dn("org-root/bios-prof-Ceph/OptionROM-Enable")
mo_70 = BiosVfPOSTErrorPause(parent_mo_or_dn=mo, vp_post_error_pause="platform-default")
mo_71 = BiosVfAllUSBDevices(parent_mo_or_dn=mo, vp_all_usb_devices="platform-default")
mo_72 = BiosVfUSBBootConfig(parent_mo_or_dn=mo, vp_legacy_usb_support="platform-default", vp_make_device_non_bootable="platform-default")
mo_73 = BiosVfOnboardStorage(parent_mo_or_dn=mo, vp_onboard_scu_storage_support="platform-default")
mo_74 = BiosVfCPUPerformance(parent_mo_or_dn=mo, vp_cpu_performance="enterprise")
mo_75 = BiosVfSIOC1OptionROM(parent_mo_or_dn=mo, vp_sio_c1_option_rom="platform-default")
mo_76 = BiosVfSIOC2OptionROM(parent_mo_or_dn=mo, vp_sio_c2_option_rom="platform-default")
mo_77 = BiosVfACPI10Support(parent_mo_or_dn=mo, vp_acp_i10_support="platform-default")
mo_78 = BiosVfLvDIMMSupport(parent_mo_or_dn=mo, vp_lv_ddr_mode="performance-mode")
mo_79 = BiosVfScrubPolicies(parent_mo_or_dn=mo, vp_patrol_scrub="disabled", vp_demand_scrub="disabled")
mo_80 = BiosVfMirroringMode(parent_mo_or_dn=mo, vp_mirroring_mode="platform-default")
mo_81 = BiosVfQPISnoopMode(parent_mo_or_dn=mo, vp_qpi_snoop_mode="platform-default")
mo_82 = BiosVfNUMAOptimized(parent_mo_or_dn=mo, vp_numa_optimized="enabled")
mo_83 = BiosVfProcessorCMCI(parent_mo_or_dn=mo, vp_processor_cmci="platform-default")
mo_84 = handle.query_dn("org-root/bios-prof-Ceph/PCH-SATA-Mode")
mo_85 = BiosVfLocalX2Apic(parent_mo_or_dn=mo, vp_local_x2_apic="platform-default")
mo_86 = BiosVfProcessorC1E(parent_mo_or_dn=mo, vp_processor_c1_e="disabled")
mo_87 = BiosVfVGAPriority(parent_mo_or_dn=mo, vp_vga_priority="platform-default")
mo_88 = BiosVfASPMSupport(parent_mo_or_dn=mo, vp_aspm_support="platform-default")
mo_89 = handle.query_dn("org-root/bios-prof-Ceph/Sriov-Config")
mo_90 = BiosVfSparingMode(parent_mo_or_dn=mo, vp_sparing_mode="platform-default")
mo_91 = handle.query_dn("org-root/bios-prof-Ceph/TPM-Support")
mo_92 = BiosVfFRB2Timer(parent_mo_or_dn=mo, vp_fr_b2_timer="platform-default")
mo_93 = BiosVfPCIROMCLP(parent_mo_or_dn=mo, vp_pciromclp="platform-default")
mo_94 = BiosVfQuietBoot(parent_mo_or_dn=mo, vp_quiet_boot="platform-default")
mo_95 = BiosVfAltitude(parent_mo_or_dn=mo, vp_altitude="auto")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = LsServer(parent_mo_or_dn=obj, uuid="derived", maint_policy_name="Server-Maint", stats_policy_name="default", ext_ip_state="none", bios_profile_name="Ceph", power_policy_name="No-Power-Cap", boot_policy_name="PXE-Boot", policy_owner="local", ext_ip_pool_name="ext-mgmt", scrub_policy_name="Disk-Scrub", ident_pool_name="UCS-Ceph-UUID-Pool", resolve_remote="yes", type="initial-template", name="UCS-C220M4S")
mo_1 = LsVConAssign(parent_mo_or_dn=mo, admin_vcon="1", vnic_name="Default", order="1", transport="ethernet", admin_host_port="ANY")
mo_2 = LsVConAssign(parent_mo_or_dn=mo, admin_vcon="1", vnic_name="Public", order="2", transport="ethernet", admin_host_port="ANY")
mo_3 = handle.query_dn("org-root/ls-UCS-C220M4S/vdrive-ref-Boot")
mo_4 = LstorageProfileBinding(parent_mo_or_dn=mo, storage_profile_name="C220M4S-MRAID")
mo_5 = VnicEther(parent_mo_or_dn=mo, nw_ctrl_policy_name="Enable-CDP", admin_host_port="ANY", admin_vcon="1", stats_policy_name="default", cdn_prop_in_sync="yes", switch_id="A-B", name="Default", order="1", qos_policy_name="QoS-Ceph", adaptor_profile_name="RHEL", ident_pool_name="UCS-Ceph-MAC-Pool", cdn_source="vnic-name", mtu="1500", nw_templ_name="Default-NIC", addr="derived")
mo_6 = VnicEtherIf(parent_mo_or_dn=mo_5, default_net="yes", name="default")
mo_7 = VnicEther(parent_mo_or_dn=mo, nw_ctrl_policy_name="Enable-CDP", admin_host_port="ANY", admin_vcon="1", stats_policy_name="default", cdn_prop_in_sync="yes", switch_id="A-B", name="Public", order="2", qos_policy_name="QoS-Ceph", adaptor_profile_name="RHEL", ident_pool_name="UCS-Ceph-MAC-Pool", cdn_source="vnic-name", mtu="9000", nw_templ_name="Public-NIC", addr="derived")
mo_8 = VnicEtherIf(parent_mo_or_dn=mo_7, default_net="no", name="Public")
mo_9 = VnicDefBeh(parent_mo_or_dn=mo, action="none", policy_owner="local", type="vhba")
mo_10 = VnicConnDef(parent_mo_or_dn=mo, )
mo_11 = VnicFcNode(parent_mo_or_dn=mo, ident_pool_name="node-default", addr="pool-derived")
mo_12 = LsRequirement(parent_mo_or_dn=mo, restrict_migration="no", name="C220M4S-MRAID")
mo_13 = FabricVCon(parent_mo_or_dn=mo, placement="physical", fabric="NONE", share="shared", select="all", transport="ethernet,fc", id="4", inst_type="manual")
mo_14 = FabricVCon(parent_mo_or_dn=mo, placement="physical", fabric="NONE", share="shared", select="all", transport="ethernet,fc", id="3", inst_type="manual")
mo_15 = FabricVCon(parent_mo_or_dn=mo, placement="physical", fabric="NONE", share="shared", select="all", transport="ethernet,fc", id="2", inst_type="manual")
mo_16 = FabricVCon(parent_mo_or_dn=mo, placement="physical", fabric="NONE", share="shared", select="all", transport="ethernet,fc", id="1", inst_type="manual")
mo_17 = LsPower(parent_mo_or_dn=mo, state="up")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = LsServer(parent_mo_or_dn=obj, uuid="derived", maint_policy_name="Server-Maint", stats_policy_name="default", ext_ip_state="none", bios_profile_name="Ceph", power_policy_name="No-Power-Cap", boot_policy_name="PXE-Boot", policy_owner="local", ext_ip_pool_name="ext-mgmt", scrub_policy_name="Disk-Scrub", ident_pool_name="UCS-Ceph-UUID-Pool", resolve_remote="yes", type="initial-template", name="C220M4S-LSI")
mo_1 = LsVConAssign(parent_mo_or_dn=mo, admin_vcon="1", vnic_name="Default", order="1", transport="ethernet", admin_host_port="ANY")
mo_2 = LsVConAssign(parent_mo_or_dn=mo, admin_vcon="1", vnic_name="Public", order="2", transport="ethernet", admin_host_port="ANY")
mo_3 = handle.query_dn("org-root/ls-C220M4S-LSI/vdrive-ref-Boot")
mo_4 = LstorageProfileBinding(parent_mo_or_dn=mo, storage_profile_name="C220M4S-LSI")
mo_5 = VnicEther(parent_mo_or_dn=mo, nw_ctrl_policy_name="Enable-CDP", admin_host_port="ANY", admin_vcon="1", stats_policy_name="default", cdn_prop_in_sync="yes", switch_id="A-B", name="Default", order="1", qos_policy_name="QoS-Ceph", adaptor_profile_name="RHEL", ident_pool_name="UCS-Ceph-MAC-Pool", cdn_source="vnic-name", mtu="1500", nw_templ_name="Default-NIC", addr="derived")
mo_6 = VnicEtherIf(parent_mo_or_dn=mo_5, default_net="yes", name="default")
mo_7 = VnicEther(parent_mo_or_dn=mo, nw_ctrl_policy_name="Enable-CDP", admin_host_port="ANY", admin_vcon="1", stats_policy_name="default", cdn_prop_in_sync="yes", switch_id="A-B", name="Public", order="2", qos_policy_name="QoS-Ceph", adaptor_profile_name="RHEL", ident_pool_name="UCS-Ceph-MAC-Pool", cdn_source="vnic-name", mtu="9000", nw_templ_name="Public-NIC", addr="derived")
mo_8 = VnicEtherIf(parent_mo_or_dn=mo_7, default_net="no", name="Public")
mo_9 = VnicDefBeh(parent_mo_or_dn=mo, action="none", policy_owner="local", type="vhba")
mo_10 = VnicConnDef(parent_mo_or_dn=mo, )
mo_11 = VnicFcNode(parent_mo_or_dn=mo, ident_pool_name="node-default", addr="pool-derived")
mo_12 = LsRequirement(parent_mo_or_dn=mo, restrict_migration="no", name="C220M4S-LSI")
mo_13 = FabricVCon(parent_mo_or_dn=mo, placement="physical", fabric="NONE", share="shared", select="all", transport="ethernet,fc", id="4", inst_type="manual")
mo_14 = FabricVCon(parent_mo_or_dn=mo, placement="physical", fabric="NONE", share="shared", select="all", transport="ethernet,fc", id="3", inst_type="manual")
mo_15 = FabricVCon(parent_mo_or_dn=mo, placement="physical", fabric="NONE", share="shared", select="all", transport="ethernet,fc", id="2", inst_type="manual")
mo_16 = FabricVCon(parent_mo_or_dn=mo, placement="physical", fabric="NONE", share="shared", select="all", transport="ethernet,fc", id="1", inst_type="manual")
mo_17 = LsPower(parent_mo_or_dn=mo, state="up")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = ComputeScrubPolicy(parent_mo_or_dn=obj, flex_flash_scrub="no", policy_owner="local", bios_settings_scrub="no", disk_scrub="no", name="default")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = LsmaintMaintPolicy(parent_mo_or_dn=obj, policy_owner="local", soft_shutdown_timer="150-secs", name="default", uptime_disr="immediate")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = handle.query_dn("org-root/vm-lc-policy")
mo.vm_retention = "15"
mo.vnic_retention = "15"
mo.policy_owner = "local"
handle.set_mo(mo)
handle.commit()

obj = handle.query_dn("org-root")
mo = FabricLacpPolicy(parent_mo_or_dn=obj, policy_owner="local", suspend_individual="false", fast_timer="normal", name="default")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = handle.query_dn("org-root/fw-auto-sync")
mo.sync_state = "No Actions"
mo.policy_owner = "local"
mo.config_issue = "No Issues"
mo.name = "default"
handle.set_mo(mo)
handle.commit()

obj = handle.query_dn("org-root")
mo = EquipmentChassisProfile(parent_mo_or_dn=obj, name="UCS-S3260", descr="Chassis Template for UCS S3260", maint_policy_name="UCS-S3260-Main", policy_owner="local", chassis_fw_policy_name="UCS-S3260-Firm", resolve_remote="yes", type="updating-template", disk_zoning_policy_name="UCS-S3260-Zoning")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("org-root")
mo = handle.query_dn("org-root/udld-policy")
mo.recovery_action = "none"
mo.policy_owner = "local"
mo.name = "default"
mo.msg_interval = "15"
handle.set_mo(mo)
handle.commit()

obj = handle.query_dn("org-root")
mo = handle.query_dn("org-root/lan-policy")
handle.commit()

obj = handle.query_dn("org-root")
mo = handle.query_dn("org-root/psu-policy")
mo.policy_owner = "local"
mo.redundancy = "n+1"
handle.set_mo(mo)
handle.commit()

obj = handle.query_dn("org-root")
mo = handle.query_dn("org-root/beh-vnic")
mo.action = "hw-inherit"
mo.policy_owner = "local"
handle.set_mo(mo)
handle.commit()

obj = handle.query_dn("org-root")
mo = handle.query_dn("org-root/beh-vhba")
mo.action = "none"
mo.policy_owner = "local"
handle.set_mo(mo)
handle.commit()

obj = handle.query_dn("org-root")
mo = handle.query_dn("org-root/log-SEL")
mo_1 = handle.query_dn("org-root/log-SEL/backup")
mo_1.clear_on_backup = "no"
mo_1.format = "ascii"
mo_1.interval = "1hour"
mo_1.remote_path = "/"
mo_1.proto = "ftp"
handle.set_mo(mo_1)
handle.commit()


obj = handle.query_dn("fabric")
mo = handle.query_dn("fabric/zone-id-universe")
handle.commit()

obj = handle.query_dn("fabric")
mo = handle.query_dn("fabric/lan-access")
handle.commit()

obj = handle.query_dn("fabric")
mo = handle.query_dn("fabric/eth-estc")
mo_1 = StatsThresholdPolicy(parent_mo_or_dn=mo, policy_owner="local", name="default")
handle.add_mo(mo_1, True)
mo_2 = NwctrlDefinition(parent_mo_or_dn=mo, lldp_transmit="enabled", name="default", lldp_receive="enabled", mac_register_mode="only-native-vlan", policy_owner="local", cdp="disabled", uplink_fail_action="link-down")
mo_3 = DpsecMac(parent_mo_or_dn=mo_2, forge="allow", policy_owner="local")
handle.add_mo(mo_2, True)
mo_4 = FabricVlan(parent_mo_or_dn=mo, sharing="none", name="default", compression_type="included", policy_owner="local", default_net="no", id="1")
handle.add_mo(mo_4, True)
mo_5 = handle.query_dn("fabric/eth-estc/B")
mo_6 = handle.query_dn("fabric/eth-estc/A")
handle.commit()

obj = handle.query_dn("fabric")
mo = handle.query_dn("fabric/Cabling")
mo_1 = handle.query_dn("fabric/Cabling/B")
mo_2 = handle.query_dn("fabric/Cabling/A")
handle.commit()

obj = handle.query_dn("fabric")
mo = handle.query_dn("fabric/fc-estc")
mo_1 = StatsThresholdPolicy(parent_mo_or_dn=mo, policy_owner="local", name="default")
handle.add_mo(mo_1, True)
mo_2 = FabricVsan(parent_mo_or_dn=mo, zoning_state="disabled", policy_owner="local", id="1", name="default", fcoe_vlan="4048")
handle.add_mo(mo_2, True)
mo_3 = handle.query_dn("fabric/fc-estc/bhnet")
mo_4 = handle.query_dn("fabric/fc-estc/B")
mo_5 = handle.query_dn("fabric/fc-estc/A")
handle.commit()

obj = handle.query_dn("fabric")
mo = handle.query_dn("fabric/server")
mo_1 = StatsThresholdPolicy(parent_mo_or_dn=mo, policy_owner="local", name="default")
mo_2 = StatsThresholdClass(parent_mo_or_dn=mo_1, stats_class_id="etherNiErrStats", policy_owner="local")
mo_3 = StatsThr64Definition(parent_mo_or_dn=mo_2, auto_recovery_time="10", auto_recovery="disabled", error_disable_fi_port="no", policy_owner="local", normal_value="0", prop_id="etherNiErrStatscrcDelta")
mo_4 = StatsThr64Value(parent_mo_or_dn=mo_3, direction="aboveNormal", escalating="5", deescalating="3", policy_owner="local", severity="major")
mo_5 = StatsThresholdClass(parent_mo_or_dn=mo_1, stats_class_id="etherErrStats", policy_owner="local")
mo_6 = StatsThr64Definition(parent_mo_or_dn=mo_5, auto_recovery_time="10", auto_recovery="disabled", error_disable_fi_port="no", policy_owner="local", normal_value="0", prop_id="etherErrStatsrcvDelta")
mo_7 = StatsThr64Value(parent_mo_or_dn=mo_6, direction="aboveNormal", escalating="5", deescalating="3", policy_owner="local", severity="major")
handle.add_mo(mo_1, True)
mo_8 = handle.query_dn("fabric/server/sw-B")
mo_9 = FabricDceSwSrvEp(parent_mo_or_dn=mo_8, admin_state="enabled", auto_negotiate="yes", slot_id="1", port_id="19")
handle.add_mo(mo_9, True)
mo_10 = FabricDceSwSrvEp(parent_mo_or_dn=mo_8, admin_state="enabled", auto_negotiate="yes", slot_id="1", port_id="18")
handle.add_mo(mo_10, True)
mo_11 = FabricDceSwSrvEp(parent_mo_or_dn=mo_8, admin_state="enabled", auto_negotiate="yes", slot_id="1", port_id="17")
handle.add_mo(mo_11, True)
mo_12 = FabricDceSwSrvEp(parent_mo_or_dn=mo_8, admin_state="enabled", auto_negotiate="yes", slot_id="1", port_id="16")
handle.add_mo(mo_12, True)
mo_13 = FabricDceSwSrvEp(parent_mo_or_dn=mo_8, admin_state="enabled", auto_negotiate="yes", slot_id="1", port_id="15")
handle.add_mo(mo_13, True)
mo_14 = FabricDceSwSrvEp(parent_mo_or_dn=mo_8, admin_state="enabled", auto_negotiate="yes", slot_id="1", port_id="14")
handle.add_mo(mo_14, True)
mo_15 = FabricDceSwSrvEp(parent_mo_or_dn=mo_8, admin_state="enabled", auto_negotiate="yes", slot_id="1", port_id="13")
handle.add_mo(mo_15, True)
mo_16 = FabricDceSwSrvEp(parent_mo_or_dn=mo_8, admin_state="enabled", auto_negotiate="yes", slot_id="1", port_id="20")
handle.add_mo(mo_16, True)
mo_17 = FabricDceSwSrvEp(parent_mo_or_dn=mo_8, admin_state="enabled", auto_negotiate="yes", slot_id="1", port_id="8")
handle.add_mo(mo_17, True)
mo_18 = FabricDceSwSrvEp(parent_mo_or_dn=mo_8, admin_state="enabled", auto_negotiate="yes", slot_id="1", port_id="7")
handle.add_mo(mo_18, True)
mo_19 = FabricDceSwSrvEp(parent_mo_or_dn=mo_8, admin_state="enabled", auto_negotiate="yes", slot_id="1", port_id="4")
handle.add_mo(mo_19, True)
mo_20 = FabricDceSwSrvEp(parent_mo_or_dn=mo_8, admin_state="enabled", auto_negotiate="yes", slot_id="1", port_id="3")
handle.add_mo(mo_20, True)
mo_21 = FabricDceSwSrvEp(parent_mo_or_dn=mo_8, admin_state="enabled", auto_negotiate="yes", slot_id="1", port_id="2")
handle.add_mo(mo_21, True)
mo_22 = FabricDceSwSrvEp(parent_mo_or_dn=mo_8, admin_state="enabled", auto_negotiate="yes", slot_id="1", port_id="1")
handle.add_mo(mo_22, True)
mo_23 = handle.query_dn("fabric/server/sw-A")
mo_24 = FabricDceSwSrvEp(parent_mo_or_dn=mo_23, admin_state="enabled", auto_negotiate="yes", slot_id="1", port_id="19")
handle.add_mo(mo_24, True)
mo_25 = FabricDceSwSrvEp(parent_mo_or_dn=mo_23, admin_state="enabled", auto_negotiate="yes", slot_id="1", port_id="18")
handle.add_mo(mo_25, True)
mo_26 = FabricDceSwSrvEp(parent_mo_or_dn=mo_23, admin_state="enabled", auto_negotiate="yes", slot_id="1", port_id="17")
handle.add_mo(mo_26, True)
mo_27 = FabricDceSwSrvEp(parent_mo_or_dn=mo_23, admin_state="enabled", auto_negotiate="yes", slot_id="1", port_id="16")
handle.add_mo(mo_27, True)
mo_28 = FabricDceSwSrvEp(parent_mo_or_dn=mo_23, admin_state="enabled", auto_negotiate="yes", slot_id="1", port_id="15")
handle.add_mo(mo_28, True)
mo_29 = FabricDceSwSrvEp(parent_mo_or_dn=mo_23, admin_state="enabled", auto_negotiate="yes", slot_id="1", port_id="14")
handle.add_mo(mo_29, True)
mo_30 = FabricDceSwSrvEp(parent_mo_or_dn=mo_23, admin_state="enabled", auto_negotiate="yes", slot_id="1", port_id="13")
handle.add_mo(mo_30, True)
mo_31 = FabricDceSwSrvEp(parent_mo_or_dn=mo_23, admin_state="enabled", auto_negotiate="yes", slot_id="1", port_id="20")
handle.add_mo(mo_31, True)
mo_32 = FabricDceSwSrvEp(parent_mo_or_dn=mo_23, admin_state="enabled", auto_negotiate="yes", slot_id="1", port_id="8")
handle.add_mo(mo_32, True)
mo_33 = FabricDceSwSrvEp(parent_mo_or_dn=mo_23, admin_state="enabled", auto_negotiate="yes", slot_id="1", port_id="7")
handle.add_mo(mo_33, True)
mo_34 = FabricDceSwSrvEp(parent_mo_or_dn=mo_23, admin_state="enabled", auto_negotiate="yes", slot_id="1", port_id="4")
handle.add_mo(mo_34, True)
mo_35 = FabricDceSwSrvEp(parent_mo_or_dn=mo_23, admin_state="enabled", auto_negotiate="yes", slot_id="1", port_id="3")
handle.add_mo(mo_35, True)
mo_36 = FabricDceSwSrvEp(parent_mo_or_dn=mo_23, admin_state="enabled", auto_negotiate="yes", slot_id="1", port_id="2")
handle.add_mo(mo_36, True)
mo_37 = FabricDceSwSrvEp(parent_mo_or_dn=mo_23, admin_state="enabled", auto_negotiate="yes", slot_id="1", port_id="1")
handle.add_mo(mo_37, True)
handle.commit()

obj = handle.query_dn("fabric")
mo = handle.query_dn("fabric/lanmon")
mo_1 = handle.query_dn("fabric/lanmon/eth-flow-monitoring")
mo_2 = handle.query_dn("fabric/lanmon/eth-flow-monitoring/flow-exporter-profile-default")
mo_3 = handle.query_dn("fabric/lanmon/eth-flow-monitoring/flow-record-full-layer2")
mo_4 = handle.query_dn("fabric/lanmon/eth-flow-monitoring/flow-record-full-ipv6")
mo_5 = handle.query_dn("fabric/lanmon/eth-flow-monitoring/flow-record-full-ipv4")
mo_6 = handle.query_dn("fabric/lanmon/eth-flow-monitoring/flow-timeout-default")
mo_7 = handle.query_dn("fabric/lanmon/eth-flow-monitoring/B")
mo_8 = handle.query_dn("fabric/lanmon/eth-flow-monitoring/A")
mo_9 = handle.query_dn("fabric/lanmon/B")
mo_10 = handle.query_dn("fabric/lanmon/A")
handle.commit()

obj = handle.query_dn("fabric")
mo = handle.query_dn("fabric/sanmon")
mo_1 = handle.query_dn("fabric/sanmon/B")
mo_2 = handle.query_dn("fabric/sanmon/A")
handle.commit()

obj = handle.query_dn("fabric")
mo = handle.query_dn("fabric/lan")
mo.vlan_compression = "disabled"
mo.mac_aging = "mode-default"
mo.mode = "end-host"
mo_1 = FabricEthLinkProfile(parent_mo_or_dn=mo, policy_owner="local", name="default", udld_link_policy_name="default")
mo_2 = FabricUdldLinkPolicy(parent_mo_or_dn=mo, policy_owner="local", admin_state="disabled", mode="normal", name="default")
mo_3 = StatsThresholdPolicy(parent_mo_or_dn=mo, policy_owner="local", name="default")
mo_4 = handle.query_dn("fabric/lan/vm-network-sets")
mo_5 = FabricNetGroup(parent_mo_or_dn=mo, policy_owner="local", type="mgmt", name="Ceph")
mo_6 = FabricEthVlanPc(parent_mo_or_dn=mo_5, name="vPC101", is_native="no", admin_speed="10gbps", switch_id="B", admin_state="enabled", oper_speed="10gbps", port_id="101")
mo_7 = FabricEthVlanPc(parent_mo_or_dn=mo_5, name="vPC100", is_native="no", admin_speed="10gbps", switch_id="A", admin_state="enabled", oper_speed="10gbps", port_id="100")
mo_8 = FabricPooledVlan(parent_mo_or_dn=mo_5, name="Cluster")
mo_9 = FabricPooledVlan(parent_mo_or_dn=mo_5, name="Public")
mo_10 = handle.query_dn("fabric/lan/network-sets")
mo_11 = FabricVlan(parent_mo_or_dn=mo, sharing="none", name="default", compression_type="included", policy_owner="local", default_net="yes", id="1")
mo_12 = FabricVlan(parent_mo_or_dn=mo, sharing="none", name="Cluster", compression_type="included", policy_owner="local", default_net="no", id="20")
mo_13 = MgmtInbandProfile(parent_mo_or_dn=mo, monitor_interval="1")
mo_14 = FabricVlan(parent_mo_or_dn=mo, sharing="none", name="Public", compression_type="included", policy_owner="local", default_net="no", id="10")
mo_15 = handle.query_dn("fabric/lan/profiles")
mo_16 = FlowctrlDefinition(parent_mo_or_dn=mo, policy_owner="local")
mo_17 = FlowctrlItem(parent_mo_or_dn=mo_16, snd="off", rcv="off", prio="auto", name="default")
mo_18 = QosclassDefinition(parent_mo_or_dn=mo, policy_owner="local")
mo_19 = QosclassEthBE(parent_mo_or_dn=mo_18, multicast_optimize="no", weight="10", mtu="9216")
mo_20 = QosclassEthClassified(parent_mo_or_dn=mo_18, cos="5", weight="10", drop="no-drop", multicast_optimize="no", mtu="normal", priority="platinum", admin_state="disabled")
mo_21 = QosclassEthClassified(parent_mo_or_dn=mo_18, cos="2", weight="8", drop="drop", multicast_optimize="no", mtu="normal", priority="silver", admin_state="disabled")
mo_22 = QosclassEthClassified(parent_mo_or_dn=mo_18, cos="1", weight="7", drop="drop", multicast_optimize="no", mtu="normal", priority="bronze", admin_state="disabled")
mo_23 = QosclassEthClassified(parent_mo_or_dn=mo_18, cos="4", weight="9", drop="drop", multicast_optimize="no", mtu="normal", priority="gold", admin_state="disabled")
mo_24 = QosclassFc(parent_mo_or_dn=mo_18, cos="3", weight="none")
mo_25 = handle.query_dn("fabric/lan/B")
mo_26 = FabricEthLanPc(parent_mo_or_dn=mo_25, name="vPC101", flow_ctrl_policy="default", admin_speed="40gbps", auto_negotiate="yes", admin_state="enabled", oper_speed="40gbps", port_id="101", lacp_policy_name="default")
mo_27 = FabricEthLanPcEp(parent_mo_or_dn=mo_26, admin_state="enabled", auto_negotiate="yes", slot_id="1", port_id="26", eth_link_profile_name="default")
mo_28 = FabricEthLanPcEp(parent_mo_or_dn=mo_26, admin_state="enabled", auto_negotiate="yes", slot_id="1", port_id="25", eth_link_profile_name="default")
mo_29 = FabricEthLanPcEp(parent_mo_or_dn=mo_26, admin_state="enabled", auto_negotiate="yes", slot_id="1", port_id="24", eth_link_profile_name="default")
mo_30 = FabricEthLanPcEp(parent_mo_or_dn=mo_26, admin_state="enabled", auto_negotiate="yes", slot_id="1", port_id="23", eth_link_profile_name="default")
handle.add_mo(mo_26, True)
mo_31 = handle.query_dn("fabric/lan/A")
mo_32 = FabricEthLanPc(parent_mo_or_dn=mo_31, name="vPC100", flow_ctrl_policy="default", admin_speed="40gbps", auto_negotiate="yes", admin_state="enabled", oper_speed="40gbps", port_id="100", lacp_policy_name="default")
mo_33 = FabricEthLanPcEp(parent_mo_or_dn=mo_32, admin_state="enabled", auto_negotiate="yes", slot_id="1", port_id="26", eth_link_profile_name="default")
mo_34 = FabricEthLanPcEp(parent_mo_or_dn=mo_32, admin_state="enabled", auto_negotiate="yes", slot_id="1", port_id="25", eth_link_profile_name="default")
mo_35 = FabricEthLanPcEp(parent_mo_or_dn=mo_32, admin_state="enabled", auto_negotiate="yes", slot_id="1", port_id="24", eth_link_profile_name="default")
mo_36 = FabricEthLanPcEp(parent_mo_or_dn=mo_32, admin_state="enabled", auto_negotiate="yes", slot_id="1", port_id="23", eth_link_profile_name="default")
handle.add_mo(mo_32, True)
handle.set_mo(mo)
handle.commit()

obj = handle.query_dn("fabric")
mo = handle.query_dn("fabric/san")
mo.mode = "end-host"
mo_1 = StatsThresholdPolicy(parent_mo_or_dn=mo, policy_owner="local", name="default")
mo_2 = FabricVsan(parent_mo_or_dn=mo, zoning_state="disabled", policy_owner="local", id="1", name="default", fcoe_vlan="4048")
mo_3 = FabricFcSan(parent_mo_or_dn=mo, id="B", uplink_trunking="disabled")
mo_4 = FabricFcSan(parent_mo_or_dn=mo, id="A", uplink_trunking="disabled")
handle.set_mo(mo)
handle.commit()

obj = handle.query_dn("fabric")
mo = handle.query_dn("fabric/B")
handle.commit()

obj = handle.query_dn("fabric")
mo = handle.query_dn("fabric/A")
handle.commit()


obj = handle.query_dn("fault")
mo = handle.query_dn("fault/fault-policy")
mo.retention_interval = "00:01:00:00"
mo.ack_action = "delete-on-clear"
mo.name = "default"
mo.size_limit = "max"
mo.clear_action = "retain"
mo.policy_owner = "local"
mo.pinning_expiration_interval = "01:00:00:00"
mo.flap_interval = "10"
mo.clear_interval = "00:00:20:00"
handle.set_mo(mo)
handle.commit()


obj = handle.query_dn("stats")
mo = handle.query_dn("stats/coll-policy-chassis")
mo.reporting_interval = "15minutes"
mo.collection_interval = "1minute"
handle.set_mo(mo)
handle.commit()

obj = handle.query_dn("stats")
mo = handle.query_dn("stats/coll-policy-adapter")
mo.reporting_interval = "15minutes"
mo.collection_interval = "1minute"
handle.set_mo(mo)
handle.commit()

obj = handle.query_dn("stats")
mo = handle.query_dn("stats/coll-policy-server")
mo.reporting_interval = "15minutes"
mo.collection_interval = "1minute"
handle.set_mo(mo)
handle.commit()

obj = handle.query_dn("stats")
mo = handle.query_dn("stats/coll-policy-host")
mo.reporting_interval = "15minutes"
mo.collection_interval = "1minute"
handle.set_mo(mo)
handle.commit()

obj = handle.query_dn("stats")
mo = handle.query_dn("stats/coll-policy-port")
mo.reporting_interval = "15minutes"
mo.collection_interval = "1minute"
handle.set_mo(mo)
handle.commit()

obj = handle.query_dn("stats")
mo = handle.query_dn("stats/coll-policy-fex")
mo.reporting_interval = "15minutes"
mo.collection_interval = "1minute"
handle.set_mo(mo)
handle.commit()


obj = handle.query_dn("sys")
mo = handle.query_dn("sys/extmgmt-intf-monitor-policy")
mo.monitor_mechanism = "gatewayPing"
mo.max_fail_report_count = "3"
mo.enable_ha_failover = "yes"
mo.poll_interval = "90"
mo.policy_owner = "local"
mo.admin_state = "enabled"
mo_1 = ExtmgmtNdiscTargets(parent_mo_or_dn=mo, ipv6_target1="::", ipv6_target3="::", max_deadline_timeout="10", number_of_ndisc_requests="3", ipv6_target2="::")
mo_2 = ExtmgmtArpTargets(parent_mo_or_dn=mo, target_ip1="0.0.0.0", target_ip3="0.0.0.0", target_ip2="0.0.0.0", max_deadline_timeout="10", number_of_arp_requests="3")
mo_3 = ExtmgmtMiiStatus(parent_mo_or_dn=mo, retry_interval="5", max_retry_count="3")
mo_4 = handle.query_dn("sys/extmgmt-intf-monitor-policy/gw-ping-policy")
handle.set_mo(mo)
handle.commit()

obj = handle.query_dn("sys")
mo = TrigSched(parent_mo_or_dn=obj, policy_owner="local", admin_state="untriggered", name="exp-bkup-outdate", descr="Auto Created by the System for raising fault once cfg backup export is found outdated")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("sys")
mo = handle.query_dn("sys/network-feature-cont")
mo_1 = handle.query_dn("sys/network-feature-cont/network-feature-VNIC_PAIRING_FEATURE")
mo_2 = handle.query_dn("sys/network-feature-cont/network-feature-USNIC_VMQ_FEATURE")
mo_3 = handle.query_dn("sys/network-feature-cont/network-feature-NETFLOW_FEATURE")
mo_4 = handle.query_dn("sys/network-feature-cont/network-feature-PVLAN_FEATURE")
handle.commit()

obj = handle.query_dn("sys")
mo = handle.query_dn("sys/storage-feature-cont")
mo_1 = handle.query_dn("sys/storage-feature-cont/storage-feature-STORAGE_CONNECTION_FEATURE")
mo_2 = handle.query_dn("sys/storage-feature-cont/storage-feature-STORAGE_PROFILE_FEATURE")
mo_3 = handle.query_dn("sys/storage-feature-cont/storage-feature-ISCSI_IPV6_FEATURE")
mo_4 = handle.query_dn("sys/storage-feature-cont/storage-feature-FC_ZONING_FEATURE")
handle.commit()

obj = handle.query_dn("sys")
mo = handle.query_dn("sys/server-feature-cont")
mo_1 = handle.query_dn("sys/server-feature-cont/server-feature-EXCLUDE_FIRMWARE_FOR_COMPONENT_POLICY_FEATURE")
mo_2 = handle.query_dn("sys/server-feature-cont/server-feature-POPULATE_TEMPLATE_NAME_FEATURE")
mo_3 = handle.query_dn("sys/server-feature-cont/server-feature-ADVANCED_BOOT_ORDER_FEATURE")
mo_4 = handle.query_dn("sys/server-feature-cont/server-feature-MAINTENANCE_POLICY_FEATURE")
mo_5 = handle.query_dn("sys/server-feature-cont/server-feature-HEALTH_POLICY_FEATURE")
mo_6 = handle.query_dn("sys/server-feature-cont/server-feature-IN_BAND_MGMT_FEATURE")
mo_7 = handle.query_dn("sys/server-feature-cont/server-feature-POLICY_MAP_FEATURE")
mo_8 = handle.query_dn("sys/server-feature-cont/server-feature-GLOBAL_SP_FEATURE")
handle.commit()

obj = handle.query_dn("sys")
mo = TrigLocalSched(parent_mo_or_dn=obj, policy_owner="local", admin_state="untriggered")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("sys")
mo = handle.query_dn("sys/env-feature-cont")
mo_1 = handle.query_dn("sys/env-feature-cont/env-feature-ESTIMATE_IMPACT_ON_RECONNECT")
mo_2 = handle.query_dn("sys/env-feature-cont/env-feature-UCS_REGISTRATION_FEATURE")
mo_3 = handle.query_dn("sys/env-feature-cont/env-feature-REMOTE_OPERATION_FEATURE")
mo_4 = handle.query_dn("sys/env-feature-cont/env-feature-HEALTH_REPORTING_FEATURE")
mo_5 = handle.query_dn("sys/env-feature-cont/env-feature-DC_POWER_GROUP_FEATURE")
mo_6 = handle.query_dn("sys/env-feature-cont/env-feature-POWER_GROUP_FEATURE")
handle.commit()

obj = handle.query_dn("sys")
mo = TrigSched(parent_mo_or_dn=obj, policy_owner="local", admin_state="untriggered", name="default")
handle.add_mo(mo, True)
handle.commit()

obj = handle.query_dn("sys")
mo = handle.query_dn("sys/HaController")
handle.set_mo(mo)
handle.commit()

obj = handle.query_dn("sys")
mo = handle.query_dn("sys/info-policy")
mo.state = "disabled"
handle.set_mo(mo)
handle.commit()

obj = handle.query_dn("sys")
mo = handle.query_dn("sys/extvm-mgmt")
mo_1 = handle.query_dn("sys/extvm-mgmt/virtual-switches")
mo_2 = VmSwitch(parent_mo_or_dn=mo_1, manager="unmanaged", admin_state="enable", policy_owner="local", vendor="undetermined", name="default")
handle.add_mo(mo_2, True)
mo_3 = handle.query_dn("sys/extvm-mgmt/key-store")
mo_4 = handle.query_dn("sys/extvm-mgmt/ext-key")
mo_4.key = "Cisco-UCSM-17c349d0-c5e9-11e6-97b"
handle.set_mo(mo_4)
handle.commit()

obj = handle.query_dn("sys")
mo = handle.query_dn("sys/svc-ext")
mo_1 = handle.query_dn("sys/svc-ext/xmlclconnpolicy-flex-ui")
mo_2 = handle.query_dn("sys/svc-ext/shell-svc-limits")
mo_3 = handle.query_dn("sys/svc-ext/svc-web-channel")
mo_4 = handle.query_dn("sys/svc-ext/svc-evt-channel")
mo_5 = handle.query_dn("sys/svc-ext/web-svc-limits")
mo_5.policy_owner = "local"
mo_5.total_sessions = "256"
mo_5.sessions_per_user = "32"
mo_5.max_event_interval = "600"
handle.set_mo(mo_5)
mo_6 = handle.query_dn("sys/svc-ext/datetime-svc")
mo_6.timezone = "America/Los_Angeles (Pacific Time)"
mo_6.policy_owner = "local"
mo_6.admin_state = "enabled"
mo_6.port = "0"
mo_7 = CommNtpProvider(parent_mo_or_dn=mo_6, name="10.29.137.1")
handle.set_mo(mo_6)
mo_8 = handle.query_dn("sys/svc-ext/cimc-web-svc")
mo_9 = handle.query_dn("sys/svc-ext/smashclp-svc")
mo_10 = handle.query_dn("sys/svc-ext/telnet-svc")
mo_10.policy_owner = "local"
mo_10.admin_state = "disabled"
mo_10.port = "23"
mo_10.descr = "Telnet Server"
handle.set_mo(mo_10)
mo_11 = handle.query_dn("sys/svc-ext/cimxml-svc")
mo_11.policy_owner = "local"
mo_11.admin_state = "disabled"
mo_11.descr = "CIM XML Service"
handle.set_mo(mo_11)
mo_12 = handle.query_dn("sys/svc-ext/wsman-svc")
mo_13 = handle.query_dn("sys/svc-ext/https-svc")
mo_13.descr = "Secure HTTP Service"
mo_13.cipher_suite = "ALL:!DH:!EDH:!ADH:!EXPORT40:!EXPORT56:!LOW:!RC4:+HIGH:+MEDIUM:+EXP:+eNULL"
mo_13.policy_owner = "local"
mo_13.admin_state = "enabled"
mo_13.cipher_suite_mode = "medium-strength"
mo_13.port = "443"
handle.set_mo(mo_13)
mo_14 = handle.query_dn("sys/svc-ext/snmp-svc")
mo_14.policy_owner = "local"
mo_14.admin_state = "disabled"
mo_14.is_set_snmp_secure = "no"
mo_14.descr = "SNMP Service"
handle.set_mo(mo_14)
mo_15 = handle.query_dn("sys/svc-ext/http-svc")
mo_15.request_timeout = "90"
mo_15.descr = "HTTP Service"
mo_15.redirect_state = "enabled"
mo_15.policy_owner = "local"
mo_15.admin_state = "enabled"
mo_15.port = "80"
handle.set_mo(mo_15)
mo_16 = handle.query_dn("sys/svc-ext/ssh-svc")
mo_17 = handle.query_dn("sys/svc-ext/dns-svc")
mo_17.policy_owner = "local"
mo_17.admin_state = "enabled"
mo_17.port = "0"
mo_18 = CommDnsProvider(parent_mo_or_dn=mo_17, name="173.36.131.10")
handle.set_mo(mo_17)
mo_19 = handle.query_dn("sys/svc-ext/syslog")
mo_19.policy_owner = "local"
mo_19.severity = "critical"
mo_19.descr = "Syslog Service"
mo_20 = CommSyslogClient(parent_mo_or_dn=mo_19, forwarding_facility="local7", hostname="none", admin_state="disabled", name="secondary", severity="critical")
mo_21 = CommSyslogClient(parent_mo_or_dn=mo_19, forwarding_facility="local7", hostname="none", admin_state="disabled", name="tertiary", severity="critical")
mo_22 = CommSyslogClient(parent_mo_or_dn=mo_19, forwarding_facility="local7", hostname="none", admin_state="disabled", name="primary", severity="critical")
mo_23 = CommSyslogMonitor(parent_mo_or_dn=mo_19, admin_state="disabled", severity="critical")
mo_24 = CommSyslogConsole(parent_mo_or_dn=mo_19, admin_state="disabled", severity="critical")
mo_25 = CommSyslogSource(parent_mo_or_dn=mo_19, faults="enabled", audits="disabled", events="disabled")
mo_26 = CommSyslogFile(parent_mo_or_dn=mo_19, severity="critical", admin_state="enabled", name="messages", size="4194304")
handle.set_mo(mo_19)
handle.commit()

obj = handle.query_dn("sys")
mo = handle.query_dn("sys/license")
handle.commit()

handle.logout()
