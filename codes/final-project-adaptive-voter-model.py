import pycxsimulator
from pylab import *
import networkx as nx
import random
import numpy as np
from analysis import *
import pandas as pd

# load data
df_data = pd.read_csv("/Users/visionwang/Documents/courses/Spring-2023/Complex-Systems/final-project/project-folder/us-election-opinion-3.csv")
df_data = df_data.loc[1000:3000,:]
state_list = list(df_data['Init_state'])
us_state_list= list(df_data['State'])
long_list = list(df_data['Longitude']) # NOTE: The Twitter user id is ordered by geoinformation already.
lat_list = list(df_data['Latitude'])
opinion_list = list(df_data['Opinion'])
us_state_rank_name = list(df_data['State'].value_counts().index)
us_state_rank_count = list(df_data['State'].value_counts())
sent_score_list = list(df_data['sent_score'])

# parameter setting
n_nodes = df_data.shape[0]
no_of_neighbors = 30
k = 3 # three states: republican (0), democratic (1), neutral (2)
p_acc = 0.5 # opinion acceptance threshold
p_self_change = 0.05 # probability threshold for a twitter user change to other opinion from the majority opinion

def initialize():
    global t, g, state_list, Rdata, Ddata, Ndata, n_edges, path_data
    t = 0

    g = nx.watts_strogatz_graph(n_nodes, no_of_neighbors, 0.3)
    g.add_nodes_from([i for i in range(n_nodes)])

    # add attributes for nodes
    for i in g.nodes:
        # initial opinion
        g.nodes[i]['state'] = state_list[i] # initial states (0: republican; 1: democratic; 2: neutral)
        # add geoinformation (state, longitude, latitude, opinion)
        g.nodes[i]['us-state'] = us_state_list[i]
        g.nodes[i]['long'] = long_list[i]
        g.nodes[i]['lat'] = lat_list[i]
        g.nodes[i]['opinion'] = opinion_list[i]
        g.nodes[i]['sentiment'] = sent_score_list[i]

    for i, j in g.edges:
        g.edges[i, j]['trust'] = random.random()

    g.pos = nx.spring_layout(g)

    Rdata = [state_list.count(0)/len(state_list)] # 0 represents republican in state_list
    Ddata = [state_list.count(2)/len(state_list)] # 2 represents democratic in state_list
    Ndata = [state_list.count(1)/len(state_list)] # 1 represents neutral in state_list

    path_data = [nx.average_shortest_path_length(g)]
    n_edges = [g.number_of_edges()]

def observe():
    global t, g, state_list, Rdata, Ddata, Ndata, n_edges, path_data
    subplot(4, 1, 1); cla();
    title("t = "+str(t))
    nx.draw(g, cmap = cm.coolwarm_r, vmin = 0, vmax = k - 1,
            node_color = [g.nodes[i]['state'] for i in g.nodes],
            pos = g.pos, node_size = 4)

    subplot(4, 1, 2); cla();
    plot(Ddata, label="Democratic")
    plot(Rdata, label="Republican")
    plot(Ndata, label="Neutral")
    xlabel("Step")
    ylabel("Percentage")
    legend()

    subplot(4, 1, 3); cla();
    plot(n_edges, label = "Number of edges")
    xlabel("Step")
    legend()

    subplot(4, 1, 4); cla();
    plot(path_data, label="Ave shortest path length")
    xlabel("Step")
    legend()

def update():
    global t, g, state_list, Rdata, Ddata, Ndata, n_edges, path_data
    t += 1
    listener = choice(list(g.nodes))
    nbs = list(g.neighbors(listener))
    nb_state_data = []
    nb_state_score = []
    for i_node in nbs:
        nb_state_data.append(g.nodes[i_node]['state'])
        nb_state_score.append(g.edges[listener, i_node]['trust']*g.nodes[i_node]['sentiment']) # weight * sentiment
    sum_score = sum(nb_state_score)
    prob_r = sum([nb_state_score[i] for i in range(len(nb_state_data)) if nb_state_data[i] == 0]) / sum_score # probability for i_node's neighbors support Republican
    prob_d = sum([nb_state_score[i] for i in range(len(nb_state_data)) if nb_state_data[i] == 1]) / sum_score # probability for i_node's neighbors are neutral
    prob_n = sum([nb_state_score[i] for i in range(len(nb_state_data)) if nb_state_data[i] == 2]) / sum_score # probability for i_node's neighbors stand Democratic
    nprobs = [prob_r, prob_d, prob_n]
    max_ind = [i for i in range(len(nprobs)) if nprobs[i] == max(nprobs)]
    if len(max_ind) == 1:
        # max probability from the other opinion
        if g.nodes[listener]['state'] != max_ind[0]:
            # decide if change opinion based on opinion acceptance threshold
            if nprobs[max_ind[0]] - nprobs[g.nodes[listener]['state']] > p_acc:
                g.nodes[listener]['state'] = max_ind[0]
                g.nodes[listener]['sentiment'] = random.random()
            else: # edge between two nodes that have opposite opinions can be removed probabilistically
                nb_ops = [i for i in nbs if g.nodes[listener]['state'] != g.nodes[i]['state']]
                for j in nb_ops:
                    g.remove_edge(listener, j)
        # max probability from the same opinion
        else:
            # the twitter user can randomly decide to change to other opinion
            # based on any external factors (i.e. news affair)
            if random.random() < p_self_change:
                mutation_sent = random.random()
                if g.nodes[listener]['sentiment'] != mutation_sent:
                    g.nodes[listener]['sentiment'] = mutation_sent
                state = random.randint(0, 2)
                while g.nodes[listener]['state'] == state:
                    state = random.randint(0, 2)
                g.nodes[listener]['state'] == state
    else: # if multiple opinions get max probability, this twitter user stand neutral
        g.nodes[listener]['state'] = 1

    state_list[listener] = g.nodes[listener]['state']

    Rdata.append(state_list.count(0)/len(state_list))  # 0 represents republican in state_list
    Ddata.append(state_list.count(2)/len(state_list))  # 2 represents democratic in state_list
    Ndata.append(state_list.count(1)/len(state_list))  # 1 represents neutral in state_list

    df_data['new_state'] = state_list

    path_data.append(nx.average_shortest_path_length(g))
    n_edges.append(g.number_of_edges())
    g.pos = nx.spring_layout(g, pos=g.pos, iterations=2)

pycxsimulator.GUI().start(func=[initialize, observe, update])