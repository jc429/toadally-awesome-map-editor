import os
import tkinter as tk
from tkinter.constants import BOTH, BOTTOM, LEFT, RIGHT, TRUE
from PIL import ImageTk, Image 
from functools import partial

### Globals ###
tilesPerRow = 16
program_dir = os.path.dirname(__file__)
rel_path = "../graphics/maps/test/testmap.png"
abs_file_path = os.path.join(program_dir, rel_path)
map_img = Image.open(abs_file_path)
msg = "Toadally Awesome Level Collision Map Generator"
tile_buttons = []
tile_label = None
###############

def choose_tile(tile_id):
	global tile_label
	tile_text = "Currently Selected Tile: (" + str(tile_id%16) + "," + str(int(tile_id/16)) + ")"
	tile_label['text'] = tile_text

def fill_window():
	global tk_img
	global tile_label
	leftFrame = tk.Frame()
	midFrame = tk.Frame()
	rightFrame = tk.Frame()

	# Image of current working map, for reference
	imageFrame = tk.Frame(
		master=leftFrame,
		borderwidth=5,
		relief=tk.RIDGE
	)
	#add form to fill this in 
	label1 = tk.Label(master=imageFrame, image=tk_img)
	label1.grid()
	imageFrame.grid(column=0,sticky=tk.W)

	# Tile Buttons
	tileAreaFrame = tk.Frame(
		master=midFrame,
		borderwidth=5,
		relief=tk.RIDGE
	)
	for i in range(0,tilesPerRow):
		rowFrame = tk.Frame(master=tileAreaFrame)
		#header = tk.Label(master=frame,text="row")
		#header.pack()
		for j in range(0,tilesPerRow):
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
				command= partial(choose_tile, i*16+j)
			)
			tile_buttons.append(button)
			#label.pack(side=tk.TOP)
			button.grid()
			f.grid(row=0, column=j)
		rowFrame.grid(row=i)
	tileAreaFrame.grid(row=1)


	# Map Path
	pathFrame = tk.Frame(
		master=midFrame
	)
	pathLabel = tk.Label(
		master=pathFrame,
		text="Map Path:"
	)
	pathEntry = tk.Entry(
		master=pathFrame,
		width=40
	)
	pathButton = tk.Button(
		master=pathFrame,
		text="Load Map"
	)

	pathLabel.grid(row=0, column=0, sticky=tk.W)
	pathEntry.grid(row=0, column=1)
	pathButton.grid(row=0, column=2, sticky=tk.E)

	pathFrame.grid(row=0, sticky=tk.N)

	
	# Tile Settings
	settingsFrame = tk.Frame(
		master=rightFrame,
		borderwidth=5,
		relief=tk.RIDGE
	)

	tile_label = tk.Label(
		master=settingsFrame,
		width=40,
		text="Currently Selected Tile: (X,Y)"
	)
	tile_label.grid(row=0)

	propsFrame= tk.Frame(
		master=settingsFrame
	)

	prop_label = tk.Label(
		master=propsFrame,
		text="Tile Properties:"
	)
	prop_label.grid(row=0, sticky=tk.W)
	prop_solid = None
	prop_hole = None
	prop_grab = None
	prop_pain = None
	prop_victory = None
	tk.Checkbutton(master=propsFrame, text="Solid", variable=prop_solid).grid(row=1, sticky=tk.W)
	tk.Checkbutton(master=propsFrame, text="Hole", variable=prop_hole).grid(row=2, sticky=tk.W)
	tk.Checkbutton(master=propsFrame, text="Grabbable", variable=prop_grab).grid(row=3, sticky=tk.W)
	tk.Checkbutton(master=propsFrame, text="Pain", variable=prop_pain).grid(row=4, sticky=tk.W)
	tk.Checkbutton(master=propsFrame, text="Victory", variable=prop_victory).grid(row=5, sticky=tk.W)

	propsFrame.grid(row=1, sticky=tk.S)

	settingsFrame.grid(row=0, sticky=tk.N)

	leftFrame.grid(row=0, column=0, sticky=tk.SW)
	midFrame.grid(row=0, column=1, sticky=tk.S)
	rightFrame.grid(row=0, column=2, sticky=tk.NE)





window = tk.Tk()
window.title(msg)
tk_img = ImageTk.PhotoImage(map_img.resize((512,512),Image.NEAREST))

fill_window()
window.mainloop()