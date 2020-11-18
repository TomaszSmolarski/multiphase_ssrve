
def neighbourhood_type_list(row, col, height, width, period_f):
    neighbourhood_list = []
    neighbourhood_list.append(period_f(row - 1, col - 1, height, width))
    neighbourhood_list.append(period_f(row - 1, col, height, width))
    neighbourhood_list.append(period_f(row - 1, col + 1, height, width))

    neighbourhood_list.append(period_f(row + 1, col - 1, height, width))
    neighbourhood_list.append(period_f(row + 1, col, height, width))
    neighbourhood_list.append(period_f(row + 1, col + 1, height, width))

    neighbourhood_list.append(period_f(row, col - 1, height, width))
    neighbourhood_list.append(period_f(row, col + 1, height, width))
    return neighbourhood_list


def neighbours_colors_list(ssrve, neighbours_list):
    return [ssrve[row][col] for row,col in neighbours_list]


def period_points(check_row, check_col, height, width):
    check_row = height + check_row if check_row < 0 else check_row % height
    check_col = width + check_col if check_col < 0 else check_col % width
    return check_row, check_col


def not_period_points(check_row, check_col, height, width):
    check_row = check_row if 0 <= check_row < height else -1
    check_col = check_col if 0 <= check_col < width else -1
    return check_row, check_col


# periodic type functions
def period_grid(check_row, check_col, height, width):
    return neighbourhood_type_list(check_row, check_col, height, width, period_points)


def not_period_grid(check_row, check_col, height, width):
    neighbours_list = neighbourhood_type_list(check_row, check_col, height, width, not_period_points)
    return [(row,col) for row, col in neighbours_list if row!=-1 and col!=-1]




