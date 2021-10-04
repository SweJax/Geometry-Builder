
# ©2021

""" IMPORT  """
from tkinter import *
from tkinter import filedialog

""" Default grid size  """
N_CELLS = 16

""" Global variables  """
WHITE = 'white'
BLACK = 'black'
NUMPOINTS = 0

class Geometry:

    """    Class variables     """
    colours = (WHITE, BLACK)
    ncolours = len(colours)
    ready = 0
    numpoints = 0

##################################################################################
##-----------------------------INIT---------------------------------------------##  
##################################################################################
    """     Initialize mainwindow       """
    def __init__(self, master, n, width=600, height=600, pad=0):
        global numpoints

        ##--Number of cells in each dimension--##
        self.n = n
        ##--Height and width of mainwindow--##
        self.width, self.height = width, height
        col_height = 40

        ##--Padding (not really used)--##
        npad = n + 1
        self.pad = pad
        ##--Cell size (x)--##
        xsize = (width - npad*pad) / n
        ##--Cell size (y)--##
        ysize = (height - npad*pad) / n

        ##--Hight and width for the grid containing colors--##
        c_width, c_height = width, height
        p_pad = 5
        p_width = p_height = col_height - 2*p_pad

        ##--mainwindow init--## 
        frame = Frame(master)
        frame.pack()

        #/root.iconbitmap('PATH') ##--Set titlebar icon--##
        root.title("Geometry Builder") ##--Set titlebar text--##

        ##--Canvas containing Color rects--## 
        self.col_canvas = Canvas(master, width=c_width,
                                     height=col_height)
        self.col_canvas.pack()


        ##--Color rects (mainwindow)--## 
        self.col_rects = []
        for i in range(self.ncolours):
            x, y = p_pad * (i+1) + i*p_width, p_pad
            rect = self.col_canvas.create_rectangle(x, y,
                            x+p_width, y+p_height, fill=self.colours[i])
            self.col_rects.append(rect)

        ##--Text and Labels (mainwindow)--##    
        self.text = StringVar()
        self.text.set(str(NUMPOINTS))
        self.numpoints = Label(frame, textvariable=self.text)
        self.numpoints.pack(side=RIGHT, padx=pad, pady = pad)
        label_numpoints = Label(frame, text='Numpoints: ')
        label_numpoints.pack(side=RIGHT, padx=pad, pady = pad)

        ##--col_index is the index of the currently selected colour--##
        self.col_index = 1
        self.select_colour(self.col_index)

        ##--The canvas onto which the grid is drawn--##
        self.w = Canvas(master, width=c_width, height=c_height)
        self.w.pack()

        ##--Add the cell rectangles to the grid canvas--##
        self.cells = []
        for iy in range(n):
            for ix in range(n):
                xpad, ypad = pad * (ix+1), pad * (iy+1) 
                x, y = xpad + ix*xsize, ypad + iy*ysize
                rect = self.w.create_rectangle(x, y, x+xsize,
                                           y+ysize, fill=WHITE)
                self.cells.append(rect)
                self.w

        ##--Buttons (Main window)--##
        ##

        ##--Load and save image buttons--##
        b_load = Button(frame, text='open', command=self.load_image)
        b_load.pack(side=LEFT, padx=pad, pady=pad)
        b_save = Button(frame, text='save', command=self.save_by_colour)
        b_save.pack(side=LEFT, padx=pad, pady=pad)
        ##--Add a button to clear the grid--##
        b_clear = Button(frame, text='clear', command=self.clear_grid)
        b_clear.pack(side=LEFT, padx=pad, pady=pad)
        ##--Add a button to display geometry--## 
        b_generate = Button(frame, text='Generate', command=self.generate_geometry)
        b_generate.pack(side=LEFT, padx=10, pady=10)

        ##
        
        """#####   Callback functions for the grid(mainwindow)     #####"""
        """                                                             """
        def color_click_callback(event):
                    x, y = event.x, event.y

                    ##--If user press on a color--##
                    if p_pad < y < p_height + p_pad:
                        ##--Index of the selected color rectangle (plus padding)--##
                        index = x // (p_width + p_pad)
                        ##--x-position with respect to the color rectangle left edge--##
                        xp = x - index*(p_width + p_pad) - p_pad
                        ##--Is the index valid and the click within the rectangle?--##
                        if index < self.ncolours and 0 < xp < p_width:
                            self.select_colour(index)

        ##--Callback function to the left mouse button--##
        self.col_canvas.bind('<ButtonPress-1>', color_click_callback)

        """ Set cell color  """
        def w_fill_callback(event):
            x, y = event.x, event.y
            fill(x, y, 0)

        """ Remove cell color  """
        def w_unfill_callback(event):
            x, y = event.x, event.y
            fill(x, y, 1)

        """ Function called when someone clicks on the grid canvas  """
        def fill(x, y, unfill):
            global NUMPOINTS
            # If user press a grid cell
            # Indexes into the grid of cells (including padding)
            ix = int(x // (xsize + pad))
            iy = int(y // (ysize + pad))
            xc = x - ix*(xsize + pad) - pad
            yc = y - iy*(ysize + pad) - pad
            if ix < n and iy < n and 0 < xc < xsize and 0 < yc < ysize:
                i = iy*n+ix
                if(unfill == 0):
                    c = self.w.itemcget(self.cells[i], 'fill')
                    if c == 'white':
                        NUMPOINTS = NUMPOINTS + 1
                        self.set_numpoints()
                    self.w.itemconfig(self.cells[i], fill=self.colours[self.col_index])
                elif(unfill == 1):
                    c = self.w.itemcget(self.cells[i], 'fill')
                    if c != 'white':
                        NUMPOINTS = NUMPOINTS - 1
                        self.set_numpoints()
                        #print(c)
                    self.w.itemconfig(self.cells[i], fill=self.colours[0])

        # Callback if user click on a cell
        self.w.bind('<ButtonPress-1>', w_fill_callback)
        # Callback if cursor cursor enters a cell with mousebutton 1 held down(Left-Click))
        self.w.bind('<B1-Motion>', w_fill_callback)
        # Callback if user right-click on cell
        self.w.bind('<ButtonPress-3>', w_unfill_callback)
        # Callback if cursor cursor enters a cell with mousebutton 3 held down(Right-Click)
        self.w.bind('<B3-Motion>', w_unfill_callback)

        """                                                             """
        """#############################################################"""

##################################################################################
##-------------------------Save and Load functions------------------------------##  
##################################################################################
    
    ##############
    """ SAVE """
    ##############

    """     Saves the Geometry coords into a file.geom      """   
    def save_by_colour(self):

        ##--Max geometrycoords per row in file.geom--##
        MAX_INPUT_PER_ROW = 12

        """Get the coords of the cell indexed at i. Formattated for a dict"""
        def _get_cell_coords(i, n):
            iy, ix = divmod(i, n)
            return '{}{}{}{}{}'.format('{', ix, ',', iy, '}')

        def _get_coloured_cells_dict():
            """Return a dictionary of cell coordinates and their colors."""

            coloured_cell_cmds = {}
            for i, rect in enumerate(self.cells):
                c = self.w.itemcget(rect, 'fill')
                if c == WHITE:
                    continue
                coloured_cell_cmds[_get_cell_coords(i, self.n)] = c
            return coloured_cell_cmds
        
        """     Puts values into a string and writes it into a file     """
        def _output_coords(coords):
            
            coords.sort(key=lambda e: (e[0], e[1], e[2], e[3], e[4]))
            nrows = len(coords) // MAX_INPUT_PER_ROW + 1
            for i in range(nrows):
                print(', '.join(coords[i*MAX_INPUT_PER_ROW:(i+1)*MAX_INPUT_PER_ROW]),file=fo)

        ##--Create a dictionary of colors and a list of cell--##
        coloured_cell_cmds = _get_coloured_cells_dict()
        cell_colours = {}
        for k, v in coloured_cell_cmds.items():
            cell_colours.setdefault(v, []).append(k)

        ##--Let user choose a file to open--##
        with filedialog.asksaveasfile(mode='w',defaultextension=".geom") as fo:
            if not fo:
                return

            self.filename = fo.name
            print('Writing file to', fo.name)
            for colour, coords in cell_colours.items():
                print('{}\n{}'.format(colour,'-'*len(colour)), file=fo)
                _output_coords(coords)
                print('\n', file=fo)

    ##############
    """ LOAD """
    ##############

    def load_image(self):
        """Load an image from a provided file."""
        x = []
        y = []

        def _coords_to_index(coords, x, y):

            list = coords.strip('}')
            if (list[0] == '{'):
                x.append(list[1:])
            else:
                y.append(list[:])

            return x, y

        self.filename = filedialog.askopenfilename(filetypes=(
                ('Geometry files', '.geom'),
                ('All files', '*.*')))
        if not self.filename:
            return
        print('Loading file from', self.filename)
        self.clear_grid()
        ##--Open the file and read the image--##
        with open(self.filename) as fi:
            global NUMPOINTS
            for line in fi.readlines():
                line = line.strip()
                ##--Get color and continue--##
                if line in self.colours:
                    this_colour = line
                    continue
                ##--Skip the (--------------) row--##
                if not line or line.startswith('-'):
                    continue
                coords = line.split(',')
                ##--Skip everything that is not coords--##
                if not coords:
                    continue
                for coord in coords:
                    coordx, coordy = _coords_to_index(coord.strip(), x, y)
                ind = 0
                NUMPOINTS = 0
                for coord in coordx:
                    i = int(coordy[ind])* n + int(coord)
                    NUMPOINTS = NUMPOINTS + 1
                    self.set_numpoints()
                    ind = ind + 1
                    self.w.itemconfig(self.cells[i], fill=this_colour)

##################################################################################
##-------------------------Class functions---------------------------------------##  
##################################################################################

    """     Set the value of numpoint Label(Main window)        """                
    def set_numpoints(self):
        global NUMPOINTS
        self.text.set(str(NUMPOINTS))

    """     Select the colour indexed at i in the colours list   """
    def select_colour(self, i):
        """Select the colour indexed at i in the colours list."""

        self.col_canvas.itemconfig(self.col_rects[self.col_index],
                                       outline=BLACK, width=1)
        self.col_index = i
        self.col_canvas.itemconfig(self.col_rects[self.col_index],
                                       outline=BLACK, width=5)

##################################################################################
##-------------------------Geomtery Window--------------------------------------##  
##################################################################################

    """     Generates the geometry cooords & Copy result to clipboard   """
    def generate_geometry(self):

        """     Open Geometrywindow and display the geometry-coords    """
        def open_geometryw(str):
            global N_CELLS

            ##--Geometrywindow init--##
            geometry = Tk()

            geometry.clipboard_clear() ##--Clear clipboard--##
            geometry.clipboard_append(str) #Set clipboard--##
            geometry.update() ##--Save clipboard--## 

            geometry.configure(width=500, height=300) ##--Set window xy--##
            geometry.configure(bg='lightgray') ##--Set window backgroundcolor--##
            geometry.title("Result") ##--Set titlebar text--##
            #/geometry.iconbitmap('PATH') ##--Set titlebar icon--##

            ##--move window center--##
            ##
            winWidth = geometry.winfo_reqwidth()
            winwHeight = geometry.winfo_reqheight()
            posRight = int(geometry.winfo_screenwidth() / 2 - winWidth / 2)
            posDown = int(geometry.winfo_screenheight() / 2 - winwHeight / 2)
            geometry.geometry("+{}+{}".format(posRight, posDown))
            ##

            ##--Configure and pack generated geometry text--##
            #
            w = Text(geometry, height = 30, width=77)
            w.insert(1.0, geotest)
            w.pack()
    
            w.configure(bg=geometry.cget('bg'), relief="flat")
            w.configure(state="disabled")
            #

            ##--Mainloop--##
            geometry.mainloop()

        """     Get the coords of the cell indexed at i as a string """
        def _get_coords(i, n):
            iy, ix = divmod(i, n)
            cord_str = '{' + str(ix) + ',' + str(iy) + '}' + ','
            return cord_str

        """     Return a list of cell coordinates       """
        def _get_pointxy_dict(self):
            geometry_dict = ""
            format_i = 0
            for i, rect in enumerate(self.cells):
                c = self.w.itemcget(rect, 'fill')
                if c == WHITE:
                    continue
                format_i = format_i + 1
                if format_i == 10:
                    geometry_dict += '\n'
                    format_i = 0
                geometry_dict += _get_coords(i, self.n)
            geostr = (geometry_dict[0:int(len(geometry_dict) - 1)])
            return geostr

        geotest = _get_pointxy_dict(self)
        open_geometryw(geotest)

    """Reset the grid to the background "WHITE" colour."""
    def clear_grid(self):
        for cell in self.cells:
            self.w.itemconfig(cell, fill=WHITE)

##################################################################################
##------------------------BEFORE MAINPROGRAM------------------------------------##            
##################################################################################

""""        Open startupwindow and display grid size alternatives       """""
def startup():

        def open_startupw():
            ##--startupwindow init--##
            startupw = Tk()

            startupw.configure(width=500, height=300) ##--Set window xy--##
            startupw.configure(bg='white') ##--Set window background color--##
            startupw.title("Start - Geometry Builder") ##--Set titlebar text--##
            #/startupw.iconbitmap('PATH') ##--Set titlebar icon-##

            # move to center of the screen
            #
            winWidth = startupw.winfo_reqwidth()
            winwHeight = startupw.winfo_reqheight()
            posRight = int(startupw.winfo_screenwidth() / 2 - winWidth / 2)
            posDown = int(startupw.winfo_screenheight() / 2 - winwHeight / 2)
            startupw.geometry("+{}+{}".format(posRight, posDown))
            #

            ##--Labels (startupwindow)--##
            H1 = Label(startupw, text="Choose grid-size:").grid(row = 0)
            def set_colrow(cells):
                #print("0")
                global N_CELLS
                N_CELLS = cells
                startupw.quit()
                startupw.destroy()

            ##--Buttons (startupwindow)--##
            B1 = Button(startupw, text='8x8', command=lambda: set_colrow(8)).grid(row = 0, column = 1)
            B1 = Button(startupw, text='10x10', command=lambda: set_colrow(10)).grid(row = 0, column = 2)
            B2 = Button(startupw, text='16x16', command=lambda: set_colrow(16)).grid(row = 0, column = 3)
            B3 = Button(startupw, text='32x32', command=lambda: set_colrow(32)).grid(row = 0, column = 4)
            B4 = Button(startupw, text='64x64', command=lambda: set_colrow(64)).grid(row = 0, column = 5)

            ##--Mainloop--##
            startupw.mainloop()
            
        open_startupw()


"""             Starts the application              """

try:
    ##--Executing startup() and wait for return-##
    while startup():
        pass
    n = N_CELLS
except IndexError:
    ##--If error or user exit window -> size of Grid = Default value (16x16)--##
    n = N_CELLS

""""        Application mainloop        """""
root = Tk()
grid = Geometry(root, n, 600, 600, 0)
root.mainloop()
##################################################################################
##------------------------------------------------------------------------------##            
##################################################################################