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
    g = nx.barabasi_albert_graph(n_agents, 5)
    #g = nx.Graph()
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
    #g.pos = nx.random_layout(g)
    g.pos = nx.spring_layout(g)
    #print(len(list(g.neighbors(0))))
    Rdata = [state_list.count(0)] # 0 represents republican in state_list
    Ddata = [state_list.count(1)] # 1 represents democratic in state_list
    Ndata = [state_list.count(2)] # 2 represents neutral in state_list

def observe():
    global n_agents, g, state_list, Rdata, Ddata, Ndata
    #pass
    subplot(2, 1, 1); cla(); ##coolwarm_r
    nx.draw(g, cmap = cm.coolwarm_r, vmin = 0, vmax = k - 1,
            node_color = [g.nodes[i]['state'] for i in g.nodes],
            pos = g.pos, node_size = 4)
    subplot(2, 1, 2); cla();
    #plot(Ddata, label = "Democratic")
    plot(Rdata, label="Republican")
    #plot(Ndata, label="Neutral")
    xlabel("Step")
    ylabel("Total counts")
    legend()

def update():
    global n_agents, g, state_list, Rdata, Ddata, Ndata
    listener = choice(list(g.nodes))
    # the listener follow the selected opinion from the neighbors based on majority rule
    nbs = list(g.neighbors(listener))
    nb_state_data = []
    for i_node in nbs:
        nb_state_data.append(g.nodes[i_node]['state'])
    prob_r = nb_state_data.count(0) / len(nb_state_data) # probability for i_node's neighbors support Republican
    prob_d = nb_state_data.count(1) / len(nb_state_data) # probability for i_node's neighbors support Democratic
    prob_n = nb_state_data.count(2) / len(nb_state_data) # probability for i_node's neighbors stand neutral
    nprobs = [prob_r, prob_d, prob_n]
    max_ind = [i for i in range(len(nprobs)) if nprobs[i] == max(nprobs)]
    if len(max_ind) == 1:
        if g.nodes[listener]['state'] != max_ind[0]:
            g.nodes[listener]['state'] = max_ind[0]
    else:
        g.nodes[listener]['state'] = 2
    state_list[listener] = g.nodes[listener]['state']

    Rdata.append(state_list.count(0))  # 0 represents republican in state_list
    Ddata.append(state_list.count(1))  # 1 represents democratic in state_list
    Ndata.append(state_list.count(2))  # 2 represents neutral in state_list

pycxsimulator.GUI().start(func=[initialize, observe, update])