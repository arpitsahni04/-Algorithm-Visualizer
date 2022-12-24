import pygame
import math
from queue import PriorityQueue


WIDTH=800

RED = (255, 0, 0)

GREEN = (0, 255, 0)

BLUE = (0, 255, 0)

YELLOW = (255, 255, 0)

WHITE = (255, 255, 255)

BLACK = (0, 0, 0)

PURPLE = (128, 0, 128)

ORANGE = (255, 165 ,0)

GREY = (128, 128, 128)

TURQUOISE = (64, 224, 208)




WIN=pygame.display.set_mode((WIDTH,WIDTH))

pygame.display.set_caption("A* Path Finding Algorithm")



class Spot:


    def __init__(self,row,col,width,total_rows):
        self.row=row
        self.col=col

        self.x=col*width

        self.y=row*width

        self.color=WHITE

        self.neighbors=[]
        self.block_width=width    # total window width
        self.total_rows=total_rows



# bunch of methods which tell us state and allow us to update it 
    def get_pos(self):
        return self.row,self.col
    
    

    def is_closed(self):

        """

        Check if this spot is already dequed or its neighbours have been checked
        #already considered or checked
        """
        return self.color==RED


    def is_open(self):
        

        return self.color==GREEN


    def is_barrier(self):

        return self.color==BLACK


    def is_start(self):

        return self.color==ORANGE


    def is_end(self):

        return self.color==TURQUOISE


    def reset(self):

        self.color=WHITE


    def make_closed(self):

        #already considered or checked

        self.color=RED


    def make_open(self):

        self.color=GREEN


    def make_barrier(self):

        self.color=BLACK


    def make_start(self):

        self.color=ORANGE


    def make_end(self):

        self.color=TURQUOISE


    def make_path(self):

        self.color=PURPLE


    def draw(self,win):

        pygame.draw.rect(win,self.color,(self.x,self.y,self.block_width,self.block_width))

    def update_neighbors(self,grid):

        self.neighbors=[]

        #finding neighbours to current node

        if self.row<self.total_rows-1 and not grid[self.row+1][self.col].is_barrier():#DOWN

            self.neighbors.append(grid[self.row+1][self.col])
        

        if self.row>0 and not grid[self.row-1][self.col].is_barrier():#UP

            self.neighbors.append(grid[self.row-1][self.col])


        if self.col<self.total_rows-1 and not grid[self.row][self.col+1].is_barrier():#RIGHT

            self.neighbors.append(grid[self.row][self.col+1])


        if self.col>0 and not grid[self.row][self.col-1].is_barrier():#LEFT

            self.neighbors.append(grid[self.row][self.col-1])


def h(p1,p2):

    #dist b/w the points, manhattan-no diag only hor and vert

    x1,y1=p1

    x2,y2=p2

    return abs(x1-x2)+abs(y1-y2)


def reconstruct_path(came_from,current,draw):

    while current in came_from:

        current=came_from[current]

        current.make_path()
        draw()



def algorithm(draw,grid,start,end):

    #count tracks when we inserted, to break tie

    count=0

    open_set=PriorityQueue()


    open_set.put((0,count,start))


    came_from={}


    g_score={spot:float("inf")for row in grid for spot in row } # dictionary for g_score

    g_score[start]=0


    f_score={spot:float("inf")for row in grid for spot in row}

    f_score[start]=h(start.get_pos(),end.get_pos())


    open_set_hash={start}


    while not open_set.empty():

        # if open set is empty we have considered all nodes

        for event in pygame.event.get():

            if event.type==pygame.QUIT:

                pygame.quit()
            
        

        current=open_set.get()[2]

        # sets current to lowest f_score node in open_set

        open_set_hash.remove(current)

        #removes same node from open_set_hash

        if current==end:

            # reconstrust the path
            reconstruct_path(came_from,end,draw)

            end.make_end()

            return True
        

        for neighbor in current.neighbors:

            temp_g_score=g_score[current]+1


            if temp_g_score <g_score[neighbor]:

               came_from[neighbor]=current

               g_score[neighbor]=temp_g_score

               f_score[neighbor]=temp_g_score+h(neighbor.get_pos(),end.get_pos())

               if neighbor not in open_set_hash:

                  count+=1

                  open_set.put((f_score[neighbor],count,neighbor))

                  open_set_hash.add(neighbor)

                  neighbor.make_open()

        draw()


        if current!=start:

            current.make_closed()

    return False

def make_grid(rows,grid_width):
    """ 
    Create a grid of spot objects that fill a given grid width and rows
    Args:
        rows (int): no of rows that discretize our window
        grid_width (_type_): width of our grid window

    Returns:
        grid containing spot objects
    """    

    grid=[]
    spot_width=grid_width//rows    

    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot=Spot(i,j,spot_width,rows)
            grid[i].append(spot)
    return grid


def draw_grid_lines(win,rows,grid_width):
    
    gap=grid_width/rows 

    for i in range(rows):
        
        pygame.draw.line(win,GREY,(0,i*gap),(grid_width,i*gap)) 

        for j in range (rows):

            pygame.draw.line(win,GREY,(j*gap,0),(j*gap,grid_width))




def draw(win,grid,rows,grid_width):


    win.fill(WHITE)

    for row in grid:
        for spot in row:
            spot.draw(win) 
            
    draw_grid_lines(win,rows,grid_width)
    pygame.display.update()



def get_click_pos(pos,rows,width):

    gap=width//rows
    x,y=pos
    row=y//gap
    col=x//gap
    
    return row,col


def main(win,grid_width):

    ROWS=50

    # initializing grid

    grid=make_grid(ROWS,grid_width)

    start=None
    end=None
    run=True
    while run:

        draw(win,grid,ROWS,grid_width)

        #check for mouseclick or keypress

        for event in pygame.event.get():

            if event.type==pygame.QUIT:
                run=False

            if pygame.mouse.get_pressed()[0]:    #left mouse button
                pos=pygame.mouse.get_pos()
                row,col=get_click_pos(pos,ROWS,grid_width) # which row,col for pos
                spot=grid[row][col]  #store the corresponding grid spot in a spot
                
                #this fetches the correct spot from grid
                if not start and spot!=end:
                    start=spot
                    start.make_start()

                elif not end and spot!=start:
                    end=spot
                    end.make_end()

                elif spot !=end and spot !=start:
                    spot.make_barrier()


            elif pygame.mouse.get_pressed()[2]:

                pos=pygame.mouse.get_pos()
                row,col=get_click_pos(pos,ROWS,grid_width)
                spot=grid[row][col]
                spot.reset()

                if spot==start:
                    start=None

                elif spot==end:
                    end=None

            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_SPACE and start and end:

                    #start

                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)


                    algorithm(lambda:draw(win,grid,ROWS,grid_width),grid,start,end )       


                if event.key==pygame.K_c:
                    start=None
                    end=None
                    grid=make_grid(ROWS,grid_width)


    pygame.quit()

if __name__=="__main__":
    main(WIN,WIDTH)