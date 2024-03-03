from django.shortcuts import render
from django.http import HttpResponse
from .models import Promt
from PIL import Image, ImageDraw, ImageFont
import os


def index(request):
    return render(request, 'main/index.html')


def input_page(request):
    if request.method == 'POST':
        input_text = request.POST.get('input_text')
        Promt.objects.create(text=input_text)

        def create_frame(text, font, width, height, x_offset, y_offset):
            frame = Image.new('RGB', (width, height), (255, 255, 255))
            draw = ImageDraw.Draw(frame)

            draw.text((x_offset, y_offset), text, fill=(0, 0, 0), font=font)

            return frame

        def create_gif(text, output_path, font_size=200, duration=10):
            font = ImageFont.truetype("arial.ttf", font_size)

            width = 500
            height = 500

            text_width, text_height = font.getmask(text).getbbox()[2], font.getmask(text).getbbox()[3]

            x_offset = width
            y_offset = (height - text_height) // 2

            temp_dir = 'temp_frames'
            os.makedirs(temp_dir, exist_ok=True)

            frames = []
            for i in range((width + text_width)//100):
                frame = create_frame(text, font, width, height, x_offset - 100*i, y_offset)
                frames.append(frame)

            frame_paths = []
            for i, frame in enumerate(frames):
                frame_path = os.path.join(temp_dir, f'frame_{i:03d}.png')
                frame.save(frame_path)
                frame_paths.append(frame_path)

            frames[0].save(output_path, format='GIF', append_images=frames[1:], save_all=True, optimize=True,
                           duration=duration, loop=0)

            for frame_path in frame_paths:
                os.remove(frame_path)

        output_path = "running_text.gif"
        create_gif(input_text, output_path)
        gif_path = r'.\running_text.gif'
        with open(gif_path, 'rb') as f:
            gif_data = f.read()

        response = HttpResponse(gif_data, content_type='image/gif')
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(gif_path)}"'
        os.remove(gif_path)
        return response
    else:
        return render(request, 'main/index.html')
