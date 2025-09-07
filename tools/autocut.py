from PIL import Image
import os

main_sprite = r"Z:\Grand-Route\assets\tiles\water\1.png"
sprite_sheet = Image.open(main_sprite)
sheet_width, sheet_height = sprite_sheet.size

# Kích thước từng sprite
sprite_w, sprite_h = 64, 64

# Thư mục lưu output
output_folder = os.path.dirname(main_sprite) + "/"
print(output_folder)
os.makedirs(output_folder, exist_ok=True)
image_name = os.path.splitext(os.path.basename(main_sprite))[0]

count = 1
for row in range(0, sheet_height, sprite_h):
    for col in range(0, sheet_width, sprite_w):
        box = (col, row, col + sprite_w, row + sprite_h)
        sprite = sprite_sheet.crop(box)
        sprite.save(f"{output_folder}{image_name}{count}.png")
        count += 1

print(f"✅ Đã cắt {count} sprites vào thư mục {output_folder}")
