def lerp(t, a, b):
    return (1 - t) * a + t * b

def rotate_index(n, i, a):
    return (n + i + a) % n
