'''
Author: Honglin Shi and Sangchu Quan
Honglin shi finished the read_bff function
Sangchu Quan finished the output_solution function
We cooperate to finish the rest of the project.
'''
import re
import itertools

class where_to_move():

    def __init__(self, Flag, x_direction, y_direction):
        self.Flag = Flag
        self.x_direction = x_direction
        self.y_direction = y_direction

    def __reflect__(self):
        if self.Flag == 'L' or self.Flag == 'R':
            new_x_direction = self.x_direction * -1
            new_y_direction = self.y_direction
        if self.Flag == 'U' or self.Flag == 'D':
            new_x_direction = self.x_direction
            new_y_direction = self.y_direction * -1
        return (new_x_direction, new_y_direction)

    def __refract__(self):
        if self.Flag == 'L' or self.Flag == 'R':
            new_x_direction = self.x_direction * -1
            new_y_direction = self.y_direction
        if self.Flag == 'U' or self.Flag == 'D':
            new_x_direction = self.x_direction
            new_y_direction = self.y_direction * -1
        return (new_x_direction, new_y_direction)

def read_bff(filename):
    '''
    Read bff files and turn it to a list representing grid, and two
    dictionaries including information about lasers and available blocks

    **Parameters**

        filename: *str*
            The name of bff file

    **Returns**

        GRID: *list*
            A 2D list representing the layout of grid
            0 represent gaps
            1 represent an allowed position for block
            2 represent reflect block
            3 represent opaque block
            4 represent refract block
            5 represent a position can not place block
            6 represent the points that need laser to intersect

        blocks: *dictionary*
            a dictionary includes how many and what kind of block we can use

        lasers: *dictionary*
            a dictionary includes the position and direction of lasers

        points_position: *list*
            a list that contains all the points we need to pass

    '''
    # ensure filename
    if ".bff" in filename:
        filename = filename.split(".bff")[0]
    bff = open(filename + ".bff")

    # read file and find the grid part
    content = bff.read()
    pattern = 'GRID START.*GRID STOP'
    grid = re.search(pattern, content, re.DOTALL)
    grid_text = content[grid.start():grid.end()]
    bff.close()

    # calculate the size of our grid
    rows = 0
    columns = 0

    # find one line of grid, calculate how many columns we need
    row = re.search('([oxABC] *)+[oxABC]', content)
    row = content[row.start():row.end()]
    for i in row:
        if i == 'o' or i == 'x' or i == 'A' or i == 'B' or i == 'C':
            columns += 1

    # creat a list and make each line of grid a element
    # to calculate the number of rows
    Rows = grid_text.split('\n')
    Rows.remove('GRID START')
    Rows.remove('GRID STOP')
    rows = len(Rows)

    # creat the 2d list
    GRID = [
        [0 for i in range(2 * columns + 1)]
        for j in range(2 * rows + 1)
    ]

    # change the number of responding position
    a = -1
    for i in Rows:
        a += 1
        k = 0
        for j in i:
            if j == 'o':
                k += 1
                GRID[2 * a + 1][2 * k - 1] = 1
            if j == 'A':
                k += 1
                GRID[2 * a + 1][2 * k - 1] = 2
            if j == 'B':
                k += 1
                GRID[2 * a + 1][2 * k - 1] = 3
            if j == 'C':
                k += 1
                GRID[2 * a + 1][2 * k - 1] = 4
            if j == 'x':
                k += 1
                GRID[2 * a + 1][2 * k - 1] = 5

    # obtain the points information of bff files
    # store them to a list and change their position
    # number to 6
    points = re.findall('P \\d \\d', content)
    points_position = []
    for i in points:
        position = i.split(' ')
        x_coord = int(position[1])
        y_coord = int(position[2])
        points_position.append((x_coord, y_coord))
        # GRID[y_coord][x_coord] = 6

    # obtain the lasers information of bff files
    # and combine them to a dictionary
    lasers = {}
    laser = re.findall('L \\d \\d .*\\d .*\\d', content)
    p = []
    d = []
    for i in laser:
        info = i.split(' ')
        x_coord = int(info[1])
        y_coord = int(info[2])
        p.append((x_coord, y_coord))
        lasers['position'] = p
        x_dir = int(info[3])
        y_dir = int(info[4])
        d.append((x_dir, y_dir))
        lasers['direction'] = d

    # obtian the blocks information of bff files
    # and combine them to a dictionary
    blocks = {}
    block = re.findall('[ABC] \\d', content)
    for i in block:
        information = i.split(' ')
        blocks[information[0]] = int(information[1])

    return (GRID, blocks, lasers, points_position)


