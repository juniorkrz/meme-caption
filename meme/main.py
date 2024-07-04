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

            # Inicializa o tamanho da fonte
            fontSize = 72

            # Carrega a fonte
            font = ImageFont.truetype(font_path, fontSize)

            # Calcula a largura da imagem com margem de 1% para ajuste
            imgWidthWithPadding = img.width * 0.99

            # Reduz o tamanho da fonte até que o texto caiba na imagem
            while draw.textlength(msg, font=font) > imgWidthWithPadding:
                fontSize -= 2
                font = ImageFont.truetype(font_path, fontSize)

            # Divide o texto em linhas
            lines = []
            words = msg.split()
            line = ""
            for word in words:
                if draw.textlength(line + word, font=font) < imgWidthWithPadding:
                    line += word + " "
                else:
                    lines.append(line.strip())
                    line = word + " "
            lines.append(line.strip())

            # Determina a posição inicial do texto baseado na posição desejada
            textY = 10 if pos == "top" else img.height - (len(lines) * (fontSize + 10)) - 10

            # Desenha o texto com sombra
            for line in lines:
                w = draw.textlength(line, font=font)
                h = fontSize
                textX = (img.width - w) / 2

                draw.text((textX-2, textY-2), line, font=font, fill="black")
                draw.text((textX+2, textY-2), line, font=font, fill="black")
                draw.text((textX-2, textY+2), line, font=font, fill="black")
                draw.text((textX+2, textY+2), line, font=font, fill="black")

                draw.text((textX, textY), line, font=font, fill="white")
                textY += h + 10  # Espaçamento entre linhas

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