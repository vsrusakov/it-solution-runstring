import cv2
import numpy as np
import argparse
import os


parser = argparse.ArgumentParser(description="Скрипт для создания видео (.mp4) с бегущей строкой")
parser.add_argument("--text", type=str, default="Hello, world!", help="Текст бегущей строки (default='Hello, world!')")
parser.add_argument("--fps", type=int, default=24, help="Число кадров в секунду (default=24)")
parser.add_argument("--outdir", type=str, default=".", help="Каталог для сохранения видео (default='.')")
parser.add_argument("--name", type=str, default="runstring", help="Имя видеофайла (default='runstring')")

args = parser.parse_args()

# задаем параметры для отображения текста и записи видео
text = args.text
fps = args.fps
path_to_save = args.outdir.rstrip("/")
video_path = os.path.join(path_to_save, args.name + ".mp4")
font_face = cv2.FONT_HERSHEY_COMPLEX
font_scale = 10.0
thickness = 14
fourcc = cv2.VideoWriter.fourcc('m', 'p', '4', 'v')

# определяем размеры и цвет фонового изображения (background image)
(width, higth), _ = cv2.getTextSize(text, font_face, font_scale, thickness)
bg_w, bg_h = higth + width, 2 * higth
bg_img = np.zeros((bg_h, bg_w, 3), np.uint8)
bg_img[:,:,0] = 153 # blue channel 
bg_img[:,:,2] = 153 # red channel 

# накладываем текст на фоновое изображение и приводим к нужному размеру
org = (int(higth / 2), int(3 * higth / 2))
img_w_text = cv2.putText(bg_img, text, org, font_face, font_scale, (255, 255, 255), thickness)
target_img = cv2.resize(img_w_text, (int(100 * bg_w / bg_h), 100))

# создаем VideoWriter и записываем кадры
num_frames = fps * 3
step = (int(100 * bg_w / bg_h) - 100) / num_frames
video = cv2.VideoWriter(video_path, fourcc, fps, (100, 100))

for i in range(num_frames):
    window_start = round(step * i)
    frame = target_img[:,window_start:window_start + 100]
    video.write(frame)

video.release()
