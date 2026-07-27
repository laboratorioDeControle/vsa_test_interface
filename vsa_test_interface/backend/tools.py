import json
import numpy as np
import math


def json_to_dict(json_path: str) -> dict:
    result: dict = {}

    try:
        with open(json_path, encoding='utf-8') as json_file:
            result = json.load(json_file)
            json_file.close()

    except FileNotFoundError:
        pass

    except json.decoder.JSONDecodeError:
        pass

    return result


def dict_to_json(output_file_path: str, output_dict: dict, output_file_extension: str = ".json") -> None:
    with open(output_file_path + output_file_extension, "w", encoding='utf-8') as f:
        output: str = json.dumps(output_dict, indent=2, ensure_ascii=False)
        f.write(output)
        f.close()


def parse_rgb_color(color: str) -> list:
    result: list = []
    color_text: str = color.strip()
    color_split: list = color_text.split(",")

    for color_field in color_split:
        try:
            result.append(int(color_field))
        except ValueError:
            result.append(0)

    return result


def poly_list_to_poly_text(coefs: list, variable_label: str) -> str:
    degree: int = len(coefs) - 1
    coef_txt: str = ""
    exp_txt: str = ""
    poly: str = ""
    abs_coef: float = 0.0

    for index, coef in enumerate(coefs):
        signal: str = " + "

        if coef.__class__ == float:
            if coef < 0:
                signal = " - "

            abs_coef = abs(coef)

            if coef != 0:
                if index == 0:
                    if coef < 0:
                        coef_txt = str(coef)
                    else:
                        coef_txt = str(abs_coef)
                else:
                    coef_txt = signal + str(abs_coef)
            else:
                coef_txt = signal + str(abs_coef)
            
        else:
            if index == 0:
                coef_txt = coef
            else:
                coef_txt = signal + coef

        if degree == 0:
            exp_txt = ""
        elif degree == 1:
            exp_txt = "*" + variable_label
        else:
            exp_txt = "*%s^%s" % (variable_label, degree)

        poly += coef_txt + exp_txt

        degree -= 1

    return poly


def poly_coef_text_to_poly_list(poly_coefs: str) -> list:
    result = []
    poly_split: list = poly_coefs.split(",")

    for value in poly_split:
        val: str = value.strip().replace("[", "").replace("]", "")
        try:
            value_float: float = float(val)
            result.append(value_float)
        except ValueError:
            result.append(0.0)

    return result

def rad2deg(rad_value: float):
    return (rad_value * 180.0) / math.pi

def deg2rad(deg_value: float):
    return ((deg_value * math.pi) / 180.0)

def map(value: float, input_min: float = -1.0, input_max: float = 1.0, output_min: float = 0, output_max: float = 255.0):
        return (value - input_min) * (output_max - output_min) / (input_max - input_min) + output_min


def calculate_calibration_parameters(x_list: list, y_list: list) -> dict:
    poly_degree: int = 1
    x: np.array = np.array(x_list)
    y: np.array = np.array(y_list)

    poly_coefs: np.array = np.polyfit(x, y, poly_degree)
    poly_coefs_float: list = []
    estimate: np.array = np.polyval(poly_coefs, x)

    for coef in poly_coefs:
        poly_coefs_float.append(float(coef))

    sq_tot: float = np.sum((y - np.mean(y)) ** 2)
    sq_res: float = np.sum((y - estimate) ** 2)
    r_2: float = 1 - (sq_res / sq_tot)

    return {
        "interpolation_poly_coef": poly_coefs_float,
        "r2": float(r_2)
    }