def pos_chk(x, y, x_dimension, y_dimension):
    '''
    Validate if the coordinates specified (x and y) are within the grid.

    **Parameters**

        x: *int*
            An x coordinate to check if it resides within the grid.
        y: *int*
            A y coordinate to check if it resides within the grid.
        x_dimension: *int*
            The boundary of x direction
        y_dimension: *int*
            The boundary of y direction

    **Returns**

        valid: *bool*
            Whether the coordiantes are valid (True) or not (True).
    '''
    if x > 0 and x < x_dimension and y > 0 and y < y_dimension:
        return True

def all_spread_out_cases(the_mad_output):
    '''
    This Function is to generate all the possible but not same cases of
    positions for all required blocks, including illegal position of 
    blocks.
    
    **Parameters**

        the_mad_out_put: *dict*
            A return value of read_bff, which contains required
            number of blocks. And number of each type of blocks.

    **Returns**

        valid: *list*
            Return a list containing each possible blocks position
            combinations, which is saved as dict. So this is a list
            of many dicts.
    '''
    point_list = the_mad_output[0]
    # Give the initial value of numbers of blocks.
    reflect_block_num = 0
    refract_block_num = 0
    opaque_block_num = 0
    illegal_position_num = 0
    # Set up each lists for each type of blocks.
    reflect_block_list = []
    refract_block_list = []
    opaque_block_list = []
    illegal_position_list = []
    all_block_list = []
    exsited_opaque = []
    exsited_refract = []
    exsited_reflect = []
    exsited_illegal = []
    # Prepare the output list and dict in the list.
    output_list = []
    output_dic = {}
    # Read the existing blocks.
    for i in range(0, len(the_mad_output[0]) - 1):
        for j in the_mad_output[0][i]:
            if j == 3:
                exsited_opaque.append([j, i])
                illegal_position_list.append([j, i])
            if j == 2:
                exsited_reflect.append([j, i])
                illegal_position_list.append([j, i])
            if j == 4:
                exsited_refract.append([j, i])
                illegal_position_list.append([j, i])
            if j == 5:
                exsited_illegal.append([j, i])
                illegal_position_list.append([j, i])
    # Read the return value from read_bff, which gives
    # the number of each types of blocks. And the 
    # illegal positions.
    for i in the_mad_output[1].keys():
        k = 0
        if i == 'A':
            reflect_block_num = the_mad_output[1]['A'] + reflect_block_num
            while k < reflect_block_num:
                reflect_block_list.append([1, 1])
                all_block_list.append([1, 1])
                k += 1
        elif i == 'C':
            refract_block_num = the_mad_output[1]['C'] + refract_block_num
            while k < refract_block_num:
                refract_block_list.append([1, 1])
                all_block_list.append([1, 1])
                k += 1
        elif i == 'B':
            opaque_block_num = the_mad_output[1]['B'] + opaque_block_num
            while k < opaque_block_num:
                opaque_block_list.append([1, 1])
                all_block_list.append([1, 1])
                k += 1
        elif i == 'x':
            illegal_position_num += 1
            while k < illegal_position_num:
                illegal_position_list.append([1, 1])
                k += 1
    # Specify where is the boundary of the grid
    x_dimension = len(the_mad_output[0][0])
    y_dimension = len(the_mad_output[0])
    reflect_block_list.append([1, 1])
    # A list containg all the coordinate of the grid.
    alist = []
    # fill the list.
    for i in range(1, x_dimension - 1, 2):
        for j in range(1, y_dimension - 1, 2):
            for k in illegal_position_list:
                if [i, j] == k:
                    pass
            else:
                alist.append([i, j])
    # Do the combination for x times, where x is the number
    # of all the required blocks. Pick up value from 
    # coordinate list, and make combination for which one
    # is reflect and which one is refract and so on.
    for i in itertools.permutations(alist, len(all_block_list)):
        output_dic = {}
        if opaque_block_num >= 1:
            list_of_opaque = []
            # Do not go beyond the length of len(i)
            for k in range(0, opaque_block_num):
                # make a list of the specified type
                # of block, which is the value in the 
                # output_dic
                list_of_opaque.append(tuple(i[k]))
            list_of_opaque.extend(exsited_opaque)
            output_dic['B'] = list_of_opaque
        else:
            output_dic['B'] = exsited_opaque[:]
        if refract_block_num >= 1:
            list_of_refract = []
            # Do not go beyond the length of len(i)
            for k in range(opaque_block_num, refract_block_num + opaque_block_num):
                list_of_refract.append(tuple(i[k]))
            list_of_refract.extend(exsited_refract)
            output_dic['C'] = list_of_refract
        else:
            output_dic['C'] = exsited_refract[:]
        if reflect_block_num >= 1:
            list_of_reflect = []
            # Do not go beyond the length of len(i)
            for k in range(refract_block_num + opaque_block_num, reflect_block_num + refract_block_num + opaque_block_num):
                list_of_reflect.append(tuple(i[k]))
            list_of_reflect.extend(exsited_reflect)
            output_dic['A'] = list_of_reflect
        else:
            output_dic['A'] = exsited_reflect[:]
        # put the dicts into the output_list, which is 
        # the return value
        output_list.append(output_dic)
    return output_list

