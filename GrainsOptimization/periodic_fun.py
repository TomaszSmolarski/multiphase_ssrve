def period_color(ssrve, check_row, check_col, height, width):
    check_row = height + check_row if check_row < 0 else check_row % height
    check_col = width + check_col if check_col < 0 else check_col % width
    return ssrve[check_row][check_col]


def period_points(check_row, check_col, height, width):
    check_row = height + check_row if check_row < 0 else check_row % height
    check_col = width + check_col if check_col < 0 else check_col % width
    return check_row, check_col
