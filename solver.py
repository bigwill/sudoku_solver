def solve_cell(cell):
    if cell.get_v():
        return False

    possibles = cell.possible_vs()
    if len(possibles) == 1:
        cell.set_v(possibles.pop())
        return True
    else:
        return False

def solve_constraint(cons):
    solved = False
    for v in cons.unused_values.copy():
        v_cells = set()
        for cell in cons.get_cells():
            if v in cell.possible_vs():
                v_cells.add(cell)
        if len(v_cells) == 1:
            v_cells.pop().set_v(v)
            solved = True
    return solved

def solve_search_board(b):
    cells = sorted((cell for cell in b.get_cells() if cell.get_v() is None), key=lambda cell: len(cell.possible_vs()))
    if not cells:
        return False

    cell = cells[0]

    for possible_v in cell.possible_vs():
        cell.set_v(possible_v)
        if b.verify():
            if b.is_solved():
                return True
            solved = solve_search_board(b)
            if solved:
                return True
            else:
                cell.set_v(None)
        else:
            cell.set_v(None)
    return False

def solve_board(b):
    progress = True
    while progress:
        progress = False

        for cell in b.get_cells():
            if solve_cell(cell):
                progress = True

        for cons in b.get_constraints():
            if solve_constraint(cons):
                progress = True

        if b.is_solved():
            return True

    if solve_search_board(b):
        return True
    else:
        return False
