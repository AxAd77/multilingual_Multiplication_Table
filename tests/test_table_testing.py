"""Tests for the multiplication table functions."""

from multiplication_table.gui import (
    COLOR_PALETTES,
    MARKER_OPTIONS,
    get_cell_color,
    get_cell_marker_color,
)

from multiplication_table.table import (
    create_multiplication_table,
    get_square_numbers,
    is_prime,
    get_legend_items,
)


def test_create_multiplication_table():
    """Test the creation of a multiplication table."""
    assert create_multiplication_table(3) == [
        [1, 2, 3],
        [2, 4, 6],
        [3, 6, 9],
    ]


def test_create_multiplication_table_size_one():
    """Test a multiplication table with size one."""
    assert create_multiplication_table(1) == [[1]]


def test_create_multiplication_table_size_fifty():
    """Test a multiplication table with size fifty."""
    multiplication_table = create_multiplication_table(50)

    assert len(multiplication_table) == 50
    assert all(len(row) == 50 for row in multiplication_table)
    assert multiplication_table[0][49] == 50
    assert multiplication_table[49][49] == 2500


def test_is_prime():
    """Test prime number detection."""
    assert is_prime(2) is True
    assert is_prime(7) is True
    assert is_prime(1) is False
    assert is_prime(9) is False


def test_is_prime_boundary_values():
    """Test prime number detection for boundary values."""
    assert is_prime(-5) is False
    assert is_prime(0) is False
    assert is_prime(1) is False
    assert is_prime(2) is True
    assert is_prime(3) is True
    assert is_prime(4) is False


def test_get_square_numbers():
    """Test the detection of square numbers."""
    assert get_square_numbers(10) == [1, 4, 9]


def test_get_square_numbers_boundary_values():
    """Test square number detection for boundary values."""
    assert get_square_numbers(0) == []
    assert get_square_numbers(1) == [1]
    assert get_square_numbers(15) == [1, 4, 9]
    assert get_square_numbers(16) == [1, 4, 9, 16]


def test_get_cell_color_first_palette_color():
    """Test the first color of a palette."""
    assert get_cell_color(
        1,
        COLOR_PALETTES["Rainbow"],
        100,
    ) == COLOR_PALETTES["Rainbow"][0]


def test_get_cell_color_middle_palette_color():
    """Test a color in the middle of a palette."""
    assert get_cell_color(
        50,
        COLOR_PALETTES["Rainbow"],
        100,
    ) == COLOR_PALETTES["Rainbow"][3]


def test_get_cell_color_last_palette_color():
    """Test the last color of a palette."""
    assert get_cell_color(
        100,
        COLOR_PALETTES["Rainbow"],
        100,
    ) == COLOR_PALETTES["Rainbow"][-1]


def test_get_cell_color_maximum_number():
    """Test the color of the maximum number."""
    assert get_cell_color(
        2500,
        COLOR_PALETTES["Ocean"],
        2500,
    ) == COLOR_PALETTES["Ocean"][-1]


def test_get_cell_marker_color_without_markers():
    """Test that no marker color is returned when markers are disabled."""
    assert get_cell_marker_color(
        7,
        2,
        3,
        MARKER_OPTIONS,
    ) is None


def test_get_cell_marker_color_prime_number():
    """Test the marker color for prime numbers."""
    enabled_markers = MARKER_OPTIONS.copy()
    enabled_markers["prime_numbers"] = True

    assert get_cell_marker_color(
        7,
        2,
        3,
        enabled_markers,
    ) == "black"

    assert get_cell_marker_color(
        8,
        2,
        4,
        enabled_markers,
    ) is None


def test_get_cell_marker_color_square_number():
    """Test the marker color for square numbers."""
    enabled_markers = MARKER_OPTIONS.copy()
    enabled_markers["square_numbers"] = True

    assert get_cell_marker_color(
        4,
        2,
        2,
        enabled_markers,
    ) == "black"

    assert get_cell_marker_color(
        6,
        2,
        3,
        enabled_markers,
    ) is None


def test_get_cell_marker_color_first_row():
    """Test the marker color for cells in the first row."""
    enabled_markers = MARKER_OPTIONS.copy()
    enabled_markers["first_row_column"] = True

    assert get_cell_marker_color(
        4,
        1,
        4,
        enabled_markers,
    ) == "black"


def test_get_cell_marker_color_first_column():
    """Test the marker color for cells in the first column."""
    enabled_markers = MARKER_OPTIONS.copy()
    enabled_markers["first_row_column"] = True

    assert get_cell_marker_color(
        4,
        4,
        1,
        enabled_markers,
    ) == "black"


def test_get_cell_marker_color_multiples_of_five():
    """Test the marker color for multiples of five."""
    enabled_markers = MARKER_OPTIONS.copy()
    enabled_markers["multiples_of_five"] = True

    assert get_cell_marker_color(
        25,
        5,
        5,
        enabled_markers,
    ) == "black"

    assert get_cell_marker_color(
        24,
        4,
        6,
        enabled_markers,
    ) is None


def test_get_cell_marker_color_even_numbers():
    """Test the marker color for even numbers."""
    enabled_markers = MARKER_OPTIONS.copy()
    enabled_markers["even_numbers"] = True

    assert get_cell_marker_color(
        8,
        2,
        4,
        enabled_markers,
    ) == "black"

    assert get_cell_marker_color(
        7,
        1,
        7,
        enabled_markers,
    ) is None


def test_get_cell_marker_color_multiple_markers():
    """Test the marker color when multiple markers are enabled."""
    enabled_markers = MARKER_OPTIONS.copy()
    enabled_markers["prime_numbers"] = True
    enabled_markers["square_numbers"] = True
    enabled_markers["even_numbers"] = True

    assert get_cell_marker_color(
        4,
        2,
        2,
        enabled_markers,
    ) == "black"


def test_get_legend_items():
    """Test the creation of legend entries."""
    legend_items = get_legend_items(
        COLOR_PALETTES["Rainbow"],
        100,
    )

    assert len(legend_items) == 12

    assert legend_items[0] == ("Prime numbers", "black")
    assert legend_items[1] == ("Square numbers (diagonal)", "black")
    assert legend_items[2] == ("First row and column", "black")
    assert legend_items[3] == ("Multiples of 5", "black")
    assert legend_items[4] == ("Even numbers", "black")

    assert legend_items[5] == (
        "Other results: 1-15",
        COLOR_PALETTES["Rainbow"][0],
    )

    assert legend_items[-1] == (
        "Other results: 87-100",
        COLOR_PALETTES["Rainbow"][-1],
    )


def test_get_legend_items_with_different_palette():
    """Test legend entries with the Ocean palette."""
    legend_items = get_legend_items(
        COLOR_PALETTES["Ocean"],
        100,
    )

    assert len(legend_items) == 12

    assert legend_items[5][1] == COLOR_PALETTES["Ocean"][0]
    assert legend_items[-1][1] == COLOR_PALETTES["Ocean"][-1]


def test_get_legend_items_with_different_table_size():
    """Test legend entries with a different table size."""
    legend_items = get_legend_items(
        COLOR_PALETTES["Rainbow"],
        50,
    )

    assert len(legend_items) == 12

    assert legend_items[5] == (
        "Other results: 1-8",
        COLOR_PALETTES["Rainbow"][0],
    )

    assert legend_items[-1] == (
        "Other results: 44-50",
        COLOR_PALETTES["Rainbow"][-1],
    )
