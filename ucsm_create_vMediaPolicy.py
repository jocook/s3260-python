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
        
        print "Creating vMedia Policy in UCSM:" #% (template)

        from ucsmsdk.mometa.cimcvmedia.CimcvmediaMountConfigPolicy import CimcvmediaMountConfigPolicy
        from ucsmsdk.mometa.cimcvmedia.CimcvmediaConfigMountEntry import CimcvmediaConfigMountEntry

        mo = CimcvmediaMountConfigPolicy(parent_mo_or_dn="org-root", policy_owner="local", retry_on_mount_fail="yes", name="RHEL-7-3", descr="RHEL 7.3")
        mo_1 = CimcvmediaConfigMountEntry(parent_mo_or_dn=mo, user_id="", description="RHEL 7.3", remote_ip_address="10.156.10.10", remote_port="0", image_name_variable="none", auth_option="default", mapping_name="RHEL-7-3", image_file_name="RHEL7.3_jabtl1203.iso", device_type="cdd", mount_protocol="nfs", password="", image_path="/export/media/")
        handle.add_mo(mo)

        handle.commit()






        handle.logout()

    except Exception, err:
        print "Exception:", str(err)
        import traceback, sys
        print '-'*60
        traceback.print_exc(file=sys.stdout)
        print '-'*60