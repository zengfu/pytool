from PIL import Image
#ASCII_CHARS = [ '#', '?', '%', '.', 'S', '+', '.', '*', ':', ',', '@']
ASCII_CHARS = [ '', '.', ',', ':', ';', 'i', 'n', 'a', 'b','%', 'L', 'F','E','@','#']
str=" .,:;ox%#@"
def scale_image(image, new_width=200):
	"""Resizes an image preserving the aspect ratio.
	"""
	(original_width, original_height) = image.size
	aspect_ratio = original_height/float(original_width)
	new_height = int(aspect_ratio * new_width)
	new_image = image.resize((new_width, new_height))
	return new_image
im = Image.open("2.jpg")
im=scale_image(im)
gray=im.convert('L')
gray.show()
(x,y)=gray.size
raw_data=list(gray.getdata())
pixels_to_chars = [ASCII_CHARS[pixel_value/18] for pixel_value in
                   raw_data]
f=open('img.txt','w')
length=len(pixels_to_chars)
for index in xrange(0,length,x):
    buf=''.join(pixels_to_chars[index:index + x])
    f.write(buf+'\n')


