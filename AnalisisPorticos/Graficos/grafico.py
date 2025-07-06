# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt

def graficar_resultados(nodos, elementos, desplazamientos):
    fig, ax = plt.subplots()

    # Dibujar elementos no deformados (en gris)
    for elem in elementos:
        i, j = elem
        xi, yi = nodos[i]
        xj, yj = nodos[j]
        ax.plot([xi, xj], [yi, yj], 'gray', linestyle='--', linewidth=1)

    # Dibujar elementos deformados (en azul)
    escala = 100  # Puedes ajustar esto según las unidades
    for idx, (i, j) in enumerate(elementos):
        xi, yi = nodos[i]
        xj, yj = nodos[j]
        dx_i, dy_i = desplazamientos[i]
        dx_j, dy_j = desplazamientos[j]

        xi_d = xi + dx_i * escala
        yi_d = yi + dy_i * escala
        xj_d = xj + dx_j * escala
        yj_d = yj + dy_j * escala

        ax.plot([xi_d, xj_d], [yi_d, yj_d], 'blue', linewidth=2)

    ax.set_aspect('equal')
    ax.set_title("Deformacion del portico (escala x{})".format(escala))
    ax.grid(True)
    return fig
