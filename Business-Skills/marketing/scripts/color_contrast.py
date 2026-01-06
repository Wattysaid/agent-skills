#!/usr/bin/env python3
import argparse


def hex_to_rgb(value):
    value = value.lstrip("#")
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))


def luminance(rgb):
    def channel(c):
        c = c / 255.0
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (channel(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast_ratio(rgb1, rgb2):
    l1 = luminance(rgb1)
    l2 = luminance(rgb2)
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


def main():
    parser = argparse.ArgumentParser(description="Compute WCAG contrast ratio.")
    parser.add_argument("--fg", required=True, help="Foreground hex color")
    parser.add_argument("--bg", required=True, help="Background hex color")
    args = parser.parse_args()

    ratio = contrast_ratio(hex_to_rgb(args.fg), hex_to_rgb(args.bg))
    print("Contrast ratio")
    print(f"{ratio:.2f}:1")
    if ratio >= 7:
        print("Rating: AAA")
    elif ratio >= 4.5:
        print("Rating: AA")
    else:
        print("Rating: Fail")


if __name__ == "__main__":
    main()
