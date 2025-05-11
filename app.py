from flask import Flask, render_template, request, send_file
import math
import matplotlib.pyplot as plt
import numpy as np
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        try:
            a = float(request.form['a'])
            b = float(request.form['b'])
            c = float(request.form['c'])

            if a == 0:
                result = {"error": "This is not a parabola (a cannot be 0)."}
            else:
                x_vertex = -b / (2 * a)
                y_vertex = a * x_vertex**2 + b * x_vertex + c
                vertex = (x_vertex, y_vertex)
                direction = "upward" if a > 0 else "downward"
                discriminant = b**2 - 4*a*c

                if discriminant > 0:
                    root1 = (-b + math.sqrt(discriminant)) / (2*a)
                    root2 = (-b - math.sqrt(discriminant)) / (2*a)
                    roots = [root1, root2]
                    root_info = "Two real roots"
                elif discriminant == 0:
                    root = -b / (2*a)
                    roots = [root]
                    root_info = "One real root"
                else:
                    roots = []
                    root_info = "No real roots"

                # Plotting
                x_vals = np.linspace(x_vertex - 10, x_vertex + 10, 400)
                y_vals = a * x_vals**2 + b * x_vals + c

                plt.figure(figsize=(6, 4))
                plt.plot(x_vals, y_vals, label=f"y = {a}x² + {b}x + {c}")
                plt.plot(x_vertex, y_vertex, 'ro', label="Vertex")
                for i, r in enumerate(roots):
                    plt.plot(r, 0, 'go' if i == 0 else 'go')
                plt.axvline(x_vertex, color='gray', linestyle='--', label="Axis of symmetry")
                plt.axhline(0, color='black')
                plt.axvline(0, color='black')
                plt.grid(True)
                plt.legend()
                plt.tight_layout()
                graph_path = 'static/parabola_plot.png'
                plt.savefig(graph_path)
                plt.close()

                result = {
                    "a": a, "b": b, "c": c,
                    "vertex": vertex,
                    "axis": x_vertex,
                    "direction": direction,
                    "discriminant": discriminant,
                    "root_info": root_info,
                    "roots": roots,
                    "graph_url": graph_path
                }
        except ValueError:
            result = {"error": "Please enter valid numbers."}
    return render_template('index.html', result=result)

if __name__ == '__main__':
    os.makedirs("static", exist_ok=True)
    app.run(debug=True)
