"""Create the graphical multiplication table."""

from __future__ import annotations

import tkinter as tk
from collections.abc import Callable
from tkinter import ttk

from .table import (
    COLOR_PALETTES,
    MARKER_OPTIONS,
    create_multiplication_table,
    get_cell_color,
    get_cell_marker_color,
)

from .translations import get_translation


def display_multiplication_table(settings):
    """Display the multiplication table using the selected settings."""
    table_size = settings["table_size"]
    selected_language = settings["language"]
    selected_palette_name = settings["palette"]

    selected_palette = COLOR_PALETTES[selected_palette_name]

    marker_options = settings.get(
        "marker_options",
        MARKER_OPTIONS.copy(),
    ).copy()

    max_number = table_size ** 2
    cell_width = len(str(max_number)) + 1
    cell_height = 1

    multiplication_table = create_multiplication_table(table_size)

    root = tk.Tk()

    root.title(
        get_translation(
            selected_language,
            "table_title",
        ).format(size=table_size)
    )

    root.update_idletasks()

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Create the main frame.
    main_frame = ttk.Frame(root)
    main_frame.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10,
    )

    # Create the scrollable table area.
    table_frame = ttk.Frame(main_frame)
    table_frame.pack(
        fill="both",
        expand=True,
    )

    canvas = tk.Canvas(
        table_frame,
        background="white",
        highlightthickness=0,
    )

    vertical_scrollbar = ttk.Scrollbar(
        table_frame,
        orient="vertical",
        command=canvas.yview,
    )

    horizontal_scrollbar = ttk.Scrollbar(
        table_frame,
        orient="horizontal",
        command=canvas.xview,
    )

    canvas.configure(
        yscrollcommand=vertical_scrollbar.set,
        xscrollcommand=horizontal_scrollbar.set,
    )

    canvas.grid(row=0, column=0, sticky="nsew")
    vertical_scrollbar.grid(row=0, column=1, sticky="ns")
    horizontal_scrollbar.grid(row=1, column=0, sticky="ew")

    table_frame.rowconfigure(0, weight=1)
    table_frame.columnconfigure(0, weight=1)

    table_content = ttk.Frame(canvas)

    table_window = canvas.create_window(
        (0, 0),
        window=table_content,
        anchor="nw",
    )

    def update_scrollregion(_event=None) -> None:
        """Update the canvas scroll region."""
        canvas.configure(
            scrollregion=canvas.bbox("all"),
        )

    table_content.bind(
        "<Configure>",
        update_scrollregion,
    )

    def is_widget_inside_table(widget) -> bool:
        """Check whether a widget belongs to the table."""
        while widget is not None:
            if widget == canvas:
                return True

            widget = getattr(widget, "master", None)

        return False

    def scroll_with_mousewheel(event: tk.Event) -> None:
        """Scroll vertically or horizontally using the mouse wheel."""
        if not is_widget_inside_table(event.widget):
            return

        scroll_direction = -1 if event.delta > 0 else 1

        if int(event.state) & 0x0001:
            canvas.xview_scroll(
                scroll_direction,
                "units",
            )
        else:
            canvas.yview_scroll(
                scroll_direction,
                "units",
            )

    def scroll_with_mousewheel_linux(event: tk.Event) -> None:
        """Scroll using the mouse wheel on Linux."""
        if not is_widget_inside_table(event.widget):
            return

        scroll_direction = -1 if event.num == 4 else 1

        if int(event.state) & 0x0001:
            canvas.xview_scroll(
                scroll_direction,
                "units",
            )
        else:
            canvas.yview_scroll(
                scroll_direction,
                "units",
            )

    # Bind mouse wheel scrolling to the application.
    root.bind_all(
        "<MouseWheel>",
        scroll_with_mousewheel,
    )

    root.bind_all(
        "<Button-4>",
        scroll_with_mousewheel_linux,
    )

    root.bind_all(
        "<Button-5>",
        scroll_with_mousewheel_linux,
    )

    # Define individual colors for special number categories.
    marker_menu_colors = {
        "prime_numbers": {
            "background": "#6A1B9A",
            "foreground": "white",
        },
        "square_numbers": {
            "background": "#2E7D32",
            "foreground": "white",
        },
        "first_row_column": {
            "background": "#1565C0",
            "foreground": "white",
        },
        "multiples_of_five": {
            "background": "#B45309",
            "foreground": "white",
        },
        "even_numbers": {
            "background": "#F9A825",
            "foreground": "black",
        },
    }

    def get_marker_background_color(
            number_to_check: int,
            row: int,
            column: int,
    ) -> str | None:
        """Return the selected category color for a marked cell."""
        if (
                marker_options["prime_numbers"]
                and number_to_check >= 2
                and all(
            number_to_check % divisor != 0
            for divisor in range(
                2,
                int(number_to_check ** 0.5) + 1,
            )
        )
        ):
            return marker_menu_colors["prime_numbers"]["background"]

        if (
                marker_options["square_numbers"]
                and row == column
        ):
            return marker_menu_colors["square_numbers"]["background"]

        if (
                marker_options["first_row_column"]
                and (row == 1 or column == 1)
        ):
            return marker_menu_colors["first_row_column"]["background"]

        if (
                marker_options["multiples_of_five"]
                and number_to_check % 5 == 0
        ):
            return marker_menu_colors["multiples_of_five"]["background"]

        if (
                marker_options["even_numbers"]
                and number_to_check % 2 == 0
        ):
            return marker_menu_colors["even_numbers"]["background"]

        return None

    def create_cell(
            parent,
            cell_text,
            background,
            grid_row,
            grid_column,
            is_header=False,
            has_marker=False,
    ):
        """Create a single table cell."""
        if is_header:
            cell = tk.Label(
                parent,
                text=cell_text,
                background=background,
                foreground="white",
                width=cell_width,
                height=cell_height,
                borderwidth=2,
                relief="ridge",
                font=("Arial", 12, "bold"),
            )
        else:
            cell = tk.Label(
                parent,
                text=cell_text,
                background=background,
                foreground="black",
                width=cell_width,
                height=cell_height,
                borderwidth=0,
                relief="flat",
                highlightthickness=3 if has_marker else 0,
                highlightbackground="black",
                highlightcolor="black",
                font=("Arial", 12),
            )

        cell.grid(
            row=grid_row,
            column=grid_column,
            sticky="nsew",
        )

        return cell

    # Create the top-left corner cell.
    create_cell(
        table_content,
        "×",
        "#1F4E78",
        0,
        0,
        is_header=True,
    )

    # Create the column headers.
    for column_number in range(1, table_size + 1):
        create_cell(
            table_content,
            str(column_number),
            "#5B9BD5",
            0,
            column_number,
            is_header=True,
        )

    # Keep references to result cells for updates.
    table_result_cells = []

    # Create the row headers and multiplication results.
    for row_number in range(1, table_size + 1):
        create_cell(
            table_content,
            str(row_number),
            "#5B9BD5",
            row_number,
            0,
            is_header=True,
        )

        for column_number in range(1, table_size + 1):
            number_to_display = multiplication_table[
                row_number - 1
                ][column_number - 1]

            palette_background = get_cell_color(
                number_to_display,
                selected_palette,
                max_number,
            )

            marker_background = get_marker_background_color(
                number_to_display,
                row_number,
                column_number,
            )

            cell_background = (
                marker_background
                if marker_background is not None
                else palette_background
            )

            border_color = get_cell_marker_color(
                number_to_display,
                row_number,
                column_number,
                marker_options,
            )

            result_cell = create_cell(
                table_content,
                str(number_to_display),
                cell_background,
                row_number,
                column_number,
                has_marker=border_color is not None,
            )

            table_result_cells.append(
                (
                    result_cell,
                    number_to_display,
                    row_number,
                    column_number,
                )
            )

    def update_marker_cells() -> None:
        """Update the background colors and borders of marked cells."""
        for (
                marker_cell,
                marker_result,
                marker_row,
                marker_column,
        ) in table_result_cells:
            new_marker_background = get_marker_background_color(
                marker_result,
                marker_row,
                marker_column,
            )

            new_palette_background = get_cell_color(
                marker_result,
                selected_palette,
                max_number,
            )

            marker_cell.configure(
                background=(
                    new_marker_background
                    if new_marker_background is not None
                    else new_palette_background
                ),
                highlightthickness=(
                    3 if new_marker_background is not None else 0
                ),
                highlightbackground="black",
                highlightcolor="black",
            )

    # Create the bottom section outside the scrollable table.
    bottom_frame = ttk.Frame(main_frame)
    bottom_frame.pack(
        fill="x",
        pady=(10, 0),
    )

    bottom_frame.columnconfigure(0, weight=3)
    bottom_frame.columnconfigure(1, weight=1)

    # Create the legend on the left.
    legend_frame = ttk.LabelFrame(
        bottom_frame,
        text=get_translation(
            selected_language,
            "other_results",
        ),
    )

    legend_frame.grid(
        row=0,
        column=0,
        sticky="nsew",
        padx=(0, 5),
    )

    for legend_column in range(3):
        legend_frame.columnconfigure(
            legend_column,
            weight=1,
        )

    # Define the special number categories.
    marker_labels = [
        (
            "prime_numbers",
            get_translation(
                selected_language,
                "prime_numbers",
            ),
        ),
        (
            "square_numbers",
            get_translation(
                selected_language,
                "square_numbers",
            ),
        ),
        (
            "first_row_column",
            get_translation(
                selected_language,
                "first_row_column",
            ),
        ),
        (
            "multiples_of_five",
            get_translation(
                selected_language,
                "multiples_of_five",
            ),
        ),
        (
            "even_numbers",
            get_translation(
                selected_language,
                "even_numbers",
            ),
        ),
    ]

    # Create the special number legend labels.
    special_legend_labels = {}

    for legend_category_key, legend_category_text in marker_labels:
        category_color = marker_menu_colors[legend_category_key]

        special_legend_labels[legend_category_key] = tk.Label(
            legend_frame,
            text=legend_category_text,
            background=category_color["background"],
            foreground=category_color["foreground"],
            borderwidth=1,
            relief="solid",
            padx=5,
            pady=5,
            wraplength=200,
        )

    # Create the palette legend.
    palette_legend_frame = ttk.LabelFrame(
        legend_frame,
        text="Farbpalette",
    )

    palette_legend_frame.grid(
        row=0,
        column=0,
        columnspan=3,
        sticky="ew",
        padx=5,
        pady=5,
    )

    # Configure the palette legend for two rows.
    palette_columns = 4

    for palette_column in range(palette_columns):
        palette_legend_frame.columnconfigure(
            palette_column,
            weight=1,
        )

    palette_legend_items = []

    for palette_index, palette_color in enumerate(selected_palette):
        palette_color_label = tk.Label(
            palette_legend_frame,
            background=palette_color,
            foreground="black",
            borderwidth=1,
            relief="solid",
            padx=5,
            pady=3,
        )

        palette_color_label.grid(
            row=palette_index // palette_columns,
            column=palette_index % palette_columns,
            padx=2,
            pady=3,
            sticky="ew",
        )

        palette_legend_items.append(palette_color_label)

    def update_marker_legend() -> None:
        """Show only the enabled special number categories."""
        visible_count = 0

        for active_category_key, category_label in (
                special_legend_labels.items()
        ):
            if marker_options[active_category_key]:
                category_label.grid(
                    row=visible_count // 3,
                    column=visible_count % 3,
                    padx=5,
                    pady=5,
                    sticky="nsew",
                )

                visible_count += 1

            elif category_label.winfo_manager() == "grid":
                category_label.grid_remove()

        palette_legend_frame.grid_configure(
            row=(visible_count + 2) // 3,
        )

    def update_palette_legend(palette) -> None:
        """Update the color ranges shown in the palette legend."""
        palette_length = len(palette)

        for color_index, palette_range_label in enumerate(
                palette_legend_items
        ):
            start_number = (
                                   color_index * max_number
                                   + palette_length
                                   - 1
                           ) // palette_length + 1

            end_number = (
                                 (color_index + 1) * max_number
                                 + palette_length
                                 - 1
                         ) // palette_length

            palette_range_label.configure(
                text=f"{start_number}-{end_number}",
                background=palette[color_index],
            )

    # Display the initial legends.
    update_marker_legend()
    update_palette_legend(selected_palette)

    # Create the controls on the right.
    controls_frame = ttk.Frame(bottom_frame)

    controls_frame.grid(
        row=0,
        column=1,
        sticky="nsew",
        padx=(5, 0),
    )

    # Create the palette selector.
    ttk.Label(
        controls_frame,
        text="Farbpalette:",
    ).pack(anchor="w")

    palette_display_names = {
        name: get_translation(
            selected_language,
            name.lower(),
        )
        for name in COLOR_PALETTES
    }

    palette_var = tk.StringVar(
        value=palette_display_names[selected_palette_name]
    )

    palette_selector = ttk.Combobox(
        controls_frame,
        textvariable=palette_var,
        values=list(palette_display_names.values()),
        state="readonly",
    )

    palette_selector.pack(
        fill="x",
        pady=(2, 10),
    )

    def change_palette(
            _event: tk.Event[ttk.Combobox],
    ) -> None:
        """Apply the selected palette to the table immediately."""
        nonlocal selected_palette

        selected_name = next(
            (
                name
                for name, display_name in palette_display_names.items()
                if display_name == palette_var.get()
            ),
            None,
        )

        if selected_name is None:
            return

        selected_palette = COLOR_PALETTES[selected_name]

        update_marker_cells()
        update_palette_legend(selected_palette)

    palette_selector.bind(
        "<<ComboboxSelected>>",
        change_palette,
    )

    # Create the table size selector.
    ttk.Label(
        controls_frame,
        text=get_translation(
            selected_language,
            "table_size",
        ),
    ).pack(anchor="w")

    table_size_var = tk.StringVar(
        value=str(table_size)
    )

    table_size_selector = ttk.Combobox(
        controls_frame,
        textvariable=table_size_var,
        values=[
            str(size)
            for size in range(10, 101, 10)
        ],
        state="readonly",
    )

    table_size_selector.pack(
        fill="x",
        pady=(2, 10),
    )

    def change_table_size(
            _event: tk.Event[ttk.Combobox],
    ) -> None:
        """Reopen the table with the newly selected size."""
        selected_table_size = int(
            table_size_var.get()
        )

        if selected_table_size == table_size:
            return

        new_settings = settings.copy()
        new_settings["table_size"] = selected_table_size
        new_settings["marker_options"] = marker_options.copy()

        new_settings["palette"] = next(
            (
                name
                for name, display_name in palette_display_names.items()
                if display_name == palette_var.get()
            ),
            selected_palette_name,
        )

        root.destroy()
        display_multiplication_table(new_settings)

    table_size_selector.bind(
        "<<ComboboxSelected>>",
        change_table_size,
    )

    # Create the special number selector.
    ttk.Label(
        controls_frame,
        text="Besondere Zahlen:",
    ).pack(anchor="w")

    marker_variables = {
        category_key: tk.BooleanVar(
            master=root,
            value=marker_options[category_key],
        )
        for category_key, _ in marker_labels
    }

    def update_marker_selection(category_key: str) -> None:
        """Update one category and refresh the table."""
        marker_options[category_key] = marker_variables[
            category_key
        ].get()

        update_marker_cells()
        update_marker_legend()

    def create_marker_callback(
            category_key: str,
    ) -> Callable[[], None]:
        """Create a callback for a marker category."""

        def callback() -> None:
            update_marker_selection(category_key)

        return callback

    marker_menu = tk.Menu(
        root,
        tearoff=False,
    )

    for category_key, category_text in marker_labels:
        category_color = marker_menu_colors[category_key]

        marker_menu.add_checkbutton(
            label=category_text,
            variable=marker_variables[category_key],
            command=create_marker_callback(category_key),
            background=category_color["background"],
            foreground=category_color["foreground"],
            activebackground=category_color["background"],
            activeforeground=category_color["foreground"],
        )

    # Configure the bold font for the special number selector.
    bold_style = ttk.Style()

    bold_style.configure(
        "Bold.TMenubutton",
        font=("Arial", 11, "bold"),
    )

    marker_selector = ttk.Menubutton(
        controls_frame,
        text="Besondere Zahlen auswählen",
        direction="below",
        menu=marker_menu,
        style="Bold.TMenubutton",
    )

    marker_selector.pack(
        fill="x",
        pady=(2, 0),
    )

    # Resize the window after all widgets have been created.
    root.update_idletasks()
    table_content.update_idletasks()
    bottom_frame.update_idletasks()

    table_width = table_content.winfo_reqwidth()
    table_height = table_content.winfo_reqheight()

    bottom_width = bottom_frame.winfo_reqwidth()
    bottom_height = bottom_frame.winfo_reqheight()

    # Calculate the required window width.
    required_width = max(
        table_width + 40,
        bottom_width + 20,
    )

    window_width = min(
        required_width,
        screen_width - 80,
    )

    # Calculate the required window height.
    required_height = table_height + bottom_height + 50

    window_height = min(
        required_height,
        screen_height - 100,
    )

    # Center the window on the screen.
    window_x = max(
        (screen_width - window_width) // 2,
        0,
    )

    window_y = max(
        (screen_height - window_height) // 2,
        0,
    )

    root.geometry(
        f"{window_width}x{window_height}"
        f"+{window_x}+{window_y}"
    )

    root.minsize(
        min(window_width, 320),
        min(window_height, 220),
    )

    # Keep the table content at its natural size.
    canvas.itemconfigure(
        table_window,
        width=table_width,
        height=table_height,
    )

    # Update the scroll region after the layout is complete.
    root.update_idletasks()
    update_scrollregion()

    # Start the graphical application.
    root.mainloop()
