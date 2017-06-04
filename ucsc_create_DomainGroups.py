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
        
        print "Creating UUID Pool:" #% (template)

        from ucscsdk.mometa.uuidpool.UuidpoolPool import UuidpoolPool
        from ucscsdk.mometa.uuidpool.UuidpoolBlock import UuidpoolBlock


        mo = UuidpoolPool(parent_mo_or_dn="org-root",
                        prefix="derived", 
                        descr="Global UUID Pool", 
                        name="G-UUID-Pool"
                        )

        mo_1 = UuidpoolBlock(parent_mo_or_dn=mo, to="0000-0000000003E8", r_from="0000-000000000001")


        handle.add_mo(mo)
        handle.commit()


        handle.logout()

    except Exception, err:
        print "Exception:", str(err)
        import traceback, sys
        print '-'*60
        traceback.print_exc(file=sys.stdout)
        print '-'*60
