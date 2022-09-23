import numpy as np
from typing import List , Union , Tuple , Optional
from copy import deepcopy
from random import choice
from colorama import Back , Fore , Style

DEBUG = False

CUBE_COLORS = [
    f"{Back.WHITE}{Fore.BLACK} W {Style.RESET_ALL}",
    f"{Back.YELLOW}{Fore.BLACK} Y {Style.RESET_ALL}",
    f"{Back.RED}{Fore.BLACK} R {Style.RESET_ALL}",
    f"{Back.GREEN}{Fore.BLACK} G {Style.RESET_ALL}",
    f"{Back.MAGENTA}{Fore.BLACK} C {Style.RESET_ALL}",
    f"{Back.BLUE}{Fore.BLACK} B {Style.RESET_ALL}"
]

VALID_MOVES = [
    "U",
    "U'",
    "D",
    "D'",
    "F",
    "F'",
    "B",
    "B'",
    "L",
    "L'",
    "R",
    "R'"
    ]

THETA = np.radians(90)

ROT_X_CW = lambda theta : np.array([[1,0,0],[0,np.cos(theta),-np.sin(theta)],[0,np.sin(theta),np.cos(theta)]]) # rotate clockwise around x
ROT_Y_CW = lambda theta : np.array([[np.cos(theta),0,np.sin(theta)],[0,1,0],[-np.sin(theta),0,np.cos(theta)]]) # rotate clockwise around y
ROT_Z_CW = lambda theta : np.array([[np.cos(theta),-np.sin(theta),0],[np.sin(theta),np.cos(theta),0],[0,0,1]]) # rotate clockwise around z

def cube_graph_repr(element_list,row_indent_n=18,width=17,tab_width=2):
    """  
    Draws the cube like,

                     _______________
                    |               |
                    |   X   X   X   |
                    |   X   X   X   |
                    |   X   X   X   |
                    |_______________|
                    |               |    
                    |   X   X   X   |
                    |   X   X   X   |
                    |   X   X   X   |
     _______________|_______________|_______________
    |               |               |               |
    |   X   X   X   |   X   X   X   |   X   X   X   |
    |   X   X   X   |   X   X   X   |   X   X   X   |
    |   X   X   X   |   X   X   X   |   X   X   X   |
    |_______________|_______________|_______________|
                    |               |
                    |   X   X   X   |
                    |   X   X   X   |
                    |   X   X   X   |
                    |_______________|
                    
    
    where each X represents one elements from element_dict
                    """

    side_up , side_back , (side_left , side_down , side_right) , side_front = element_list

    side_up = side_up[0]
    side_back = side_back[0]
    side_front = side_front[0]

    row_indent = " "*row_indent_n
    delim = "|"
    w = width
    tab = " "*tab_width
    single_hline = "_"*w

    top_mid_row = row_indent + " " + single_hline
    
    empty_row = delim + " "*w
    empty_mid_row = row_indent + empty_row + delim

    row_entries = lambda ele_list : ''.join([tab + str(ele) for ele in ele_list])
    ending = tab + delim
    single_mid_row = lambda ele_list : row_indent + delim + row_entries(ele_list) + ending

    row_upper = delim + single_hline + delim

    mid_row_upper = row_indent + row_upper

    wide_row_upper = " " + (single_hline + delim)*2 + single_hline
    wide_row_lower = "|" + (single_hline + delim)*2 + single_hline + "|"

    wide_empty_row = empty_row*3 + delim

    wide_row_entries = lambda ele_list_list : ''.join([delim + row_entries(ele_list) + tab for ele_list in ele_list_list]) + delim

    names = ["UP (U) ","BACK (B)", "LEFT (L) DOWN (D) RIGHT (R) ","FRONT (F)"]

    text_max_width = len(max(names,key=len))

    lens = [text_max_width - len(name) for name in names]
    empty_tab = " "*text_max_width + "\t"
    
    cube_str = [
        empty_tab + top_mid_row,
        empty_tab + empty_mid_row,
        empty_tab + single_mid_row(side_up[0]),
        names[0] + " "*lens[0] + '\t' + single_mid_row(side_up[1]),
        empty_tab + single_mid_row(side_up[2]),
        empty_tab + mid_row_upper,
        empty_tab + empty_mid_row,
        empty_tab + single_mid_row(side_back[0]),
        names[1] + " "*lens[1] + '\t' + single_mid_row(side_back[1]),
        empty_tab + single_mid_row(side_back[2]),
        empty_tab + wide_row_upper,
        empty_tab + wide_empty_row,
        empty_tab + wide_row_entries([side_left[0],side_down[0],side_right[0]]),
        names[2] + ""*lens[2] + '\t' + wide_row_entries([side_left[1],side_down[1],side_right[1]]),
        empty_tab + wide_row_entries([side_left[2],side_down[2],side_right[2]]),
        empty_tab + wide_row_lower,
        empty_tab + empty_mid_row,
        empty_tab + single_mid_row(side_front[0]),
        names[3] + " "*lens[3] + '\t' + single_mid_row(side_front[1]),
        empty_tab + single_mid_row(side_front[2]),
        empty_tab + mid_row_upper
    ]

    return cube_str

