from PIL import Image

img = Image.open('beehive10.jpg')
img.show()
pix = img.load()
print(img.size)
counter = 0
for y in range(img.size[1]):
    for x in range(img.size[0]):
        if(all(i>150 for i in pix[x,y])):
            counter += 1

print(str(counter/(img.size[1] * img.size[0]) * 100)+"%")
"""
for (x,y) , pixels in np.ndenumerate(img):
    print(pix[x,y])
"""
