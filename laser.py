'''
Author: Honglin Shi and Sangchu Quan
Honglin shi finished the read_bff function
Sangchu Quan finished the output_solution function
We cooperate to finish the rest of the project.
'''
import re


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
            # print(x)
            # print(y)
            # print(d_x)
            # print(d_y)
            if flag == 'L' or flag == 'R':
                d_x = -1 * d_x
                d_y = d_y
            if flag == 'U' or flag == 'D':
                d_x = d_x
                d_y = -1 * d_y
        elif block in blocks['C']:
            path_after_refract = laser_path(
                (x + d_x, y + d_y), (d_x, d_y), x_dimension, y_dimension, blocks)
            if flag == 'L' or flag == 'R':
                d_x = -1 * d_x
                d_y = d_y
            if flag == 'U' or flag == 'D':
                d_x = d_x
                d_y = -1 * d_y

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


if __name__ == '__main__':
    filename = input('Please enter the filename you want to solve: ')
    Read = read_bff(filename)
    GRID = Read[0]
    blocks = Read[1]
    lasers = Read[2]
    points_position = Read[3]

    blocks = {}
    blocks['A'] = [(1, 5), (7, 3)]
    blocks['B'] = []
    blocks['C'] = [(5, 1)]
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
    print(check_answer(points_position, PATH))
    if check_answer(points_position, PATH) is True:
        answer = blocks
