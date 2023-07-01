def calculate_coef(point1, point2):
    """Calculate coefficients a and b of f(x) = a*x**2 + b*x."""
    x1, y1 = point1
    x2, y2 = point2
    a = (y2 - x2 * y1 / x1) / (x2**2 - x1 * x2)
    b = y1 / x1 - x1 * a
    return a, b


def main():
    point1 = (20, 200)
    point2 = (30, 1000)
    print(*calculate_coef(point1, point2))


if __name__ == '__main__':
    main()
