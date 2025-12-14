# with open('Day11Part2SampleInput.txt', 'r') as file:
with open('Day11Input.txt', 'r') as file:
        lines = file.readlines()
lines = [line.strip() for line in lines]

connections = {}
for line in lines:
    parent = line.split(':')[0]
    children = line.split(': ')[1].split(' ')
    connections[parent] = children

# Basically a copy of one of the algorithms on https://www.python.org/doc/essays/graphs/
def find_paths(start_node: str, end_node: str, connections: dict, visited_nodes: list):
    visited_nodes = visited_nodes + [start_node]
    if start_node == end_node:
        return [visited_nodes]
    paths = []
    children = connections[start_node]
    for child in children:
        new_paths = find_paths(child, end_node, connections, visited_nodes)
        for new_path in new_paths:
            paths.append(new_path)
    return paths

# Some manual examination of the graph structure helped in reducing the number of possible paths
# Code run in a notebook
# import networkx as nx
# import plotly.graph_objects as go
# import pandas as pd

# Create graph and positions
# G = nx.Graph()
# G.add_nodes_from(connections.keys())
#
# # Add edges to graph
# for node, children in connections.items():
#     for child in children:
#         G.add_edge(node, child)
#
# positions = nx.spring_layout(G)
#
# # Prepare node data
# nodes_df = pd.DataFrame({
#     'node': list(G.nodes()),
#     'x': [positions[n][0] for n in G.nodes()],
#     'y': [positions[n][1] for n in G.nodes()],
#     'label': [f"Node: {n}" for n in G.nodes()]
# })
#
# # Prepare edge data
# edge_lines = []
# for n1, n2 in G.edges():
#     edge_lines.append(
#         go.Scatter(
#             x=[positions[n1][0], positions[n2][0]],
#             y=[positions[n1][1], positions[n2][1]],
#             mode='lines',
#             line=dict(color='gray', width=1),
#             hoverinfo='skip',
#             opacity=0.3
#         )
#     )
#
# node_colours = [
#     'red' if node in ['svr', 'fft', 'dac', 'out'] else 'lightgreen' for node in G.nodes()
# ]
# node_sizes = [
#     10 if node in ['svr', 'fft', 'dac', 'out'] else 5 for node in G.nodes()
# ]
# # Node trace with hover text
# node_trace = go.Scatter(
#     x=nodes_df['x'],
#     y=nodes_df['y'],
#     mode='markers',
#     marker=dict(size=node_sizes, color=node_colours),
#     text=nodes_df['label'],
#     hoverinfo='text'
# )
#
# fig = go.Figure(edge_lines + [node_trace])
# fig.update_layout(showlegend=False, template='simple_white')
# fig.show()

# Code to examine the nodes that lead to the nodes of interest
# for node, children in connections.items():
#     if 'fft' in children:
#         print(f"{node} --> {children}")
# Output:
# tjp --> ['fft']
# ryx --> ['zmf', 'zvz', 'fft', 'hvj', 'xaf']
# ijt --> ['fft', 'hvj']

# Go another layer back
# for node, children in connections.items():
#     if 'tjp' in children or 'ryx' in children or 'ijt' in children:
#         print(f"{node} -->{children}")
# Output
# ovq --> ['tud', 'qci', 'tpo', 'cry', 'lbn', 'xqo', 'dxr', 'xme', 'ilj', 'obr', 'wkn', 'mze', 'vqb', 'ryx', 'gls', 'ijt']
# yky --> ['xqo', 'tjp', 'xme', 'cry', 'fbg', 'qci', 'ijt', 'gls']
# row --> ['gls', 'lbn', 'ggy', 'vqb', 'ryx', 'mze', 'obr', 'fbg', 'tpo', 'ilj']

