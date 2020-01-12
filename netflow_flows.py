import ipaddress
import csv
from collections import defaultdict
import plotly.graph_objects as go
shapedData = defaultdict()
shapedData = {'labels':{}}
data = defaultdict()

src = list()
tgt = list()
vals = list()

def check_address(ipaddr):
    ''' This function takes a string converts it to an IP address and then returns either private RFC1918 subnet or host address'''
    network = ipaddress.ip_interface(ipaddr + '/24').network
    if network.is_private:
        return network
    else:
        return ipaddress.ip_address(ipaddr)


def update_add_record(source, destination, tag, quantity):
    '''data structure to hold each consolidated line index to three fields source, destination, tag
    record = {(source,destination,tag):[source, destination, tag, quantity]}'''
    if source.is_global: source = 'Internet-Source'
    if destination.is_global: destination = 'Internet-Destination'
    if (str(source), str(destination), tag) in data.keys():
        data[(str(source), str(destination), tag)][3] += quantity
    else:
        data[(str(source), str(destination), tag)] = [str(source), str(destination), tag, quantity]

with open('/Users/andrewratcliffe/OneDrive - Nswc Systems Ltd/SANS/SEC530/sankey_data.csv', newline='',
          encoding='utf-8-sig') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in csvreader:
        # print(', '.join(row))
        # source = row[0]
        quantity = int(row[1].strip('[]'))
        # destination = row[2]
        tag = row[3]
        source = check_address(row[0])
        destination = check_address(row[2])
        update_add_record(source, destination, tag, quantity)

# 10.0.0.60 [30] tag4
# tag4 [30] 10.1.1.3

def add_shapedData(keyData):
    if not keyData in shapedData['labels']:
        shapedData['labels'][keyData] = keyData


for k, v in data.items():
    source, destination, tag, quantity = v
    #print("{} [{}] {}".format(source, quantity, tag))
    #print("{} [{}] {}".format(tag, quantity, destination))
    add_shapedData(source)
    add_shapedData(tag)
    add_shapedData(destination)


labels = [x for x in shapedData['labels']]
for k, v in data.items():
    source, destination, tag, quantity = v
    src.append(labels.index(source))
    tgt.append(labels.index(tag))
    src.append(labels.index(tag))
    tgt.append(labels.index(destination))
    vals.append(quantity)
    vals.append(quantity)

fig = go.Figure(data=[go.Sankey(
    node = dict(
      pad = 15,
      thickness = 20,
      line = dict(color = "black", width = 0.5),
      label = labels,
      color = "blue"
    ),
    link = dict(
      source = src, # indices correspond to labels, eg A1, A2, A2, B1, ...
      target = tgt,
      value = vals
  ))])


fig.update_layout(title_text="Basic Sankey Diagram", font_size=10)
fig.show()

