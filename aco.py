# TODO
# constraint propagation
# aco algorithm
# convert everything to numpy

# SUS List
# add get row, get column, get box functions

def propogate_constraints(puzzle):
    # loop through all units
    # if the unit is already fixed, continue
    fixed_total = 0
    for i in range(0, puzzle.d*puzzle.d):
        if len(puzzle.value_sets[i]) != 1:
            # get all fixed values from row, column, and box of the unit
            fixed_in_cell = set()
            for x in range(i - i % puzzle.d, i - i % puzzle.d + puzzle.d, 1):
                if len(puzzle.value_sets[x]) == 1:
                    fixed_in_cell.add(puzzle.value_sets[x][0])
            for x in range(i % puzzle.d, puzzle.d*puzzle.d,9):
                if len(puzzle.value_sets[x]) == 1:
                    fixed_in_cell.add(puzzle.value_sets[x][0])
            # x + 3y
            # x = (i%9)/3
            # y = (i/9)/3
            box_index = int((i % puzzle.d) / puzzle.cell_dim) + puzzle.cell_dim * int(int(i / puzzle.d) / puzzle.cell_dim)
            #print(box_index)
            for x in puzzle.get_box(box_index):
                if len(puzzle.value_sets[x]) == 1:
                    fixed_in_cell.add(puzzle.value_sets[x][0])
            # update the unit's value set
            #print(fixed_in_cell)
            for f in fixed_in_cell:
                if f in puzzle.value_sets[i]:
                    puzzle.value_sets[i].remove(f)

            # if unit is fixed
            if len(puzzle.value_sets[i]) == 1:
                fixed_total += 1

            # if any value is the only one of its kind in a row, column, or box
            for v in puzzle.value_sets[i]:
                # check if v is in the row, column, box
                # row
                row_singleton = True
                for x in range(i - i % puzzle.d, i - i % puzzle.d + puzzle.d, 1):
                    if x != i and v in puzzle.value_sets[x]:
                        row_singleton = False
                if row_singleton:
                    puzzle.value_sets[i] = [v]
                    break

                # column
                column_singleton = True
                for x in range(i % puzzle.d, puzzle.d * puzzle.d, 9):
                    if x != i and v in puzzle.value_sets[x]:
                        column_singleton = False
                if column_singleton:
                    puzzle.value_sets[i] = [v]
                    break

                # box
                box_singleton = True
                for x in puzzle.get_box(box_index):
                    if x != i and v in puzzle.value_sets[x]:
                        box_singleton = False
                if box_singleton:
                    puzzle.value_sets[i] = [v]
                    break
    return fixed_total
    # eliminate
    # return the number of fixed cells