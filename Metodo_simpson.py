from sympy import *
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
import multiprocessing as mp

class Simpson():
    def __init__(self):
        self.x = symbols('x')
        self.a = 0
        self.b = 0
        self.n = 2
        self.h = 0

    def has_tan(self, f):
        f = sympify(f)
        return f.has(tan)
    
    def check_denominator(self, f):
            numerator, denominator = fraction(f)
            return any(denominator.has(trig) for trig in (sin, cos, tan))
    
    def has_trig_in_denominador(self, f):
        f = sympify(f)

        if isinstance(f, (Add, Mul)):
            terms = f.args
        else:
            terms = [f]
        for term in terms:
            if self.check_denominator(term):
                return True
        return False
    
    def analize(self,f):
        f = sympify(f)
        discontinuities = singularities(f,self.x)
        interval = Interval(self.a,self.b)
        if self.has_tan(f) or self.has_trig_in_denominador(f):
            j=0
            for discontinuity in discontinuities:
                if discontinuity in interval:
                    return True
                if j == self.b:
                    return False
                j+=1
        for discontinuity in discontinuities:
            if discontinuity in interval:
                return True
        return False
    
    def calculate_points(self):
        points = np.zeros(self.n + 1)
        points[:] = self.a + self.h * np.arange(self.n + 1)
        return points
    
    def calculate_max_derived_point(self,points,f,queue):
        f_diff = diff(f,self.x,4)
        y_diff = lambdify(self.x, f_diff)
        dpoints = []
        try:
            y_diff_values = np.array([y_diff(p) for p in points])
        except ZeroDivisionError:
            y_diff_values = np.zeros_like(points)
        dpoints = np.abs(y_diff_values)
        dpoints = np.nan_to_num(dpoints, nan=0.0, posinf=0.0, neginf=0.0)
        max = np.max(dpoints)
        queue.put(max)
    
    def calculate_sum(self,points,y,queue, odd=True):
        indices = np.arange(1, self.n)
        if odd:
            odd_indices = indices[indices % 2 != 0]
            y_odd = np.array([y(points[i]) for i in odd_indices])
            odd_sum = np.sum(y_odd)
            queue.put(('odd', odd_sum))
        else:
            even_indices = indices[indices % 2 == 0]
            y_even = np.array([y(points[i]) for i in even_indices])
            even_sum = np.sum(y_even)
            queue.put(('even', even_sum))

    def calculate(self,f ,aprox=4):
        f = sympify(f)
        self.h = (self.b-self.a)/self.n
        if self.analize(f):
            return "Integral no valida"
        
        S = 0
        R = 0

        y = lambdify(self.x,f)
        points = self.calculate_points()
        max_queue = mp.Queue()
        sum_queue = mp.Queue()


        max_process = mp.Process(target=self.calculate_max_derived_point, args=(points, f, max_queue))
        odd_sum_process = mp.Process(target=self.calculate_sum, args=(points, y, sum_queue, True))
        even_sum_process = mp.Process(target=self.calculate_sum, args=(points, y, sum_queue, False))



        max_process.start()
        odd_sum_process.start()
        even_sum_process.start()


        max_process.join()
        odd_sum_process.join()
        even_sum_process.join()
        max = max_queue.get()
        sum_results = [sum_queue.get(), sum_queue.get()]


        odd_sum = next(result[1] for result in sum_results if result[0] == 'odd')
        even_sum = next(result[1] for result in sum_results if result[0] == 'even')

        #try:
        S = float((y(points[0])+ 4*odd_sum + 2*even_sum + y(points[self.n]))/(3*self.n))
        """        except Exception: #Cambiar
            if points[0] == 0:
                S = float((0+ 4*odd_sum + 2*even_sum + y(points[self.n]))/(3*self.n))
            else:
                S = float((y(points[0])+ 4*odd_sum + 2*even_sum + 0)/(3*self.n))"""
        R = float(-(self.h**5/90)*max)
        result = round(S + R,aprox)
        simp_aprox = round(S, aprox)
        error_aprox = round(R, aprox)
        return result, simp_aprox, error_aprox
    
    def graph(self,f):
        x_sym = symbols('x')
        x = np.linspace(self.a-1, self.b+1, 500)
        f = sympify(f)
        y = np.array([f.subs(x_sym, val) for val in x], dtype=float)
        plt.figure(figsize=(8, 6))
        plt.plot(x, y, label=f'y = {f}')
        plt.fill_between(x, y, where=((x >= self.a) & (x <= self.b)), color='skyblue', alpha=0.4)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title(f'Gráfico de {f}')
        plt.grid(True)
        plt.legend()
        plt.show()