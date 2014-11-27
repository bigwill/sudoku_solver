def solve_board(b):
    cells = sorted((cell for cell in b.get_cells() if cell.get_v() is None), key=lambda cell: len(cell.possible_vs()))
    if not cells:
        return False

    cell = cells[0]

    for possible_v in cell.possible_vs():
        cell.set_v(possible_v)
        if b.verify():
            if b.is_solved():
                return True
            solved = solve_board(b)
            if solved:
                return True
            else:
                cell.set_v(None)
        else:
            cell.set_v(None)
    return False
