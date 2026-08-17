#!/user/bin/env python3

from ncclient import manager
from ncclient.operations import RPCError
from lxml import etree

    # 2. Lock Candidate Datastore
    #m.lock(target='candidate')
    
    # 3. Edit Configuration
    #m.edit_config(target='candidate', config=xml_config)
    
    # 4. Validate Changes
    #m.validate(source='candidate')
    
    # 5. Commit to Running Configuration
    #m.commit()
    
    # 6. Unlock Datastore
   # m.unlock(target='candidate')

ROLLBACK = "rollback-on-error"

filter = '''
<native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <interface>
            <GigabitEthernet>
            <name>1</name>
            <description/>
        </GigabitEthernet>
    </interface>
</native>
'''
payload = '''
<config>
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <interface>
        <GigabitEthernet>
            <name>1</name>
            <description>Containerlab management interfaceF</description>
        </GigabitEthernet>
        </interface>
        </native>
</config>
'''

payload_two = '''
<config>
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
        <interface>
        <GigabitEthernet>
            <name>1</name>
            <description>Containerlab management interfaceFFFFF</description>
        </GigabitEthernet>
        </interface>
        </native>
</config>
'''


def get_conf():
    with manager.connect(host="172.20.20.3", port=830, username="admin", password="admin", hostkey_verify=False, device_params={"name": "iosxe"}) as m:
        schema = m.get_config(source="candidate",filter=("subtree", filter))
        print(str(etree.tostring(schema.data, pretty_print=True).decode()))

def getting_schema():
    #with manager.connect(host="172.20.20.3", port=830, username="admin", password="admin", hostkey_verify=False, device_params={"name": "iosxe"}) as m:
    #schema = m.get_schema('XXXXXXXXX')
    #print(str(etree.tostring(schema.data, pretty_print=True).decode()))
    pass
    
def push_config():
    with manager.connect(host="172.20.20.3", port=830, username="admin", password="admin", hostkey_verify=False, device_params={"name": "iosxe"}) as m:
        with m.locked(target="candidate"):
            m.discard_changes()
            try: #THIS IS MEANT TO SUCCEED
                schema = m.edit_config(config=payload, target="candidate") 
                print("PAYLOAD ONE HAS BEEN DEPLOYED")
            except RPCError as R:
                print(f"failed and rolling back! Error: {R.tag}, {R.message}, {R.severity}")
            try: #THIS IS MEANT TO FAIL AND ROLLBACK
                schema = m.edit_config(config=payload_two, target="candidate", error_option=ROLLBACK)
                print("PAYLOAD TWO HAS BEEN DEPLOYED")
            except RPCError as R:
                print(f"failed and rolling back! Error: {R.tag}, {R.message}, {R.severity}")
            try:
                m.commit()
                print("COMMIT COMPLETED")
            except RPCError as R:
                print(f"failed and rolling back! Error: {R.tag}, {R.message}, {R.severity}")

    '''
    OPTIONS: (config, format='xml', target='candidate', default_operation=None, test_option=None, error_option=None)
    ---
    default_operation if specified must be one of { “merge”, “replace”, or “none” }
    test_option if specified must be one of { “test-then-set”, “set”, “test-only” }
    error_option if specified must be one of { “stop-on-error”, “continue-on-error”, “rollback-on-error” }
        The “rollback-on-error” error_option depends on the :rollback-on-error capability.
    '''

def get_capabilities():
     with manager.connect(host="172.20.20.3", port=830, username="admin", password="admin", hostkey_verify=False, device_params={"name": "iosxe"}) as m:
        for capability in m.server_capabilities:
            print(capability)



push_config()

get_conf()

#get_capabilities()

#getting_schema()