from flask import Flask, render_template, request, send_file, send_from_directory
from PIL import Image
from io import BytesIO
import math

app = Flask(__name__)

@app.route('/favicon')
def favicon():
    return send_from_directory("./", 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route("/", methods=["GET"])
def home():
    user_agent = request.headers.get('User-Agent')
    if 'Mobile' in user_agent or 'Android' in user_agent or 'iPhone' in user_agent:
        return render_template("phone.html")
    else:
        return render_template("computer.html")
    

@app.route("/collage/horizontal", methods=["POST"])
def horizontal():
    imgs = [Image.open(BytesIO(x.read())) for x in list(request.files.values())]
    borderColor = request.form["color"]
    borderSize = int(request.form["border"])

    minH = min([x.height for x in imgs])
    for image in imgs:
        # TODO : tweak this so it saves the middle and crops out the borders
        if image.height > minH:  
            imgs[imgs.index(image)] = image.resize((image.width - (image.height - minH), minH))

    widths = [x.width for x in imgs]
    heights = [x.height for x in imgs]

    minH = min(heights)
    lastWidth = 0 
    borderHalf = int(borderSize / 2)

    result = Image.new("RGB", (sum(widths) + borderHalf * len(imgs) + borderHalf, minH + borderSize), color=borderColor)

    for img in imgs:    
        result.paste(im=img, box=(lastWidth + borderHalf, borderHalf))
        lastWidth += img.width + borderHalf

        img.close()
    
    img_byte_array = BytesIO()
    result.save(img_byte_array, format='PNG')
    img_byte_array.seek(0)

    return send_file(img_byte_array, mimetype='image/png')


@app.route("/collage/vertical", methods=["POST"])
def vertical():
    imgs = [Image.open(BytesIO(x.read())) for x in list(request.files.values())]
    borderColor = request.form["color"]
    borderSize = int(request.form["border"])
    
    minW = min([x.width for x in imgs])
    for image in imgs:
        # TODO : tweak this so it saves the middle and crops out the borders
        if image.width > minW:
            imgs[imgs.index(image)] = image.resize((minW, image.height - (image.width - minW)))

    lastHeight = 0
    borderHalf = int(borderSize / 2)

    reusltHeight = sum([x.height for x in imgs]) + borderHalf * len(imgs) + borderHalf
    resultWidth = min([x.width for x in imgs]) + borderSize

    result = Image.new("RGB", (resultWidth, reusltHeight), color=borderColor)

    for img in imgs:    
        result.paste(im=img, box=(borderHalf, lastHeight + borderHalf))
        lastHeight += img.height + borderHalf

        img.close()
    
    img_byte_array = BytesIO()
    result.save(img_byte_array, format='PNG')
    img_byte_array.seek(0)

    return send_file(img_byte_array, mimetype='image/png')


@app.route("/collage/box", methods=["POST"])
def random():
    imgs = [Image.open(BytesIO(x.read())) for x in list(request.files.values())]
    borderColor = request.form["color"]
    borderSize = int(request.form["border"])

    minW = min([x.width for x in imgs])
    minH = min([x.height for x in imgs])
    for image in imgs:
        newWidth = round((image.width - minW) / 2)
        newHeight = round((image.height - minH) / 2)

        imgs[imgs.index(image)] = image.crop((newWidth, newHeight, image.width - newWidth, image.height - newHeight))

    borderHalf = int(borderSize / 2)
    lastHeight = 0
    lastWidth = 0

    rows, columns = calculate_grid(len(request.files))

    reusltHeight = rows * minH + borderHalf * rows + borderHalf
    resultWidth = columns * minW + borderHalf * columns + borderHalf

    result = Image.new("RGB", (resultWidth, reusltHeight), color=borderColor)

    imgCntr = 0
    for row in range(1, rows + 1):
        for column in range(columns):
            if len(imgs) - 1 < imgCntr:
                break

            img = imgs[imgCntr]
            result.paste(im=img, box=(lastWidth + borderHalf, lastHeight + borderHalf))
            lastWidth += img.width + borderHalf

            img.close()
            imgCntr += 1

        lastWidth = 0
        lastHeight += row * minH + borderHalf
    
    img_byte_array = BytesIO() 
    result.save(img_byte_array, format='PNG')
    img_byte_array.seek(0)

    return send_file(img_byte_array, mimetype='image/png')
    
def calculate_grid(total_cells):
    square_root = math.sqrt(total_cells)

    closest_integer = round(square_root)

    rows = closest_integer
    columns = closest_integer

    # Adjust rows and columns if necessary
    if rows * columns < total_cells:
        if rows * (columns + 1) >= total_cells:
            columns += 1
        elif (rows + 1) * columns >= total_cells:
            rows += 1
        else:
            rows += 1
            columns += 1

    return rows, columns


if __name__ == "__main__":
    app.run(debug=True)
