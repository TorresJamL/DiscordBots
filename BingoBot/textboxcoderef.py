from PIL import Image, ImageDraw, ImageFont

def wrap_text(text:str, font, max_width, draw:ImageDraw):
    """
    Wraps text to fit within the max_width.
    """
    words = text.split()
    lines = [] # Holds each line in the text box
    current_line = [] # Holds each word in the current line under evaluation.

    for word in words:
        # Check the width of the current line with the new word added
        test_line = ' '.join(current_line + [word])
        width = draw.textlength(test_line, font=font)
        if width <= max_width:
            current_line.append(word)
        else:
            # If the line is too wide, finalize the current line and start a new one
            lines.append(' '.join(current_line))
            current_line = [word]

    # Add the last line
    if current_line:
        lines.append(' '.join(current_line))

    return lines

img = Image.new(mode='RGBA', size=(1000, 1000), color=(255, 255, 255, 255))

drawing_ctx = ImageDraw.Draw(img)

# Set text, font, and max width
text = "This is a user profile on dev.to. It contains the user name, profile picture, and bio"
font = ImageFont.truetype("Google_Sans_Code\\static\\GoogleSansCode-Light.ttf", 16)  # Use default font if you don't have this
max_width = 200 # Width for the text box

wrapped_lines = wrap_text(text, font, max_width, drawing_ctx)

# Calculate positions
x, y = 500, 500  # Starting position for the text box
end_x, end_y = x + max_width, y + (24 * int(len(wrapped_lines))) # Ending position for the text box


# Dimensions for the background box
padding = 10
background_box = [(x - padding, y - padding), (end_x + padding, end_y + padding)]

# Draw background box
drawing_ctx.rectangle(background_box, fill="green")

# Draw multiline text
description = ""
for line in wrapped_lines:
    description += line + "\n"

# Draw multiline text.
drawing_ctx.multiline_text((x, y), description, font=font, fill="white", spacing=6)

img.show()

# img.show()
# img.save("BingoBot/test.png", "PNG")
