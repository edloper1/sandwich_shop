#!/usr/bin/env python
"""
Script sencillo para aplicar la línea gráfica (overlay UI + watermark logo)
a las imágenes dentro de `media/Nproductos` y guardar resultado .jpg en
`media/productos`.

Comportamiento:
- Toma cada imagen de la carpeta de entrada, mantiene la relación de aspecto
  y la redimensiona si supera `max_width`.
- Aplica `ui` como overlay (blend) sobre la imagen de producto.
- Pega el `logo` en la esquina inferior derecha como marca de agua.
- Guarda como JPEG de alta calidad en la carpeta de salida con el mismo
  nombre base.

Uso:
python apply_ui_to_images.py --input media/Nproductos --output media/productos
    --logo media/Nproductos/logo.jpg --ui media/Nproductos/ui.jpg

Requisitos: Pillow (ya está en requirements.txt)
"""
from PIL import Image, ImageEnhance
import os
import argparse


def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)


def process_image(path, out_dir, logo_path, ui_path, blend=0.18, logo_scale=0.15, max_width=1200):
    base_name = os.path.splitext(os.path.basename(path))[0]
    out_path = os.path.join(out_dir, f"{base_name}.jpg")

    try:
        with Image.open(path).convert('RGBA') as im:
            # Resize to max_width preserving aspect ratio
            w, h = im.size
            if max_width and w > max_width:
                new_h = int(h * (max_width / w))
                im = im.resize((max_width, new_h), Image.LANCZOS)

            # Open UI overlay and resize to match
            if ui_path and os.path.exists(ui_path):
                with Image.open(ui_path).convert('RGBA') as ui:
                    ui_resized = ui.resize(im.size, Image.LANCZOS)
                    # Blend UI on top of image
                    im = Image.blend(im, ui_resized, alpha=blend)

            # Add logo watermark
            if logo_path and os.path.exists(logo_path):
                with Image.open(logo_path).convert('RGBA') as logo:
                    lw, lh = logo.size
                    target_w = int(im.size[0] * logo_scale)
                    # preserve aspect ratio
                    if lw != target_w:
                        new_logo_h = int(lh * (target_w / lw))
                        logo = logo.resize((target_w, new_logo_h), Image.LANCZOS)

                    # position: bottom-right with margin
                    margin = int(im.size[0] * 0.03)
                    pos = (im.size[0] - logo.size[0] - margin, im.size[1] - logo.size[1] - margin)
                    # ensure logo has some transparency
                    if logo.mode != 'RGBA':
                        logo = logo.convert('RGBA')
                    im.paste(logo, pos, logo)

            # Convert to RGB and save as JPG
            rgb = im.convert('RGB')
            rgb.save(out_path, format='JPEG', quality=92)
            print(f"Guardado: {out_path}")
    except Exception as e:
        print(f"Error procesando {path}: {e}")


def main():
    parser = argparse.ArgumentParser(description='Aplicar línea gráfica a imágenes de productos')
    parser.add_argument('--input', '-i', required=True, help='Carpeta con imágenes de entrada')
    parser.add_argument('--output', '-o', required=True, help='Carpeta de salida para JPG')
    parser.add_argument('--logo', help='Ruta al archivo logo (PNG/JPG)')
    parser.add_argument('--ui', help='Ruta al archivo ui (imagen) para overlay')
    parser.add_argument('--blend', type=float, default=0.18, help='Alpha blending para ui overlay (0-1)')
    parser.add_argument('--logo-scale', type=float, default=0.15, help='Proporción del ancho de la imagen para el logo (0-1)')
    parser.add_argument('--max-width', type=int, default=1200, help='Ancho máximo para redimensionar')

    args = parser.parse_args()

    in_dir = args.input
    out_dir = args.output
    ensure_dir(out_dir)

    # iterate files
    for fname in os.listdir(in_dir):
        if fname.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.bmp', '.tiff')):
            # skip logo and ui if they are in same folder
            if args.logo and os.path.abspath(os.path.join(in_dir, fname)) == os.path.abspath(args.logo):
                continue
            if args.ui and os.path.abspath(os.path.join(in_dir, fname)) == os.path.abspath(args.ui):
                continue

            src = os.path.join(in_dir, fname)
            process_image(src, out_dir, args.logo, args.ui, blend=args.blend, logo_scale=args.logo_scale, max_width=args.max_width)


if __name__ == '__main__':
    main()
