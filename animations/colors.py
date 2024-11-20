import matplotlib
import matplotlib.pyplot as plt

colors = {
    "blue2": "#0db9d7",
    "black": "#1b1d2b",
    "bg_dark": "#1e2030",
    "bg": "#222436",
    "diff_change": "#252a3f",
    "diff_add": "#273849",
    "bg_visual": "#2d3f76",
    "bg_highlight": "#2f334d",
    "blue7": "#394b70",
    "diff_delete": "#3a273a",
    "fg_gutter": "#3b4261",
    "bg_search": "#3e68d7",
    "green2": "#41a6b5",
    "terminal_black_bright": "#444a73",
    "green1": "#4fd6be",
    "dark3": "#545c7e",
    "border_highlight": "#589ed7",
    "comment": "#636da6",
    "blue1": "#65bcff",
    "dark5": "#737aa2",
    "git_change": "#7ca1f2",
    "fg_dark": "#828bb8",
    "blue": "#82aaff",
    "cyan": "#86e1fc",
    "blue5": "#89ddff",
    "terminal_blue_bright": "#9ab8ff",
    "terminal_cyan_bright": "#b2ebff",
    "blue6": "#b4f9f8",
    "green4": "#b8db87",
    "magenta": "#c099ff",
    "green": "#c3e88d",
    "red": "#c53b53",
    "green3": "#c7fb6d",
    "fg": "#c8d3f5",
    "magenta3": "#caabff",
    "git_delete": "#e26a75",
    "purple": "#fca7ea",
    "magenta2": "#ff007c",
    "purple_orange": "#ff757f",
    "purple2": "#ff8d94",
    "orange": "#ff966c",
    "beige2": "#ffc777",
    "beige": "#ffd8ab",
}

if __name__ == "__main__":
    # Create a figure
    matplotlib.rcParams["toolbar"] = "none"
    fig, ax = plt.subplots(figsize=(8, len(colors)))
    fig.set_facecolor(colors["bg"])
    # ax.set_facecolor(colors["bg"])
    

    # Plot each color as a rectangle
    for i, (name, hex_value) in enumerate(colors.items()):
        ax.add_patch(plt.Rectangle((0, i), 1, 1, color=hex_value))
        ax.text(1.1, i + 0.5, name, va="center", fontsize=12)

    # Set limits and hide axes
    ax.set_xlim(0, 2)
    ax.set_ylim(0, len(colors))
    ax.axis("off")

    plt.title("Color Dictionary Visualization")
    plt.show()
