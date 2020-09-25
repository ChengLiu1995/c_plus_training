# -*- coding: utf-8 -*-
"""
Created on Wed May 27 15:01:45 2020

@author: 73766
"""    
import matplotlib.pyplot as plt
import numpy as np
import cv2

class FindContours:
    def __init__(self):
        self.grid = np.array([[0,0,0,0,0,0,0,0,0,0,0,0],
                              [0,0,0,0,0,0,0,0,0,0,0,0],
                              [0,0,0,0,0,0,0,0,0,0,0,0],
                              [0,0,1,1,1,1,1,1,1,0,0,0],
                              [0,0,1,0,0,1,0,0,1,0,1,0],
                              [0,0,1,0,0,1,0,0,1,0,0,0],
                              [0,0,1,0,0,1,0,0,1,0,0,0],
                              [0,0,1,1,1,1,1,1,1,0,0,0],
                              [0,0,0,0,0,0,0,0,0,0,0,0],
                              [0,0,0,0,0,0,0,0,0,0,0,0],
                              [0,0,0,0,0,0,0,0,0,0,0,0],])
        self.LNBD = 1
        self.NBD = 1
        self.Disp_with_number = True
        self.MAX_BODER = self.grid.shape[0]*self.grid.shape[1]

        
    def load_map_from_array(self,grid):
        grid_temp = grid.copy().astype("int32")
        self.grid = np.pad(grid_temp, ((1, 1), (1, 1)), 'constant', constant_values=0)
        self.LNBD = 1
        self.NBD = 1
        self.MAX_BODER = self.grid.shape[0]*self.grid.shape[1]
        
    def trans_number_to_char(self,num):
        if self.Disp_with_number:
            return str(num)
        if num >1:
            return chr(63 + num)
        if num <0:
            return chr(95 - num)
        else:
            return str(num)
        
    def disp_grid(self):
        for i in range(self.grid.shape[0]):
            num = '\033[0;37m' + '['
            print(num,end = ' ')
            for j in range(self.grid.shape[1]):
                if self.grid[i][j] == 0:
                    num = '\033[0;37m' + self.trans_number_to_char(self.grid[i][j]) 
                    print(num,end = ' ')
                else:
                    num = '\033[1;37m' + self.trans_number_to_char(self.grid[i][j]) 
                    print(num,end = ' ')
            num = '\033[0;37m' + ']'
            print(num)
        print("\033[1;37m")

        
    def find_neighbor(self,center,start,clock_wise = 1):
        weight = -1
        if clock_wise == 1:
            weight = 1
        #direction = np.array([[1,0],[0,-1],[0,-1],[-1,0],[-1,0],[0,1],[0,1]])
        neighbors = np.array([[0,0],[0,1],[0,2],[1,2],[2,2],[2,1],[2,0],[1,0]])
        indexs = np.array([[0,1,2],
                          [7,9,3],
                          [6,5,4]])
        #print(center,start)
        start_ind = indexs[start[0] - center[0]+1][start[1] - center[1]+1]
        # print(start_ind)
        for i in range(1,len(neighbors)+1): 
            cur_ind = (start_ind + i*weight+8)%8
            #print(cur_ind)
            x = neighbors[cur_ind][0] + center[0] - 1
            y = neighbors[cur_ind][1] + center[1] - 1
            # grid[x][y] = a
            # a+=1
            if self.grid[x][y] != 0:
                return [x,y]
        return [-1,-1]
    
    def board_follow(self,center_p,start_p,mode):
        ij = center_p
        ij2 = start_p
        ij1 = self.find_neighbor(ij,ij2,1)
        x = ij1[0]
        y = ij1[1]
        if ij1 == [-1,-1]:
                self.grid[ij[0]][ij[1]]  = -self.NBD
                return
        ij2 = ij1
        ij3 = ij
        initial_NBD = self.NBD# * self.O_H_type
        print("initial_NBD",initial_NBD)
        for k in range(self.MAX_BODER):
            #self.disp_grid()
            #step 3.3
            ij4 = self.find_neighbor(ij3,ij2,0)
            # grid[ij1[0]][ij1[1]] = 2
            # grid[ij4[0]][ij4[1]] = 3
            x = ij3[0]
            y = ij3[1]
            #print(ij4[1],ij2[1])
            if ij4[0] - ij2[0] <=0:
                weight = -1
            else:
                weight = 1
            #print(ij4[0],ij2[0],weight)
            if self.grid[x][y] < 0:
                self.grid[x][y] = self.grid[x][y]
                
            elif self.grid[x][y-1] == 0 and self.grid[x][y+1] ==0:
                self.grid[x][y] = initial_NBD*weight
                #if ij3[0] > ij2[0] and ij3[1] == ij2[1]:
                #    self.grid[x][y] = initial_NBD*self.O_H_type*
                # ij3[1] == ij2[1]:
                #    self.grid[x][y] = -initial_NBD*self.O_H_type 
                    
            elif self.grid[x][y+1]== 0:
                self.grid[x][y] = -initial_NBD
                
            elif self.grid[x][y]== 1 and self.grid[x][y+1] != 0:
                self.grid[x][y] = initial_NBD
                
            else:
                self.grid[x][y] = self.grid[x][y]
                
            if ij4 == ij and ij3 ==ij1:
                return 
            ij2 = ij3
            ij3 = ij4
    
    def raster_scan(self):
        #self.disp_grid()
        for i in range(self.grid.shape[0]):
            for j in range(self.grid.shape[1]):
                if self.grid[i][j] >= 1:
                    if self.grid[i][j] > 1:
                        self.LNBD = abs(self.grid[i][j])
                    if self.grid[i][j] == 1 and self.grid[i][j-1] == 0:
                        self.NBD += 1
                        self.board_follow([i,j],[i,j-1],1)
                     
                    elif self.grid[i][j] > 1 and self.grid[i][j+1] == 0:
                        self.NBD += 1
                        self.board_follow([i,j],[i,j+1],1)
 


def main(): 
    fc = FindContours()       
    fc.raster_scan()
    fc.disp_grid()
    
    grid1 = np.array([[0,0,0,0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,1,0,0,0,0,0,0,0,0,0],
                      [0,0,1,1,1,1,1,1,1,0,0,0,0],
                      [0,0,1,0,0,1,0,0,0,1,1,0,0],
                      [0,0,1,0,0,1,0,0,1,0,0,0,0],
                      [0,0,1,0,0,1,0,0,1,0,0,0,0],
                      [0,0,1,1,1,1,1,1,1,0,0,0,0],
                      [0,0,0,1,0,0,1,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0,0,0,0,0,0],])
    fc.load_map_from_array(grid1)
    fc.raster_scan()
    fc.disp_grid()

    '''
    img = cv2.imread("../imgs/luoxuan1.png",0)
    img[img<130] = 0
    img[img>0] = 1
    img = 1-img
    
    fc.load_map_from_array(img)
    fc.raster_scan()
    ret =abs(fc.grid) 
    ret[ret<2] = 0
    ret[ret>0] = 1
    plt.figure()
    plt.imshow(img,"gray") # 显示图片
    plt.axis('off') # 不显示坐标轴
    plt.show()
    plt.figure()
    plt.imshow(ret,"gray") # 显示图片
    plt.axis('off') # 不显示坐标轴
    plt.show()
    '''

if __name__ == "__main__":
    main()




