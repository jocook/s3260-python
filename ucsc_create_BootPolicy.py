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

        from ucscsdk.ucschandle import UcscHandle
        handle = UcscHandle(ip=settings_file['ip'], username=settings_file['user'], password=settings_file['pw'])
        handle.login()
        
        print "Creating Boot Policy:" #% (template)

        from ucscsdk.mometa.lsboot.LsbootPolicy import LsbootPolicy
        from ucscsdk.mometa.lsboot.LsbootVirtualMedia import LsbootVirtualMedia
        from ucscsdk.mometa.lsboot.LsbootStorage import LsbootStorage
        from ucscsdk.mometa.lsboot.LsbootLocalStorage import LsbootLocalStorage
        from ucscsdk.mometa.lsboot.LsbootLocalHddImage import LsbootLocalHddImage

        mo = LsbootPolicy(parent_mo_or_dn="org-root", name="ceph-c220-boot", descr="Boot Policy for c220 CEPH RHEL Build", reboot_on_update="no", enforce_vnic_name="yes", boot_mode="legacy")
        mo_1 = LsbootVirtualMedia(parent_mo_or_dn=mo, access="read-only-local", lun_id="0", mapping_name="", order="2")
        mo_2 = LsbootStorage(parent_mo_or_dn=mo, order="1")
        mo_2_1 = LsbootLocalStorage(parent_mo_or_dn=mo_2, )
        mo_2_1_1 = LsbootLocalHddImage(parent_mo_or_dn=mo_2_1, order="1")
        handle.add_mo(mo)

        handle.commit()


        mo = LsbootPolicy(parent_mo_or_dn="org-root", name="ceph-c3260-boot", descr="Boot Policy for s3260 CEPH RHEL Build", reboot_on_update="no", enforce_vnic_name="yes", boot_mode="legacy")
        mo_1 = LsbootVirtualMedia(parent_mo_or_dn=mo, access="read-only-local", lun_id="0", mapping_name="", order="2")
        mo_2 = LsbootStorage(parent_mo_or_dn=mo, order="1")
        mo_2_1 = LsbootLocalStorage(parent_mo_or_dn=mo_2, )
        mo_2_1_1 = LsbootLocalHddImage(parent_mo_or_dn=mo_2_1, order="1")
        handle.add_mo(mo)

        handle.commit()



        handle.logout()

    except Exception, err:
        print "Exception:", str(err)
        import traceback, sys
        print '-'*60
        traceback.print_exc(file=sys.stdout)
        print '-'*60
