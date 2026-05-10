# integracion_trapecios_no_paralelo.py
# INTEGRACION NUMERICA POR EL METODO DE LOS TRAPECIOS
# ENTRADA: NINGUNA.
# SALIDA:  ESTIMACION DE LA INTEGRAL DESDE a HASTA b DE f(x)
# USANDO EL METODO DE LOS TRAPECIOS CON n TRAPECIOS

def f(x):
    return (1-x*x)**0.5

a = -1.0
b = 1.0
n = 100000
h = (b-a)/n

integral = (f(a) + f(b))/2.0

for i in range(1,n):
    integral += f(a+i*(b-a)/n)

integral *= h

print (f"ESTIMACION USANDO n={n} TRAPECIOS")
print (f"DE LA INTEGRAL DESDE {a} HASTA {b} = {integral:.2f}")
print (f"ESTIMACION DE PI: {2*integral:.2f}")