from PIL import Image, ImageDraw, ImageFont


def estimate_text_size(text, font):
    draw = ImageDraw.Draw(Image.new('RGB', (1, 1)))
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
    return text_width, text_height


def wrap_text(text, font, max_width):
    words = text.split()
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + " " + word if current_line else word
        test_line_size = estimate_text_size(test_line, font)[0]
        if test_line_size <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word

    if current_line:
        lines.append(current_line)

    return "\n".join(lines)


def add_text(draw, text, font, max_width, image_width, padding, start_y, color):
    wrapped_text = wrap_text(text, font, max_width)
    lines = wrapped_text.split('\n')
    font_size = font.size
    text_height = font_size * len(lines)
    text_x = padding
    text_y = start_y

    y = text_y
    for line in lines:
        draw.text((text_x, y), line, font=font, fill=color)
        y += font_size + 5  # Add some spacing between lines

    return text_height + text_y


def add_text_to_image(input_image_path, output_image_path, large_text, small_text, padding=100, spacing_between_texts=50):
    image = Image.open(input_image_path).convert("RGBA")
    image_width, image_height = image.size
    draw = ImageDraw.Draw(image)
    large_font_path = "arialbd.ttf"  # Bold version of Arial font
    small_font_path = "arial.ttf"

    large_font_size = int(image_height / 12)
    small_font_size = int(image_height / 20)

    try:
        large_font = ImageFont.truetype(large_font_path, large_font_size)
        small_font = ImageFont.truetype(small_font_path, small_font_size)
    except IOError:
        large_font = ImageFont.load_default()
        small_font = ImageFont.load_default()

    max_width_large = image_width - 2 * padding
    max_width_small = image_width - 2 * padding

    start_y = (image_height - (large_font_size * len(wrap_text(large_text, large_font, max_width_large).split('\n')) + small_font_size * len(wrap_text(small_text, small_font, max_width_small).split('\n')) + spacing_between_texts)) / 2

    large_text_height = add_text(draw, large_text, large_font, max_width_large, image_width, padding, start_y, "white")
    add_text(draw, small_text, small_font, max_width_small, image_width, padding, large_text_height + spacing_between_texts, "#ff914d")  # Pastel orange color

    image.save(output_image_path)


def main():
    input_image_path = "1.png"
    output_image_path = "output_image.png"
    large_text = "This is an example of a paragraph with larger text."
    small_text = "This is a smaller text that follows the larger paragraph."

    add_text_to_image(input_image_path, output_image_path, large_text, small_text)

    output_image = Image.open(output_image_path)
    output_image.show()


if __name__ == "__main__":
    main()
