import numpy as np

def obtener_longitud_y_angulos(nodo_i, nodo_j):
    dx = nodo_j["x"] - nodo_i["x"]
    dy = nodo_j["y"] - nodo_i["y"]
    L = np.sqrt(dx**2 + dy**2)
    c = dx / L
    s = dy / L
    return L, c, s

def matriz_rigidez_local(E, A, L, I, c, s):
    c2 = c * c
    s2 = s * s
    cs = c * s
    return E / L * np.array([
        [ A * c2,  A * cs, -A * c2, -A * cs],
        [ A * cs,  A * s2, -A * cs, -A * s2],
        [-A * c2, -A * cs,  A * c2,  A * cs],
        [-A * cs, -A * s2,  A * cs,  A * s2]
    ]) + \
    12 * E * I / L**3 * np.array([
        [ s2, -cs, -s2,  cs],
        [-cs,  c2,  cs, -c2],
        [-s2,  cs,  s2, -cs],
        [ cs, -c2, -cs,  c2]
    ]) + \
    6 * E * I / L**2 * np.array([
        [ 0,  1,  0, -1],
        [-1, 0,  1,  0],
        [ 0, -1,  0,  1],
        [ 1, 0, -1,  0]
    ]) + \
    E * I / L * np.array([
        [ 0,  0,  0,  0],
        [ 0,  4,  0,  2],
        [ 0,  0,  0,  0],
        [ 0,  2,  0,  4]
    ])

def analizar_portico(datos):
    # --- Conversión de listas a diccionarios ---
    if isinstance(datos["nodos"], list):
        datos["nodos"] = {
            str(i + 1): {"x": nodo["x"], "y": nodo["y"]}
            for i, nodo in enumerate(datos["nodos"])
        }

    if isinstance(datos["elementos"], list):
        datos["elementos"] = {
            str(i + 1): {
                "nodo_i": elem["nodo_i"],
                "nodo_j": elem["nodo_j"],
                "E": elem["E"],
                "A": elem["A"],
                "I": elem["I"],
            }
            for i, elem in enumerate(datos["elementos"])
        }

    if isinstance(datos["apoyos"], list):
        datos["apoyos"] = {
            str(i + 1): apoyo for i, apoyo in enumerate(datos["apoyos"])
        }

    if isinstance(datos["cargas"], list):
        datos["cargas"] = [carga for carga in datos["cargas"]]

    # --- Análisis ---
    nodos = sorted([int(k) for k in datos["nodos"].keys()])
    gdl_por_nodo = 2
    total_gdl = len(nodos) * gdl_por_nodo
    mapa_gdl = {nodo: [i * 2, i * 2 + 1] for i, nodo in enumerate(nodos)}
    K = np.zeros((total_gdl, total_gdl))

    for _, e in datos["elementos"].items():
        ni, nj = e["nodo_i"], e["nodo_j"]
        nodo_i, nodo_j = datos["nodos"][str(ni)], datos["nodos"][str(nj)]
        L, c, s = obtener_longitud_y_angulos(nodo_i, nodo_j)
        k_local = matriz_rigidez_local(e["E"], e["A"], L, e["I"], c, s)
        dofs = mapa_gdl[ni] + mapa_gdl[nj]
        for i in range(4):
            for j in range(4):
                K[dofs[i], dofs[j]] += k_local[i, j]

    F = np.zeros(total_gdl)
    for carga in datos["cargas"]:
        if carga["tipo"] == "puntual":
            direccion = 0 if carga["Fx"] != 0 else 1
            valor = carga["Fx"] if direccion == 0 else carga["Fy"]
            gdl = mapa_gdl[carga["nodo"]][direccion]
            F[gdl] += valor

    gdl_restringidos = []
    for _, a in datos["apoyos"].items():
        nodo = a["nodo"]
        if a["x"]:
            gdl_restringidos.append(mapa_gdl[nodo][0])
        if a["y"]:
            gdl_restringidos.append(mapa_gdl[nodo][1])

    gdl_libres = list(set(range(total_gdl)) - set(gdl_restringidos))
    K_ff = K[np.ix_(gdl_libres, gdl_libres)]
    K_fc = K[np.ix_(gdl_libres, gdl_restringidos)]
    F_f = F[gdl_libres]

    desplazamientos = np.zeros(total_gdl)
    desplazamientos[gdl_libres] = np.linalg.solve(K_ff, F_f)

    reacciones = K_fc.T @ desplazamientos[gdl_libres]

    return {
        "desplazamientos": desplazamientos.tolist(),
        "reacciones": reacciones.tolist()
    }
