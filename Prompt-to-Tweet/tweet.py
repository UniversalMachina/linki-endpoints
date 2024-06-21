from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

def create_high_res_circular_image(diameter, color):
    # Create a larger square image for high resolution
    large_diameter = diameter * 10  # Scale up by a factor of 10
    square_image = Image.new('RGBA', (large_diameter, large_diameter), (255, 255, 255, 0))

    # Initialize ImageDraw
    draw = ImageDraw.Draw(square_image)

    # Draw a filled circle
    draw.ellipse((0, 0, large_diameter, large_diameter), fill=color)

    # Scale down to the desired size
    circular_image = square_image.resize((diameter, diameter), Image.LANCZOS)

    # Save the circular image
    circle_image_path = 'high_res_circular_image.png'
    circular_image.save(circle_image_path)

    return circle_image_path

def render_icon_name_tag(banner_image, draw, circle_image, display_name, username, circle_position, text_x_offset,
                         font_display_name, font_username):
    # Paste the circular image on the banner
    banner_image.paste(circle_image, circle_position, circle_image)

    # Define text positions
    display_name_position = (text_x_offset, circle_position[1])  # Adjusted position for display name
    username_position = (text_x_offset, circle_position[1] + 50)  # Further adjusted position for username

    # Add display name and username to the banner
    draw.text(display_name_position, display_name, font=font_display_name, fill=(0, 0, 0))
    draw.text(username_position, username, font=font_username, fill=(100, 100, 100))

def get_text_width_approx(text, font_size):
    # Approximate the width of each character based on the font size
    avg_char_width = font_size * 0.5  # Average width of characters
    return int(avg_char_width * len(text))

def render_tweet_text(draw, tweet_text, tweet_text_position, font_tweet, banner_width):
    # Replace ". " with ".\n\n" only if not at the end of the string
    tweet_text = tweet_text.replace(". ", ".\n\n")

    # Wrap tweet text to fit within the banner width
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

    # Draw each line of text
    y = tweet_text_position[1]
    for line in wrapped_lines:
        draw.text((tweet_text_position[0], y), line, font=font_tweet, fill=(0, 0, 0))
        y += font_tweet.size + 15  # Adding a larger gap between lines for the double line break

    return y, len(wrapped_lines)  # Return the y position after the last line and number of lines

def render_tweet_info(draw, tweet_time, time_position, font_time):
    # Add tweet time to the banner
    draw.text(time_position, tweet_time, font=font_time, fill=(100, 100, 100))

def create_twitter_banner(circle_image_path, display_name, username, tweet_text, tweet_time):
    # Open the circular image
    circle_image = Image.open(circle_image_path).convert("RGBA")
    circle_size = circle_image.size[0]

    # Define the initial height for the banner
    initial_banner_height = 1000  # Set initial height to 1000px
    banner_width = 1200  # Updated banner width

    # Initialize ImageDraw for a temporary image to calculate text dimensions
    temp_image = Image.new("RGB", (banner_width, initial_banner_height), (255, 255, 255))
    temp_draw = ImageDraw.Draw(temp_image)

    # Define text and font
    font_path_bold = "HelveticaNeue-Bold.ttf"  # Path to bold font
    font_path_regular = "arial.ttf"  # Path to regular font
    font_size_display_name = 36  # Adjusted for larger banner
    font_size_username = 28  # Adjusted for larger banner
    font_size_tweet = 36  # Adjusted for larger banner
    font_size_time = 24  # Adjusted for larger banner

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

    # Define positions
    circle_position = (20, 60)  # Adding more padding to the top
    text_x_offset = circle_size + 40
    tweet_text_position = (40, circle_size + 100)

    # Calculate tweet text position and number of lines
    tweet_end_y, num_lines = render_tweet_text(temp_draw, tweet_text, tweet_text_position, font_tweet, banner_width)

    # Calculate the new height of the banner based on the number of lines in the tweet text
    new_banner_height = max(tweet_end_y + font_size_time + 60, initial_banner_height)  # Ensure minimum height of 1000px

    # Create a new image for the Twitter banner with the calculated height
    banner_image = Image.new("RGB", (banner_width, new_banner_height), (255, 255, 255))
    draw = ImageDraw.Draw(banner_image)

    # Calculate the vertical center position
    center_y = (new_banner_height - circle_size - (tweet_end_y - circle_position[1])) // 2

    # Update positions to be centered vertically
    circle_position = (20, center_y)
    text_x_offset = circle_size + 40
    tweet_text_position = (40, center_y + circle_size + 40)

    # Render icon, name, and tag
    render_icon_name_tag(banner_image, draw, circle_image, display_name, username, circle_position, text_x_offset,
                         font_display_name, font_username)

    # Render tweet text and get the ending y position
    tweet_end_y, num_lines = render_tweet_text(draw, tweet_text, tweet_text_position, font_tweet, banner_width)

    # Render tweet info
    time_position = (20, tweet_end_y + 20)  # Add some padding after the tweet text
    render_tweet_info(draw, tweet_time, time_position, font_time)

    # Save the Twitter banner image
    twitter_banner_path = 'high_res_twitter_banner.png'
    banner_image.save(twitter_banner_path)

    return twitter_banner_path

# Main function to execute the steps
def main():
    # Parameters
    circle_diameter = 100  # Larger diameter for the icon
    background_color = (73, 109, 137)  # A blue shade
    display_name = "Your Name"
    username = "@yourusername"
    tweet_text = "This is an example twethe width of the image. owing hample twethe width of the image. owing how the banner will look when the text wraps to a new line if it goes past the widtample twethe width of the image. owing how the banner will look when the text wraps to a new line if it goes past the widtow the banner will look when the text wraps to a new line if it goes past the width of the image. It is important to see how it centers and adjusts."

    # Get current date and time
    now = datetime.now()
    tweet_time = now.strftime("%I:%M %p · %b %d, %Y")

    # Create high resolution circular image
    circular_image_path = create_high_res_circular_image(circle_diameter, background_color)

    # Create high resolution Twitter banner
    twitter_banner_path = create_twitter_banner(circular_image_path, display_name, username, tweet_text, tweet_time)

    # Show the Twitter banner image
    banner_image = Image.open(twitter_banner_path)
    banner_image.show()

# Execute the main function
if __name__ == "__main__":
    main()
