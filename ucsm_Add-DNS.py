import sys
import json

if __name__ == "__main__":
    try:
        if len(sys.argv) < 2:
            print "Usage: %s <JSON settings file>" % sys.argv[0]
            print "       <settings file>: access settings (IP/user/password)"
            sys.exit(0)
        f = open(sys.argv[1], 'r')
        settings_file = json.load(f)

	from ucsmsdk import ucshandle
	handle = ucshandle.UcsHandle(ip=settings_file['ip'], username=settings_file['user'], password=settings_file['pw'])
        handle.login()


	print ("Adding DNS Server(s) to UCSM")

	from ucsmsdk.mometa.comm.CommDnsProvider import CommDnsProvider

	mo = CommDnsProvider(parent_mo_or_dn="sys/svc-ext/dns-svc", name="8.8.8.8", descr="")

	handle.add_mo(mo)
	handle.commit()

        mo = CommDnsProvider(parent_mo_or_dn="sys/svc-ext/dns-svc", name="75.75.75.75", descr="")

        handle.add_mo(mo)
        handle.commit()

	handle.logout()

    except Exception, err:
        print "Exception:", str(err)
        import traceback, sys
        print '-'*60
        traceback.print_exc(file=sys.stdout)
        print '-'*60

