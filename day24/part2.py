from time import time

from part1 import read_input, Ray, intersect_rays


Vector = tuple[int, int, int]
Line = tuple[Vector, Vector]


def parse_line(line: str, rescaling) -> Line:
    # "19, 13, 30 @ -2, 1, -2"
    point_str, direction_str = line.split(" @ ")
    x, y, z = [int(i) * rescaling for i in point_str.split(",")]
    dx, dy, dz = [int(i) for i in direction_str.split(",")]
    return (x, y, z), (dx, dy, dz)


def solve(lines: list[str], rescaling=1e-13, lr=1e-6) -> int:
    lines = [parse_line(line, rescaling) for line in lines]

    approximate_solution = get_approximate_solution(lines, lr)
    print(f"{approximate_solution = }")

    dx, dy, dz = [round(v) for v in approximate_solution[1]]
    print(f"{dx = }, {dy = }, {dz = }")

    x, y, z = get_exact_x_y_z(lines, (dx, dy, dz), int(1/rescaling))
    print(f"{x = }, {y = }, {z = }")

    return x + y + z


def get_approximate_solution(lines: list[Line], lr) -> Line:
    current_line = [[0, 0, 0], [0, 0, 0]]

    for iteration in range(1, 1001):
        iteration_loss = 0
        for line in lines:
            for i1, i2 in [(0, 1), (1, 2), (2, 0)]:
                x, y = current_line[0][i1], current_line[0][i2]
                dx, dy = current_line[1][i1], current_line[1][i2]
                lx, ly = line[0][i1], line[0][i2]
                ldx, ldy = line[1][i1], line[1][i2]

                loss, ux, uy, udx, udy = get_gradients(
                    x, y, dx, dy, lx, ly, ldx, ldy
                )
                current_line[0][i1] -= lr * ux
                current_line[0][i2] -= lr * uy
                current_line[1][i1] -= lr * udx
                current_line[1][i2] -= lr * udy

                iteration_loss += loss

        # print(f"{iteration = }, {iteration_loss = }")

    return current_line


def get_gradients(x, y, dx, dy, lx, ly, ldx, ldy):
    loss_sqrt = (lx - x) * (ldy - dy) - (ly - y) * (ldx - dx)

    loss = loss_sqrt ** 2
    ux = loss_sqrt * (ldy - dy) * (-1)
    uy = loss_sqrt * (ldx - dx)
    udx = loss_sqrt * (ly - y)
    udy = loss_sqrt * (lx - x) * (-1)

    return loss, ux, uy, udx, udy


def get_exact_x_y_z(lines: list[Line], direction, inverse_rescaling: int):
    l1, dl1 = lines[0]
    l2, dl2 = lines[1]

    x_y_z = [0, 0, 0]

    for i1, i2 in [(0, 1), (1, 2), (2, 0)]:
        d = direction
        u = inverse_rescaling
        ray1 = Ray((l1[i1]*u, l1[i2]*u), (-d[i1]+dl1[i1], -d[i2]+dl1[i2]))
        ray2 = Ray((l2[i1]*u, l2[i2]*u), (-d[i1]+dl2[i1], -d[i2]+dl2[i2]))

        intersection = intersect_rays(ray1, ray2)

        x_y_z[i1] = round(intersection[0])
        x_y_z[i2] = round(intersection[1])

    return x_y_z


def main():
    lines = read_input()
    solution = solve(lines)
    print(f"{solution = }")


if __name__ == "__main__":
    start_time = time()
    main()
    print(f"Solved in about {time() - start_time:.4f} seconds")
