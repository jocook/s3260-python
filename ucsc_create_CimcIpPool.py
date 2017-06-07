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
        
        print "Creating CIMC IP Pool:" #% (template)

        from ucscsdk.mometa.ippool.IppoolPool import IppoolPool
        from ucscsdk.mometa.ippool.IppoolBlock import IppoolBlock

        mo = IppoolPool(parent_mo_or_dn="org-root", name="qcja-lab-cimc", descr="QCJA 2nd Flor lab CIMC IP Pool")
        mo_1 = IppoolBlock(parent_mo_or_dn=mo, prim_dns="8.8.8.8", r_from="10.1.212.30", def_gw="10.1.212.250", sec_dns="75.75.75.75", to="10.1.212.44")
        handle.add_mo(mo)

        handle.commit()





        handle.logout()

    except Exception, err:
        print "Exception:", str(err)
        import traceback, sys
        print '-'*60
        traceback.print_exc(file=sys.stdout)
        print '-'*60
