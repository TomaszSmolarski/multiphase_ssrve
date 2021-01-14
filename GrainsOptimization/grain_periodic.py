class GrainPeriodic:
    def __init__(self, height, width, periodic):
        self.height = height
        self.width = width
        self.periodic_type_f = self.period_grid if periodic else self.not_period_grid

    def __neighbourhood_type_list(self, row, col, period_f):
        neighbourhood_list = [period_f(row - 1, col - 1),
                              period_f(row - 1, col),
                              period_f(row - 1, col + 1),
                              period_f(row + 1, col - 1),
                              period_f(row + 1, col),
                              period_f(row + 1, col + 1),
                              period_f(row, col - 1),
                              period_f(row, col + 1)]
        return neighbourhood_list

    def neighbours_colors_list(self, ssrve, neighbours_list):
        return [ssrve[row][col] for row, col in neighbours_list]

    def __period_points(self, check_row, check_col):
        check_row = self.height + check_row if check_row < 0 else check_row % self.height
        check_col = self.width + check_col if check_col < 0 else check_col % self.width
        return check_row, check_col

    def __not_period_points(self, check_row, check_col):
        check_row = check_row if 0 <= check_row < self.height else -1
        check_col = check_col if 0 <= check_col < self.width else -1
        return check_row, check_col

    # periodic type functions
    def period_grid(self, check_row, check_col):
        return self.__neighbourhood_type_list(check_row, check_col, self.__period_points)

    def not_period_grid(self, check_row, check_col):
        neighbours_list = self.__neighbourhood_type_list(check_row, check_col, self.__not_period_points)
        return [(row, col) for row, col in neighbours_list if row != -1 and col != -1]


'''
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

'''
