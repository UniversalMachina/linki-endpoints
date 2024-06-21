from PIL import Image, ImageDraw, ImageFont


def create_icon(output_path):
    icon_size = (160, 160)
    icon = Image.open("icon.png").resize(icon_size).convert("RGBA")
    icon.save(output_path)


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


def add_text(draw, text, font, max_width, image_width, padding, start_y, color="white", icon=None, line_spacing=5):
    wrapped_text = wrap_text(text, font, max_width)
    lines = wrapped_text.split('\n')
    font_size = font.size
    text_height = font_size * len(lines)
    text_x = padding + (icon.size[0] + 70 if icon else 0)
    text_y = start_y

    y = text_y
    for line in lines:
        draw.text((text_x, y), line, font=font, fill=color)
        y += font_size + line_spacing  # Add some spacing between lines

    return text_height + text_y


def add_text_to_image(input_image_path, output_image_path, title, paragraphs, icon_path, padding=150, spacing_between_texts=50):
    image = Image.open(input_image_path).convert("RGBA")
    image = image.resize((int(image.width * 1.5), int(image.height * 1.5)))  # Increase image size by 50%
    image_width, image_height = image.size
    draw = ImageDraw.Draw(image)
    icon = Image.open(icon_path).resize((160, 160)).convert("RGBA")
    font_path = "arial.ttf"
    bold_font_path = "arialbd.ttf"  # Path to bold font

    title_font_size = int(image_height / 15)  # Decrease title size
    paragraph_font_size = int(image_height / 25)  # Increase paragraph font size

    try:
        title_font = ImageFont.truetype(bold_font_path, title_font_size)
        paragraph_font = ImageFont.truetype(font_path, paragraph_font_size)
    except IOError:
        title_font = ImageFont.load_default()
        paragraph_font = ImageFont.load_default()

    max_width = image_width - 2 * padding - icon.size[0] - 70

    start_y = image_height / 6  # Adjusted to provide more padding between title and text

    # Add title
    title_height = add_text(draw, title, title_font, image_width - 2 * padding, image_width, padding, start_y, color="#ff914d")
    current_y = title_height + spacing_between_texts + 50  # Increased space between title and first point

    # Add each paragraph with an icon and additional padding between points
    point_spacing = 30  # Additional spacing between points
    for paragraph in paragraphs:
        image.paste(icon, (padding, int(current_y)), icon)
        paragraph_height = add_text(draw, paragraph, paragraph_font, max_width, image_width, padding, current_y, icon=icon)
        current_y = paragraph_height + spacing_between_texts + point_spacing

    image.save(output_image_path)


def main():
    # Create the icon image
    icon_path = "icon.png"
    create_icon(icon_path)

    # Define paths and text
    input_image_path = "1.png"
    output_image_path = "output_image.png"
    title = "This is the Title"
    paragraphs = [
        "First point. Introduction to the topic.",
        "Second point. Details about the subject.",
        "Third point. Examples and explanations.",
        "Fourth point. Conclusions or next steps."
    ]

    # Add text and icons to the image
    add_text_to_image(input_image_path, output_image_path, title, paragraphs, icon_path)

    # Show the output image
    output_image = Image.open(output_image_path)
    output_image.show()


if __name__ == "__main__":
    main()
