from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

def create_high_res_circular_image(diameter, color):
    large_diameter = diameter * 10
    square_image = Image.new('RGBA', (large_diameter, large_diameter), (0, 0, 0, 0))

    draw = ImageDraw.Draw(square_image)
    draw.ellipse((0, 0, large_diameter, large_diameter), fill=color)

    circular_image = square_image.resize((diameter, diameter), Image.LANCZOS)
    circle_image_path = 'high_res_circular_image.png'
    circular_image.save(circle_image_path)

    return circle_image_path

def render_icon_name_tag(banner_image, draw, circle_image, display_name, username, circle_position, text_x_offset,
                         font_display_name, font_username, text_color, sub_text_color):
    banner_image.paste(circle_image, circle_position, circle_image)

    display_name_position = (text_x_offset, circle_position[1])
    username_position = (text_x_offset, circle_position[1] + 50)

    draw.text(display_name_position, display_name, font=font_display_name, fill=text_color)
    draw.text(username_position, username, font=font_username, fill=sub_text_color)

def get_text_width_approx(text, font_size):
    avg_char_width = font_size * 0.5
    return int(avg_char_width * len(text))

def render_tweet_text(draw, tweet_text, tweet_text_position, font_tweet, banner_width, text_color):
    tweet_text = tweet_text.replace(". ", ".\n\n")

    lines = tweet_text.split('\n')
    wrapped_lines = []

    for line in lines:
        words = line.split()
        current_line = []

        for word in words:
            current_line.append(word)
            w = get_text_width_approx(' '.join(current_line), font_tweet.size)
            if w > banner_width - 20:
                current_line.pop()
                wrapped_lines.append(' '.join(current_line))
                current_line = [word]

        wrapped_lines.append(' '.join(current_line))

    y = tweet_text_position[1]
    for line in wrapped_lines:
        draw.text((tweet_text_position[0], y), line, font=font_tweet, fill=text_color)
        y += font_tweet.size + 15

    return y, len(wrapped_lines)

def render_tweet_info(draw, tweet_time, time_position, font_time, sub_text_color):
    draw.text(time_position, tweet_time, font=font_time, fill=sub_text_color)

def create_twitter_banner(circle_image_path, display_name, username, tweet_text, tweet_time, mode='light'):
    circle_image = Image.open(circle_image_path).convert("RGBA")
    circle_size = circle_image.size[0]

    initial_banner_height = 1000
    banner_width = 1200

    if mode == 'dark':
        background_color = (18, 27, 38)
        text_color = (255, 255, 255)
        sub_text_color = (150, 150, 150)
    else:
        background_color = (255, 255, 255)
        text_color = (0, 0, 0)
        sub_text_color = (100, 100, 100)

    temp_image = Image.new("RGB", (banner_width, initial_banner_height), background_color)
    temp_draw = ImageDraw.Draw(temp_image)

    font_path_bold = "HelveticaNeue-Bold.ttf"
    font_path_regular = "arial.ttf"
    font_size_display_name = 36
    font_size_username = 28
    font_size_tweet = 36
    font_size_time = 24

    try:
        font_display_name = ImageFont.truetype(font_path_bold, font_size_display_name)
        font_username = ImageFont.truetype(font_path_regular, font_size_username)
        font_tweet = ImageFont.truetype(font_path_regular, font_size_tweet)
        font_time = ImageFont.truetype(font_path_regular, font_size_time)
    except IOError:
        font_display_name = ImageFont.load_default()
        font_username = ImageFont.load_default()
        font_tweet = ImageFont.load_default()
        font_time = ImageFont.load_default()

    circle_position = (20, 60)
    text_x_offset = circle_size + 40
    tweet_text_position = (40, circle_size + 100)

    tweet_end_y, num_lines = render_tweet_text(temp_draw, tweet_text, tweet_text_position, font_tweet, banner_width, text_color)

    new_banner_height = max(tweet_end_y + font_size_time + 60, initial_banner_height)

    banner_image = Image.new("RGB", (banner_width, new_banner_height), background_color)
    draw = ImageDraw.Draw(banner_image)

    center_y = (new_banner_height - circle_size - (tweet_end_y - circle_position[1])) // 2

    circle_position = (20, center_y)
    text_x_offset = circle_size + 40
    tweet_text_position = (40, center_y + circle_size + 40)

    render_icon_name_tag(banner_image, draw, circle_image, display_name, username, circle_position, text_x_offset,
                         font_display_name, font_username, text_color, sub_text_color)

    tweet_end_y, num_lines = render_tweet_text(draw, tweet_text, tweet_text_position, font_tweet, banner_width, text_color)

    time_position = (20, tweet_end_y + 20)
    render_tweet_info(draw, tweet_time, time_position, font_time, sub_text_color)

    twitter_banner_path = 'high_res_twitter_banner.png'
    banner_image.save(twitter_banner_path)

    return twitter_banner_path

def main():
    circle_diameter = 100
    background_color = (73, 109, 137)
    display_name = "Your Name"
    username = "@yourusername"
    tweet_text = "This is an example tweet showing how the banner will look when the text wraps to a new line if it goes past the width of the image. It is important to see how it centers and adjusts."

    now = datetime.now()
    tweet_time = now.strftime("%I:%M %p · %b %d, %Y")

    circular_image_path = create_high_res_circular_image(circle_diameter, background_color)

    # Toggle between 'light' and 'dark' mode
    mode = 'light'  # Change to 'light' for light mode

    twitter_banner_path = create_twitter_banner(circular_image_path, display_name, username, tweet_text, tweet_time, mode)

    banner_image = Image.open(twitter_banner_path)
    banner_image.show()

if __name__ == "__main__":
    main()
