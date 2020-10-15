def not_period_splines(x_size, y_size, base_x, base_y):
    x = [x_el if x_size > x_el >= 0
         else -1 if x_el < 0
    else x_size for x_el in base_x]

    y = [y_el if y_size > y_el >= 0
         else -1 if y_el < 0
    else y_size for y_el in base_y]

    return [x], [y]


def period_splines(x_size, y_size, base_x, base_y):
    # there is 8 regions around the picture (4 is regular region)
    # 0 | 1 | 2
    # ---------
    # 3 | 4 | 5
    # ---------
    # 6 | 7 | 8

    x = [[] for i in range(9)]
    y = [[] for i in range(9)]

    np_x, np_y = not_period_splines(x_size, y_size, base_x, base_y)
    x[4] = np_x[0]
    y[4] = np_y[0]

    for x_el, y_el in zip(base_x, base_y):
        if not x_size > x_el >= 0 or not y_size > y_el >= 0:
            if x_size > x_el >= 0 and y_el >= y_size:
                x[1].append(x_el)
                y[1].append(y_el % y_size)
                x[1].append(x_el)
                y[1].append(-1)

            elif x_size > x_el >= 0 and y_el < 0:
                x[7].append(x_el)
                y[7].append(y_size + y_el)
                x[7].append(x_el)
                y[7].append(y_size)

            elif y_size > y_el >= 0 and x_el >= x_size:
                x[5].append(x_el % x_size)
                y[5].append(y_el)
                x[5].append(-1)
                y[5].append(y_el)
            elif y_size > y_el >= 0 and x_el < 0:
                x[3].append(x_size + x_el)
                y[3].append(y_el)
                x[3].append(x_size)
                y[3].append(y_el)
            elif x_el < 0 and y_el < 0:
                x[6].append(x_size + x_el)
                y[6].append(y_size + y_el)
                x[6].append(x_size)
                y[6].append(y_size)
            elif x_el >= x_size and y_el >= y_size:
                x[2].append(x_el % x_size)
                y[2].append(y_el % y_size)
                x[2].append(-1)
                y[2].append(-1)
            elif x_el < 0 and y_el >= y_size:
                x[0].append(x_size + x_el)
                y[0].append(y_el % y_size)
                x[0].append(x_size)
                y[0].append(-1)
            elif x_el >= x_size and y_el < 0:
                x[8].append(x_el % x_size)
                y[8].append(y_size + y_el)
                x[8].append(-1)
                y[8].append(y_size)
    return x, y
