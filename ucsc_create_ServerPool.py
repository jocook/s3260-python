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
        
        print "Creating Server Pool(s):"

	from ucscsdk.mometa.compute.ComputePool import ComputePool
	from ucscsdk.mometa.compute.ComputePooledRackUnit import ComputePooledRackUnit

	mo = ComputePool(parent_mo_or_dn="org-root", name="C220-server-pool", descr="Server Pool for C220 Servers")
	mo_1 = ComputePooledRackUnit(parent_mo_or_dn=mo, id="1")
	mo_2 = ComputePooledRackUnit(parent_mo_or_dn=mo, id="2")
	mo_3 = ComputePooledRackUnit(parent_mo_or_dn=mo, id="3")
	mo_4 = ComputePooledRackUnit(parent_mo_or_dn=mo, id="4")
	handle.add_mo(mo)

	handle.commit()

	from ucscsdk.mometa.compute.ComputePool import ComputePool
	from ucscsdk.mometa.compute.ComputePooledSlot import ComputePooledSlot

	mo = ComputePool(parent_mo_or_dn="org-root", policy_owner="local", name="s3260-server-pool-Node1", descr="Server Pool for s3260 Node1")
	mo_1 = ComputePooledSlot(parent_mo_or_dn=mo, slot_id="1", chassis_id="1")
	mo_2 = ComputePooledSlot(parent_mo_or_dn=mo, slot_id="1", chassis_id="2")
	handle.add_mo(mo)

	handle.commit()

	from ucscsdk.mometa.compute.ComputePool import ComputePool
	from ucscsdk.mometa.compute.ComputePooledSlot import ComputePooledSlot

	mo = ComputePool(parent_mo_or_dn="org-root", policy_owner="local", name="s3260-server-pool-Node2", descr="Server Pool for s3260 Node2")
	mo_1 = ComputePooledSlot(parent_mo_or_dn=mo, slot_id="2", chassis_id="1")
	mo_2 = ComputePooledSlot(parent_mo_or_dn=mo, slot_id="2", chassis_id="2")
	handle.add_mo(mo)

	handle.commit()


        handle.logout()

    except Exception, err:
        print "Exception:", str(err)
        import traceback, sys
        print '-'*60
        traceback.print_exc(file=sys.stdout)
        print '-'*60