from random import randint, uniform


def sensors_read():
    init_arr = []
    speed = randint(0, 200)
    init_arr.append(speed)

    ignition = randint(0,1)
    init_arr.append(ignition)

    fuel = randint(0, 60)
    init_arr.append(fuel)

    errors_count = randint(0, 5)
    init_arr.append(errors_count)

    lat = uniform(-90, 90)
    lat = float('{:.7f}'.format(lat))
    init_arr.append(lat)

    lon = uniform(-180, 180)
    lon = float('{:.7f}'.format(lon))
    init_arr.append(lon)

    accelerometer_x = uniform(1, 10)
    accelerometer_x = float('{:.7f}'.format(accelerometer_x))
    init_arr.append(accelerometer_x)

    accelerometer_y = uniform(1, 10)
    accelerometer_y = float('{:.7f}'.format(accelerometer_y))
    init_arr.append(accelerometer_y)

    accelerometer_z = uniform(1, 10)
    accelerometer_z = float('{:.7f}'.format(accelerometer_z))
    init_arr.append(accelerometer_z)
    return init_arr
