import os
import tkinter as tk
from tkinter.constants import BOTH, BOTTOM, LEFT, RIGHT, TRUE
from PIL import ImageTk, Image 
from functools import partial


### Globals ###
TILES_PER_ROW = 16
### WARNING: VERY IMPORTANT THAT THESE MATCH THE VALUES HARD CODED IN THE GAME ###
TILEPROP_SOLID		= 0x01
TILEPROP_HOLE		= 0x02
TILEPROP_GRAB		= 0x04
TILEPROP_PAIN		= 0x08
TILEPROP_VICTORY	= 0x80

program_dir = os.path.dirname(__file__)
rel_path = "../graphics/maps/test/testmap.png"
abs_file_path = os.path.join(program_dir, rel_path)
map_img = Image.open(abs_file_path)
title = "Toadally Awesome Level Collision Map Generator"

tile_properties = []	# array of tile properties
tile_buttons = []		# array of buttons corresponding to tiles on the map grid
tile_label = None		# label referencing currently selected tile
path_entry = None		# text form for entering a path to a map
map_canvas = None		# canvas that displays the currently open map


selected_tile = 0
###############

def loadMap(rel_path):
	global map_tkimg
	global map_canvas
	abs_file_path = os.path.join(program_dir, rel_path)
	map_img = Image.open(abs_file_path)
	map_tkimg = ImageTk.PhotoImage(map_img.resize((512,512),Image.NEAREST))
	map_canvas.create_image(0, 0, anchor=tk.NW, image=map_tkimg)
	drawGrid()
	return 
# loadMap


def loadMapFromTextbox():
	global path_entry
	rel_path = path_entry.get()
	#rel_path = "../graphics/maps/map1/map1.png"
	loadMap(rel_path)
	return
# loadMapFromTextbox


def selectTile(tile_id):
	global selected_tile
	global tile_label
	selected_tile = tile_id
	tile_text = "Currently Selected Tile: (" + str(tile_id%16) + "," + str(int(tile_id/16)) + ")"
	tile_label['text'] = tile_text
	loadTileProperties(tile_id)
	return
# selectTile


def drawGrid():
	global map_canvas
	for i in range(1,TILES_PER_ROW):
		map_canvas.create_line(32*i, 0, 32*i, 512, fill="red")
		map_canvas.create_line(0, 32*i, 512, 32*i, fill="red")
	return
# drawGrid


def colorTile(tile_id, red_val, green_val, blue_val):
	global tile_buttons
	color = '#%02X%02X%02X' % (red_val,green_val,blue_val)
	tile_buttons[tile_id]['bg'] = color
	return
# colorTile


def setTileProperties(tile_id, props):
	global tile_properties
	tile_properties[tile_id] = props
	red_v = max(0, min((props & TILEPROP_SOLID), 2)) * 255
	grn_v = 0
	blu_v = 0
	colorTile(tile_id, red_v, grn_v, blu_v)
	return
# setTileProperties


def clearTileProperties():
	global prop_solid
	global prop_hole
	global prop_grab
	global prop_pain
	global prop_victory
	prop_solid.set(False)
	prop_hole.set(False)
	prop_grab.set(False)
	prop_pain.set(False)
	prop_victory.set(False)
	return
# clearTileProperties


def loadTileProperties(tile_id):
	global tile_properties
	global prop_solid
	global prop_hole
	global prop_grab
	global prop_pain
	global prop_victory

	props = tile_properties[tile_id]
	prop_solid.set((props & TILEPROP_SOLID) != 0)
	prop_hole.set((props & TILEPROP_HOLE) != 0)
	prop_grab.set((props & TILEPROP_GRAB) != 0)
	prop_pain.set((props & TILEPROP_PAIN) != 0)
	prop_victory.set((props & TILEPROP_VICTORY) != 0)
	return
# loadTileProperties


def saveTileProperties():
	global selected_tile
	global prop_solid
	global prop_hole
	global prop_grab
	global prop_pain
	global prop_victory

	props = 0
	if(prop_solid.get()):
		props |= TILEPROP_SOLID
	if(prop_hole.get()):
		props |= TILEPROP_HOLE
	if(prop_grab.get()):
		props |= TILEPROP_GRAB
	if(prop_pain.get()):
		props |= TILEPROP_PAIN
	if(prop_victory.get()):
		props |= TILEPROP_VICTORY

	setTileProperties(selected_tile, props)
	return
# saveTileProperties


def fillLeftFrame():
	global map_canvas
	left_frame = tk.Frame()
	# Image of current working map, for reference
	image_frame = tk.Frame(
		master=left_frame,
		borderwidth=5,
		relief=tk.RIDGE
	)
	map_canvas = tk.Canvas(master=image_frame,width=510,height=510)
	map_canvas.grid()
	image_frame.grid(column=0,sticky=tk.W)
	loadMap(rel_path)
	left_frame.grid(row=0, column=0, sticky=tk.SW)
	return
