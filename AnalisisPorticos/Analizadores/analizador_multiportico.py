import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def obtener_longitud_y_angulos(nodo_i, nodo_j):
    xi = nodo_i['x']
    yi = nodo_i['y']
    xj = nodo_j['x']
    yj = nodo_j['y']
    L = ((xj - xi)**2 + (yj - yi)**2) ** 0.5
    cos = (xj - xi) / L
    sen = (yj - yi) / L
    return L, cos, sen

def matriz_rigidez_local(E, A, L, c, s):
    k = (E * A) / L
    return k * np.array([
        [ c*c,  c*s, -c*c, -c*s],
        [ c*s,  s*s, -c*s, -s*s],
        [-c*c, -c*s,  c*c,  c*s],
        [-c*s, -s*s,  c*s,  s*s]
    ])

def analizar_portico(archivo_json):
    with open(archivo_json) as archivo:
        datos = json.load(archivo)

    nodos = sorted([int(n) for n in datos['nodos'].keys()])
    gdl_por_nodo = 2
    total_gdl = len(nodos) * gdl_por_nodo

    mapa_gdl = {n: [i * 2, i * 2 + 1] for i, n in enumerate(nodos)}
    K = np.zeros((total_gdl, total_gdl))

    for eid, e in datos['elementos'].items():
        ni, nj = e['nodo_i'], e['nodo_j']
        nodo_i = datos['nodos'][str(ni)]
        nodo_j = datos['nodos'][str(nj)]
        L, c, s = obtener_longitud_y_angulos(nodo_i, nodo_j)
        k_local = matriz_rigidez_local(e['E'], e['A'], L, c, s)
        dofs = mapa_gdl[ni] + mapa_gdl[nj]
        for i in range(4):
            for j in range(4):
                K[dofs[i], dofs[j]] += k_local[i, j]

    F = np.zeros(total_gdl)
    for carga in datos['cargas']:
        if carga['tipo'] == 'distribuida':
            e = datos['elementos'][str(carga['elemento'])]
            ni, nj = e['nodo_i'], e['nodo_j']
            nodo_i = datos['nodos'][str(ni)]
            nodo_j = datos['nodos'][str(nj)]
            L, _, _ = obtener_longitud_y_angulos(nodo_i, nodo_j)
            q = carga['valor']
            F[mapa_gdl[ni][1]] += q * L / 2
            F[mapa_gdl[nj][1]] += q * L / 2

    gdl_res = []
    for nodo_id, nodo in datos['nodos'].items():
        for i, r in enumerate(nodo['restricciones']):
            if r == 1:
                gdl_res.append(mapa_gdl[int(nodo_id)][i])

    gdl_libres = [i for i in range(total_gdl) if i not in gdl_res]
    K_LL = K[np.ix_(gdl_libres, gdl_libres)]
    F_L = F[gdl_libres]

    U = np.zeros(total_gdl)
    U[gdl_libres] = np.linalg.solve(K_LL, F_L)
    R = K @ U - F

    # Guardar resultados
    nombre_base = archivo_json.replace('.json', '')
    with open(f"{nombre_base}_resultados.txt", "w") as f:
        f.write("Desplazamientos nodales:")
        f.write(str(np.round(U, 5)) + "\n\n")
        f.write("Reacciones en apoyos:\n")
        for i in gdl_res:
            f.write(f"gdl {i}: {round(R[i], 3)}\n")

    # Gráfico
    plt.figure(figsize=(8, 6))
    escala = 100
    for eid, e in datos['elementos'].items():
        ni, nj = e['nodo_i'], e['nodo_j']
        xi, yi = datos["nodos"][str(ni)]["x"], datos["nodos"][str(ni)]["y"]
        xj, yj = datos["nodos"][str(nj)]["x"], datos["nodos"][str(nj)]["y"]
        plt.plot([xi, xj], [yi, yj], 'k--', label='Original' if eid == "1" else "")
        ui, vi = U[mapa_gdl[ni][0]], U[mapa_gdl[ni][1]]
        uj, vj = U[mapa_gdl[nj][0]], U[mapa_gdl[nj][1]]
        plt.plot([xi + escala*ui, xj + escala*uj], [yi + escala*vi, yj + escala*vj], 'r-', label='Deformada' if eid == "1" else "")
    for nid, nodo in datos["nodos"].items():
        x, y = nodo["x"], nodo["y"]
        plt.text(x, y + 0.1, f'N{nid}', color='blue', fontsize=9, ha='center')

    plt.title(f"Estructura {archivo_json} - Original vs Deformada")
    plt.xlabel("X [m]")
    plt.ylabel("Y [m]")
    plt.axis('equal')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    print(f"Guardando gráfico: {nombre_base}")
    ruta_png = os.path.abspath(os.path.join("..", "Graficos", f"{nombre_base}_grafico.png"))
    plt.savefig(ruta_png)
    os.startfile(ruta_png)  # Abre el archivo automáticamente
    plt.close()

# --- Ejecutar todos los pórticos ---
import os
import pandas as pd

# Obtener la ruta absoluta al archivo CSV
ruta_csv = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Datos", "porticos.csv"))
df = pd.read_csv(ruta_csv)

for ruta in df["Nombre"]:
    archivo_json = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Generadores", f"{ruta}.json"))
    analizar_portico(archivo_json)

def procesar_archivo_csv(archivo):
    df = pd.read_csv(archivo)

    resultados = []

    for _, fila in df.iterrows():
        nombre = fila["Nombre"]
        altura = fila["Altura"]
        longitud = fila["Longitud"]
        carga = fila["CargaDistribuida"]

        # Simulación de análisis (ejemplo simple)
        resultado = {
            "nombre": nombre,
            "reacciones": [round(longitud * 0.5, 2), round(longitud * 0.5, 2)],
            "desplazamientos": [round(altura * 0.1, 2)],
            "fuerzas_internas": [round(carga * longitud, 2)]
        }

        resultados.append(resultado)

    return resultados

