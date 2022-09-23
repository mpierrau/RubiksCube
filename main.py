from rubiks import CubeFace , CubeElement, ROT_X_CW , ROT_Y_CW , ROT_Z_CW , Cube , THETA
import numpy as np

my_face = np.array([[0],[1],[0],[0]])
my_face_rot = np.array([[0],[0],[1],[0]])

def test_faces():
    face1 = CubeFace([0,-1,0],1)
    face2 = CubeFace([0,0,1],2)
    face3 = CubeFace([1,0,0],5)

    ele = CubeElement([1,-1,1],[face1,face2,face3])
    print(ele)
    ele.rotate_element(ROT_Z_CW(THETA))
    print(ele)
    ele.rotate_element(ROT_Z_CW)
    print(ele)

def build_cube():
    c = Cube()
    print(c)
    c.rotate('U')
    c.print_changed_eles()

def main():
    #test_faces()
    build_cube()
    

if __name__ == '__main__':
    main()

