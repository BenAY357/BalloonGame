import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import shutil


def main(): # for testing the file when run directly
    list_size = 10
    x = list(np.arange(1, list_size + 1))
    y = np.random.randint(1, list_size+1, size=(list_size))
    line_graph_gif = LineGraphGif(x = x, y = y, duration = 300, folder_name = "gif_pngs_temp", gif_name = "line_graph.gif",
                                    title = "Pumps Over Time", y_label="Pumps", x_label = "Balloon Number") # create_pngs will delete the "folder_name" so make sure that it isn't important
    line_graph_gif.create_gif()

class LineGraphGif(): # Generates a png of the graph at each stage and then creates a gif out of them

    def __init__(self,x,y, duration,gif_name, title, x_label, y_label,
                        x_ax_int = True, y_ax_int = True,folder_name = "gif_pngs_temp"): 
        self.x = x # x co-ordinates in list format
        self.y = y # y co-ordinates in list format
        self.duration = duration # time between each transition
        self.folder_name = folder_name # folder the pngs are stored in
        self.gif_name = gif_name # gif's file name
        self.title = title
        self.x_label = x_label
        self.y_label = y_label
        self.x_ax_int = x_ax_int # True- force x axis to only use integers. Can't have decimal places for the balloon number. 
        self.y_ax_int = y_ax_int # True- force y axis to only use integers. Can't have decimal places for the number of pumps. 

    def create_pngs(self): # create pngs
        if os.path.exists(f"{self.gif_name}.gif"):
            os.path.remove(f"{self.gif_name}.gif") # delete the previous participant's gif
        os.makedirs(f"{self.folder_name}/") # create folder to store the PNGs in
        # Create graph
        for i in self.x: 
            plt.plot(self.x[:i],self.y[:i])
            # Add labels
            plt.title(self.title)
            plt.ylabel(self.y_label)
            plt.xlabel(self.x_label)
            # keeping the axis constant makes the gif look nicer. 
            plt.xlim(min(self.x), max(self.x)) 
            plt.ylim(0, max(self.y) + 0.5)
            # save graph
            plt.savefig(f"{self.folder_name}/{i:003}", dpi = 400, facecolor = "white") 
            plt.figure(figsize=(20, 4))
            plt.close()

    def pngs_to_gif(self): # combine the pngs into a gif
        pngs = os.listdir(self.folder_name) # get all the png file names into a list
        # Open them as images 
        frames = []
        for png in pngs:
            new_frame = Image.open(f"{self.folder_name}/{png}")
            frames.append(new_frame)
        # Combine them into a gif
        frames[0].save(self.gif_name, format='GIF', # start from frame 0 (i.e. the first picture)
                append_images=frames[1:], # append all the other frames to it. 
                save_all=True,
                duration=self.duration, # set time between each transition.
                loop=1)
       # delete PNGs after the gif has been created
        shutil.rmtree(f"{self.folder_name}/")

    def create_gif(self): # run the two above methods one after the other to create the gif. 
        self.create_pngs()
        self.pngs_to_gif()

if __name__ == "__main__": 
    main()


