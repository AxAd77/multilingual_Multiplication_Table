"""Functions for creating and analyzing multiplication tables."""

COLOR_PALETTES = {
    "Rainbow": [
        "#FF6666",
        "#FF8000",
        "#FFFF00",
        "#00C000",
        "#00BFFF",
        "#6699FF",
        "#C084FC",
    ],
    "Pastel": [
        "#FFB3BA",
        "#FFDFBA",
        "#FFFFBA",
        "#BAFFC9",
        "#BAE1FF",
        "#D5BAFF",
        "#FFBAED",
    ],
    "Ocean": [
        "#E0FFFF",
        "#B0E0E6",
        "#87CEEB",
        "#00BFFF",
        "#1E90FF",
        "#7BA7F7",
        "#9ABCF5",
    ],
    "Heatmap": [
        "#FFFFCC",
        "#FFEDA0",
        "#FED976",
        "#FEB24C",
        "#FD8D3C",
        "#FC4E2A",
        "#E31A1C",
    ],
}

MARKER_OPTIONS = {
    "prime_numbers": False,
    "square_numbers": False,
    "first_row_column": False,
    "multiples_of_five": False,
    "even_numbers": False,
}


def create_multiplication_table(table_size):
    """Create a multiplication table for the given size."""
    multiplication_table = []

    for row in range(1, table_size + 1):
        table_row = []

        for column in range(1, table_size + 1):
            result = row * column
            table_row.append(result)

        multiplication_table.append(table_row)

    return multiplication_table


def is_prime(number):
    """Check whether a number is prime."""
    if number < 2:
        return False

    for divisor in range(2, int(number ** 0.5) + 1):
        if number % divisor == 0:
            return False

    return True


def get_square_numbers(max_number):
    """Return all square numbers up to the given maximum."""
    square_numbers = []

    number = 1

    while number ** 2 <= max_number:
        square_numbers.append(number ** 2)
        number += 1

    return square_numbers


def get_cell_color(result, palette, max_number):
    """Determine the base color of a multiplication table cell."""
    color_index = min(
        (result - 1) * len(palette) // max_number,
        len(palette) - 1,
    )

    return palette[color_index]


def get_cell_marker_color(
        result,
        row,
        column,
        enabled_markers=None,
):
    """Determine whether a cell needs a black border."""
    if enabled_markers is None:
        enabled_markers = MARKER_OPTIONS

    if (
            enabled_markers["prime_numbers"]
            and is_prime(result)
    ):
        return "black"

    if (
            enabled_markers["square_numbers"]
            and row == column
    ):
        return "black"

    if (
            enabled_markers["first_row_column"]
            and (row == 1 or column == 1)
    ):
        return "black"

    if (
            enabled_markers["multiples_of_five"]
            and result % 5 == 0
    ):
        return "black"

    if (
            enabled_markers["even_numbers"]
            and result % 2 == 0
    ):
        return "black"

    return None


def get_legend_items(palette, max_number):
    """Create legend entries for the selected color palette."""
    legend_items = [
        ("Prime numbers", "black"),
        ("Square numbers (diagonal)", "black"),
        ("First row and column", "black"),
        ("Multiples of 5", "black"),
        ("Even numbers", "black"),
    ]

    palette_size = len(palette)

    for color_index, color in enumerate(palette):
        start_number = (
                               color_index * max_number + palette_size - 1
                       ) // palette_size + 1

        end_number = (
                             (color_index + 1) * max_number + palette_size - 1
                     ) // palette_size

        legend_items.append(
            (
                f"Other results: {start_number}-{end_number}",
                color,
            )
        )

    return legend_items