def laser_path(laser_position, laser_direction, x_dimension, y_dimension, blocks):
    '''
    For a given grid, find and record the laser path.

    **Parameter**

        laser position: *tuple*
            A tuple recording the coordinates of lasers
        laser_direction: *tuple*
            A tuple recording the initial direction of lasers
        x_dimension: *int*
            The boundary of x direction
        y_dimension: *int*
            The boundary of y direction

    **Returns**

        path: *list*
            A list of all coordinates that lasers passes between
            two adjacent blocks.
    '''
    # extract the coordinate and direction of x and y direction.
    x = laser_position[0]
    y = laser_position[1]
    d_x = laser_direction[0]
    d_y = laser_direction[1]

    # use path_after_refract list to store the laser coordinate
    # after laser directly traverse the refract block,
    # use path list to store other coordinates.
    path = []
    path.append((x, y))
    path_after_refract = []

    # use present laser coordinate to predict which block this
    # laser will traverse in the next step. If the laser was stucked
    # at the first place, end the process.
    if x % 2 == 0:
        if d_x == 1:
            block_x = x + 1
            block_y = y
            flag = 'R'
        if d_x == -1:
            block_x = x - 1
            block_y = y
            flag = 'L'
        if (x - 1, y) in blocks['A'] and (x + 1, y) in blocks['A']:
            return path
    else:
        if d_y == 1:
            block_x = x
            block_y = y + 1
            flag = 'D'
        if d_y == -1:
            block_x = x
            block_y = y + 1
            flag = 'U'
        if (x, y - 1) in blocks['A'] and (x, y + 1) in blocks['A']:
            return path
    block = (block_x, block_y)

    # if laser will traverse nothing in next step, make a step forward
    # if the laser traverse the opaque block, end the process.
    # if the laser traverse the reflect block, change one direction
    # if the laser traverse the refract block, make a step forward
    # and also do the same thing as the reflect block. If so, we will
    # have one more laser in the grid, and also follow the rules stated
    # above
    while pos_chk(block[0], block[1], x_dimension, y_dimension):
        # print(block)
        # print((7,3) in blocks['A'])
        if block in blocks['B']:
            return path
        elif block in blocks['A']:
            reflect_move = where_to_move(flag, d_x, d_y)
            d_x = where_to_move(flag, d_x, d_y).__reflect__()[0]
            d_y = where_to_move(flag, d_x, d_y).__reflect__()[1]
        elif block in blocks['C']:
            path_after_refract = laser_path(
                (x + d_x, y + d_y), (d_x, d_y), x_dimension, y_dimension, blocks)
            refract_move = where_to_move(flag, d_x, d_y)
            d_x = where_to_move(flag, d_x, d_y).__refract__()[0]
            d_y = where_to_move(flag, d_x, d_y).__refract__()[1]

        # calculate the next laser and block coordinates.
        x = x + d_x
        y = y + d_y
        if x % 2 == 0:
            if d_x == 1:
                block_x = x + 1
                block_y = y
                flag = 'R'
            if d_x == -1:
                block_x = x - 1
                block_y = y
                flag = 'L'
        else:
            if d_y == 1:
                block_x = x
                block_y = y + 1
                flag = 'D'
            if d_y == -1:
                block_x = x
                block_y = y - 1
                flag = 'U'
        block = (block_x, block_y)
        path.append((x, y))

    # merge the path list and the path_after_refract list together.
    path = list(set(path).union(set(path_after_refract)))
    return path


