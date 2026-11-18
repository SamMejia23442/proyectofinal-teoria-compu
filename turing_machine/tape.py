"""
Módulo de Cinta Infinita Bidireccional para Máquina de Turing.
"""
from collections import defaultdict
from typing import Dict, Tuple, Optional


class InfiniteTape:
    """
    Representa una cinta infinita en ambas direcciones (índices positivos y negativos).
    El espacio no escrito se considera lleno con el símbolo de blanco.
    """

    def __init__(self, initial_content: str = "", blank_symbol: str = "B"):
        self.blank_symbol = blank_symbol
        self.tape: Dict[int, str] = defaultdict(lambda: self.blank_symbol)

        # Cargar la cadena de entrada en las posiciones 0, 1, ..., n-1
        for idx, char in enumerate(initial_content):
            self.tape[idx] = char

    def read(self, position: int) -> str:
        """Lee el símbolo en la posición dada del cabezal."""
        return self.tape[position]

    def write(self, position: int, symbol: str) -> None:
        """Escribe un símbolo en la posición dada del cabezal."""
        self.tape[position] = symbol

    def get_bounds(self) -> Tuple[int, int]:
        """
        Retorna los índices (mínimo, máximo) que contienen símbolos distintos al blanco.
        Si la cinta está vacía, retorna (0, 0).
        """
        non_blank_positions = [
            pos for pos, char in self.tape.items() if char != self.blank_symbol
        ]
        if not non_blank_positions:
            return (0, 0)
        return (min(non_blank_positions), max(non_blank_positions))

    def get_non_blank_content(self) -> str:
        """
        Extrae la cadena resultante sobre la cinta, ignorando los blancos
        a los extremos. Si la cinta quedó totalmente en blanco, retorna cadena vacía.
        """
        min_pos, max_pos = self.get_bounds()
        chars = []
        for i in range(min_pos, max_pos + 1):
            chars.append(self.tape[i])
        result = "".join(chars).strip(self.blank_symbol)
        return result

    def format_instantaneous_description(self, state: str, head_pos: int) -> str:
        """
        Genera la Descripción Instantánea (ID) formal en notación estándar:
        alpha (q) beta
        donde alpha es la cinta a la izquierda del cabezal,
        q es el estado actual,
        y beta es el contenido de la cinta desde la posición del cabezal en adelante.
        """
        min_pos, max_pos = self.get_bounds()
        # Asegurar que el cabezal esté dentro del rango visual
        start = min(min_pos, head_pos)
        end = max(max_pos, head_pos)

        left_symbols = [self.tape[i] for i in range(start, head_pos)]
        right_symbols = [self.tape[i] for i in range(head_pos, end + 1)]

        left_str = "".join(left_symbols)
        right_str = "".join(right_symbols)

        # Si el cabezal está sobre una casilla vacía fuera de límites
        if not right_str:
            right_str = self.blank_symbol

        return f"{left_str}[{state}]{right_str}"

    def format_visual(self, state: str, head_pos: int, window: int = 5) -> str:
        """
        Genera una vista visual clara de la cinta con el cabezal indicado.
        Muestra una ventana alrededor del cabezal.
        """
        start = head_pos - window
        end = head_pos + window

        cells = []
        for i in range(start, end + 1):
            val = self.tape[i]
            if i == head_pos:
                cells.append(f"[{val}]")
            else:
                cells.append(f" {val} ")

        tape_line = " ".join(cells)
        return f"... {tape_line} ...  (Estado: {state}, Pos: {head_pos})"
