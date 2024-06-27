import unittest
from Metodo_simpson import Simpson
from unittest.mock import patch
from main import get_interval, get_subintervals, get_approximation, main
from queue import Queue
from sympy import *
import matplotlib.pyplot as plt
from colorama import Fore, init, AnsiToWin32
from io import StringIO
import re

ansi_escape = re.compile(r'\x1b\[[0-9;]*m')
init(strip=True)
    
class TestMetodoSimpson(unittest.TestCase):
    def setUp(self):
        self.simpson = Simpson()
        self.simpson.a = 0
        self.simpson.b = 1

    def test_simple(self):
        simpson,s,r = self.simpson.calculate("x**2")
        self.assertEqual(simpson, 0.3333)

    def test_polynomial_function_degree_2_simple(self):
        simpson,s,r = self.simpson.calculate("x**2+x+1")
        self.assertEqual(simpson, 1.8333)

    def test_polynomial_function_complex(self):
        simpson,s,r = self.simpson.calculate("x**3+6*x**2+8*x+53")
        self.assertEqual(simpson, 59.25)

    def test_sen_simple(self):
        self.simpson.n = 8
        simpson,s,r = self.simpson.calculate("sin(x)",5)
        self.assertEqual(simpson, 0.4597)

    def test_cos_simple(self):
        self.simpson.n = 8
        simpson,s,r = self.simpson.calculate("cos(x)",5)
        self.assertEqual(simpson, 0.84147)

    def test_tan_simple(self):
        self.simpson.n = 12
        simpson,s,r = self.simpson.calculate("tan(x)",5)
        self.assertEqual(simpson, 0.61562)

    def test_e_simple(self):
        self.simpson.n = 8
        simpson,s,r = self.simpson.calculate("exp(x)",5)
        self.assertEqual(simpson, 1.71828)

    def test_analize_simple(self):
        simpson = self.simpson.analize("x**2")
        self.assertEqual(simpson, False)

    def test_analize_ln(self):
        simpson = self.simpson.analize("log(x)")
        self.assertEqual(simpson, True)

    def test_analize_reciprocal(self):
        simpson = self.simpson.analize("1/x")
        self.assertEqual(simpson, True)

    def test_analize_tan_false(self):
        simpson = self.simpson.analize("tan(x)")
        self.assertEqual(simpson, False)

    def test_analize_tan_true(self):
        self.simpson.a = 1
        self.simpson.b = 2
        simpson = self.simpson.analize("tan(x)")
        self.assertEqual(simpson, True)

    def test_calculate_invalid_ln(self):
        simpson = self.simpson.calculate("log(x)",5)
        self.assertEqual(simpson, "Integral no valida")

    def test_calculate_invalid_reciprocal(self):
        simpson = self.simpson.calculate("1/x",5)
        self.assertEqual(simpson, "Integral no valida")

    def test_has_tan_True(self):
        simpson = self.simpson.has_tan("sin(x)/tan(x**2)")
        self.assertEqual(simpson, True)
    
    def test_has_trig_true(self):
        simpson = self.simpson.has_trig_in_denominador("sin(x)/cos(x)")
        self.assertEqual(simpson, True)

    def test_has_trig_true_complicate_substraction(self):
        simpson = self.simpson.has_trig_in_denominador("1/x-1/sin(x)")
        self.assertEqual(simpson, True)

    def test_has_trig_true_complicate_add(self):
        simpson = self.simpson.has_trig_in_denominador("1/x+1/sin(x)")
        self.assertEqual(simpson, True)

    def test_has_trig_false(self):
        simpson = self.simpson.has_trig_in_denominador("cos(x)+sin(x)")
        self.assertEqual(simpson, False)

    def test_has_trig_false_complicate(self):
        simpson = self.simpson.has_trig_in_denominador("1/x**2+sin(x)/x**4")
        self.assertEqual(simpson, False)

    def test_calculate_exercise_1(self):
        self.simpson.a = 1
        self.simpson.b = 2
        simpson,s,r = self.simpson.calculate("x*log(x)",3)
        self.assertEqual(simpson, 0.636)

    def test_calculate_exercise_2(self):
        self.simpson.n = 10
        simpson,s,r = self.simpson.calculate("x/((x+1)*(x+2))",5)
        self.assertEqual(simpson, 0.11778)

    def test_calculate_exercise_1_equal_to_calculator(self):
        self.simpson.a = 1
        self.simpson.b = 2
        self.simpson.n = 10000
        simpson,s,r = self.simpson.calculate("x*log(x)",14)
        self.assertEqual(simpson, 0.63629436111989)
        
    def test_calculate_exercise_2_equal_to_calculator(self):
        self.simpson.n = 10000
        simpson,s,r = self.simpson.calculate("x/((x+1)*(x+2))",14)
        self.assertEqual(simpson, 0.11778303565638)

    def test_calculate_max_derived_point(self):
        points = [1, 2, 3, 4, 5]
        f = 'x**5'
        queue = Queue()
        self.simpson.calculate_max_derived_point(points, f, queue)
        max_val_from_queue = queue.get()
        self.assertAlmostEqual(max_val_from_queue, 600)
    
    def test_calculate_max_derived_point_invalid(self):
        points = [0,1, 2, 3, 4]
        f = '1/x'
        queue = Queue()
        self.simpson.calculate_max_derived_point(points, f, queue)
        max_val_from_queue = queue.get()
        self.assertAlmostEqual(max_val_from_queue, 0)

    def test_calculate_sum_odd(self):
        self.simpson.n=6
        points = [1, 2, 3, 4, 5, 6, 7]
        f = "x**2"
        x = symbols('x')
        y = lambdify(x,f)
        queue = Queue()
        self.simpson.calculate_sum(points, y, queue, odd=True)
        result = queue.get()
        self.assertEqual(result, ('odd', 56))

    def test_calculate_sum_even(self):
        self.simpson.n=6
        points = [1, 2, 3, 4, 5, 6, 7]
        f = "x**2"
        x = symbols('x')
        y = lambdify(x,f)
        queue = Queue()
        self.simpson.calculate_sum(points, y, queue, odd=False)
        result = queue.get()
        self.assertEqual(result, ('even', 34))

    @patch('matplotlib.pyplot.figure')
    @patch('matplotlib.pyplot.plot')
    @patch('matplotlib.pyplot.fill_between')
    @patch('matplotlib.pyplot.xlabel')
    @patch('matplotlib.pyplot.ylabel')
    @patch('matplotlib.pyplot.title')
    @patch('matplotlib.pyplot.grid')
    @patch('matplotlib.pyplot.legend')
    @patch('matplotlib.pyplot.show')
    def test_graph(self, mock_show, mock_legend, mock_grid, mock_title, mock_ylabel, mock_xlabel, mock_fill_between, mock_plot, mock_figure):
        f = 'x**2'  # Función de ejemplo
        expected_title = f'Gráfico de {f}'
        
        # Ejecutar el método que estamos probando
        self.simpson.graph(f)
        
        # Verificar llamadas a las funciones de matplotlib
        mock_show.assert_called_once()  # Verificar que show() de matplotlib fue llamado una vez
        mock_title.assert_called_once_with(expected_title)