# And one more layer back
# for node, children in connections.items():
#     if 'ovq' in children or 'yky' in children or 'row' in children:
#         print(f"{node} --> {children}")
# ggc --> ['row', 'ovq']
# gvz --> ['ovq']
# cky --> ['yky']
# drm --> ['yky']
# smm --> ['yky']
# dax --> ['ovq', 'row']
# cng --> ['ovq']
# iyy --> ['ovq', 'yky']
# vio --> ['ovq', 'yky']
# czv --> ['row', 'ovq', 'yky']
# aql --> ['row', 'yky']
# jyv --> ['row']
# bws --> ['row', 'ovq', 'yky']
# icq --> ['row']
# gzf --> ['ovq', 'row']
# fwq --> ['ovq', 'row']
# iud --> ['row', 'yky', 'ovq']
# anm --> ['yky']
# frs --> ['row']
# yxg --> ['ovq', 'row']
# mcd --> ['row', 'yky', 'ovq']
# wlg --> ['yky']
# qet --> ['yky', 'row']

# So nothing to be done here, but we can simplify some of the connections closer to fft
# (i.e., where there are options that don't lead to fft, ignore them)
# connections['ryx'] = ['fft']
# connections['ijt'] = ['fft']
# #
# connections['ovq'] = ['ryx', 'ijt']
# connections['yky'] = ['tjp', 'ijt']
# connections['row'] = ['ryx']


# Similarly for dac
# for node, children in connections.items():
#     if 'dac' in children:
#         print(f"{node} --> {children}")
# sto --> ['dac', 'ycs']
# wxq --> ['dac', 'pfs']
# ywb --> ['dac', 'ycs']
# muw --> ['dac', 'pfs', 'ycs']

# for node, children in connections.items():
#     if 'sto' in children or 'wxq' in children or 'ywb' in children or 'muw' in children:
#         print(f"{node} -->{children}")
# nwh -->['ywb']
# zrz -->['wxq', 'sto', 'muw']
# cxc -->['muw', 'sto', 'wxq']
# zdo -->['sto']

# for node, children in connections.items():
#     if 'nwh' in children or 'zrz' in children or 'cxc' in children or 'zdo' in children:
#         print(f"{node} -->{children}")
# lyu -->['sag', 'zrz', 'wfl', 'eek', 'yrt', 'nmm', 'sxo', 'qtk', 'ipg', 'djz', 'ajg']
# keq -->['fzm', 'nmm', 'hza', 'oob', 'zrz', 'wfl', 'sag', 'zdo', 'vdk', 'eih', 'cfn']
# qov -->['wfl', 'yrt', 'ohw', 'fzm', 'djz', 'ajg', 'hop', 'nwh', 'cxc', 'xmh', 'vdk']

# Simplifications
# connections['sto'] = ['dac']
# connections['wxq'] = ['dac']
# connections['ywb'] = ['dac']
# connections['muw'] = ['dac']
#
# connections['lyu'] = ['zrz']
# connections['keq'] = ['zrz', 'zdo']
# connections['qov'] = ['nwh', 'cxc']

# Rerunning the plotting code above but with these updated connections results in a graph where
# all paths from svr to out have to go through both fft and dag

# Output of analysis above means allows us to simplify network:
connections['ryx'] = ['fft']
connections['ijt'] = ['fft']

connections['ovq'] = ['ryx', 'ijt']
connections['yky'] = ['tjp', 'ijt']
connections['row'] = ['ryx']

connections['sto'] = ['dac']
connections['wxq'] = ['dac']
connections['ywb'] = ['dac']
connections['muw'] = ['dac']

connections['lyu'] = ['zrz']
connections['keq'] = ['zrz', 'zdo']
connections['qov'] = ['nwh', 'cxc']


# Now all paths must go through 'fft' and 'dac', so we can split the path check into stages, and
# get the final result by multiplying the number of paths in each individual stage
paths = find_paths('svr', 'fft', connections, [])
paths_to_fft = len(paths)

paths = find_paths('fft', 'dac', connections, [])
paths_from_fft_to_dac = len(paths)

paths = find_paths('dac', 'out', connections, [])
paths_from_dac_to_out = len(paths)
print(paths_to_fft * paths_from_fft_to_dac * paths_from_dac_to_out)
