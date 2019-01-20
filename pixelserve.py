import unicornhat as unicorn
from flask import Flask
from flask import request
from flask import Response

app = Flask(__name__)

unicorn.set_layout(unicorn.AUTO)
unicorn.rotation(0)
unicorn.brightness(1.0)
width, height = unicorn.get_shape()


@app.route("/on")
def turn_on():
    for y in range(height):
        for x in range(width):
            unicorn.set_pixel(x, y, 0, 0, 255)
            unicorn.show()
    return Response(status=204)


@app.route("/lights", methods=['PUT'])
def set_lights():
    req_data = request.get_json()
    x = req_data['x']
    y = req_data['y']
    count = req_data['count']
    data = req_data['data']
    for idx_of_data in range(0, count):
        start_idx = idx_of_data * 6
        r_str = "0x" + data[start_idx:start_idx + 2]
        g_str = "0x" + data[start_idx + 2:start_idx + 4]
        b_str = "0x" + data[start_idx + 4:start_idx + 6]
        r = int(r_str, 16)
        g = int(g_str, 16)
        b = int(b_str, 16)
        unicorn.set_pixel(x, y, r, g, b)
        unicorn.show()
        if x < width-1:
            x = x + 1
        else:
            x = 0
            y = y + 1
    return Response(status=204)


@app.route("/lights", methods=["DELETE"])
def turn_off():
    unicorn.clear()
    unicorn.show()
    return Response(status=204)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
