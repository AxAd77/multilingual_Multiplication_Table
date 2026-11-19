"""Create the settings window for the multiplication table."""

import tkinter as tk
from tkinter import ttk

from .translations import (
    LANGUAGE_NAMES,
    get_translation,
)


def get_settings():
    """Display the settings window and return the selected settings."""
    settings = {}

    root = tk.Tk()
    root.geometry("450x300")
    root.resizable(False, False)

    selected_language = tk.StringVar(value="de")
    selected_table_size = tk.StringVar(value="10")
    selected_palette = tk.StringVar(value="Rainbow")

    palette_names = [
        "Rainbow",
        "Pastel",
        "Ocean",
        "Heatmap",
    ]

    language_names = list(LANGUAGE_NAMES.values())

    language_codes = {
        name: code
        for code, name in LANGUAGE_NAMES.items()
    }

    language_label = ttk.Label(root)
    language_label.grid(
        row=0,
        column=0,
        padx=20,
        pady=10,
        sticky="w",
    )

    language_combobox = ttk.Combobox(
        root,
        values=language_names,
        state="readonly",
        width=25,
    )

    language_combobox.set(
        LANGUAGE_NAMES[selected_language.get()]
    )

    language_combobox.grid(
        row=0,
        column=1,
        padx=20,
        pady=10,
    )

    table_size_label = ttk.Label(root)
    table_size_label.grid(
        row=1,
        column=0,
        padx=20,
        pady=10,
        sticky="w",
    )

    table_size_combobox = ttk.Combobox(
        root,
        values=["10", "20", "30", "50"],
        state="readonly",
        width=25,
        textvariable=selected_table_size,
    )

    table_size_combobox.grid(
        row=1,
        column=1,
        padx=20,
        pady=10,
    )

    color_scheme_label = ttk.Label(root)
    color_scheme_label.grid(
        row=2,
        column=0,
        padx=20,
        pady=10,
        sticky="w",
    )

    color_scheme_combobox = ttk.Combobox(
        root,
        state="readonly",
        width=25,
    )

    color_scheme_combobox.grid(
        row=2,
        column=1,
        padx=20,
        pady=10,
    )

    def start_application():
        """Save the selected settings and close the window."""
        settings["language"] = selected_language.get()

        settings["table_size"] = int(
            selected_table_size.get()
        )

        settings["palette"] = selected_palette.get()

        root.destroy()

    start_button = ttk.Button(
        root,
        command=start_application,
    )

    start_button.grid(
        row=3,
        column=0,
        columnspan=2,
        pady=25,
    )

    def update_language():
        """Update all labels according to the selected language."""
        language = selected_language.get()

        root.title(
            get_translation(
                language,
                "settings_title",
            )
        )

        language_label.config(
            text=get_translation(
                language,
                "language",
            )
        )

        table_size_label.config(
            text=get_translation(
                language,
                "table_size",
            )
        )

        color_scheme_label.config(
            text=get_translation(
                language,
                "color_scheme",
            )
        )

        start_button.config(
            text=get_translation(
                language,
                "start",
            )
        )

        translated_palette_names = [
            get_translation(
                language,
                palette.lower(),
            )
            for palette in palette_names
        ]

        color_scheme_combobox["values"] = (
            translated_palette_names
        )

        selected_palette_index = palette_names.index(
            selected_palette.get()
        )

        color_scheme_combobox.current(
            selected_palette_index
        )

    def change_language():
        """Update the selected language."""
        selected_language_name = language_combobox.get()

        language_code = language_codes[
            selected_language_name
        ]

        selected_language.set(language_code)

        update_language()

    def change_palette():
        """Update the selected color palette."""
        language = selected_language.get()

        selected_palette_name = (
            color_scheme_combobox.get()
        )

        for palette in palette_names:
            translated_name = get_translation(
                language,
                palette.lower(),
            )

            if translated_name == selected_palette_name:
                selected_palette.set(palette)
                break

    language_combobox.bind(
        "<<ComboboxSelected>>",
        lambda unused_event: change_language(),
    )

    color_scheme_combobox.bind(
        "<<ComboboxSelected>>",
        lambda unused_event: change_palette(),
    )

    update_language()

    root.mainloop()

    if settings:
        return settings

    return None
