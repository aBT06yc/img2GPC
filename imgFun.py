import cv2
import numpy as np

def make_picture(picture:str,x_main:int,y_main:int,black_border:int,invColour:bool,canny:bool,tLower:int,tUpper:int):      
    
    img=cv2.imread(picture, cv2.IMREAD_GRAYSCALE)
    img=cv2.resize(img,(x_main,y_main))
    
    example_print=np.zeros((y_main,x_main))
    if(canny):example_print = cv2.Canny(img,tLower,tUpper)
    
    white_pixel = 0

    for y,line in enumerate(img):
        for x,pixel in enumerate(line):
            if pixel > black_border:
                white_pixel+=1
                example_print[y,x]=255

    black_pixel = x_main*y_main-white_pixel
    black_per = (100*black_pixel)/(white_pixel+black_pixel)

    if (invColour):
        example_print = 255 - example_print
        black_per = 100 - black_per
    
    cv2.imwrite("example.jpg", example_print)

    return black_per

def make_gpc(x_main:int,y_main:int,colour:str,black_border:int,optimization:bool):

    if(colour == "White"): colour = 1
    else: colour = 0
    #preparing the file
    file= open("myScript.gpc", "w+")
    file.write("init{\nmyPrint()\n}\n\n"
                  +"function myPrint(){\n"
                  +f"cls_oled({1 - colour})\n")
    #+1 from right
    example_print = cv2.imread('example.jpg',cv2.IMREAD_GRAYSCALE)
    new_column = np.full((y_main, 1), 0 if colour == 0 else 0)
    example_print = np.hstack((example_print, new_column))

    if( optimization):
        for y,line in enumerate(example_print):
            x_count=0
            for x,pixel in enumerate(line):
                if(pixel > black_border ):
                    x_count+=1
                elif x_count != 0:
                    if x_count > 1:   #line
                        string = f"line_oled({x - x_count}, {y}, {x-1}, {y}, 1, {colour}); "
                    else:             # pixel
                        string = f"pixel_oled({x-1}, {y}, {colour}); "

                    x_count=0
                    file.write(string)

            file.write("\n")
    else:
         for y,line in enumerate(example_print):
            string=""
            for x,pixel in enumerate(line):
                if(pixel > black_border ):
                    string += f"pixel_oled({x}, {y}, {colour}); "
              
            file.write(string)
            file.write("\n")

    file.write("}")
    file.close()

