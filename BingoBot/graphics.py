from PIL import Image, ImageDraw, ImageFont

class CardGraphic:
    @staticmethod
    def find_max_width(grid:list[list]):
        max_width = 0
        for row in grid:
            for col in row:
                max_width = len(col.sq_val) if len(col.sq_val) > max_width else max_width
        return max_width
    
    @staticmethod
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

    @staticmethod
    def generate_image(grid:list[list]):
        max_width = 300 # CardGraphic.find_max_width(grid)
        img_size, img_color = (max_width * len(grid), max_width * len(grid)), (255,255,255)

        img = Image.new(mode='RGB', size=img_size, color=img_color)
        drawing_ctx = ImageDraw.Draw(img)
        x, y = 0, 0
        for i in range(len(grid)):
            for j in range(len(grid)):
                if not grid[i][j].state: 
                    font = ImageFont.truetype("Google_Sans_Code\\static\\GoogleSansCode-Bold.ttf", 20)
                else: 
                    font = ImageFont.truetype("Google_Sans_Code\\static\\GoogleSansCode-Light.ttf", 20)
                wrapped_text = CardGraphic.wrap_text(grid[i][j].sq_val, font, max_width, drawing_ctx)
                end_x, end_y = x + max_width, y + max_width

                background_box = [(x, y), 
                                  (end_x, end_y)]
                if grid[i][j].state:
                    drawing_ctx.rectangle(background_box, 
                                        fill="white", 
                                        outline="black", width=2)
                else:
                    drawing_ctx.rectangle(background_box, 
                                        fill="red", 
                                        outline="black", width=2)

                contents = ""
                for t in wrapped_text:
                    contents += t + "\n"

                text = "\n".join(wrapped_text)

                drawing_ctx.multiline_textbbox((0, 0), text, font=font, spacing=6)

                center_x = x + max_width // 2
                center_y = y + max_width // 2

                drawing_ctx.multiline_text(
                    (center_x, center_y),
                    text,
                    font=font,
                    fill="black",
                    spacing=6,
                    align="center",
                    anchor="mm" 
                ) 
                
                x += max_width
            x = 0
            y += max_width
        
        img.show()