def draw_cube(element_list,row_indent_n=2,width=15,tab_width=3):
    cube_str = cube_graph_repr(element_list,row_indent_n,width,tab_width)    

    for s in cube_str:
        print(s)

class CubeFace:

    def __init__(self, face_coord : List[int], face_col : int) -> None:
        self.face_col = face_col
        self.face_coord = np.array(face_coord)

    @property
    def x(self):
        return self.face_coord[0]

    @property
    def y(self):
        return self.face_coord[1]

    @property
    def z(self):
        return self.face_coord[2]

    def get_face(self):
        return self.face_coord

    def rotate_face(self,rot_mat,verbose=False):
        if verbose: print("Hello i am a face with coords", self.face_coord)
        self.face_coord = np.round(rot_mat @ self.face_coord)
        #self.face_coord = np.array(list(map(int,self.face_coord)))
        if verbose: print("I (the face) was rotated and now have coord", self.face_coord)

    def __repr__(self):
        return f'{CUBE_COLORS[self.face_col]}'

    def __str__(self):
        return f'{CUBE_COLORS[self.face_col]}'

class CubeElement:

    def __init__(self,coords : List[List[int]], faces : List[CubeFace]) -> None: 
        self.faces = faces
        self.coords = coords

    def rotate_element(self,rot_mat : List[List[float]],verbose : Optional[bool] = False) -> None:
        if verbose: print('Hello i am an element with coords', self.coords)
        self.coords = np.round(rot_mat @ self.coords)
        #self.coords = np.array(list(map(int,self.coords)))
        if verbose: print(f'I am now rotating all my {len(self.faces)} faces')
        for face in self.faces:
            if verbose: print("rotating", face)
            face.rotate_face(rot_mat,verbose=verbose)
        if verbose: print('\nI (the element) was rotated and my new coords are', self.coords)

    def __repr__(self) -> str:
        f_string = ''
        for face in self.faces:
            f_string += f'{face} '
        return f'\nCoords: {self.coords}\nFaces: {f_string}\n'

