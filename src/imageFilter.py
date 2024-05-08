import sys
import cv2
import scipy.ndimage 
import matplotlib.pyplot as plt
import numpy as np
import os

def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]
    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))
    resized = cv2.resize(image, dim, interpolation = inter)
    return resized

def make_same_size(img1, img2):
    x = min(img1.shape[0], img2.shape[0])
    y = min(img1.shape[1], img2.shape[1])
    img1 = img1[0:x, 0:y]
    img2 = img2[0:x, 0:y]
    return (img1, img2)

def blackAndColor_render (img_rgb):
    src = img_rgb
    img = src    

    src = cv2.GaussianBlur(src, (3, 3), 0)
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    
    grad_x = cv2.Sobel(gray, cv2.CV_16S, 1, 0, ksize=3, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)
    grad_y = cv2.Sobel(gray, cv2.CV_16S, 0, 1, ksize=3, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)     
    abs_grad_x = cv2.convertScaleAbs(grad_x)
    abs_grad_y = cv2.convertScaleAbs(grad_y) 
    grad = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)
    img_edge = 255-grad
      
    print(img.shape)
    print(grad.shape)

    img = image_resize(img ,width = 800 ,height = 800 )
    grad = image_resize(grad ,width = 800 ,height = 800 )

    for i in range(0 ,grad.shape[0]):
        for j in range(0 ,grad.shape[1]):
            if grad[i][j] <= 85:
                img[i][j][0] = 0
                img[i][j][1] = 0
                img[i][j][2] = 0

    return img

def edge_render (img_rgb):
    src = img_rgb
    img = src    

    src = cv2.GaussianBlur(src, (3, 3), 0)
    gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    
    grad_x = cv2.Sobel(gray, cv2.CV_16S, 1, 0, ksize=3, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)
    grad_y = cv2.Sobel(gray, cv2.CV_16S, 0, 1, ksize=3, scale=1, delta=0, borderType=cv2.BORDER_DEFAULT)     
    abs_grad_x = cv2.convertScaleAbs(grad_x)
    abs_grad_y = cv2.convertScaleAbs(grad_y) 
    grad = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)
    img_edge = 255-grad
    return img_edge

def grayScale(img_rgb): 
    return np.dot(img_rgb[...,:3], [0.299, 0.587, 0.114])

def result(blur,gray): 
    r=blur*255/(255-gray)  
    r[r>255]=255 
    r[gray==255]=255 
    return r.astype('uint8')

def sketch_render(img_rgb) : 
    start_img = img_rgb
    img_gray = grayScale(start_img)
    img_inverted = 255-img_gray
    img_blur = scipy.ndimage.filters.gaussian_filter(img_inverted,sigma=5)
    img_color= result(img_blur,img_gray)
    return img_color


def blackAndOrange_render (img_rgb):
    img = img_rgb.copy()
    img_edge = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    _, img_edge = cv2.threshold(img_edge, 150, 255, cv2.THRESH_BINARY_INV)
    for i in range(0 ,img_edge.shape[0]):
        for j in range(0 ,img_edge.shape[1]):
            if img_edge[i][j] <= 0:
                img[i][j][0] = 15
                img[i][j][1] = 165
                img[i][j][2] = 253
            else:
                img[i][j][0] = 0
                img[i][j][1] = 0
                img[i][j][2] = 0
    return img
def cartoon_render (img_rgb):
    img_edge = edge_render(img_rgb)
    numDownSamples = 2 
    numBilateralFilters = 1  

    img_color = img_rgb
    for _ in range(0 ,numDownSamples):
        img_color = cv2.pyrDown(img_color)
    for _ in range(0 ,numBilateralFilters):
        img_color = cv2.bilateralFilter(img_color, 9, 9, 7)
    for _ in range(0 ,numDownSamples):
        img_color = cv2.pyrUp(img_color)

    img_color, img_edge = make_same_size(img_color, img_edge)

    for i in range(0 ,img_edge.shape[0]):
        for j in range(0 ,img_edge.shape[1]):
            if img_edge[i][j] <= 210 :
                img_color[i][j][0] = 0
                img_color[i][j][1] = 0
                img_color[i][j][2] = 0
    return img_color






path = 'image1.png'
img_rgb = cv2.imread(path)
    
while(1) :
    filterNumber = input(
    ''' List of filter :    
            Black&Color = 1 
            Cartoon = 2
            Orange_Black = 3
            Sketch = 4
            Quit = 0
        Plese insert number of filter : ''')
    filterNumber = int(filterNumber)
    if (filterNumber == 0):
        break
    elif(filterNumber == 1):
        img_rgb = image_resize(img_rgb ,width = 600 ,height = 600 )
        cv2.imshow('OrginalImage',img_rgb)
        cv2.waitKey()
        blackAndColor = blackAndColor_render(img_rgb)
        blackAndColor = image_resize(blackAndColor ,width = 600 ,height = 600 )
        cv2.imshow('blackAndColor_Filter',blackAndColor)
        cv2.waitKey()  
        cv2.destroyAllWindows() 
    elif(filterNumber == 2):
        img_rgb = image_resize(img_rgb ,width = 600 ,height = 600 )
        cv2.imshow('OrginalImage',img_rgb)
        cv2.waitKey()
        cartoon = cartoon_render(img_rgb)
        cv2.imshow('cartoon_Filter',cartoon)
        cv2.waitKey()
        cv2.destroyAllWindows()
    elif(filterNumber == 3):
        img_rgb = image_resize(img_rgb ,width = 600 ,height = 600 )
        cv2.imshow('OrginalImage',img_rgb)
        cv2.waitKey()
        blackAndOrange = blackAndOrange_render(img_rgb)
        cv2.imshow('blackAndOrange_Filter',blackAndOrange)
        cv2.waitKey()
        cv2.destroyAllWindows()
    elif(filterNumber == 4):
        img_rgb = image_resize(img_rgb ,width = 600 ,height = 600 )
        cv2.imshow('OrginalImage',img_rgb)
        cv2.waitKey()
        import imageio
        sketch = sketch_render(img_rgb)
        cv2.imshow('sketch_Filter',sketch)
        cv2.waitKey()
        cv2.destroyAllWindows()
    else:
        print ("wrong number!! Try again")
