from PIL import Image, ImageDraw, ImageFont


def estimate_text_size(text, font):
    bbox = font.getbbox(text)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    return text_width, text_height


def wrap_text(text, max_chars_per_line):
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        if len(current_line) + len(word) + 1 <= max_chars_per_line:
            current_line += " " + word if current_line else word
        else:
            lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    return "\n".join(lines)


def split_text_with_colors(text):
    parts = []
    current_part = ""
    inside_brackets = False

    for char in text:
        if char == '<':
            if current_part:
                parts.append((current_part, "white"))
            current_part = ""
            inside_brackets = True
        elif char == '>':
            if current_part:
                parts.append((current_part, "pastel_orange"))
            current_part = ""
            inside_brackets = False
        else:
            current_part += char

    if current_part:
        color = "pastel_orange" if inside_brackets else "white"
        parts.append((current_part, color))

    return parts


def add_text_to_image(input_image_path, output_image_path, text, max_chars_per_line=15):
    image = Image.open(input_image_path).convert("RGBA")
    image_width, image_height = image.size
    draw = ImageDraw.Draw(image)

    font_path = "arialbd.ttf"  # Bold version of Arial font
    font_size = int(image_height / 12)

    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        font = ImageFont.load_default()

    wrapped_text = wrap_text(text, max_chars_per_line)
    lines = wrapped_text.split('\n')
    line_height = font_size
    total_text_height = line_height * len(lines)
    max_line_width = max(estimate_text_size(line, font)[0] for line in lines)

    text_x = (image_width - max_line_width) / 2
    text_y = (image_height - total_text_height) / 2

    # pastel_orange = (255, 179, 102)  # Pastel orange color
    pastel_orange="#ff914d"
    y = text_y
    for line in lines:
        x = text_x
        parts = split_text_with_colors(line)
        for part, color in parts:
            fill_color = pastel_orange if color == "pastel_orange" else "white"
            draw.text((x, y), part, font=font, fill=fill_color)
            part_width, _ = estimate_text_size(part, font)
            x += part_width
        y += line_height + 5

    image.save(output_image_path)


def main():
    input_image_path = "1.png"
    output_image_path = "output_image.png"
    text = "This is an <example> of a longer text that needs to be wrapped into multiple lines."
    add_text_to_image(input_image_path, output_image_path, text)
    output_image = Image.open(output_image_path)
    output_image.show()


if __name__ == "__main__":
    main()
