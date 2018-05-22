from PIL import Image
from resizeimage import resizeimage
import sudokuSolver
import os
import cv2
import math
import numpy as np
import sys
import operator

#resizes image into a 450 x 450 grid
def resizeImageIntoSquare(original_img_name):  
  original_img=open(original_img_name,'rb')
  new_img=Image.open(original_img)
  new_img=resizeimage.resize_width(new_img,450)
  longer_side=max(new_img.size)
  horizontal_padding=(longer_side-new_img.size[0])/2
  vertical_padding=(longer_side-new_img.size[1])/2
  new_img=new_img.crop((-horizontal_padding,-vertical_padding,new_img.size[0] + horizontal_padding,new_img.size[1] + vertical_padding))
  new_img.convert('RGB').save("img_02.png", "PNG", optimize=True)
  original_img.close()

#creates 81 50 x 50 images from the 450 x 450 image
def makeIndividualSquares(original_img):  
  original_img=open("img_02.png",'rb')
  for i in range(0,401,50):
    for j in range(0,401,50):
      cube=Image.open(original_img)
      cube=cube.crop((j,i,j+50,i+50))          
      cube.save("cube_"+str(i//50)+str(j//50)+".png")
      removeBlackBorders("cube_"+str(i//50)+str(j//50)+".png")
  original_img.close()

#removes the black borders of image
def removeBlackBorders(img_name):
  im=cv2.imread(img_name)
  for i in range(len(im)):
    for j in range(7):
      im[i][j]=[255,255,255]
  
  for i in range(len(im)):
    for j in range(len(im)-7,len(im),1):
      im[i][j]=[255,255,255]

  for i in range(len(im)-7,len(im),1):
    for j in range(len(im)):
      im[i][j]=[255,255,255]

  for i in range(7):
    for j in range(len(im)):
      im[i][j]=[255,255,255]

  os.remove(img_name)
  img=Image.fromarray(im,"RGB")
  img.save(img_name)

#center all numbers in their individual images
def centerCubes():
  for i in range(9):
    for j in range(9):
      center("cube_"+str(i)+str(j)+".png")

#returns the coordinates of the rectangle with smallest area such that the number
#is in that rectangle
def getCoordinatesOfRectangle(img_name):
  im=cv2.imread(img_name)
  tol=235
  x1=y1=x2=y2=-1
  for i in range(len(im)):
    for j in range(len(im[0])):
      for k in range(len(im[0][0])):
        if(im[i][j][k]<=tol):
          y1=i
          break
      if(y1!=-1):
        break

  for i in range(len(im[0])):
    for j in range(len(im)):
      for k in range(len(im[0][0])):
        if(im[j][i][k]<=tol):
          x1=i
          break
      if(x1!=-1):
        break

  for i in range(len(im[0])-1,-1,-1):
    for j in range(len(im)):
      for k in range(len(im[0][0])):
        if(im[j][i][k]<=tol):
          x2=i
          break
      if(x2!=-1):
        break

  for i in range(len(im)-1,-1,-1):
    for j in range(len(im[0])):
      for k in range(len(im[0][0])):
        if(im[i][j][k]<=tol):
          y2=i
          break
      if(y2!=-1):
        break
  
  return x1,y1,x2,y2  

#centers the number in an image
def center(img_name):
  im=cv2.imread(img_name)
  x1,y1,x2,y2=getCoordinatesOfRectangle(img_name)
  #(x1,y1) is the coordinates of the top left corner of rectangle
  #(x2,y2) is the coordinates of the bottom right corner of rectangle 
  #now that we've found the corners, we pad the left,top,right,bottom with white pixels
  data = np.zeros((len(im),len(im[0]),3),dtype=np.uint8)
  for i in range(len(im)):
    for j in range(len(im[0])):
      data[i][j]=[255,255,255]
  new_x1=(len(im)-x2+x1)//2
  new_x2=new_x1+x2-x1
  new_y1=(len(im)-y2+y1)//2+1
  new_y2=new_y1+y2-y1
  k=x1
  for i in range(new_x1,new_x2+1):
    l=y1
    for j in range(new_y1,new_y2+1):
      data[j][i]=im[l][k][:]
      l+=1
    k+=1
  img=Image.fromarray(data,"RGB")
  os.remove(img_name)
  img.save(img_name)
  
#uses readImage() to read each 50 x 50 image and store into the grid
def makeGrid():
  grid=[[-1 for i in range(9)] for j in range(9)]
  for i in range(9):
    for j in range(9):
      grid[i][j]=readImage("cube_"+str(i)+str(j)+".png")
  return grid

#compares a 50 x 50 image to pre-saved 50 x 50 images of numbers
#returns the value of the number in the image
def readImage(img_name):
  if(isWhite(img_name)):
    return 0
  num_matches={"1":0,"2":0,"3":0,"4":0,"5":0,"6":0,"7":0,"8":0,"9":0,"11":0,"21":0,"31":0,"41":0,"51":0,"61":0,"71":0,"81":0,"91":0}
  for i in num_matches.keys():
    num_matches[i]=compareImage(img_name,"Numbers/"+i+".png")
  return int(max(num_matches.items(),key=operator.itemgetter(1))[0][0])

#returns the number of matching pixels
def compareImage(img1_name,img2_name):
  im_1=cv2.imread(img1_name)
  im_2=cv2.imread(img2_name)
  if(len(im_1)!=len(im_2) or len(im_1[0])!=len(im_2[0])):
    return 0
  num_matching_pixels=0
  for i in range(len(im_1)):
    for j in range(len(im_2)):
      if(pixelsMatch(im_1[i][j],im_2[i][j])):
        num_matching_pixels+=1
  return num_matching_pixels

#return true if the RGB values of pix1 are reasonably close to the RGB values of pix2
def pixelsMatch(pix1,pix2):
  for i in range(len(pix1)):
    if(abs(int(pix1[i])-int(pix2[i]))>15):
      return False
  return True

#looks at an image, and return True if it's just a white background, i.e, the RGB value
#of each pixel is >=240 (leeway)
def isWhite(img_name):
  im=cv2.imread(img_name)
  for i in range(len(im)):
    for j in range(len(im[0])):
      for k in range(len(im[0][0])):
        if(im[i][j][k]<240):
          return False
  return True 

#delete img_02.png and cube_??.png
def deleteAllEvidence():
  os.remove("img_02.png")
  for i in range(9):
    for j in range(9):
      os.remove("cube_"+str(i)+str(j)+".png")

def main():
  resizeImageIntoSquare(input("Enter the name of the image file: "))
  makeIndividualSquares("img_02.png")
  centerCubes()
  grid=makeGrid()
  print("The puzzle is: ")
  sudokuSolver.printGrid(grid)
  if(sudokuSolver.solve(grid)):
    print("\n\nThe solved grid is: ")
    sudokuSolver.printGrid(grid)
  else:
    print("Grid is not solvable")
  deleteAllEvidence()

if(__name__ == "__main__"):
  main()
