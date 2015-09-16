# coding=utf-8
__author__ = 'adrian'


def new_line(text, final_line=22):
    """
    Insertar saltos de lineas para q el QLabel sea mostrado completa y correctamente,
    porque si no sale de pantalla sin mostrar los caract q faltan
    :param final_line es un estimado de cuantos caract tiene una linea
    """
    chars = [char for char in text]
    i = 1
    while True:
        if len(chars) < final_line:
            break
        pos = final_line * i
        pos_ = pos
        i += 1
        try:
            if chars[pos] != " ":
                while True:
                    pos_ -= 1
                    if chars[pos_] == " ":
                        break
            chars[pos_] = u"\n"
        except IndexError:
            break
        if pos > len(chars):
            break
    return "".join(chars)


def capitalize_finalize(text):
    text = text.strip()
    chars = [char for char in text]
    chars[0] = chars[0].upper()
    sig = [".", "?", "!"]
    if chars[-1] not in sig:
        chars.append(".")
    return "".join(chars)


def sorted_couple(couple):
    sorted_ = [("", -1)]
    for tup in couple:
        # print(tup[1])
        if tup[1] > sorted_[0][1]:
            sorted_.insert(0, tup)
        else:
            for i in range(1, len(sorted_)):
                if tup[1] > sorted_[i][1]:
                    sorted_.insert(i, tup)
                    break
    sorted_.pop()
    return sorted_