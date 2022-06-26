import cv2

def generate_grid(rows,cols,path):
    grid_unit = cv2.imread(path, -1)
    my_list = []
    for i in range(int(rows)):
        my_list.append(grid_unit)
    grid_column = cv2.vconcat(my_list)
    my_list=[]
    for i in range(int(cols)):
        my_list.append(grid_column)
    full_grid = cv2.hconcat(my_list)
    #cv2.imwrite(out_path, full_grid)
    return full_grid