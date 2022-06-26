import networkx
import pylab
from math import sin, cos, radians
from random import randint
import matplotlib.pyplot as plt
import numpy as np

#input
'''seq_str = 'INDPLLCVMS'
first_resi = 1
surface_mode = False
my_colour_nos = []'''

def generate_wheel(sequence, output_path, first_res, surface_mode, surface_data='', cmap_input=0):
    #settings
    fig = plt.figure(figsize=(12,12))
    my_angle = 99.3

    #--------------------------------------

    #get master variables
    seq_list = list(sequence)
    my_len = len(seq_list)

    #make coords
    my_coords = []
    c = 0
    for i in range(my_len):
        my_tuple = (round(sin(radians(c)),4),round(cos(radians(c)),4))
        my_coords.append(my_tuple)
        c+=my_angle

    #make shapes
    #AA library
    positive_charge = ['K','R']
    negative_charge = ['D','E']
    nucleophiles = ['C']
    aromatics = ['W','F','Y']
    #make colours
    if str(surface_mode) == 'True':
        print('surface mode is true')
        #generate auto
        '''my_colour_nos = [] #The list of surface numbers
        colour_max=180
        for i in range(my_len):
            my_colour_nos.append(randint(0,180))'''
        my_colour_nos = []
        for i in surface_data:
            my_colour_nos.append(int(i))
        colour_max=180
        my_font_colours = []
        if int(cmap_input) == 3 or int(cmap_input) == 4:
            #If Camp is viridis or bone
            for i in my_colour_nos:
                if i > colour_max*0.5:
                    my_font_colours.append('white')
                else:
                    my_font_colours.append('black')
        if int(cmap_input) == 1:
            #If Camp is grey
            for i in my_colour_nos:
                if i > colour_max*0.6:
                    my_font_colours.append('white')
                else:
                    my_font_colours.append('black')
        elif int(cmap_input) == 2:
            #if cmap is rdbu
            for i in my_colour_nos:
                if i > colour_max*0.7:
                    my_font_colours.append('white')
                elif i < colour_max*0.2:
                    my_font_colours.append('white')
                else:
                    my_font_colours.append('black')
        else:
            for i in my_colour_nos:
                if i > colour_max*0.7:
                    my_font_colours.append('white')
                else:
                    my_font_colours.append('black')

    else:
        print('not ture yo', surface_mode)
        kd_scale = {'I':4.5,'V':4.2,'L':3.8,'F':2.8,'C':2.5,'M':1.9,'A':1.8,'G':-0.4,'T':-0.7,'S':-0.8,'W':-0.9,'Y':-1.3,'P':-1.6,'H':-3.2,'E':-3.5,'Q':-3.5,'D':-3.5,'N':-3.5,'K':-3.9,'R':-4.5}
        my_colours=[]
        my_font_colours=[]
        for i in seq_list:
            my_colours.append(kd_scale[i]*-1)
            if kd_scale[i] < 0:
                my_font_colours.append('white')
            else:
                my_font_colours.append('black')

    #make labels
    my_labels = seq_list
    new_labels = []
    for i in range(my_len):
        my_item = my_labels[i]+str(first_res+i)
        new_labels.append(my_item)
        my_item = ''

    labels = {}
    for i in range(my_len):
        labels[i] = new_labels[i]

    my_thickness = []
    unit = 9/my_len
    for i in range(my_len):
        j = my_len-1-i
        my_thickness.append(4+unit*j)
    my_thickness.reverse()

    my_node_size = []
    if my_len > 11:
        print('>11')
        unit = 1700/my_len
        for i in range(my_len):
            j = my_len-1-i
            my_node_size.append(1700+unit*j)
    elif my_len < 8:
        print('<8')
        unit = 4500/my_len
        for i in range(my_len):
            j = my_len-1-i
            my_node_size.append(2500+unit*j)
    else:
        print('mid')
        unit = 2000/my_len
        for i in range(my_len):
            j = my_len-1-i
            my_node_size.append(2700+unit*j)

    my_edge_colours = []
    for i in range(my_len):
        unit = 1/(my_len+1)
        x = unit*i
        this_colour = (x,x,x)
        my_edge_colours.append(this_colour)
    hello = my_edge_colours.reverse()



    G = networkx.Graph()

    for i in range(my_len):
        G.add_node(i)

    for i in range(my_len-1):
        G.add_edge(i,i+1)

    nodePos = {}
    c=0
    for i in my_coords:
        nodePos[c]=i
        c+=1 

    #Make new pos dict for edges to order overlap
    edge_pos = {}
    for i in range(my_len):
        j = my_len-1-i
        edge_pos[i]=my_coords[j]


    #make graph

    nodelist = []
    for i in range(my_len):
        nodelist.append(my_len-1-i)

    my_cmap_list = [
        plt.cm.Blues,
        plt.cm.Greys,
        plt.cm.RdBu,
        plt.cm.viridis,
        plt.cm.bone,
    ]
    my_cmap = my_cmap_list[int(cmap_input)]

    if surface_mode == 'True':
        my_colour_nos.reverse()
        my_node_size.reverse()
        networkx.draw_networkx_nodes(G,nodePos,nodelist=nodelist,node_shape = 'o',node_color=my_colour_nos,linewidths=2,edgecolors='black',node_size=my_node_size,vmax=180,vmin=0,cmap=my_cmap)
    else:
        my_colours.reverse()
        my_node_size.reverse()
        networkx.draw_networkx_nodes(G,nodePos,nodelist=nodelist, node_shape = 'o',node_color=my_colours,linewidths=2,edgecolors='black',node_size=my_node_size,cmap=my_cmap, vmax = 4.5,vmin=-4.5)


    networkx.draw_networkx_edges(G,edge_pos,width=my_thickness,edge_color=my_edge_colours) 

    inner_labels = []
    my_font_sizes = []
    my_font_weight = []
    for i in seq_list:
        if i in positive_charge:
            inner_labels.append('+')
            if my_len > 11:
                my_font_sizes.append(40)
            else:
                my_font_sizes.append(50)
            my_font_weight.append(600)
        elif i in negative_charge:
            inner_labels.append('-')
            if my_len > 11:
                my_font_sizes.append(40)
            else:
                my_font_sizes.append(50)
            my_font_weight.append(600)
        elif i in nucleophiles:
            inner_labels.append('Nu')
            my_font_sizes.append(28)
            my_font_weight.append(250)
        elif i in aromatics:
            inner_labels.append('Ar')
            my_font_sizes.append(28)
            my_font_weight.append(250)
        else:
            inner_labels.append('')
            my_font_sizes.append(28)
            my_font_weight.append(250)
        
    label_list = []
    c = 0
    for i in range(my_len):
        my_tuple = (round(1.4*sin(radians(c)),4),round(1.4*cos(radians(c)),4))
        label_list.append(my_tuple)
        c+=my_angle
    label_pos = {}
    for i in range(my_len):
        label_pos[i] = label_list[i]


    for i in range(len(new_labels)):
        labels = {}
        labels[i] = new_labels[i]
        networkx.draw_networkx_labels(G, label_pos, labels, font_size=30, font_color='black',font_weight = 590)

    if int(cmap_input) == 3 or int(cmap_input) == 4:
        my_font_colours = my_font_colours[::-1]
    if surface_mode == 'True':
        for i in my_colour_nos:
            print('Colour Nos')
            print(i)
    else:
        for i in my_colours:
            print('Colours')
            print(i)

    for i in range(len(inner_labels)):
        labels = {}
        labels[i] = inner_labels[i]
        print(inner_labels[i],my_font_colours[i])
        networkx.draw_networkx_labels(G, nodePos, labels, font_size=my_font_sizes[i], font_color=my_font_colours[i],font_weight = my_font_weight[i])



    '''def fct():
        f = fig
        ax = f.add_subplot(111)
        x, y = np.mgrid[0:5,0:5]
        z = np.sin(x**2+y**2)
        mesh = ax.pcolormesh(x, y ,z)
        return ax, mesh

    ax, mesh = fct()
    plt.colorbar(mesh, ax=ax)'''



    plt.margins(x=0.25,y=0.25)
    plt.savefig(output_path)

