from colorama import init, Fore, Style
from Metodo_simpson import Simpson
from sympy import *

# Inicializar colorama
init(autoreset=True)

def get_interval():
    while True:
        try:
            a = float(input(Fore.CYAN + "Ahora escriba el punto a del intervalo: "))
            b = float(input(Fore.CYAN + "Ahora escriba el punto b del intervalo: "))
            if b > a:
                return a, b
            else:
                print(Fore.RED + "El valor b tiene que ser mayor al valor a. Intente de nuevo.")
        except ValueError:
            print(Fore.RED + "Por favor, introduzca un número válido.")

def get_subintervals():
    while True:
        n = input(Fore.CYAN + "(Opcional) Escriba la cantidad de subintervalos, en caso de no querer especificar solo presione Enter: ")
        if n == "":
            return None
        try:
            n = int(n)
            if n % 2 == 0:
                return n
            else:
                print(Fore.RED + "Los subintervalos tienen que ser pares. Intente de nuevo.")
        except ValueError:
            print(Fore.RED + "Por favor, introduzca un número válido.")

def get_approximation():
    while True:
        aprox = input(Fore.CYAN + "(Opcional) A cuántos decimales quieres aproximarlo, en caso de no querer especificar solo presione Enter: ")
        if aprox == "":
            return None
        try:
            return int(aprox)
        except ValueError:
            print(Fore.RED + "Por favor, introduzca un número válido.")

def main():
    print(Fore.GREEN + Style.BRIGHT + "Calculadora de Simpson")
    print(Fore.YELLOW + Style.BRIGHT + "Aviso: El límite de subintervalos es de 1.000.000")
    print(Fore.YELLOW + Style.BRIGHT + "La variable independiente solamente puede ser x")
    
    simpson = Simpson()
    f = input(Fore.CYAN + "Escriba la función que desea calcular su integral: ")

    a, b = get_interval()
    n = get_subintervals()
    aprox = get_approximation()

    simpson.a = a
    simpson.b = b
    if n is not None:
        simpson.n = n
    try:
        if aprox is not None:
            resultado, S, R = simpson.calculate(f, aprox)
        else:
            resultado, S, R = simpson.calculate(f)
    except:
        print(Fore.RED + Style.BRIGHT + f"La función no es valida en ese intervalo con el método simpson")
        exit()

    print(Fore.GREEN + Style.BRIGHT + f"La integral aproximada es: {S}")
    print(Fore.RED + Style.BRIGHT + f"El residuo del método es: {R}")
    print(Fore.GREEN + Style.BRIGHT + f"El resultado de la integral aproximada sumada su residuo es: {resultado}")
    x = symbols('x')
    integral = integrate(f,(x,a,b))
    error_absoluto = integral - S
    error_porcentual = Abs((error_absoluto / integral) * 100)
    print(Fore.RED + Style.BRIGHT + f"El error porcental del método es: {error_porcentual}%")
    simpson.graph(f)

if __name__ == "__main__":
    main()
