import pandas as pd
import json

# Carga los datos del CSV
import os

ruta_csv = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Datos", "porticos.csv"))
df = pd.read_csv(ruta_csv)

for i, fila in df.iterrows():
    nombre = fila["Nombre"]
    H = float(fila["Altura"])
    L = float(fila["Longitud"])
    q = float(fila["CargaDistribuida"])

    estructura = {
        "nodos": {
            "1": {"x": 0, "y": 0, "restricciones": [1, 1]},
            "2": {"x": L, "y": 0, "restricciones": [0, 1]},
            "3": {"x": L, "y": H, "restricciones": [0, 1]},
            "4": {"x": 0, "y": H, "restricciones": [1, 1]}
        },
        "elementos": {
            "1": {"nodo_i": 1, "nodo_j": 2, "E": 200000, "A": 0.02},
            "2": {"nodo_i": 2, "nodo_j": 3, "E": 200000, "A": 0.02},
            "3": {"nodo_i": 3, "nodo_j": 4, "E": 200000, "A": 0.02},
            "4": {"nodo_i": 4, "nodo_j": 1, "E": 200000, "A": 0.02}
        },
        "cargas": [
            {
                "tipo": "distribuida",
                "elemento": 4,
                "valor": q
            }
        ]
    }

    with open(f"{nombre}.json", "w") as f:
        json.dump(estructura, f, indent=2)

print("✅ Archivos JSON generados.")
