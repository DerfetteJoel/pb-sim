enable_log = 0


def log(msg):
    if enable_log:
        print('[LOG] ', end='')
        print(msg)
