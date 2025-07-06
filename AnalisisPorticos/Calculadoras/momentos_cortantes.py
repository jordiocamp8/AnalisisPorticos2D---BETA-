import math

def carga_distribuida(w, L):
    Mw = round(w * L**2 / 12, 3)
    Vw = round(w * L / 2, 3)
    return {
        "tipo": "distribuida uniforme",
        "M_i": Mw,
        "M_j": Mw,
        "V_i": Vw,
        "V_j": Vw
    }

def carga_no_uniforme(w, L):
    Mn_i = round(w * L**2 / 30, 3)
    Mn_j = round(w * L**2 / 20, 3)
    Vn_i = round(3 * w * L / 20, 3)
    Vn_j = round(7 * w * L / 20, 3)
    return {
        "tipo": "distribuida no uniforme",
        "M_i": Mn_i,
        "M_j": Mn_j,
        "V_i": Vn_i,
        "V_j": Vn_j
    }

def carga_triangular(w, L):
    Mt = round(5 * w * L**2 / 96, 3)
    Vt = round(w * L / 4, 3)
    return {
        "tipo": "triangular",
        "M_i": Mt,
        "M_j": Mt,
        "V_i": Vt,
        "V_j": Vt
    }

def carga_puntual(P, a, b, L):
    Mpi = round((P * b**2 * a) / L**2, 3)
    Mpj = round((P * a**2 * b) / L**2, 3)
    Vpi = round(P * b**2 / L**2, 3)
    Vpj = round(P * a**2 / L**2, 3)
    return {
        "tipo": "puntual",
        "M_i": Mpi,
        "M_j": Mpj,
        "V_i": Vpi,
        "V_j": Vpj
    }

def carga_trapezoidal(w, a, L):
    coef = (L**3 - a**2 * (2 * L - a))
    Mt = round(w * coef / (12 * L), 3)
    return {
        "tipo": "trapezoidal isósceles",
        "M_i": Mt,
        "M_j": Mt
    }

# Ejemplo de uso si lo corres como script independiente
if __name__ == "__main__":
    print(carga_distribuida(w=10, L=6))
    print(carga_no_uniforme(w=8, L=6))
    print(carga_triangular(w=12, L=5))
    print(carga_puntual(P=20, a=2, b=3, L=5))
    print(carga_trapezoidal(w=-0.4, a=1.06, L=6))
