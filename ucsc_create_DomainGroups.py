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
        
        print "Creating Domain Group Heirarchy:" #% (template)

        from ucscsdk.mometa.org.OrgDomainGroup import OrgDomainGroup

        mo = OrgDomainGroup(parent_mo_or_dn="domaingroup-root",
                        descr="Domain Group for North America", 
                        name="DG-NA"
                        )

        handle.add_mo(mo)
        handle.commit()

	mo = OrgDomainGroup(parent_mo_or_dn="domaingroup-root/domaingroup-DG-NA",
                        descr="Domain Group for United States",
                        name="DG-US"
                        )

        handle.add_mo(mo)
        handle.commit()

        mo = OrgDomainGroup(parent_mo_or_dn="domaingroup-root/domaingroup-DG-NA/domaingroup-DG-US",
                            descr="Domain Group for United States",
                            name="DG-QCJA-Lab"
                            )

        handle.add_mo(mo)
        handle.commit()

        handle.logout()

    except Exception, err:
        print "Exception:", str(err)
        import traceback, sys
        print '-'*60
        traceback.print_exc(file=sys.stdout)
        print '-'*60
