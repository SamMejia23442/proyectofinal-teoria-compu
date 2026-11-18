"""
Pruebas Unitarias Automatizadas para el Simulador de Máquinas de Turing.
Teoría de la Computación - CC2019
"""

import unittest
import os
from turing_machine import parse_and_validate_yaml, TuringMachine, SpecificationError


class TestTuringMachineSimulator(unittest.TestCase):

    def setUp(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.pred_path = os.path.join(self.base_dir, "ejemplos", "predecesor_binario.yaml")
        self.palin_path = os.path.join(self.base_dir, "ejemplos", "verificador_palindromos.yaml")

    def test_predecesor_binario(self):
        spec = parse_and_validate_yaml(self.pred_path)
        casos = [
            ("1100", "1011"),
            ("1010", "1001"),
            ("1000", "0111"),
            ("11", "10"),
            ("10", "01"),
            ("1", "0"),
            ("1111", "1110")
        ]
        for entrada, esperado in casos:
            with self.subTest(entrada=entrada):
                tm = TuringMachine(spec, entrada)
                res = tm.run()
                self.assertEqual(res["resultado_cinta"], esperado)

    def test_verificador_palindromos_aceptados(self):
        spec = parse_and_validate_yaml(self.palin_path)
        palindromos = ["10101", "1001", "0110", "11", "00", "1", "0", "11111", "01010", ""]
        for p in palindromos:
            with self.subTest(cadena=p):
                tm = TuringMachine(spec, p)
                res = tm.run()
                self.assertEqual(res["resultado_cinta"], "Y")

    def test_verificador_palindromos_rechazados(self):
        spec = parse_and_validate_yaml(self.palin_path)
        no_palindromos = ["10110", "10", "01", "110", "1000", "11110", "01100"]
        for np in no_palindromos:
            with self.subTest(cadena=np):
                tm = TuringMachine(spec, np)
                res = tm.run()
                self.assertEqual(res["resultado_cinta"], "N")

    def test_defensa_caracter_invalido(self):
        spec = parse_and_validate_yaml(self.pred_path)
        with self.assertRaises(SpecificationError):
            TuringMachine(spec, "10201")  # '2' no está en el alfabeto

    def test_defensa_archivo_inexistente(self):
        with self.assertRaises(SpecificationError):
            parse_and_validate_yaml("archivo_que_no_existe.yaml")


if __name__ == "__main__":
    unittest.main()
