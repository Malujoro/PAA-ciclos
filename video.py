from moviepy.video.io.ImageSequenceClip import ImageSequenceClip
import os

tamanhos = [5, 10]
lista = [f"grafo{num}" for num in tamanhos]

for name in lista:
    # Configurações
    image_folder = f'imagens/{name}'
    output_folder = "videos"
    os.makedirs(output_folder, exist_ok=True)
    output_video = f'{output_folder}/{name}.mp4'
    fps = 1

    # Coleta e ordena as imagens
    images = sorted([
        os.path.join(image_folder, img)
        for img in os.listdir(image_folder)
        if img.endswith(".png")
    ])

    # Cria e exporta o vídeo
    clip = ImageSequenceClip(images, fps=fps)
    clip.write_videofile(output_video, codec='libx264')

    print(f"Vídeo salvo como: {output_video}")
