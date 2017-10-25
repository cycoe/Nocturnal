from PIL import Image
im = Image.open('check_12.gif')
im = im.convert("RGBA")

pixdata = im.load()

for y in range(im.size[1]):
    for x in range(im.size[0]):
        if pixdata[x,y][0] < 90:
            pixdata[x,y] = (0,0,0,255)

for y in range(im.size[1]):
    for x in range(im.size[0]):
        if pixdata[x,y][1] < 136:
            pixdata[x,y] = (0,0,0,255)

for y in range(im.size[1]):
    for x in range(im.size[0]):
        if pixdata[x,y][2] > 0:
            pixdata[x,y] = (255,255,255,255)


for y in range(1,im.size[1]-1):
    for x in range(1,im.size[0]-1):
        num = 0
        for j in range(y-1,y+2):
            for i in range(x-1,x+2):
                if(i != x or j != y):
                    if pixdata[i,j] == (255,255,255,255):
                        num +=1
        if num >= 6:
            pixdata[x,y] = (255,255,255,255)


im.save("output_12.gif","GIF")