class TestMain(unittest.TestCase):
    @patch('builtins.input', side_effect=["1", "4"])
    def test_get_interval(self, mock_input):
        a, b = get_interval()
        self.assertEqual(a, 1.0)
        self.assertEqual(b, 4.0)

    @patch('builtins.input', side_effect=["4", "1", "1", "4"])
    def test_get_interval_incorrect(self, mock_input):
        a, b = get_interval()
        self.assertEqual(a, 1.0)
        self.assertEqual(b, 4.0)
    
    @patch('builtins.input', side_effect=["a", "b", "1", "2",])  
    @patch('sys.stdout', new_callable=StringIO) 
    def test_get_interval_invalid_input(self, mock_stdout, mock_input):
        expected_output = [
            "Por favor, introduzca un número válido.\n", 
            "Por favor, introduzca un número válido.\n",  
        ]
        a,b = get_interval()
        actual_output = mock_stdout.getvalue()
        
        actual_output_clean = ansi_escape.sub('', actual_output)

        for expected_message in expected_output:
            self.assertIn(expected_message, actual_output_clean)

    @patch('builtins.input', side_effect=["", "100", "101"])
    def test_get_subintervals(self, mock_input):
        self.assertIsNone(get_subintervals())
        self.assertEqual(get_subintervals(), 100)

    @patch('builtins.input', side_effect=["a", "b", "99","100"])
    @patch('sys.stdout', new_callable=StringIO) 
    def test_get_subintervals_invalid(self,mock_stdout, mock_input):
        expected_output = [
            "Por favor, introduzca un número válido.\n", 
            "Por favor, introduzca un número válido.\n",
            "Los subintervalos tienen que ser pares. Intente de nuevo."  
        ]
        n = get_subintervals()
        actual_output = mock_stdout.getvalue()
        
        actual_output_clean = ansi_escape.sub('', actual_output)

        for expected_message in expected_output:
            self.assertIn(expected_message, actual_output_clean)

    @patch('builtins.input', side_effect=["", "5", "3"])
    def test_get_approximation(self, mock_input):
        self.assertIsNone(get_approximation())
        self.assertEqual(get_approximation(), 5)
    
    @patch('builtins.input', side_effect=["a", "b", "5"])
    @patch('sys.stdout', new_callable=StringIO) 
    def test_get_approximation_invalid(self,mock_stdout, mock_input):
        expected_output = [
            "Por favor, introduzca un número válido.\n", 
            "Por favor, introduzca un número válido.\n",
        ]
        aprox = get_approximation()
        actual_output = mock_stdout.getvalue()
        
        actual_output_clean = ansi_escape.sub('', actual_output)

        for expected_message in expected_output:
            self.assertIn(expected_message, actual_output_clean)

    @patch('builtins.input', side_effect=[
        "x**2",  # function input
        "0", "10",  # interval input
        "1000",  # subintervals input
        "5"  # approximation input
    ])
    @patch('builtins.print')
    @patch('Metodo_simpson.Simpson.graph')
    def test_main(self,mock_graph, mock_print, mock_input):
        main()
        self.assertTrue(mock_print.called)
        expected_output = "El resultado de la integral usando el método de Simpson es:"
        printed_lines = [call.args[0] for call in mock_print.call_args_list]
        self.assertTrue(any(expected_output in line for line in printed_lines))
        mock_graph.assert_called_once()

    @patch('builtins.input', side_effect=[
        "x**2",  # function input
        "0", "10",  # interval input
        "",  # subintervals input
        ""  # approximation input
    ])
    @patch('builtins.print')
    @patch('Metodo_simpson.Simpson.graph')
    def test_main_not_subintervals_and_not_approximation(self,mock_graph, mock_print, mock_input):
        main()
        self.assertTrue(mock_print.called)
        expected_output = "El resultado de la integral usando el método de Simpson es:"
        printed_lines = [call.args[0] for call in mock_print.call_args_list]
        self.assertTrue(any(expected_output in line for line in printed_lines))
        mock_graph.assert_called_once()
