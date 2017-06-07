import sys
import json
import csv

if __name__ == "__main__":
    try:
        if len(sys.argv) < 2:
            print "Usage: %s <JSON settings file>" % sys.argv[0]
            print "       <settings file>: access settings (IP/user/password)"
            sys.exit(0)
        f = open(sys.argv[1], 'r')
        settings_file = json.load(f)

        from ucsmsdk.ucshandle import UcsHandle
        handle = UcsHandle(ip=settings_file['ip'], username=settings_file['user'], password=settings_file['pw'])
        handle.login()
        
        print "Associating vMedia Policy to a Service Profile in UCSM:" #% (template)

        from ucsmsdk.mometa.ls.LsServer import LsServer

        mo = LsServer(parent_mo_or_dn="org-root", vmedia_policy_name="RHEL-7-3", ext_ip_state="none", bios_profile_name="", mgmt_fw_policy_name="", agent_policy_name="", mgmt_access_policy_name="", dynamic_con_policy_name="", kvm_mgmt_policy_name="", sol_policy_name="", uuid="0", descr="Rados Gateway 1", stats_policy_name="default", policy_owner="local", ext_ip_pool_name="ext-mgmt", boot_policy_name="", usr_lbl="", host_fw_policy_name="", vcon_profile_name="", ident_pool_name="", src_templ_name="", local_disk_policy_name="", scrub_policy_name="", power_policy_name="default", maint_policy_name="", name="RGW-1", power_sync_policy_name="", resolve_remote="yes")
        handle.add_mo(mo, True)

        handle.commit()






        handle.logout()

    except Exception, err:
        print "Exception:", str(err)
        import traceback, sys
        print '-'*60
        traceback.print_exc(file=sys.stdout)
        print '-'*60