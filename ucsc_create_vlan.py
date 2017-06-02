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
        
        print "Creating VLAN:" #% (template)

        from ucscsdk.mometa.fabric.FabricVlan import FabricVlan

        mo = FabricVlan(parent_mo_or_dn="domaingroup-root/fabric/lan",
                        sharing="none",
                        name="192-10.10.192.0_24",
                        id="192",
                        policy_owner="local",
                        default_net="no",
                        )


        handle.add_mo(mo, True)
        handle.commit()

        mo = FabricVlan(parent_mo_or_dn="domaingroup-root/fabric/lan",
                        sharing="none",
                        name="193-10.10.193.0_24",
                        id="193",
                        policy_owner="local",
                        default_net="no",
                        )


        handle.add_mo(mo, True)
        handle.commit()




        handle.logout()

    except Exception, err:
        print "Exception:", str(err)
        import traceback, sys
        print '-'*60
        traceback.print_exc(file=sys.stdout)
        print '-'*60
