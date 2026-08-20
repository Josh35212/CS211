"""Break a list of strings into columns"""

def columns(text: list[str], col_width: int=5,  line_length: int = 80) -> str:
    """Arranges elements of text into columns.  Text shorter than a column
    will be padded out to a column.  Text longer than a column will be spread
    across columns.  Text that is not in column 1 and would extend over the end
    of a line will be moved to the next line.

    If a column is completely filled, a blank column separates it from the next.
    """

   # Since a single item could take one or ore columns, it simpler
    # to iterate through the items.
    rows = []
    this_row = ""
    for item in text:

        # Time to break to next line?
        extent = len(this_row) + len(item)
        if extent > line_length:
            rows.append(this_row.rstrip())
            this_row = ""

        this_row += item

        # Now pad out to a column boundary
        over_column = len(this_row) % col_width
        pad = col_width - over_column # How far to next column
        this_row += " " * pad

    # We probably have a partly formed line in the buffer
    if len(this_row) > 0:
        rows.append(this_row.rstrip())

    return "\n".join(rows)







