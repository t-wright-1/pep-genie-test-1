from django.conf import settings
media_root = settings.MEDIA_ROOT
import os
import seaborn
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

#Enter the name of the output csv file with array format
output_file_name = os.path.join(media_root,'csv_array.csv')

#Enter the name of the output csv file with column format
output_file_name_2 = os.path.join(media_root,'csv_column.csv')

#-------------------------------------------------
#-------------------------------------------------

import numpy as np
import string
import csv

#--------------------------------------------------------------------

def Formatter(file_path, file_path_control, normalisation, id_root):

    def OpenExtract(my_path):
            
        #open file and save into np.array
        with open(my_path,'r') as dest_f:
            data_iter = csv.reader(dest_f,
                                delimiter = ',',
                                quotechar = '"')
            data = [data for data in data_iter]
        data_array = np.asarray(data)

        #cut out desired section of input array
        slice_array = []
        my_row = []

        if len(data_array[1][2]) == 2:
            for i in data_array[1:]:
                my_row.append(i[2][1]) 
                my_row.append(i[2][0])
                my_row.append(i[3]) #set to 3 for signal, set to 4 for total
                slice_array.append(my_row)
                my_row = []

        if len(data_array[1][2]) > 2:
            for i in data_array[1:]:
                my_row.append(i[2][1]+i[2][2])
                my_row.append(i[2][0])
                my_row.append(i[3]) #set to 3 for signal, set to 4 for total
                slice_array.append(my_row)
                my_row = []

        return slice_array

    #--------------------------------------------------------------------
    #open files into numpy array
    array_protein = OpenExtract(file_path)
    output_array = OpenExtract(file_path)
    
    #normalise
    if normalisation == 'True':
        array_control = OpenExtract(file_path_control)
        for i in range(len(output_array)):
            output_array[i][2] = float(array_protein[i][2]) - float(array_control[i][2])

    #find last column for adding number row 
    numbers = []
    for i in output_array:
        numbers.append(int(i[0]))
    my_max = max(numbers)

    #add top row numbers
    my_row = []
    output_list = []

    for n in range(my_max+1):
        my_row.append(n)
    output_list.append(my_row)
    my_row = []

    #add first column numbers and densitometry values (by row, so unsorted)
    c=0
    for i in range(20):
        my_row.append(list(string.ascii_uppercase)[i])
        for j in range(my_max):
            my_row.append(output_array[c][2])
            c += 1
        output_list.append(my_row)    
        my_row = []
        
    #add data as column format below
    output_list_2 = []
    my_row = []
    for i in sorted(output_array):
        my_row.append(i[0])
        my_row.append(i[1])
        my_row.append(i[2])
        output_list_2.append(my_row)
        my_row = []

    #save csv file in array format
    np_array_array = np.asarray(output_list, dtype = object)
    save_path = os.path.join(id_root,'csv_array.csv')
    np.savetxt(save_path, np_array_array, delimiter = ',', fmt = '%s')

    #save csv file in column format
    np_array_col = np.asarray(output_list_2, dtype = object)
    save_path = os.path.join(id_root,'csv_column.csv')
    np.savetxt(save_path, np_array_col, delimiter = ',', fmt = '%s')

    #cut data from array
    my_data_1 = np_array_array[1:,1:]

    #convert ndarray of str to ndarray of floats
    my_data_2 = my_data_1.astype(np.float)

    #make heatmap
    plt.clf()
    my_palette = seaborn.color_palette("viridis", as_cmap=True)
    my_heatmap = seaborn.heatmap(my_data_2,cmap=my_palette, xticklabels=False, yticklabels=False, square=True)
    my_path = os.path.join(id_root, 'heatmap.png')
    plt.savefig(my_path, bbox_inches='tight')
    return None

