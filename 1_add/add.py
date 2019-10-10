def add(*args):
    to_return = [[0 for _ in range(len(args[0][0]))] for _ in range(len(args[0]))]
    for arg in args:
        for outer in range(len(args[0])):
            for inner in range(len(args[0][outer])):
                to_return[outer][inner] += arg[outer][inner]
    return to_return


first = [[1, 2], [3, 8]]
second = [[-1, -2], [-3, -4]]

print(add([[5]], [[-2]]))
print(add(first, second))
