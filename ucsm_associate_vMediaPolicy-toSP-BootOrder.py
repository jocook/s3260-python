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
        
        print "Placing vMedia Policy at the top boot order:" #% (template)

        from ucsmsdk.mometa.lsboot.LsbootDef import LsbootDef
        from ucsmsdk.mometa.lsboot.LsbootVirtualMedia import LsbootVirtualMedia
        from ucsmsdk.mometa.lsboot.LsbootStorage import LsbootStorage
        from ucsmsdk.mometa.lsboot.LsbootLocalStorage import LsbootLocalStorage
        from ucsmsdk.mometa.lsboot.LsbootDefaultLocalImage import LsbootDefaultLocalImage

        obj = handle.query_dn("org-root/ls-RGW-1")
        mo = LsbootDef(parent_mo_or_dn=obj, descr="", reboot_on_update="no", adv_boot_order_applicable="no", policy_owner="local", enforce_vnic_name="yes", boot_mode="legacy")
        mo_1 = LsbootVirtualMedia(parent_mo_or_dn=mo, access="read-only-remote-cimc", lun_id="0", mapping_name="RHEL-7-3", order="1")
        mo_2 = LsbootVirtualMedia(parent_mo_or_dn=mo, access="read-only", lun_id="0", mapping_name="", order="2")
        mo_3 = LsbootStorage(parent_mo_or_dn=mo, order="3")
        mo_3_1 = LsbootLocalStorage(parent_mo_or_dn=mo_3, )
        mo_3_1_1 = LsbootDefaultLocalImage(parent_mo_or_dn=mo_3_1, order="3")
        handle.add_mo(mo, True)

        handle.commit()







        handle.logout()

    except Exception, err:
        print "Exception:", str(err)
        import traceback, sys
        print '-'*60
        traceback.print_exc(file=sys.stdout)
        print '-'*60