def check_answer(points_position, PATH):
    '''
    Check if all target points in the laser path

    **Parameter**

        points_position: *list*
            A list containing all coordinates of target points
        PATH: *list*
            A list containing all coordinates on the laser path
            in a specific grid

    **Returns**
        valid: *bool*
        whether this grid will solve the puzzle

    '''

    times = 0
    for i in points_position:
        # print('i',i)
        for j in PATH:
            # print('j',j)
            if i in j:
                times += 1
    if len(points_position) == times:
        return True
    else:
        return False
    
def output_solution(answer, GRID, filename):
    for i in answer['A']:
        x = i[0]
        y = i[1]
        GRID[y][x] = 2
    for j in answer['B']:
        x = j[0]
        y = j[1]
        GRID[y][x] = 3
    for k in answer['C']:
        x = k[0]
        y = k[1]
        GRID[y][x] = 4
    for m in GRID:
        if 1 in m:
            continue
        else:
            GRID.remove(m)
    for n in GRID:
        for o in n:
            if o == 0:
                n.remove(o)
    for o in range(len(GRID)):
        for p in range(len(GRID[o])):
            if GRID[o][p] == 1:
                GRID[o][p] = 'o'
            elif GRID[o][p] == 2:
                GRID[o][p] = 'A'
            elif GRID[o][p] == 3:
                GRID[o][p] = 'B'
            elif GRID[o][p] == 4:
                GRID[o][p] = 'C'
            elif GRID[o][p] == 5:
            	GRID[o][p] = 'x'
    solution = open(filename + ' solution.txt', 'w')
    text = 'The solution for ' + filename + ' is: \n'
    solution.write(text)
    for q in GRID:
        text = " ".join(q)
        solution.write(text + '\n')
    solution.close
    
    
if __name__ == '__main__':
    filename = input('Please enter the filename you want to solve: ')
    Read = read_bff(filename)
    GRID = Read[0]
    blocks = Read[1]
    lasers = Read[2]
    points_position = Read[3]
    for i in all_spread_out_cases(Read):
        blocks = i
        PATH = []
        for j in range(len(lasers['position'])):
            laser_position = lasers['position'][j]
            laser_direction = lasers['direction'][j]
            # print(laser_position)
            x_dimension = len(GRID[0]) - 1
            y_dimension = len(GRID) - 1
            # print(y_dimension)
            path = laser_path(laser_position, laser_direction,
                              x_dimension, y_dimension, blocks)
            PATH.append(path)
        # print(PATH)
        #print(check_answer(points_position, PATH))
        if check_answer(points_position, PATH) is True:
            answer = blocks
            output_solution(answer, GRID, filename)
            break
