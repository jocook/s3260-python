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
        
        print "Swapping Boot Policy for a rebuild:" #% (template)

        from ucscsdk.mometa.ls.LsServer import LsServer

      
        mo = LsServer(parent_mo_or_dn="org-root",
                      name="G-RGW-C220M4",
                      boot_policy_name="ceph-c220-rebuil",
                      )

        handle.add_mo(mo,True)
        handle.commit()

        

        handle.logout()

    except Exception, err:
        print "Exception:", str(err)
        import traceback, sys
        print '-'*60
        traceback.print_exc(file=sys.stdout)
        print '-'*60