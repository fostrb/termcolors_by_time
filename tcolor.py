import datetime
from itertools import tee


# main color determined by sky color
# secondary colors determined by current sky accents (stars, clouds, etc)

# month      color season
# date       season primary color based gradient

# hour      based on time of day (and season daylight)
# minute    hour primary color based gradient


#
# Twilight angles (degrees below horizon)
# Astro      :12-18
# Nautical   :6-12
# Civil      :< 6

# Dawn Angles (Degrees below horizon)
# Astro      :18
# Nautical   :12
# Civil      :6

# Dusk Angles (Degrees below horizon [evening])
# Astro      :12-18
# Nautical   :6-12
# Civil      :<6

td = {
    0: [0, 89, 179],
    1: [51, 102, 255],
    2: [0, 64, 255],
    3: [89, 0, 179],
    4: [136, 77, 255],
    5: [179, 0, 179],
    6: [204, 82, 0],
    7: [204, 136, 0],
    8: [102, 204, 0],
    9: [0, 255, 153],
    10: [0, 204, 0],
    11: [0, 255, 255],
    12: [255, 255, 255],
    13: [255, 255, 51],
    14: [102, 255, 102],
    15: [255, 128, 0],
    16: [0, 153, 255],
    17: [179, 0, 134],
    18: [204, 0, 68],
    19: [153, 102, 255],
    20: [51, 153, 255],
    21: [0, 119, 179],
    22: [0, 153, 153],
    23: [153, 51, 153],
}


def print_colored(ansi_color, text):
    cmd = '''\x1b[38;5;''' + str(ansi_color) + '''m'''
    print(cmd + str(text))


def get_color_string(ansi_color, text):
    cmd = '''\x1b[38;5;''' + str(ansi_color) + '''m'''
    return str(cmd + str(text))


def convert_to_256(rgb_color):
    r = rgb_color[0]
    g = rgb_color[1]
    b = rgb_color[2]

    if r == g == b:
        if r < 8:
            return 16
        if r > 248:
            return 231
        return (((r-8)/247)*24)+232

    r = int((r * 5) / 255)
    g = int((g * 5) / 255)
    b = int((b * 5) / 255)
    # print(r, g, b)
    ansi = 16 + 36 * r + 6 * g + b
    return ansi


def poly_gradient(colors, steps, components=3):
    def linear_gradient(start, finish, sub_steps):
        yield start
        for i in range(1, sub_steps):
            yield tuple([(start[j] + (float(i) / (sub_steps - 1)) * (finish[j] - start[j])) for j in range(components)])

    def pairs(seq):
        a, b = tee(seq)
        next(b, None)
        return zip(a, b)

    sub_sub_steps = int(float(steps)/(len(colors)-1))

    for a, b in pairs(colors):
        for c in linear_gradient(a, b, sub_sub_steps):
            yield c


def print_gradient():
    for time, color in td.items():
        next_color = td[0]
        if not time == 23:
            next_color = td[time+1]
        grad = poly_gradient([color, next_color], 60)
        for each in grad:
            ansi_color = convert_to_256(each)
            s = get_color_string(ansi_color, '.')
            print(s, end='')
        print()


def get_color_by_time():
    now = datetime.datetime.now()
    h = now.hour
    m = now.minute
    nexth = 0
    if h != 23:
        nexth = h+1

    this_color = td[h]
    next_color = td[nexth]
    grad = poly_gradient([this_color, next_color], 60)

    ansi = convert_to_256(list(grad)[m])
    return ansi


if __name__ == '__main__':
    now = datetime.datetime.now()
    print_gradient()
    ansi = get_color_by_time()
    print_colored(ansi, str(now.hour) + ':' + str(now.minute))
