# Multilingual Multiplication Table

A graphical, multilingual multiplication table built with Python and Tkinter. The application provides a customizable table with color palettes, special number highlighting, and a scrollable interface.

## Features

- **Multilingual interface** – supports 40 languages.
- **Adjustable table size** – choose multiplication tables from 10 × 10 to 100 × 100 in increments of 10.
- **Color palettes** – choose from four different color schemes:
  - Rainbow
  - Pastel
  - Ocean
  - Heatmap
- **Color-coded results** – multiplication results are displayed using the selected color palette.
- **Special number highlighting** – highlight specific number categories:
  - Prime numbers
  - Square numbers (diagonal)
  - First row and column
  - Multiples of five
  - Even numbers
- **Interactive controls** – change the color palette and special number categories without restarting the application.
- **Dynamic legend** – displays the active special number categories and the color ranges of the selected palette.
- **Scrollable table** – navigate large multiplication tables using horizontal and vertical scrollbars or the mouse wheel.
- **Responsive window sizing** – the application automatically adjusts its window size to the selected multiplication table and available screen space.

## Screenshots

<!-- Add screenshots of the application here -->

## Requirements

- Python 3.10 or newer
- Tkinter
- pytest (for running tests)

Tkinter is included with most standard Python installations.

## Installation

Clone the repository:

```bash
git clone https://github.com/AxAd77/multilingual_Multiplication_Table.git
```

Navigate to the project directory:

```bash
cd multilingual_Multiplication_Table
```

## Usage

Start the application:

```bash
python main.py
```

The application opens a graphical multiplication table using the settings defined in `scr/multiplication_table/settings.py`.

### Changing the table size

Select a table size from the dropdown menu. Available sizes range from 10 to 100 in increments of 10.

The application automatically recreates the table with the selected size.

### Changing the color palette

Select one of the available color palettes from the dropdown menu.

The table cells and legend update immediately.

### Highlighting special numbers

Open the **Special Numbers** menu and activate the categories you want to highlight.

The available categories are:

| Category | Description |
|---|---|
| Prime numbers | Highlights prime numbers |
| Square numbers | Highlights square numbers along the diagonal |
| First row and column | Highlights results in the first row and first column |
| Multiples of five | Highlights multiples of five |
| Even numbers | Highlights even numbers |

Highlighted cells receive a category-specific background color and a black border.

Multiple categories can be activated simultaneously.

## Color Palettes

The application currently includes four color palettes.

| Palette | Description |
|---|---|
| Rainbow | Vibrant colors across the spectrum |
| Pastel | Soft pastel colors |
| Ocean | Blue and turquoise shades |
| Heatmap | Colors ranging from light yellow to red |

The legend dynamically displays the number ranges associated with each palette color.

## Project Structure

```text
multilingual_Multiplication_Table/
│
├── main.py
├── gui.py
├── table.py
├── translations.py
├── settings.py
│
└── tests/
    └── test_table_testing.py
```

### Files

| File | Description |
|---|---|
| `main.py` | Application entry point |
| `scr/multiplication_table/gui.py` | Creates and manages the graphical user interface |
| `scr/multiplication_table/table.py` | Contains functions for creating and analyzing multiplication tables, color palettes, and marker logic |
| `scr/multiplication_table/translations.py` | Provides translations for the supported languages |
| `scr/multiplication_table/settings.py` | Defines application settings, including language, table size, and color palette |
| `tests/test_table_testing.py` | Contains automated tests for the table functions |

## Testing

The project uses pytest for automated testing.

Run all tests:

```bash
python -m pytest
```

Run the tests for the multiplication table functions:

```bash
python -m pytest tests/test_table_testing.py -v
```

The test suite currently covers:

- Multiplication table generation
- Prime number detection
- Square number detection
- Cell color calculation
- Special number marker logic
- Legend generation
- Different table sizes and color palettes

## Technologies

- Python
- Tkinter
- pytest

## License

This project is intended for educational purposes and as a personal software development portfolio project.
