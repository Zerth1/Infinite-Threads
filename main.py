from enum import Enum, auto
from typing import *
from pyray import *
from sympy import *
import matplotlib.pyplot as plt
import matplotlib as mpl
import os
import json
import math
import random
import user_interface
RESOLUTION_X = 1450 # No Touchie
RESOLUTION_Y = 800 # No Touchie
RESOLUTION_MULTIPLIER = 1.0 # Touch Me

ACTUAL_RESOLUTION_X = int(RESOLUTION_X * RESOLUTION_MULTIPLIER)
ACTUAL_RESOLUTION_Y = int(RESOLUTION_Y * RESOLUTION_MULTIPLIER)
SETTINGS = {
    "MatrixDimension": 2
}
init_window(ACTUAL_RESOLUTION_X, ACTUAL_RESOLUTION_Y, "Infinite-Threads")
set_target_fps(get_monitor_refresh_rate(get_current_monitor()))
if os.path.getsize("settings_data.json") == 0:
    with open("settings_data.json", "w") as settings_file:
        settings_file.write(json.dumps(SETTINGS, indent=4))
with open("settings_data.json", "r") as file:
    settings_data = json.load(file)
is_generating = False
is_playing = False
is_settings = False
entered_settings = False
deep_settings = False
def scale_UI(quantity: float):
    return int(RESOLUTION_MULTIPLIER * quantity)
settings_buttons = {}
settings_buttons["matrix_dimension"] = user_interface.InputButton("Matrix Dimension:", scale_UI(25), Rectangle(scale_UI(50 + measure_text("Matrix Dimension:", 25) + 10), scale_UI(75), scale_UI(measure_text("0", 25)), scale_UI(25)))
settings_buttons["matrix_dimension"].text = str(settings_data["MatrixDimension"])
matrix_to_solve = []
def reset_game():
    global matrix_to_solve
    matrix_to_solve = []
def latex_to_png(latex_string, output_filename):
    mpl.rcParams['font.size'] = 20
    mpl.rcParams['text.usetex'] = True
    mpl.rcParams['text.latex.preamble'] = r'\usepackage{{amsmath}}'
    fig, ax = plt.subplots(figsize=(1 * RESOLUTION_MULTIPLIER, 0.33 * RESOLUTION_MULTIPLIER))
    ax.text(0.5, 0.5, f'${latex_string}$', fontsize=scale_UI(5), ha='center', va='center', color='white')
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')
    ax.axis('off')
    plt.savefig(output_filename, dpi=300, bbox_inches='tight')
    plt.close(fig)
matrix_texture = ""
while not window_should_close():
    begin_drawing()
    clear_background(BLACK)
    if is_generating:
        is_generating = False
        for i in range(settings_data["MatrixDimension"]):
            matrix_to_solve.append([])
            for j in range(settings_data["MatrixDimension"]):
                matrix_to_solve[-1].append(random.randint(-9, 9))
        latex_code = r"\left[\begin{matrix}-4 & 5\\5 & 1\end{matrix}\right]"
        latex_to_png(latex(Matrix(matrix_to_solve)), "to_solve.png")
        matrix_texture = load_texture("to_solve.png")
    if is_settings:
        pass
    else:
        draw_text("[Space] Start/Stop", scale_UI(int(RESOLUTION_X / 2) - int(measure_text("[Space] Start/Stop", 50) / 2)), scale_UI(int(0.85 * (RESOLUTION_Y))), scale_UI(50), WHITE)
        if is_playing:
            draw_texture_ex(matrix_texture, Vector2(scale_UI((RESOLUTION_X / 2) - (matrix_texture.width / 2)), scale_UI((RESOLUTION_Y / 2) - (matrix_texture.height / 2))), 0.0, max(1.0, scale_UI(1.0)), WHITE)
        else:
            draw_text("[S] Settings", scale_UI(50), scale_UI(30), scale_UI(25), WHITE)
        if is_key_pressed(KeyboardKey.KEY_SPACE):
            if not is_playing:
                is_generating = True
                reset_game()
            is_playing = not is_playing
    if not is_playing and is_key_pressed(KeyboardKey.KEY_S):
        reset_game()
        is_settings = not is_settings
        settings_buttons["matrix_dimension"].toggle()
        settings_data["MatrixDimension"] = max(int(settings_buttons["matrix_dimension"].text), 2)
        with open("settings_data.json", "w") as file:
            json.dump(settings_data, file)
    for settings_object in settings_buttons.values():
        settings_object.update()
    end_drawing()
close_window()     
