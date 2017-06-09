import sys
#BROKEN
'''
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
        
        print "Promoting CIMC Mounted vMedia to Rebuild Host:" #% (template)

        from ucscsdk.mometa.lsboot.LsbootVirtualMedia import LsbootVirtualMedia
        from ucscsdk.mometa.lsboot.LsbootStorage import LsbootStorage
        from ucscsdk.mometa.lsboot.LsbootLocalStorage import LsbootLocalStorage
        from ucscsdk.mometa.lsboot.LsbootLocalHddImage import LsbootLocalHddImage

        obj = handle.query_dn("org-root/boot-policy-ceph-c220-boot")
        mo = LsbootVirtualMedia(parent_mo_or_dn=obj, access="read-only-local", lun_id="0", mapping_name="", order="2")
        handle.add_mo(mo, True)

        mo = LsbootVirtualMedia(parent_mo_or_dn=obj, access="read-only-remote-cimc", lun_id="0", mapping_name="", order="1")
        handle.add_mo(mo, True)

        mo = LsbootStorage(parent_mo_or_dn="org-root/boot-policy-ceph-c220-boot/storage/", order="3")
        mo_1 = LsbootLocalStorage(parent_mo_or_dn=mo, )
        mo_1_1 = LsbootLocalHddImage(parent_mo_or_dn=mo_1, order="3")
        handle.add_mo(mo, True)

        handle.commit()





        handle.logout()

    except Exception, err:
        print "Exception:", str(err)
        import traceback, sys
        print '-'*60
        traceback.print_exc(file=sys.stdout)
        print '-'*60
