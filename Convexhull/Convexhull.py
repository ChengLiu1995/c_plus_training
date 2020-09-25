# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 16:47:02 2020

@author: Cheng
"""


from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import numpy as np

def cross_product(arr1,arr2):
    '''
    逆时针 >0
    顺时针 <0 (expected)
    共线 = 0
    '''
    return arr1[0]*arr2[1] - arr1[1]*arr2[0]

def draw_nodes(node_arr,c): 
    for i in range(0,len(node_arr)):
        x = [node_arr[i-1][0],node_arr[i][0]]
        y = [node_arr[i-1][1],node_arr[i][1]]
        plt.plot(x,y,color=c)

def main():
    node_arr= np.array([[2,1.1],[4,4],[2.5,10],[5,7],[4,7],[6,3],[6,14],
                        [10,7],[15,9],[12,1],[9,6],[6,2],[5,3]])
    
    min_idx = np.argmin(node_arr[:,1])
    start_point = node_arr[min_idx]
    Line_V0j = np.array([-1,0])
    Line_Zij = np.array([-1,0])
    ZPR = []
    ZPR.append(start_point)
    
    for i in range(1,node_arr.shape[0]+1):  
        cur_inx =(min_idx + i )%(node_arr.shape[0])
        Line_V0m = node_arr[cur_inx] - start_point
        a = cross_product(Line_Zij,Line_V0m)
        b = cross_product(Line_V0j,Line_V0m)
        if a < 0 and b >= 0:#Q1b
            continue
        elif a < 0 and b < 0:#Q1a
            ZPR.append(node_arr[cur_inx])
        else:#Q2a and Q2b,echo back
            #while ZPR[-1][0] != start_point[0] and ZPR[-1][1] != start_point[1]:
            while (len(ZPR)) > 1:
                Line_Zj_cur = node_arr[cur_inx] - ZPR[-1]
                Line_cur_Zj_1 = ZPR[-2] - node_arr[cur_inx]
                if cross_product(Line_Zj_cur,Line_cur_Zj_1) < 0:                
                    break
                else:
                    ZPR.pop()
            ZPR.append(node_arr[cur_inx])
                
        Line_Zij = node_arr[cur_inx] - ZPR[-1]
        Line_V0j = Line_V0m
        
    plt.figure()   
    draw_nodes(node_arr,'k')
    draw_nodes(ZPR,'b')
    plt.show()
    
if __name__ == "__main__":
    main()
