
from __future__ import with_statement
#from pygame.surface import Surface
import pygame
from math import cos, sin
#from pygame.locals import *
import os
import logging
from constants import __app__
from constants import *

__version__ = '1.0'
__release__ = '1.0.1b'
__author__ = 'Shawn Driscoll <shawndriscoll@hotmail.com>\nshawndriscoll.blogspot.com'

mapper_log = logging.getLogger('mapper')
mapper_log.setLevel(logging.DEBUG)

if not os.path.exists('Logs'):
    os.mkdir('Logs')

fh = logging.FileHandler('Logs/mapper.log', 'w')

formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s - %(message)s',
                              datefmt = '%a, %d %b %Y %H:%M:%S')
fh.setFormatter(formatter)
mapper_log.addHandler(fh)

mapper_log.info('Logging started.')
mapper_log.info('mapper v' + __version__ + ' started, and running...')

white = (255,255,255)
black = (0,0,0)
gray = (60,60,60)
green = (0, 255, 0)
red = (255, 0, 0)
yellow  = (255, 255, 0)
orange = (255,165,0)
amber = (255,191,0)
blue = (0, 0, 255)
darker_blue = (0, 0, 150)
purple = (255, 0, 255)
cyan = (0,255,255)
light_green = (144, 238, 144)
pink = (255,105,180)
dark_green = (100, 190, 100)
light_blue = (135,206,250)
gold = (255, 215, 0)
maya_blue = (79, 214, 255)
bright_green = (102, 255, 0)
brown = (150,75,0)
light_purple = (177, 156, 217)
light_red = (255, 102, 102)
lightish_blue = (153, 153, 255)
canary_yellow = (255, 239, 0)
dark_red = (139,0,0)
light_brown = (181, 101, 29)
tan = (210,180,140)
light_gray = (200, 200, 200)
silver = (192,192,192)
rust = (183,65,14)
yellow_green = (154,205,50)
peach = (255,229,180)
pear = (209,226,49)
dark_grey = (40,40,40)
wood = (193,154,107)
maroon = (123,17,19)
dark_purple = (48,25,52)
white_pink = (171, 39, 79)
deep_purple = (255,0,224)

allegiance_color = {'ImDa': gold,
                    'ImDd': rust,
                    'ImDv': light_red,
                    'ImDs': deep_purple,
                    'ImLa': maya_blue,
                    'ImLc': lightish_blue,
                    'ImSy': red,
                    'ImDc': pink,
                    'ImLu': cyan,
                    'ImDg': green,
                    'ImDi': yellow,
                    'LnRp': cyan,
                    'BlSo': dark_purple,
                    'SoCf': orange,
                    'StCl': maroon,
                    'SeFo': white_pink,
                    'AsOf': dark_red,
                    'FlLe': wood,
                    'ZhIN': blue,
                    'ZhJp': darker_blue,
                    'ZhIa': blue,
                    'VDzF': peach,
                    'MaUn': light_brown,
                    'NaAs': canary_yellow,
                    'NaHu': bright_green,
                    'NaVa': light_purple,
                    'NaXX': light_gray,
                    'JuHl': pear,
                    'JuRu': dark_green,
                    'DaCf': light_green,
                    'SwCf': light_blue,
                    'TrBr': tan,
                    'CsIm': brown,
                    'CsTw': dark_grey,
                    'CsZh': blue,
                    'VAug': yellow_green,
                    'Zh': blue
                    }

hex_code = {'0': 0,
            '1': 1,
            '2': 2,
            '3': 3,
            '4': 4,
            '5': 5,
            '6': 6,
            '7': 7,
            '8': 8,
            '9': 9,
            'A': 10,
            'B': 11,
            'C': 12,
            'D': 13,
            'E': 14,
            'F': 15,
            'G': 16,
            'H': 17,
            'J': 18,
            'K': 19,
            '?': 0
            }

added_sectors = {}

text_rotate_degrees = 45

pygame.init()

screen = pygame.display.set_mode(SCREEN_SIZE, 0, 32)
window_title = __app__
pygame.display.set_caption(window_title)
window_icon = pygame.image.load('images/shonner_die_alpha.png')
pygame.display.set_icon(window_icon)

def _pixel(surface, color, pos):
    pygame.draw.line(surface, color, pos, pos)

def _circle(surface, color, pos, radius, thickness, see_thru=False):
    if see_thru:
        temp_surf = pygame.Surface((radius*2, radius*2))
        temp_surf.fill(TRANSPARENT)
        temp_surf.set_colorkey(TRANSPARENT)
        pygame.draw.circle(temp_surf, (color[0], color[1], color[2], 120), (radius, radius), radius)
        temp_surf.set_alpha(120)
        surface.blit(temp_surf, (pos[0]-radius, pos[1]-radius, radius*2, radius*2))
    else:
        pygame.draw.circle(surface, color, pos, radius, thickness)

