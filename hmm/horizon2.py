#!/usr/local/bin/python3
#
# Authors: Shujun Liu(liushuj)
#
# Mountain ridge finder
# Based on skeleton code by D. Crandall, Oct 2019
#

from PIL import Image
from numpy import *
from scipy.ndimage import filters
import sys
import imageio
from scipy.stats import norm

# calculate "Edge strength map" of an image
#
def edge_strength(input_image):
    grayscale = array(input_image.convert('L'))
    filtered_y = zeros(grayscale.shape)
    filters.sobel(grayscale,0,filtered_y)
    return sqrt(filtered_y**2)

# draw a "line" on an image (actually just plot the given y-coordinates
#  for each x-coordinate)
# - image is the image to draw on
# - y_coordinates is a list, containing the y-coordinates and length equal to the x dimension size
#   of the image
# - color is a (red, green, blue) color triple (e.g. (255, 0, 0) would be pure red
# - thickness is thickness of line in pixels
#
def draw_edge(image, y_coordinates, color, thickness):
    for (x, y) in enumerate(y_coordinates):
        for t in range( int(max(y-int(thickness/2), 0)), int(min(y+int(thickness/2), image.size[1]-1 )) ):
            image.putpixel((x, t), color)
    return image

# main program
#
(input_filename, gt_row, gt_col) = sys.argv[1:]

# load in image 
input_image = Image.open(input_filename)

# compute edge strength mask
edge_strength = edge_strength(input_image)
imageio.imwrite('edges.jpg', uint8(255 * edge_strength / (amax(edge_strength))))

# Viterbi
ep=(edge_strength**2)/((edge_strength**2).sum(0))
lep=ma.log(ep).filled(-inf)
rows,cols=edge_strength.shape
lv=zeros((rows,cols))
r=zeros((rows,cols))
p=diff(norm(0,1.33).cdf([range(-12,13)]))[0]
ltp=(-inf)*ones((rows,rows))
for i in range(rows):
    for j in range(i-12,i+12):
        if(j>=0 and j<rows):
            ltp[i,j]=log(p[(j-i)+12])
lv[:,0]=lep[:,0]+log(p[12])
for i in range(1,cols):
    vp=lv[:,i-1]+ltp.T
    r[:,i]=argmax(vp,1)
    lv[:,i]=lep[:,i]+vp.max(1)
path=[]
prev=int(r[argmax(lv[:,cols-1]),cols-1])
path.append(argmax(lv[:,cols-1]))
path.append(prev)
i=cols-2
while(i>0):
    prev=int(r[prev,i])
    path.append(prev)
    i=i-1
path.reverse()    
ridge=path

# output answer
imageio.imwrite("output.jpg", draw_edge(input_image, ridge, (255, 0, 0), 5))
