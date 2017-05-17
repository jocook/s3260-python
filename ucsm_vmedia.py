import sys
import json
from ucsmsdk import ucshandle

def createVirtualMedia(handle):
    print "Adding Virtual Media Policy"
    from ucsmsdk.mometa.cimcvmedia.CimcvmediaMountConfigPolicy import CimcvmediaMountConfigPolicy
    from ucsmsdk.mometa.cimcvmedia.CimcvmediaConfigMountEntry import CimcvmediaConfigMountEntry
    mo = CimcvmediaMountConfigPolicy(name="RHEL-7-3",
        retry_on_mount_fail="yes",
        parent_mo_or_dn="org-root",
        policy_owner="local",
        descr="RHEL 7.3")

    mo_1 = CimcvmediaConfigMountEntry(parent_mo_or_dn=mo,
        mapping_name="RHEL-7-3",
        device_type="cdd",
        mount_protocol="http",
        remote_ip_address="192.168.2.2",
        image_name_variable="none",
        image_file_name="rhel-server-7.3-x86_64-dvd.iso",
        image_path="install")

    mo_2 = CimcvmediaConfigMountEntry(parent_mo_or_dn=mo,
        mapping_name="kickstartImage",
        device_type="hdd",
        mount_protocol="http",
        remote_ip_address="192.168.2.2",
        image_name_variable="service-profile-name",
        image_path="install")
    handle.add_mo(mo, modify_present=True)
    try:
        handle.commit()
    except UcsException as err:
        if err.error_code == "103":
            print "\talready exists"

if __name__ == "__main__":
    try:
        if len(sys.argv) < 2:
            print "Usage: %s <JSON settings file>" % sys.argv[0]
            sys.exit(0)
        f = open(sys.argv[1], 'r')
        settings_file = json.load(f)
        is_secure = True
        if settings_file['secure'] == "False":
            is_secure = False
        handle = ucshandle.UcsHandle(settings_file['ip'], settings_file['user'], settings_file['pw'], secure=is_secure)
        handle.login()
        createVirtualMedia(handle)
	handle.logout()

    except Exception, err:
        print "Exception:", str(err)
        import traceback, sys
        print '-'*60
        traceback.print_exc(file=sys.stdout)
        print '-'*60

