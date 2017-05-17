import sys
import json
import csv

if __name__ == "__main__":
    try:
        if len(sys.argv) < 3:
            print "Usage: %s <JSON settings file> <csv file>" % sys.argv[0]
            print "       <settings file>: access settings (IP/user/password)"
            print "       <csv file>: settings for service profile template"
            sys.exit(0)
        f = open(sys.argv[1], 'r')
        settings_file = json.load(f)

        from ucscsdk.ucschandle import UcscHandle
        handle = UcscHandle(ip=settings_file['ip'], username=settings_file['user'], password=settings_file['pw'])
        handle.login()

	# delete spt from each row in the csv file
        csv_filename = sys.argv[2]
	csv_file = open(csv_filename, "r")
	if not csv_file:
	    print "Error: could not open %s" % csv_filename
	    sys.exit(1)
        csv_reader = csv.DictReader(csv_file)
	row_num = 1
	for row in csv_reader:
	    row_num += 1
	    
	    # set org (org-root as default)
	    if row['org']:
	        org = row['org']
	    else:
	        org = 'org-root'

            if not row['Template']:
	        print "Error on row %d: no template name found" % row_num
	        continue
	    template = row['Template']

	    print "Deleting global service profile template: %s" % (template)

            from ucscsdk.mometa.ls.LsServer import LsServer

            obj = handle.query_dn(org)
            mo = LsServer(parent_mo_or_dn=obj, 
			  name=template)

            handle.remove_mo(mo)
            handle.commit()

        handle.logout()

    except Exception, err:
        print "Exception:", str(err)
        import traceback, sys
        print '-'*60
        traceback.print_exc(file=sys.stdout)
        print '-'*60