def _rectangle(surface, color, coords, thickness, see_thru=False):
    if see_thru:
        temp_surf = pygame.Surface((coords[2], coords[3]))
        temp_surf.fill(TRANSPARENT)
        temp_surf.set_colorkey(TRANSPARENT)
        pygame.draw.rect(temp_surf, (color[0], color[1], color[2], 120), [0, 0, coords[2], coords[3]])
        temp_surf.set_alpha(120)
        surface.blit(temp_surf, (coords[0], coords[1], coords[2], coords[3]))
    else:
        pygame.draw.rect(surface, color, coords, thickness)
    
def _hexagon(surface, color, pos, radius, thickness, see_thru=False):
    n_sides = 6
    step = 360 / n_sides
    angle = 0
    points = []
    for i in range(n_sides):
        if see_thru:
            x = radius + radius*cos(angle*3.14159265359/180)
            y = radius + radius*sin(angle*3.14159265359/180)
        else:
            x = pos[0] + radius*cos(angle*3.14159265359/180)
            y = pos[1] + radius*sin(angle*3.14159265359/180)
        angle += step
        points.append((x,y))
    if see_thru:
        temp_surf = pygame.Surface((radius*2, radius*2))
        temp_surf.fill(TRANSPARENT)
        temp_surf.set_colorkey(TRANSPARENT)
        pygame.draw.polygon(temp_surf, (color[0], color[1], color[2], 120), points)
        temp_surf.set_alpha(120)
        surface.blit(temp_surf, (pos[0]-radius, pos[1]-radius, radius*2, radius*2))
    else:
        pygame.draw.polygon(surface, color, points, thickness)

