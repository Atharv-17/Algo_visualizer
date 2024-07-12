import math
import random
import pygame
import math
pygame.init()

#strating initialization class
class DrawInfo :
    black=0, 0, 0
    white=255, 255, 255
    green=0,  0, 255
    red=255, 0, 0
    grey= 128, 128, 128
    Background_color= white


    greyzz=[
        (128, 128, 128),
        (160, 160, 160),
        (192, 192, 192)
    ]

    font = pygame.font.SysFont("comicsans", 15)
    larger_font=pygame.font.SysFont("comicsans", size=25)

    side_pad=100
    top_pad=150

    def __init__(self, width, height, lst):
        self.width= width
        self.height = height

        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorithm Visualization")
        self.set_list(lst)

    def set_list(self, lst):
        self.lst=lst
        self.min_val=min(lst)
        self.max_val=max(lst)

        self.block_width=round((self.width - self.side_pad) / len(lst))
        self.block_height= math.floor((self.height - self.top_pad)/ (self.max_val - self.min_val))

        self.start_x= self.side_pad//2


#drawing liist

def draw(draw_info, algo_name, asce):
    draw_info.window.fill(draw_info.Background_color)

    title = draw_info.larger_font.render(f"{algo_name} - {'Ascending' if asce else 'Descending'}", 1, draw_info.green)
    draw_info.window.blit(title, (draw_info.width / 2 - title.get_width() / 2, 35))

    controls = draw_info.font.render("R=Reset||SPACE=Start Sorting||A=ascending||D=descending", 1, draw_info.black)
    draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2, 45))

    sorting = draw_info.font.render("I=insertion sort || B=bubble sort", 1, draw_info.black)
    draw_info.window.blit(sorting, (draw_info.width / 2 - sorting.get_width() / 2, 75))

    draw_list(draw_info)
    pygame.display.update()

def draw_list(draw_info, color_position={}, clear_bg=False):
    lst = draw_info.lst

    if clear_bg:
        clear_rect = (draw_info.side_pad//2, draw_info.top_pad,
                      draw_info.width - draw_info.side_pad,
                      draw_info.height - draw_info.top_pad )
        pygame.draw.rect(draw_info.window, draw_info.Background_color, clear_rect)



    for i, val in enumerate(lst):
        x= draw_info.start_x + i * draw_info.block_width
        y= draw_info.height - (val- draw_info.min_val) * draw_info.block_height

        color=draw_info.greyzz[i%3]

        if i in color_position:
            color = color_position[i]

        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))

    if clear_bg:
        pygame.display.update()
#generating random starting list
def generate_starting_list(n, min_val, max_val):
    lst= []
    for _ in range (n):
        val = random.randint(min_val, max_val)
        lst.append(val)

    return lst

#main even loop



def bubble_sort(draw_info, asce=True):
    lst = draw_info.lst

    for i in range(len(lst) - 1):
        for j in range(len(lst) - 1 - i):
            n1= lst[j]
            n2=lst[j+1]

            if(n1 > n2 and asce) or (n1 < n2 and not asce):
                lst[j], lst[j+1] = lst[j + 1], lst[j]
                draw_list(draw_info, {j: draw_info.green, j+1: draw_info.red}, True)
                yield  True

    return lst

def insertion_sort(draw_info, asce=True):
    lst = draw_info.lst

    for i in range (1, len(lst)):
        current=lst[i]

        while True:
            asce_sort = i > 0 and lst[i-1] > current and asce
            desce_sort = i > 0 and lst[i-1] < current and not asce

            if not asce_sort and not desce_sort:
                break
            lst[i] = lst[i-1]
            i= i -1
            lst[i] = current
            draw_list(draw_info, {i-1: draw_info.green, i: draw_info.red}, True)
            yield True
    return lst







def main():
    run = True
    clock=pygame.time.Clock()

    n=50
    min_val=0
    max_val=100

    lst=generate_starting_list(n,min_val, max_val)
    draw_info = DrawInfo(800, 600, lst)
    sorting=False
    asce=True


    sorting_algo=bubble_sort
    sorting_algo_name="Bubble Sort"
    sorting_algo_generator=None

    while run:
        clock.tick(60)

        if sorting:
            try:
                next(sorting_algo_generator)
            except StopIteration:
                sorting=False
        else:
            draw(draw_info, sorting_algo_name, asce)



        draw(draw_info, sorting_algo_name,asce)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT :
                run = False

            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_r:
                lst = generate_starting_list(n, min_val, max_val)
                draw_info.set_list(lst)
                sorting=False

            elif event.key == pygame.K_SPACE and sorting==False:
                sorting=True
                sorting_algo_generator=sorting_algo(draw_info, asce)

            elif event.key == pygame.K_a and not  sorting:
                asce=True
            elif event.key == pygame.K_d and not  sorting:
                asce=False

            elif event.key == pygame.K_i and not sorting:
                sorting_algo=insertion_sort
                sorting_algo_name="Insertion Sort"

            elif event.key == pygame.K_b and not sorting:
                sorting_algo = bubble_sort
                sorting_algo_name = "Bubble Sort"




    pygame.quit()

if __name__ =="__main__":
    main()