# fillLeftFrame


def fillMidFrame():
	global path_entry

	mid_frame = tk.Frame()
	# Tile Buttons
	tile_area_frame = tk.Frame(
		master=mid_frame,
		borderwidth=5,
		relief=tk.RIDGE
	)
	for i in range(0,TILES_PER_ROW):
		rowFrame = tk.Frame(master=tile_area_frame)
		#header = tk.Label(master=frame,text="row")
		#header.pack()
		for j in range(0,TILES_PER_ROW):
			f = tk.Frame(master=rowFrame, width=16, height=16)
			#label = tk.Label(master=f, text=i)
			g = 8*i
			b = 8*j
			
			color = '#%02X%02X%02X' % (88,g,b)
			button = tk.Button(
				master=f,
				name="button("+str(i)+","+str(j)+")",
				text="    ",
				bg=color,
				command= partial(selectTile, i*16+j)
			)
			tile_buttons.append(button)
			#label.pack(side=tk.TOP)
			button.grid()
			f.grid(row=0, column=j)
		rowFrame.grid(row=i)
	tile_area_frame.grid(row=1)


	# Map Path
	path_frame = tk.Frame(
		master=mid_frame
	)
	path_label = tk.Label(
		master=path_frame,
		text="Map Path:"
	)
	path_entry = tk.Entry(
		master=path_frame,
		width=40
	)
	path_entry.insert(0,"../graphics/maps/map1/map1.png")
	path_button = tk.Button(
		master=path_frame,
		text="Load Map",
		command=loadMapFromTextbox
	)

	path_label.grid(row=0, column=0, sticky=tk.W)
	path_entry.grid(row=0, column=1)
	path_button.grid(row=0, column=2, sticky=tk.E)

	path_frame.grid(row=0, sticky=tk.N)
	mid_frame.grid(row=0, column=1, sticky=tk.S)
	return
# fillMidFrame



def fillRightFrame():
	global tile_label
	# Tile Props
	global prop_solid
	global prop_hole
	global prop_grab
	global prop_pain
	global prop_victory

	
	right_frame = tk.Frame()

	# Tile Settings
	settings_frame = tk.Frame(
		master=right_frame,
		borderwidth=5,
		relief=tk.RIDGE
	)

	tile_label = tk.Label(
		master=settings_frame,
		width=40,
		text="Currently Selected Tile: (X,Y)"
	)
	tile_label.grid(row=0)

	props_frame= tk.Frame(
		master=settings_frame
	)

	prop_label = tk.Label(
		master=props_frame,
		text="Tile Properties:"
	)
	prop_label.grid(row=0, sticky=tk.W)
	
	tk.Checkbutton(
			master=props_frame, 
			text="Solid", 
			variable=prop_solid
			).grid(row=1, sticky=tk.W)
	tk.Checkbutton(
			master=props_frame, 
			text="Hole", 
			variable=prop_hole
			).grid(row=2, sticky=tk.W)
	tk.Checkbutton(
			master=props_frame, 
			text="Grabbable", 
			variable=prop_grab
			).grid(row=3, sticky=tk.W)
	tk.Checkbutton(
			master=props_frame, 
			text="Pain", 
			variable=prop_pain
			).grid(row=4, sticky=tk.W)
	tk.Checkbutton(
			master=props_frame, 
			text="Victory", 
			variable=prop_victory
			).grid(row=5, sticky=tk.W)

	tk.Button(
			master=props_frame, 
			text='Clear', 
			width=10,
			command=clearTileProperties
			).grid(row=6, column=0, sticky=tk.W)
	tk.Button(
			master=props_frame, 
			text='Save', 
			width=10,
			command=saveTileProperties
			).grid(row=6, column=1, sticky=tk.W)

	props_frame.grid(row=1, sticky=tk.S)

	settings_frame.grid(row=0, sticky=tk.N)

	right_frame.grid(row=0, column=2, sticky=tk.NE)
	return
# fillRightFrame


def fillWindow():
	fillLeftFrame()
	fillMidFrame()
	fillRightFrame()
	return
# fillWindow





### Main Code ###


for i in range(0,256):
	tile_properties.append(0)
window = tk.Tk()
window.title(title)
map_tkimg = ImageTk.PhotoImage(map_img.resize((512,512),Image.NEAREST))
# Tile Properties
prop_solid = tk.BooleanVar()
prop_hole = tk.BooleanVar()
prop_grab = tk.BooleanVar()
prop_pain = tk.BooleanVar()
prop_victory = tk.BooleanVar()


fillWindow()

colorTile(47,0,255,0)

window.mainloop()