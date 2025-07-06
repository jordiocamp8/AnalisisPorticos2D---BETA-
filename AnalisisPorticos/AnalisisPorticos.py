import pandas as pd
import matplotlib.pyplot as plt

# Leer archivo
data = pd.read_csv('porticos.csv')

# Funciones de cálculo
def calc_deformacion(L, q, E=200e6, I=0.0001):
    return (5 * abs(q) * L**4) / (384 * E * I)

def calc_momento_max(q, L):
    return abs(q) * L**2 / 8  # Momento máximo en centro para viga simplemente apoyada

def calc_reacciones(q, L):
    return abs(q) * L / 2  # Reacción en cada apoyo para carga distribuida uniforme

# Aplicar cálculos
data['Deformacion_mm'] = data.apply(lambda row: calc_deformacion(row['Longitud'], row['CargaDistribuida']) * 1000, axis=1)
data['Momento_max_kNm'] = data.apply(lambda row: calc_momento_max(row['CargaDistribuida'], row['Longitud']), axis=1)
data['Reaccion_kN'] = data.apply(lambda row: calc_reacciones(row['CargaDistribuida'], row['Longitud']), axis=1)

# Mostrar tabla
print("\nResultados:")
print(data[['Nombre', 'Deformacion_mm', 'Momento_max_kNm', 'Reaccion_kN']])

# Guardar resultados en Excel
data.to_excel('resultados.xlsx', index=False)

# Graficar y guardar imagen
plt.figure(figsize=(8, 5))
plt.bar(data['Nombre'], data['Deformacion_mm'], color='skyblue')
plt.xlabel('Pórtico')
plt.ylabel('Deformación (mm)')
plt.title('Deformación Máxima por Pórtico')
plt.grid(True)
plt.tight_layout()
plt.savefig('grafico.png')
plt.show()

