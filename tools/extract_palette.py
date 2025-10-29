from PIL import Image
import sys

def get_palette(path, num=4):
    im = Image.open(path).convert('RGB')
    im = im.resize((200, 200))
    result = im.convert('P', palette=Image.ADAPTIVE, colors=num)
    palette = result.getpalette()
    color_counts = sorted(result.getcolors(), reverse=True)
    colors = []
    for count, idx in color_counts[:num]:
        r = palette[idx*3]
        g = palette[idx*3+1]
        b = palette[idx*3+2]
        colors.append('#{:02x}{:02x}{:02x}'.format(r,g,b))
    return colors

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Uso: extract_palette.py <imagen> [num]')
        sys.exit(1)
    path = sys.argv[1]
    num = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    cols = get_palette(path, num)
    for c in cols:
        print(c)
