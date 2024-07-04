import os
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import FileResponse
from PIL import Image, ImageDraw, ImageFont
import tempfile

app = FastAPI()

font_path = os.path.join(os.path.dirname(__file__), 'impact.ttf')

def add_text_to_image(image_path, top_text=None, bottom_text=None):
    try:
        img = Image.open(image_path)
        draw = ImageDraw.Draw(img)

        def draw_text(msg, pos):
            print(f"Drawing text: {msg}, Position: {pos}")

            # Initialize font size
            font_size = 72

            # Load font
            font = ImageFont.truetype(font_path, font_size)

            # Calculate image width with 1% padding adjustment
            img_width_with_padding = img.width * 0.99

            # Reduce font size until text fits within the image
            while draw.textlength(msg, font=font) > img_width_with_padding:
                font_size -= 2
                font = ImageFont.truetype(font_path, font_size)

            # Split text into lines
            lines = []
            words = msg.split()
            line = ""
            for word in words:
                if draw.textlength(line + word, font=font) < img_width_with_padding:
                    line += word + " "
                else:
                    lines.append(line.strip())
                    line = word + " "
            lines.append(line.strip())

            # Determine initial text position based on desired position
            text_y = 10 if pos == "top" else img.height - (len(lines) * (font_size + 10)) - 10

            # Draw text with shadow
            for line in lines:
                w = draw.textlength(line, font=font)
                h = font_size
                text_x = (img.width - w) / 2

                for dx, dy in [(-2, -2), (2, -2), (-2, 2), (2, 2)]:
                    draw.text((text_x + dx, text_y + dy), line, font=font, fill="black")

                draw.text((text_x, text_y), line, font=font, fill="white")
                text_y += h + 10  # Line spacing

        if top_text:
            draw_text(top_text.upper(), "top")

        if bottom_text:
            draw_text(bottom_text.upper(), "bottom")

        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
        img.save(temp_file.name)
        temp_file.close()

        return temp_file.name

    except Exception as e:
        print(f"Error adding text to image: {str(e)}")
        return None

@app.post("/addCaption")
async def add_text(topText: str = Form(None), bottomText: str = Form(...), file: UploadFile = File(...)):
    try:
        temp_image = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
        with open(temp_image.name, "wb") as f:
            f.write(file.file.read())

        modified_image_path = add_text_to_image(temp_image.name, topText, bottomText)

        if modified_image_path:
            return FileResponse(modified_image_path, media_type="image/jpeg")

        raise HTTPException(status_code=500, detail="Error processing image")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