class Cube:

    pre_prev_rotated_eles : List[CubeElement]
    post_prev_rotated_eles : List[CubeElement]

    def __init__(self) -> None:
        white_down = CubeFace([0,0,-1],0)
        ylw_up = CubeFace([0,0,1],1)
        red_back = CubeFace([0,1,0],2)
        green_left = CubeFace([-1,0,0],3)
        orange_front = CubeFace([0,-1,0],4)
        blue_right = CubeFace([1,0,0],5)

        facetypes = [white_down,ylw_up,red_back,green_left,orange_front,blue_right]

        # Holds the cube graphics
        self.eles_graphics = [
            [
                np.zeros((3,3),dtype=object)
                ], # UP 
            [
                np.zeros((3,3),dtype=object)
                ], # BACK
            [
                np.zeros((3,3),dtype=object), 
                np.zeros((3,3),dtype=object), 
                np.zeros((3,3),dtype=object)
                ], # LEFT BOTTOM RIGHT 
            [
                np.zeros((3,3),dtype=object)
                ]  # FRONT
            ]
        idxes = [-1,0,1]
        self.eles = []
        for i in idxes:
            for j in idxes:
                for k in idxes:
                    coords = np.array([i,j,k])
                    
                    faces = []
                    for face in facetypes:
                        if (face.x == i and face.x != 0) or (face.y == j and face.y != 0) or (face.z == k and face.z != 0):
                            facecopy = deepcopy(face)
                            faces.append(facecopy)
                            glob_row , glob_col , loc_row , loc_col = face_to_graphic(facecopy,coords)
                            
                            self.eles_graphics[glob_row][glob_col][loc_row,loc_col] = face
                    
                    if faces:
                        ele = CubeElement(coords,faces)
                        self.eles.append(ele)
                    
    def __repr__(self):
        return '\n'.join(cube_graph_repr(self.eles_graphics))

    def print_cube(self):
        draw_cube(self.eles_graphics)

    def move(self,rot_cmd : str, show_cube : Optional[bool] = False):
        send_cmd = ""
        for cmd in rot_cmd:
            if not cmd == "'":
                if send_cmd: 
                    try:
                        self.rotate(send_cmd,show_cube)
                    except AssertionError:
                        print("Illegal move! Not rotating.")
                
                send_cmd = cmd
            else:
                send_cmd += cmd
                self.rotate(send_cmd,show_cube)
                send_cmd = ""
        
        if send_cmd:
            self.rotate(send_cmd,show_cube)

    def rotate(self,rot_cmd : str, show_cube : Optional[bool] = True, verbose : Optional[bool] = False):
        #U UPPER
        #R RIGHT
        #L LEFT
        #F FRONT
        #B BACK
        #D DOWN
        rot_cmd = rot_cmd.upper()
        assert rot_cmd in VALID_MOVES , f"Illegal move '{rot_cmd}' Move must be one of: {VALID_MOVES}"

        rot_layer = rot_cmd[0]
        if len(rot_cmd) == 2:
            prime_cmd = "CW" if rot_cmd[1] == "'" else "ACW"
        else:
            prime_cmd = "ACW"

        if rot_layer == "U": # OK!
            # z coord must be 1
            idx = 2
            val = 1
            rot_mat = ROT_Z_CW
            rot_dir = 1 if prime_cmd == "CW" else -1
        elif rot_layer == "D": # OK!
            # z coord must be -1
            idx = 2
            val = -1
            rot_mat = ROT_Z_CW
            rot_dir = 1 if prime_cmd == "CW" else -1
        elif rot_layer == "R": # OK!
            # x coord must be 1
            idx = 0
            val = 1
            rot_mat = ROT_X_CW
            rot_dir = 1 if prime_cmd == "CW" else -1
        elif rot_layer == "L": # OK!
            # x coord must be -1
            idx = 0
            val = -1
            rot_mat = ROT_X_CW
            rot_dir = -1 if prime_cmd == "CW" else 1
        elif rot_layer == "F": # OK!
            # y coord must be 1
            idx = 1
            val = -1
            rot_mat = ROT_Y_CW
            rot_dir = -1 if prime_cmd == "CW" else 1
        elif rot_layer == "B": # OK!
            # y coord must be -1
            idx = 1
            val = 1
            rot_mat = ROT_Y_CW
            rot_dir = 1 if prime_cmd == "CW" else -1
        else:
            print('ILLEGAL MOVE!')
            return

        try:
            eles_to_rotate = self.__filter_elements(idx,val) 
            self.pre_prev_rotated_eles = deepcopy(eles_to_rotate)
        except NameError:
            print('ILLEGAL MOVE!!')
        
        for ele in eles_to_rotate:
            ele.rotate_element(rot_mat(rot_dir*THETA))
            for face in ele.faces:
                glob_row , glob_col , loc_row , loc_col = face_to_graphic(face,ele.coords)
                self.eles_graphics[glob_row][glob_col][int(loc_row),int(loc_col)] = face

        self.post_prev_rotated_eles = eles_to_rotate

        if show_cube: print(self)

        # Add counting of each color as error check
    def scramble(self,n_rotations=100):
        
        for _ in range(n_rotations):
            move = choice(VALID_MOVES)
            self.rotate(move,show_cube=False)
        print(f"Cube scrambled randomly {n_rotations} times!")
        print(self)

    def reset(self,show_cube=True):
        self.__init__()
        if show_cube: print(self)

    def __filter_elements(self,coord_idx,coord_val):
        eles_to_rotate = []
        
        for ele in self.eles:
            if ele.coords[coord_idx] == coord_val:
                eles_to_rotate.append(ele)

        return eles_to_rotate

    def print_changed_eles(self):
        for ele_pre , ele_post in zip(self.pre_prev_rotated_eles,self.post_prev_rotated_eles):
            print(ele_pre,'|\n |\n V',ele_post)


def face_to_graphic(face,coord):

    x , y , z = coord + 1
    
    if face.z == 1: # Och pekar uppåt
        if DEBUG: print(f'{face} {face.x,face.y,face.z} {coord} UPPÅT')
        global_idx = 0
        global_col = 0
        local_row = y
        local_col = x
    elif face.z == -1: # Och pekar nedåt
        if DEBUG: print(f'{face} {face.x,face.y,face.z} {coord} NEDÅT')
        global_idx = 2
        global_col = 1
        local_row = 2-y
        local_col = x
    elif face.x == 1: # Och pekar åt höger
        if DEBUG: print(f'{face} {face.x,face.y,face.z} {coord} HÖGER')
        global_idx = 2
        global_col = 2
        local_row = 2-y
        local_col = z
    elif face.x == -1: # Och pekar åt vänster
        if DEBUG: print(f'{face} {face.x,face.y,face.z} {coord} VÄNSTER')
        global_idx = 2
        global_col = 0
        local_row = 2-y
        local_col = 2-z
    elif face.y == 1: # Och pekar bakåt
        if DEBUG: print(f'{face} {face.x,face.y,face.z} {coord} BAKÅT')
        global_idx = 1
        global_col = 0
        local_row = 2-z
        local_col = x
    elif face.y == -1: # Och pekar framåt
        if DEBUG: print(f'{face} {face.x,face.y,face.z} {coord} FRAMÅT')
        global_idx = 3
        global_col = 0
        local_row = z
        local_col = x
    else:
        print('INGET!')
        raise ValueError(f'Incorrect coordinate, {coord}')
    
    return global_idx , global_col , local_row , local_col



if __name__ == "__main__": 
    all_cols = [[r for _ in range(3)] for r in [["R"]*3,["B"]*3,["Y"]*3,["W"]*3,["O"]*3,["G"]*3]]
    
    #face1 = CubeFace([0,0,-1],0)
    #print(face_to_graphic(face1,np.array([-1,-1,-1])))
    
    c = Cube()
    #c.print_cube()
    c.rotate("L")
    c.rotate("L")
    #print(c)