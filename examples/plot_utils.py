from io import StringIO
from pathlib import Path

SVG_FOREGROUND = "#1f2328"
SVG_DARK_FOREGROUND = "#f0f6fc"
SVG_PLOT_STYLE = {
    "axes.edgecolor": SVG_FOREGROUND,
    "axes.labelcolor": SVG_FOREGROUND,
    "axes.titlecolor": SVG_FOREGROUND,
    "text.color": SVG_FOREGROUND,
    "xtick.color": SVG_FOREGROUND,
    "ytick.color": SVG_FOREGROUND,
}


def save_svg(fig, output_path: Path) -> None:
    buffer = StringIO()
    fig.savefig(buffer, format="svg", transparent=True)
    svg = buffer.getvalue().replace(SVG_FOREGROUND, "currentColor")
    # Embedded SVG images cannot inherit the page's text color, but they can follow its color scheme.
    theme_style = (
        "<style type=\"text/css\">\n"
        f":root {{ color-scheme: light dark; color: {SVG_FOREGROUND}; }}\n"
        f"@media (prefers-color-scheme: dark) {{ :root {{ color: {SVG_DARK_FOREGROUND}; }} }}\n"
        "</style>\n"
    )
    svg = svg.replace("<defs>", f"<defs>\n{theme_style}", 1)
    output_path.write_text(svg, encoding="utf-8")
