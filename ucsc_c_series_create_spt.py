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

	# apply settings from each row in the csv file
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

	    print "Creating global service profile template: %s" % (template)

            from ucscsdk.mometa.ls.LsServer import LsServer
            from ucscsdk.mometa.ls.LsVConAssign import LsVConAssign
            from ucscsdk.mometa.lstorage.LstorageProfileBinding import LstorageProfileBinding
            from ucscsdk.mometa.vnic.VnicEther import VnicEther
            from ucscsdk.mometa.vnic.VnicEtherIf import VnicEtherIf
            from ucscsdk.mometa.ls.LsPower import LsPower
            from ucscsdk.mometa.ls.LsRequirement import LsRequirement

            obj = handle.query_dn(org)
            mo = LsServer(parent_mo_or_dn=obj, 
			  name=template,
			  type="initial-template", 
			  ext_ip_state="none", 
			  ext_ip_pool_name=row['Mgmt_IP_Pool'],
			  ident_pool_name=row['UUID'],
			  bios_profile_name="S3260", 
			  boot_policy_name=row['Boot_Policy'],
			  maint_policy_name=row['Maint_Policy'],
			  power_policy_name="Ceph-Power", 
	                  uuid="derived")
            
	    mo_1 = VnicEther(parent_mo_or_dn=mo, 
			     name="Default", 
			     switch_id="A-B", 
			     mtu="1500", 
			     cdn_source="vnic-name", 
			     ident_pool_name="mac-pool", 
			     qos_policy_name="Ceph_Qos_Policy", 
	                     admin_host_port="ANY", 
			     admin_vcon="1", 
			     order="1", 
			     addr="derived")
	    mo_2 = VnicEtherIf(parent_mo_or_dn=mo_1, default_net="yes", name="G-default")
	    mo_1 = LsVConAssign(parent_mo_or_dn=mo, admin_vcon="1", vnic_name="Default", 
	                        order="1", transport="ethernet", admin_host_port="ANY")
            
	    mo_1 = LsRequirement(parent_mo_or_dn=mo, restrict_migration="no", name=row['Server_Pool'])

            mo_1 = LsPower(parent_mo_or_dn=mo, state="up")
            handle.add_mo(mo, True)
            handle.commit()

        handle.logout()

    except Exception, err:
        print "Exception:", str(err)
        import traceback, sys
        print '-'*60
        traceback.print_exc(file=sys.stdout)
        print '-'*60


