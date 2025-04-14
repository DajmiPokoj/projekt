from PIL import Image, ImageDraw

def render_ves(ves_code):
    width = 800
    height = 600
    img = Image.new("RGB", (width, height), (255, 255, 255))

    def hex2dec(cislo):
        vysledok = 0
        for index in range(len(cislo)):
            cifra = cislo[(index+1)*(-1)].upper()
            if ord("A") <= ord(cifra) <= ord("F"):
                cifra = ord(cifra) - 65 + 10
            else:
                cifra = int(cifra)
            vysledok += cifra * 16 ** index
        return vysledok

    def hexColor(color):
        r = hex2dec(color[1:3])
        g = hex2dec(color[3:5])
        b = hex2dec(color[5:])
        return (r, g, b)

    def boundary_check(x, y, im):
        if x < 0: x = 0
        if y < 0: y = 0
        if x >= im.width: x = im.width - 1
        if y >= im.height: y = im.height - 1
        return x, y

    def line(im, A, B, color):
        A = boundary_check(A[0], A[1], im)
        B = boundary_check(B[0], B[1], im)
        x1, y1 = A
        x2, y2 = B
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy
        while True:
            x1, y1 = boundary_check(x1, y1, im)
            im.putpixel((x1, y1), color)
            if x1 == x2 and y1 == y2:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy
        return line

    def rectangle(im, A, B, color):
        ax, ay = A
        bx, by = B
        line(im, (ax, ay), (bx, ay), color)
        line(im, (bx, ay), (bx, by), color)
        line(im, (bx, by), (ax, by), color)
        line(im, (ax, by), (ax, ay), color)
        return rectangle
    def filled_rectangle(im, A, B, color):
        ax, ay = A
        bx, by = B
        for x in range(min(ax, bx), max(ax, bx) + 1):
            for y in range(min(ay, by), max(ay, by) + 1):
                x, y = boundary_check(x, y, im)
                im.putpixel((x, y), color)
        return filled_rectangle

    def circle(im, S, r, color):
        cx, cy = S
        for x in range(-r, r + 1):
            for y in range(-r, r + 1):
                if x**2 + y**2 <= r**2 + r:
                    if abs(x**2 + y**2 - r**2) <= r:
                        xx, yy = boundary_check(cx + x, cy + y, im)
                        im.putpixel((xx, yy), color)
        return circle

    def filled_circle(im, S, r, color):
        cx, cy = S
        for x in range(-r, r + 1):
            for y in range(-r, r + 1):
                if x**2 + y**2 <= r**2:
                    xx, yy = boundary_check(cx + x, cy + y, im)
                    im.putpixel((xx, yy), color)
        return filled_circle

    def triangle(im, A, B, C, color):
        line(im, A, B, color)
        line(im, B, C, color)
        line(im, C, A, color)
        return triangle

    def filled_triangle(im, A, B, C, color):
        draw = ImageDraw.Draw(im)
        draw.polygon([A, B, C], fill=color)
        return filled_triangle
    try:
        for line_text in ves_code.strip().splitlines():
            parts = line_text.strip().split()
            if not parts:
                continue
            cmd = parts[0].upper()

            if cmd == "LINE":
                x1, y1, x2, y2 = map(int, parts[1:5])
                color = hexColor(parts[-1])
                line(img, (x1, y1), (x2, y2), color)

            elif cmd == "RECT":
                x1, y1, x2, y2 = map(int, parts[1:5])
                color = hexColor(parts[-1])
                rectangle(img, (x1, y1), (x2, y2), color)

            elif cmd == "FILL_RECT":
                x1, y1, w, h = map(int, parts[1:5])
                color = hexColor(parts[-1])
                filled_rectangle(img, (x1, y1), (x1 + w, y1 + h), color)

            elif cmd == "CIRCLE":
                cx, cy, r = map(int, parts[1:4])
                color = hexColor(parts[-1])
                circle(img, (cx, cy), r, color)

            elif cmd == "FILL_CIRCLE":
                cx, cy, r = map(int, parts[1:4])
                color = hexColor(parts[-1])
                filled_circle(img, (cx, cy), r, color)

            elif cmd == "TRIANGLE":
                x1, y1, x2, y2, x3, y3 = map(int, parts[1:7])
                color = hexColor(parts[-1])
                triangle(img, (x1, y1), (x2, y2), (x3, y3), color)

            elif cmd == "FILL_TRIANGLE":
                x1, y1, x2, y2, x3, y3 = map(int, parts[1:7])
                color = hexColor(parts[-1])
                filled_triangle(img, (x1, y1), (x2, y2), (x3, y3), color)


    except Exception as e:
        print(f"❌ Chyba pri vykonávaní VES kódu: {str(e)}")
        return None

    img.show()
    return img
