import pycxsimulator
from pylab import *
import networkx as nx
import random
import numpy as np
from analysis import *
from visualization import visualize_network
import pandas as pd

# load data
df_data = pd.read_csv("/Users/visionwang/Documents/courses/Spring-2023/Complex-Systems/final-project/project-folder/us-election-opinion.csv")
df_data = df_data.loc[:1000,:]
state_list = list(df_data['Init_state'])
us_state_list= list(df_data['State'])
long_list = list(df_data['Longitude'])
lat_list = list(df_data['Latitude'])
opinion_list = list(df_data['Opinion'])
us_state_rank_name = list(df_data['State'].value_counts().index)
us_state_rank_count = list(df_data['State'].value_counts())

# parameter setting
n_agents = df_data.shape[0]
no_of_neighbors = 30
k = 3 # three states: republican (0), democratic (1), neutral (2)

def initialize():
    global n_agents, g, state_list, Rdata, Ddata, Ndata
    #g = nx.barabasi_albert_graph(n_agents)
    g = nx.Graph()
    g.add_nodes_from([i for i in range(n_agents)])

    #g.pos = nx.spring_layout(g)

    #g.pos = nx.random_layout(g)
    # add attributes for nodes
    for i in g.nodes:
        # initial opinion
        g.nodes[i]['state'] = state_list[i] # initial states (0: republican; 1: democratic; 2: neutral)
        # add geoinformation (state, longitude, latitude, opinion)
        g.nodes[i]['us-state'] = us_state_list[i]
        g.nodes[i]['long'] = long_list[i]
        g.nodes[i]['lat'] = lat_list[i]
        g.nodes[i]['opinion'] = opinion_list[i]

    # add edges: all twitter users from same state will be connected
    for i in range(n_agents):
        if i + 1 != n_agents:
            for j in range(i + 1, n_agents):
                if g.nodes[i]['us-state'] == g.nodes[j]['us-state']:
                    g.add_edge(i, j)
                else: # from each state, a random twitter user can have few relatives from other states
                    if random.random() < 0.03:
                        g.add_edge(i, j)
    g.pos = nx.random_layout(g)
    #print(len(list(g.neighbors(0))))
    Rdata = [state_list.count(0)] # 0 represents republican in state_list
    Ddata = [state_list.count(1)] # 1 represents democratic in state_list
    Ndata = [state_list.count(2)] # 2 represents neutral in state_list

def observe():
    global n_agents, g, state_list, Rdata, Ddata, Ndata
    #pass
    subplot(2, 1, 1); cla();
    nx.draw(g, cmap = cm.coolwarm_r, vmin = 0, vmax = k - 1,
            node_color = [g.nodes[i]['state'] for i in g.nodes],
            pos = g.pos)
    subplot(2, 1, 2); cla();
    #plot(Ddata, label = "Democratic")
    plot(Rdata, label="Republican")
    #plot(Ndata, label="Neutral")
    xlabel("Step")
    ylabel("Total counts")
    legend()

def update():
    global n_agents, g, state_list, Rdata, Ddata, Ndata
    #pass



    listener = choice(list(g.nodes))
    nbs = list(g.neighbors(listener))
    if nbs != []:
        speaker = choice(nbs)
        g.nodes[listener]['state'] = g.nodes[speaker]['state']
        state_list[listener] = g.nodes[speaker]['state']

    Rdata.append(state_list.count(0))  # 0 represents republican in state_list
    Ddata.append(state_list.count(1))  # 1 represents democratic in state_list
    Ndata.append(state_list.count(2))  # 2 represents neutral in state_list

pycxsimulator.GUI().start(func=[initialize, observe, update])