def display_map(xx=0, yy=0, zoom=1, grid_style='RECT_grid', zone_style='circled', see_thru=False, subxx=0, subyy=0):
    
    log = logging.getLogger('MapGen_0.0.3b.mapper')

    # was information for this program asked for?
    if xx == 'info':
        ver = 'mapper, release version ' + __release__ + ' for Python 2.5.4'
        mapper_log.info('Reporting: mapper release version: %s' % __release__)
        return __version__, ver

    mapper_log.debug('Displaying map at ' + str(zoom) + 'X zoom. Style used = ' + grid_style)

    x_zoom = zoom
    y_zoom = zoom
    
    #print 'xx=%d, yy=%d zoom=%d' % (xx,yy, zoom)
    
    screen.fill(black)
    
    voiced_sector_name = 'BLANK'
    sector_names = []
    sectors_filled = []
    voiced_subector_name = 'BLANK'
    subsector_names = []
    
    if zoom < 8:
        for y in range(ROWS/y_zoom):
            for x in range(COLUMNS/x_zoom):
                
                sectors_filled.append(0)
                
        sect_point = 0   
        
        capitals_list = []
        
        for y in range(ROWS/y_zoom):
            for x in range(COLUMNS/x_zoom):
                if zoom == 1:
                    sector_x = x - COLUMNS/2 + xx
                    sector_y = y - ROWS/2 + 1 - yy
                elif zoom == 2:
                    sector_x = x - COLUMNS/4 + xx
                    sector_y = y - ROWS/4 + 1 - yy
                elif zoom == 4:
                    sector_x = x - 1 + xx
                    sector_y = -yy
                
                sec_filename = 'sec'
                
                if sector_x < 0:
                    sec_filename += '_m'
                else:
                    sec_filename += '_p'
                if sector_x < -9 or sector_x > 9:
                    sec_filename += str(abs(sector_x))
                else:
                    sec_filename += '0' + str(abs(sector_x))
                
                if sector_y < 0:
                    sec_filename += '_m'
                else:
                    sec_filename += '_p'
                if sector_y < -9 or sector_y > 9:
                    sec_filename += str(abs(sector_y))
                else:
                    sec_filename += '0' + str(abs(sector_y))
    
                try:
                    read_line = 0
                    with open('data/' + sec_filename + '.dat', 'r') as sec_file_in:
                        
                        color = gray
                        pygame.draw.rect(screen, color, (x*32*X_SPACING*x_zoom, y*40*Y_SPACING*y_zoom, 32*X_SPACING*x_zoom, 40*Y_SPACING*y_zoom), DOT_SIZE*zoom)
                        
                        
                        
                        for i in range(32):
                            for j in range(40):
                    
                                color = gray
                                
                                if i / 2 == i / 2.0:
                                    if zoom < 4:
                                        _pixel(screen, color, (i*X_SPACING*x_zoom + x*32*X_SPACING*x_zoom, j*Y_SPACING*y_zoom + y*40*Y_SPACING*y_zoom))
                                    else:
                                        #_circle(screen, color, (i*X_SPACING*x_zoom + x*32*X_SPACING*x_zoom, j*Y_SPACING*y_zoom + y*40*Y_SPACING*y_zoom), DOT_SIZE, 0)
                                        if grid_style == 'RECT_grid':
                                            _rectangle(screen, color, [i*X_SPACING*x_zoom + x*32*X_SPACING*x_zoom + 2,
                                                                       j*Y_SPACING*y_zoom + y*40*Y_SPACING*y_zoom + 2,
                                                                       14,
                                                                       15],
                                                                       DOT_SIZE-1)
                                        elif grid_style == 'HEX_grid_20' or grid_style == 'HEX_grid_18':
                                            _hexagon(screen, color, (i*X_SPACING*x_zoom + x*32*X_SPACING*x_zoom + 9,
                                                                     j*Y_SPACING*y_zoom + y*40*Y_SPACING*y_zoom + 9),
                                                                     int(grid_style[9:11])/2,
                                                                     1)
                                else:
                                    if zoom < 4:
                                        _pixel(screen, color, (i*X_SPACING*x_zoom + x*32*X_SPACING*x_zoom, j*Y_SPACING*y_zoom + OFFSET*y_zoom + y*40*Y_SPACING*y_zoom))
                                    else:
                                        #_circle(screen, color, (i*X_SPACING*x_zoom + x*32*X_SPACING*x_zoom, j*Y_SPACING*y_zoom + OFFSET*y_zoom + y*40*Y_SPACING*y_zoom), DOT_SIZE, 0)
                                        if grid_style == 'RECT_grid':
                                            _rectangle(screen, color, [i*X_SPACING*x_zoom + x*32*X_SPACING*x_zoom + 2,
                                                                       j*Y_SPACING*y_zoom + y*40*Y_SPACING*y_zoom + OFFSET*y_zoom + 2,
                                                                       14,
                                                                       15],
                                                                       DOT_SIZE-1)
                                        elif grid_style == 'HEX_grid_20' or grid_style == 'HEX_grid_18':
                                            _hexagon(screen, color, (i*X_SPACING*x_zoom + x*32*X_SPACING*x_zoom + 9,
                                                                     j*Y_SPACING*y_zoom + OFFSET*y_zoom + y*40*Y_SPACING*y_zoom + 9),
                                                                     int(grid_style[9:11])/2,
                                                                     1)
                        
                        for line in sec_file_in:
                            #print line[:len(line)-1]
                            read_line += 1
                            if read_line == 4:
                                sector_name = line[2:len(line)-1]
                                #print sector_x, sector_y, (xx, yy)
                                if sector_x == xx and sector_y == -yy:
                                    voiced_sector_name = sector_name
                                #print sector_name
                                sector_names.append(sector_name)
                                sectors_filled[sect_point] = 1
                                sect_point += 1
                            if read_line == 5:
                                sector_offset = eval(line[2:len(line)-1])
                                #print sector_offset,
                                #print sector_offset[0], -sector_offset[1]
                                added_sectors[sector_name] = (sector_offset[0], -sector_offset[1])
                            if line[:3] == 'Hex':
                                name_tab = line.find('Name')
                                allegiance_tab = line.find('A')
                                world_tab = line.find('UWP')
                                pop_m_tab = line.find('PBG')
                                travel_code_tab = line.find('Z')
                            if line[:1] == '-':
                                allegiance_length = line[allegiance_tab:allegiance_tab+6].find(' ')
                            if line[:1] <> '#' and line[:1] <> '-' and line[:1] <> 'H' and len(line) > 3:
                                if int(line[:4]) > 0:
                                    #print line[allegiance_tab:allegiance_tab+allegiance_length], len(line[allegiance_tab:allegiance_tab+allegiance_length])
                                    if line[allegiance_tab:allegiance_tab+allegiance_length] not in allegiance_color:
                                        color = white
                                    else:
                                        color = allegiance_color[line[allegiance_tab:allegiance_tab+allegiance_length]]
                                        
                                    hex_x=int(line[0:2]) - 1
                                    hex_y=int(line[2:4]) - 1
    
                                    #population = hex_code[line[world_tab+4]] * int(line[pop_m_tab])
                                    population = hex_code[line[world_tab+4]]
                                    world_name = line[name_tab:name_tab+19].strip()
                                    if hex_x / 2 == hex_x / 2.0:
                                        
                                        if world_name == 'Reference' or world_name == 'Capital' or world_name == 'Regina' or world_name == 'Vland' or world_name == 'Terra':
                                            color = yellow
                                            if zoom == 4:
                                                _circle(screen, color, (int(hex_x*X_SPACING*x_zoom + x*32*X_SPACING*x_zoom) + 10 , int(hex_y*Y_SPACING*y_zoom + y*40*Y_SPACING*y_zoom) + 10), 8, 0)
                                                capitals_list.append((world_name, int(hex_x*X_SPACING*x_zoom + x*32*X_SPACING*x_zoom) + 10, int(hex_y*Y_SPACING*y_zoom + y*40*Y_SPACING*y_zoom) + 10))
                                            else:
                                                _circle(screen, color, (int(hex_x*X_SPACING*x_zoom + x*32*X_SPACING*x_zoom), int(hex_y*Y_SPACING*y_zoom + y*40*Y_SPACING*y_zoom)), 8, 0)
                                                capitals_list.append((world_name, int(hex_x*X_SPACING*x_zoom + x*32*X_SPACING*x_zoom), int(hex_y*Y_SPACING*y_zoom + y*40*Y_SPACING*y_zoom)))
    #                                     if color == red or color == amber:
    #                                         _circle(screen, color, (hex_x*X_SPACING*x_zoom + x*32*X_SPACING*x_zoom, hex_y*Y_SPACING*y_zoom + y*40*Y_SPACING*y_zoom), DOT_SIZE*population**.5 + 1, 1)
                                        #color = white
                                        if population < 10:
                                            if zoom == 1:
                                                _pixel(screen, color, (hex_x*X_SPACING*x_zoom + x*32*X_SPACING*x_zoom, hex_y*Y_SPACING*y_zoom + y*40*Y_SPACING*y_zoom))
                                            else:
                                                if zoom == 4:
                                                    if line[travel_code_tab] == 'R':
                                                        zone_color = red
                                                        _circle(screen, zone_color, (int(hex_x*X_SPACING*x_zoom + x*32*X_SPACING*x_zoom) + 10, int(hex_y*Y_SPACING*y_zoom + y*40*Y_SPACING*y_zoom) + 10), int(zoom+2), 1)
                                                    if line[travel_code_tab] == 'A':
                                                        zone_color = amber
                                                        _circle(screen, zone_color, (int(hex_x*X_SPACING*x_zoom + x*32*X_SPACING*x_zoom) + 10, int(hex_y*Y_SPACING*y_zoom + y*40*Y_SPACING*y_zoom) + 10), int(zoom+2), 1)
                                                    _circle(screen, color, (int(hex_x*X_SPACING*x_zoom + x*32*X_SPACING*x_zoom) + 10, int(hex_y*Y_SPACING*y_zoom + y*40*Y_SPACING*y_zoom) + 10), int(zoom), 0)
                                                else:
                                                    _circle(screen, color, (int(hex_x*X_SPACING*x_zoom + x*32*X_SPACING*x_zoom), int(hex_y*Y_SPACING*y_zoom + y*40*Y_SPACING*y_zoom)), 2, 0)
                                        else:
                                            #color = orange
                                            if zoom == 4:
                                                if line[travel_code_tab] == 'R':
                                                    zone_color = red
                                                    _circle(screen, zone_color, (int(hex_x*X_SPACING*x_zoom + x*32*X_SPACING*x_zoom) + 10, int(hex_y*Y_SPACING*y_zoom + y*40*Y_SPACING*y_zoom) + 10), int(zoom+2), 1)
                                                if line[travel_code_tab] == 'A':
                                                    zone_color = amber
                                                    _circle(screen, zone_color, (int(hex_x*X_SPACING*x_zoom + x*32*X_SPACING*x_zoom) + 10, int(hex_y*Y_SPACING*y_zoom + y*40*Y_SPACING*y_zoom) + 10), int(zoom+2), 1)
                                                _circle(screen, color, (int(hex_x*X_SPACING*x_zoom + x*32*X_SPACING*x_zoom) + 10, int(hex_y*Y_SPACING*y_zoom + y*40*Y_SPACING*y_zoom) + 10), int(zoom), 0)
                                            else:
                                                _circle(screen, color, (int(hex_x*X_SPACING*x_zoom + x*32*X_SPACING*x_zoom), int(hex_y*Y_SPACING*y_zoom + y*40*Y_SPACING*y_zoom)), int(zoom*2), 0)
                                    else:
                                        if world_name == 'Reference' or world_name == 'Capital' or world_name == 'Regina' or world_name == 'Vland' or world_name == 'Terra':
                                            color = yellow
                                            if zoom == 4:
                                                _circle(screen, color, (int(hex_x*X_SPACING*x_zoom + x*32*X_SPACING*x_zoom) + 10, int(hex_y*Y_SPACING*y_zoom + OFFSET*y_zoom + y*40*Y_SPACING*y_zoom) + 10), 8, 0)
                                                capitals_list.append((world_name, int(hex_x*X_SPACING*x_zoom + x*32*X_SPACING*x_zoom) + 10, int(hex_y*Y_SPACING*y_zoom + OFFSET*y_zoom + y*40*Y_SPACING*y_zoom) + 10))
                                            else:
                                                _circle(screen, color, (int(hex_x*X_SPACING*x_zoom + x*32*X_SPACING*x_zoom), int(hex_y*Y_SPACING*y_zoom + OFFSET*y_zoom + y*40*Y_SPACING*y_zoom)), 8, 0)
                                                capitals_list.append((world_name, int(hex_x*X_SPACING*x_zoom + x*32*X_SPACING*x_zoom), int(hex_y*Y_SPACING*y_zoom + OFFSET*y_zoom + y*40*Y_SPACING*y_zoom)))
    #                                     if color == red or color == amber:
    #                                         _circle(screen, color, (hex_x*X_SPACING*x_zoom + x*32*X_SPACING*x_zoom, hex_y*Y_SPACING*y_zoom + OFFSET*y_zoom + y*40*Y_SPACING*y_zoom), DOT_SIZE*population**.5 + 1, 1)
                                        #color = white
                                        if population < 10:
                                            if zoom == 1:
                                                _pixel(screen, color, (hex_x*X_SPACING*x_zoom + x*32*X_SPACING*x_zoom, hex_y*Y_SPACING*y_zoom + OFFSET*y_zoom + y*40*Y_SPACING*y_zoom))
                                            else:
                                                if zoom == 4:
                                                    if line[travel_code_tab] == 'R':
                                                        zone_color = red
                                                        _circle(screen, zone_color, (int(hex_x*X_SPACING*x_zoom + x*32*X_SPACING*x_zoom) + 10, int(hex_y*Y_SPACING*y_zoom + OFFSET*y_zoom + y*40*Y_SPACING*y_zoom) + 10), int(zoom+2), 1)
                                                    if line[travel_code_tab] == 'A':
                                                        zone_color = amber
                                                        _circle(screen, zone_color, (int(hex_x*X_SPACING*x_zoom + x*32*X_SPACING*x_zoom) + 10, int(hex_y*Y_SPACING*y_zoom + OFFSET*y_zoom + y*40*Y_SPACING*y_zoom) + 10), int(zoom+2), 1)
                                                    _circle(screen, color, (int(hex_x*X_SPACING*x_zoom + x*32*X_SPACING*x_zoom) + 10, int(hex_y*Y_SPACING*y_zoom + OFFSET*y_zoom + y*40*Y_SPACING*y_zoom) + 10), int(zoom), 0)
                                                else:
                                                    _circle(screen, color, (int(hex_x*X_SPACING*x_zoom + x*32*X_SPACING*x_zoom), int(hex_y*Y_SPACING*y_zoom + OFFSET*y_zoom + y*40*Y_SPACING*y_zoom)), 2, 0)
                                        else:
                                            #color = orange
                                            if zoom == 4:
                                                if line[travel_code_tab] == 'R':
                                                    zone_color = red
                                                    _circle(screen, zone_color, (int(hex_x*X_SPACING*x_zoom + x*32*X_SPACING*x_zoom) + 10, int(hex_y*Y_SPACING*y_zoom + OFFSET*y_zoom + y*40*Y_SPACING*y_zoom) + 10), int(zoom+2), 1)
                                                if line[travel_code_tab] == 'A':
                                                    zone_color = amber
                                                    _circle(screen, zone_color, (int(hex_x*X_SPACING*x_zoom + x*32*X_SPACING*x_zoom) + 10, int(hex_y*Y_SPACING*y_zoom + OFFSET*y_zoom + y*40*Y_SPACING*y_zoom) + 10), int(zoom+2), 1)
                                                _circle(screen, color, (int(hex_x*X_SPACING*x_zoom + x*32*X_SPACING*x_zoom) + 10, int(hex_y*Y_SPACING*y_zoom + OFFSET*y_zoom + y*40*Y_SPACING*y_zoom) + 10), int(zoom), 0)
                                            else:
                                                _circle(screen, color, (int(hex_x*X_SPACING*x_zoom + x*32*X_SPACING*x_zoom), int(hex_y*Y_SPACING*y_zoom + OFFSET*y_zoom + y*40*Y_SPACING*y_zoom)), int(zoom*2), 0)                       
                    
                except IOError:
                    #print 'No ' + sec_filename + '.dat'
                    log.warning("Missing '" + sec_filename + ".dat' file [Warning]")
                    mapper_log.warning("Display Warning! '" + sec_filename + ".dat' is missing.")
                    sect_point += 1

        for i in range(len(capitals_list)):
            world_name_font = pygame.font.SysFont('Eras ITC Demi', 24, False, False)
            world_name_text = world_name_font.render(capitals_list[i][0], True, white)
            screen.blit(world_name_text, [capitals_list[i][1],
                                          capitals_list[i][2]-20])
        #print added_sectors
        #print sector_names
        #print sectors_filled
        saved_sector_list = list(sector_names)
        sector_name_pointer = 0
        
        # rotate sector labels and print them
        sect_point = 0
        for y in range(ROWS/y_zoom):
            for x in range(COLUMNS/x_zoom):
                if sectors_filled[sect_point] == 1:
                    printing = True
                    x_line_spacing = 0
                    y_line_spacing = 0
                    while printing:
                        space_check = sector_names[sector_name_pointer].find(' ')
                        if space_check == -1:
                            font = pygame.font.SysFont('Eras ITC Demi', 26*zoom, False, True)
                            text = font.render(sector_names[sector_name_pointer], True, white)
                            text = pygame.transform.rotate(text, text_rotate_degrees)
                            alpha_img = pygame.Surface(text.get_rect().size, pygame.SRCALPHA)
                            alpha_img.fill((255, 255, 255, 180 + (255-180)/(zoom*3)))
                            text.blit(alpha_img, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                            screen.blit(text, [x*32*X_SPACING*x_zoom + 32*X_SPACING*x_zoom/6 + x_line_spacing, y*40*Y_SPACING*y_zoom + 40*Y_SPACING*y_zoom/6 + y_line_spacing])
                            printing = False
                            sector_name_pointer += 1
                        else:
                            font = pygame.font.SysFont('Eras ITC Demi', 26*zoom, False, True)
                            text = font.render(sector_names[sector_name_pointer][:space_check], True, white)
                            text = pygame.transform.rotate(text, text_rotate_degrees)
                            alpha_img = pygame.Surface(text.get_rect().size, pygame.SRCALPHA)
                            alpha_img.fill((255, 255, 255, 180 + (255-180)/(zoom*3)))
                            text.blit(alpha_img, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                            screen.blit(text, [x*32*X_SPACING*x_zoom + 32*X_SPACING*x_zoom/6 + x_line_spacing, y*40*Y_SPACING*y_zoom + 40*Y_SPACING*y_zoom/6 + y_line_spacing])
                            sector_names[sector_name_pointer] = sector_names[sector_name_pointer][space_check+1:len(sector_names[sector_name_pointer])]
                            x_line_spacing += 20
                            y_line_spacing += 40*zoom
                sect_point += 1
    else:
        #print 'subxx=%d, subyy=%d, zoom-8, style=%s' % (subxx,subyy,grid_style)
        
        for x in range(2):
            
            sec_filename = 'sec'
                
            if xx < 0:
                sec_filename += '_m'
            else:
                sec_filename += '_p'
            if xx < -9 or xx > 9:
                sec_filename += str(abs(xx))
            else:
                sec_filename += '0' + str(abs(xx))
            
            if -yy < 0:
                sec_filename += '_m'
            else:
                sec_filename += '_p'
            if -yy < -9 or -yy > 9:
                sec_filename += str(abs(-yy))
            else:
                sec_filename += '0' + str(abs(-yy))

            try:
                read_line = 0
                with open('data/' + sec_filename + '.dat', 'r') as sec_file_in:
                    
                    color = gray
                    pygame.draw.rect(screen, color, (x*512, 0, 512, 703), DOT_SIZE*2)
                    
                    for i in range(8):
                        for j in range(10):
                            
                            parsec_loc = ''
                            p_column = i + (subxx+x)*8 + 1
                            if p_column < 10:
                                parsec_loc += '0' + str(p_column)
                            else:
                                parsec_loc += str(p_column)
                            p_row = j + subyy*10 + 1
                            if p_row < 10:
                                parsec_loc += '0' + str(p_row)
                            else:
                                parsec_loc += str(p_row)
                                
                            color = gray
                            
                            font = pygame.font.SysFont('Eras ITC Demi', 12, False, False)
                            text = font.render(parsec_loc, True, color)
                            
                            if i / 2 == i / 2.0:
                                if grid_style == 'RECT_grid':
                                    _rectangle(screen, color, [i*64 + 4 + x*512,
                                                               j*70.4 + 4,
                                                               56,
                                                               63],
                                                               DOT_SIZE-1)
                                    screen.blit(text, [i*64 + 22 + x*512,
                                                       j*70.4 + 7])
                                elif grid_style == 'HEX_grid_40':
                                    _hexagon(screen, color, (i*64 + 24 + x*512,
                                                             j*70.4 + 32),
                                                             int(grid_style[9:11]), 1)
                                    screen.blit(text, [i*64 + 14 + x*512,
                                                       j*70.4])
                            else:
                                if grid_style == 'RECT_grid':
                                    _rectangle(screen, color, [i*64 + 4 + x*512,
                                                               j*70.4 + 4 + 36,
                                                               56,
                                                               63],
                                                               DOT_SIZE-1)
                                    screen.blit(text, [i*64 + 22 + x*512,
                                                       j*70.4 + 7 + 36])
                                elif grid_style == 'HEX_grid_40':
                                    _hexagon(screen, color, (i*64 + 24 + x*512,
                                                             j*70.4 + 32 + 36),
                                                             int(grid_style[9:11]), 1)
                                    screen.blit(text, [i*64 + 14 + x*512,
                                                       j*70.4 + 36])
                    
                    subsector_list = []
                    
                    for line in sec_file_in:
                        #print line[:len(line)-1]
                        if line[:11] == '# Subsector':
                            subsector_list.append(line[15:len(line)-1])
                        read_line += 1
                        if read_line == 4:
                            sector_name = line[2:len(line)-1]
                            #print sector_x, sector_y, (xx, yy)
                            #if sector_x == xx and sector_y == -yy:
                            voiced_sector_name = sector_name
                            #print sector_name
                            #sector_names.append(sector_name)
                            #sectors_filled[sect_point] = 1
                            #sect_point += 1
                        if read_line == 5:
                            sector_offset = eval(line[2:len(line)-1])
                            #print sector_offset,
                            #print sector_offset[0], -sector_offset[1]
                            #added_sectors[sector_name] = (sector_offset[0], -sector_offset[1])
                        if line[:3] == 'Hex':
                            name_tab = line.find('Name')
                            remarks_tab = line.find('Remarks')
                            allegiance_tab = line.find('A')
                            world_tab = line.find('UWP')
                            pop_m_tab = line.find('PBG')
                            travel_code_tab = line.find('Z')
                        if line[:1] == '-':
                            allegiance_length = line[allegiance_tab:allegiance_tab+6].find(' ')
                        if line[:1] <> '#' and line[:1] <> '-' and line[:1] <> 'H' and len(line) > 3:
                            if int(line[:4]) > 0:
                                #print line[allegiance_tab:allegiance_tab+allegiance_length], len(line[allegiance_tab:allegiance_tab+allegiance_length])
                                if line[allegiance_tab:allegiance_tab+allegiance_length] not in allegiance_color:
                                    color = white
                                else:
                                    color = allegiance_color[line[allegiance_tab:allegiance_tab+allegiance_length]]
                                    
                                hex_x=int(line[0:2])
                                hex_y=int(line[2:4])
                                #print hex_x, hex_y
                                if hex_x > (subxx+x)*8 and hex_x <= (subxx+x)*8+8 and hex_y > subyy*10 and hex_y <= subyy*10+10:
                                    
                                    
                                    temp_x = hex_x - 8*(subxx+x)
                                    temp_y = hex_y - 10*subyy
                                    
                                    #population = hex_code[line[world_tab+4]] * int(line[pop_m_tab])
                                    population = hex_code[line[world_tab+4]]
                                    world_name = line[name_tab:name_tab+19].strip()
                                    world_name_color = white
                                    if 'Cx' in line[remarks_tab:remarks_tab+20] or 'Cp' in line[remarks_tab:remarks_tab+20]:
                                        world_name_color = red
                                    if population >= 10:
                                        world_name = world_name.upper()
                                    world_name_font = pygame.font.SysFont('Eras ITC Demi', 18, False, False)
                                    world_name_text = world_name_font.render(world_name, True, world_name_color)
                                    world_uwp_font = pygame.font.SysFont('OCR A Extended', 10, False, False)
                                    world_uwp_text = world_uwp_font.render(line[world_tab:world_tab+9], True, white)
                                    if hex_x / 2 == hex_x / 2.0:
                                        if grid_style == 'RECT_grid':
                                            if line[travel_code_tab] == 'R' or line[travel_code_tab] == 'A':
                                                if line[travel_code_tab] == 'R':
                                                    zone_color = red
                                                if line[travel_code_tab] == 'A':
                                                    zone_color = amber
                                                if zone_style == 'circled':
                                                    _circle(screen, zone_color, (int((temp_x-1)*64 + 33 + x*512),
                                                                                 int((temp_y-1)*70.4) + 70),
                                                                                 int(zoom*2.5),
                                                                                 1,
                                                                                 see_thru)
                                                else:
                                                    _rectangle(screen, zone_color, [(temp_x-1)*64 + 4 + x*512,
                                                                                    (temp_y-1)*70.4 + 40,
                                                                                    56,
                                                                                    63],
                                                                                    DOT_SIZE-1,
                                                                                    see_thru)
                                            
                                            _circle(screen, color, (int((temp_x-1)*64 + 33 + x*512),
                                                                    int((temp_y-1)*70.4) + 70),
                                                                    int(zoom), 0)
                                            
                                            screen.blit(world_name_text, [int((temp_x-1)*64 + 32 - len(world_name)*7/2 + x*512),
                                                                          int((temp_y-1)*70.4) + 46])
                                            screen.blit(world_uwp_text, [int((temp_x-1)*64 + 30 - 25 + x*512),
                                                                         int((temp_y-1)*70.4) + 86])
                                        elif grid_style == 'HEX_grid_40':
#                                         if world_name == 'Reference' or world_name == 'Capital' or world_name == 'Regina' or world_name == 'Vland' or world_name == 'Terra':
#                                             color = yellow
#                                             _circle(screen, color, (int(hex_x*X_SPACING*x_zoom + subxx*32*X_SPACING*x_zoom), int(hex_y*Y_SPACING*y_zoom + subyy*40*Y_SPACING*y_zoom)), 8, 0)

                                            if line[travel_code_tab] == 'R' or line[travel_code_tab] == 'A':
                                                if line[travel_code_tab] == 'R':
                                                    zone_color = red
                                                if line[travel_code_tab] == 'A':
                                                    zone_color = amber
                                                if zone_style == 'circled':
                                                    _circle(screen, zone_color, (int((temp_x-1)*64 + 24 + x*512),
                                                                                 int((temp_y-1)*70.4) + 67),
                                                                                 int(zoom*2.5),
                                                                                 1,
                                                                                 see_thru)
                                                else:
                                                    _hexagon(screen, zone_color, (int((temp_x-1)*64 + 24 + x*512),
                                                                                  int((temp_y-1)*70.4) + 67),
                                                                                  int(grid_style[9:11]),
                                                                                  1,
                                                                                  see_thru)
                                                             
                                            _circle(screen, color, (int((temp_x-1)*64 + 24 + x*512),
                                                                    int((temp_y-1)*70.4) + 67),
                                                                    int(zoom), 0)
    
                                            screen.blit(world_name_text, [int((temp_x-1)*64 + 24 - len(world_name)*7/2 + x*512),
                                                                          int((temp_y-1)*70.4) + 46])
                                            screen.blit(world_uwp_text, [int((temp_x-1)*64 + 24 - 25 + x*512),
                                                                         int((temp_y-1)*70.4) + 86])
                                        
                                    else:
                                        if grid_style == 'RECT_grid':
                                            if line[travel_code_tab] == 'R' or line[travel_code_tab] == 'A':
                                                if line[travel_code_tab] == 'R':
                                                    zone_color = red
                                                if line[travel_code_tab] == 'A':
                                                    zone_color = amber
                                                if zone_style == 'circled':
                                                    _circle(screen, zone_color, (int((temp_x-1)*64 + 33 + x*512),
                                                                                 int((temp_y-1)*70.4) + 37),
                                                                                 int(zoom*2.5),
                                                                                 1,
                                                                                 see_thru)
                                                else:
                                                    _rectangle(screen, zone_color, [(temp_x-1)*64 + 4 + x*512,
                                                                                    (temp_y-1)*70.4 + 4,
                                                                                    56,
                                                                                    63],
                                                                                    DOT_SIZE-1,
                                                                                    see_thru)
                                            
                                            _circle(screen, color, (int((temp_x-1)*64 + 33 + x*512),
                                                                    int((temp_y-1)*70.4) + 37),
                                                                    int(zoom), 0)
                                            
                                            screen.blit(world_name_text, [int((temp_x-1)*64 + 32 - len(world_name)*7/2 + x*512),
                                                                          int((temp_y-1)*70.4) + 12])
                                            screen.blit(world_uwp_text, [int((temp_x-1)*64 + 30 - 25 + x*512),
                                                                         int((temp_y-1)*70.4) + 52])
                                        elif grid_style == 'HEX_grid_40':
#                                         if world_name == 'Reference' or world_name == 'Capital' or world_name == 'Regina' or world_name == 'Vland' or world_name == 'Terra':
#                                             color = yellow
#                                             _circle(screen, color, (int(hex_x*X_SPACING*x_zoom + subxx*32*X_SPACING*x_zoom), int(hex_y*Y_SPACING*y_zoom + OFFSET*y_zoom + subyy*40*Y_SPACING*y_zoom)), 8, 0)

                                        
                                            if line[travel_code_tab] == 'R' or line[travel_code_tab] == 'A':
                                                if line[travel_code_tab] == 'R':
                                                    zone_color = red
                                                if line[travel_code_tab] == 'A':
                                                    zone_color = amber
                                                if zone_style == 'circled':
                                                    _circle(screen, zone_color, (int((temp_x-1)*64 + 24 + x*512),
                                                                                 int((temp_y-1)*70.4) + 33),
                                                                                 int(zoom*2.5),
                                                                                 1,
                                                                                 see_thru)
                                                else:
                                                    _hexagon(screen, zone_color, (int((temp_x-1)*64 + 24 + x*512),
                                                                                  int((temp_y-1)*70.4) + 32),
                                                                                  int(grid_style[9:11]),
                                                                                  1,
                                                                                  see_thru)
                                            
                                            _circle(screen, color, (int((temp_x-1)*64 + 24 + x*512),
                                                                    int((temp_y-1)*70.4) + 33),
                                                                    int(zoom), 0)
                                        
                                            screen.blit(world_name_text, [int((temp_x-1)*64 + 24 - len(world_name)*7/2 + x*512),
                                                                          int((temp_y-1)*70.4) + 12])
                                            screen.blit(world_uwp_text, [int((temp_x-1)*64 + 24 - 25 + x*512),
                                                                         int((temp_y-1)*70.4) + 52])
                    
                    #print subsector_list
                    #print subsector_list[subxx + subyy*4], subsector_list[subxx+1 + subyy*4]
                    subsector_names = []
                    subsector_names.append(subsector_list[subxx + subyy*4])
                    subsector_names.append(subsector_list[subxx+1 + subyy*4])
                    #print subsector_names
                    
                                            
            except IOError:
                #print 'No ' + sec_filename + '.dat'
                log.warning("Missing '" + sec_filename + ".dat' file for viewing subsectors [Warning]")
                mapper_log.warning("Subsector Display Warning! '" + sec_filename + ".dat' is missing.")
        
        
        
        
        
    pygame.display.update()
    
    if zoom == 1:
        return voiced_sector_name
    elif zoom == 4:
        return saved_sector_list
    elif zoom == 8:
        return subsector_names
    else:
        return 'RESERVED'