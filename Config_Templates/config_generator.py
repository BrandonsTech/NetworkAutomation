from jinja2 import Environment, FileSystemLoader
import yaml

ENV = Environment(loader=FileSystemLoader('.'))
template = ENV.get_template('template.jinja')

with open('data.yml') as f:
    interfaces = yaml.safe_load(f)
    print(template.render(interfaces_list=interfaces))

class interface:
    def __init__(self, name, description, vlan, uplink=False):
        self.name = name
        self.description = description
        self.vlan = vlan
        self.uplink = uplink

#R1 = interface('ethernet1/1', 'HR-Port', '10', True)
#R2 = interface('ethernet1/2', 'IT-Port', '20', False)

#routers = [
   # R1,
    #R2
#]


#print(template.render(interfaces_list=routers))