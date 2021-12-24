def _one_align_char(a, char):
    return all([item.count(char) == 1 for item in a])


def _max_col_length(a):
    return max(len(item) for item in a)


def _guess_delimiter(lines):
    # remove empty lines
    lines = [line for line in lines if line.strip()]

    for delimiter in "|&;,":
        # Check if the delimiter appears more than once in every line.
        if all([line.count(delimiter) > 1 for line in lines]):
            return delimiter

    return None


def _guess_column_type(col):
    ignore_header = min(1, len(col) - 1)
    # strictly_numerical = [str(n) for n in range(10)]
    # extra_numerical = ['^', '+', '-', 'E', 'e', '%', '$', '.', ',', ' ']
    # all_numerical = strictly_numerical + extra_numerical
    numeric = 0
    alpha = 0
    test_cells = min(len(col), 100)
    for i, cell in enumerate(col[ignore_header: test_cells]):
        try:
            float(cell.strip('%$€¥£').replace(',', ''))
        except ValueError:
            alpha += 1
        else:
            numeric += 1
        if numeric >= alpha:
            col_type = 'numeric'
        else:
            col_type = 'alpha'
    return(col_type)


def _align(data, align_char):
    before_sizes = []
    after_sizes = []
    for item in data:
        before, after = item.split(align_char)
        before_sizes.append(len(before))
        after_sizes.append(len(after))

    num_char_before_dot = max(before_sizes)
    num_char_after_dot = max(after_sizes)

    return [
        (
            " " * (num_char_before_dot - before_sizes[i])
            + item
            + " " * (num_char_after_dot - after_sizes[i])
        )
        for i, item in enumerate(data)
    ]


def tablign(string, align_char=".", delimiter=None):
    lines = string.splitlines()

    if delimiter is None:
        delimiter = _guess_delimiter(lines)

    # split and strip
    # list of list, i.e, lines of cells
    data = [[item.strip() for item in line.split(delimiter)] for line in lines]

    max_num_cols = max(len(row) for row in data)

    # extend short rows with ''
    for i, row in enumerate(data):
        data[i].extend([""] * (max_num_cols - len(row)))

    # transpose <https://stackoverflow.com/a/6473724/353337>
    cols = list(map(list, zip(*data)))

    for j, col in enumerate(cols):
        if _one_align_char(col, align_char):
            cols[j] = _align(col, align_char)
        else:
            # append spaces to make all entries equally long
            col_type = _guess_column_type(col)
            max_length = _max_col_length(col)
            if col_type == 'numeric':
                cols[j] = [item.rjust(max_length) for item in col]
            else:
                cols[j] = [item.ljust(max_length) for item in col]

    # transpose back
    data = list(map(list, zip(*cols)))

    sep = f" {delimiter} " if delimiter else " "

    first_col_empty = all(s == "" for s in cols[0])
    last_col_empty = all(s == "" for s in cols[-1])

    # If the delimiter is None, only strip trailing whitespace
    lstrp = str.lstrip if first_col_empty and delimiter is not None else lambda x: x
    rstrp = str.rstrip if last_col_empty and delimiter is not None else lambda x: x

    return "\n".join([rstrp(lstrp(sep.join(row))) for row in data])
