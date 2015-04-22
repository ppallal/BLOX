import Image, ImageFont, ImageDraw

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 480

thenode = {	'dtype':'div',
			'children': 	[
							{
								'dtype': 'text',
								'size': 16,
								'text':'hey',
								'align': 'left',
								'width':20,
								'height':10
							},
							{
								'dtype': 'image',
								'src': 'blox.png',
								'align': 'right',
								'width':300,
								'height':300
							}

						],
			'align': 'left',
			'width': 400,
			'height': 400
		  }

img = Image.new('L',(SCREEN_WIDTH, SCREEN_HEIGHT),'white')
draw = ImageDraw.Draw(img)

# def img_test_01():
# 	img = Image.new('L',(100,50),'white')
# 	img.save('/Users/praveenchukka/Desktop/image.BMP','BMP')
# 	del img

#def addText(img,(x,y),(insidex,insidey,width))

lineheight = 2

def drawme(node,(parentwidth,parentheight)):
	
	#place point
	placex,placey = 0,0
	if(node['align'] == "left"):
		if(node.has_key('x')):
			placex = node['x']+2
		else:
			placex = 2
	elif(node['align']=="center"):
		placex = (parentwidth-node['width'])/2
	elif(node.align=='right'):
		placex = parentwidth-2-node['width']
	
	# placey = parentheight+node['y']+2
	placey = parentheight+2

	print str(placex)+" "+str(placey)+"\n"

	if(node['dtype'] == "text"):
		font = ImageFont.truetype("TNR.ttf", node['size'])
		draw.text((placex,placey),node['text'],font=font)
	elif(node['dtype'] == "image"):
		img2 = Image.open(node['src'])
		#region = img2.crop(0,0,node.width,node.height) cropping
		draw.paste(img,(placex,placey))
	elif(node['dtype'] == "div"):
		global lineheight
		for i in node['children']:
			img.show()
			drawme(i,(node['width'],lineheight))
		lineheight+= node['height']


drawme(thenode,(2,2))
img.show()
del draw
