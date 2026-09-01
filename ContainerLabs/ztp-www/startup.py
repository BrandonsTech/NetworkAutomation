import cli


def config ():
    cli.configurep(["hostname R3", 
                "username admin secret admin privilege 15",
                "no ip domain lookup", 
                "ip http server",
                "ip http secure-server",
                "ip domain name lab.local",
                "crypto key generate rsa modulus 2048",
                "ip ssh version 2",
                "aaa new-model",
                "aaa authentication login default local",
                "aaa authorization exec default local"
                "restconf",
                "netconf-yang",
                "netconf-yang feature candidate-datastore",
                "end"
])

config()