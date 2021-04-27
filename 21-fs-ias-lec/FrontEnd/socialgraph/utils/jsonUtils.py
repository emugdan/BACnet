
def extract_connections(data):

    nodes = data['nodes']
    links = data['links']

    connections = []

    for x in range(len(links)):
        s = links[x]['source']
        t = links[x]['target']

        if not any(s in q.values() for q in connections):
            connections.append({"source": s, "target": [t]})

        for y in range(len(connections)):
            d = connections[y]
            if d['source'] == s:
                if t not in d['target']:
                    d['target'].append(t)

    return connections