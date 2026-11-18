"""
Módulo del Motor de Simulación de la Máquina de Turing.
"""
from typing import Dict, Tuple, Optional, Callable, List, Any
from .tape import InfiniteTape
from .parser import Transition, validate_input_string, SpecificationError


class TuringMachine:
    """
    Simulador de Máquina de Turing de una cinta y cabezal único.
    """

    def __init__(self, spec: Dict[str, Any], input_string: str = ""):
        self.estados = spec["estados"]
        self.alfabeto = spec["alfabeto"]
        self.estado_inicial = spec["estado_inicial"]
        self.blanco = spec["blanco"]
        self.transiciones: Dict[Tuple[str, str], Transition] = spec["transiciones"]

        # Validar la cadena de entrada defensivamente
        validate_input_string(input_string, self.alfabeto, self.blanco)

        self.input_string = input_string
        self.tape = InfiniteTape(initial_content=input_string, blank_symbol=self.blanco)
        self.current_state = self.estado_inicial
        self.head_pos = 0
        self.step_count = 0
        self.is_halted = False
        self.halt_reason = ""
        self.history_ids: List[str] = []

    def get_current_id(self) -> str:
        """Retorna la Descripción Instantánea (ID) actual."""
        return self.tape.format_instantaneous_description(self.current_state, self.head_pos)

    def get_visual_tape(self, window: int = 5) -> str:
        """Retorna una representación visual de la cinta centrada en el cabezal."""
        return self.tape.format_visual(self.current_state, self.head_pos, window=window)

    def step(self) -> Tuple[bool, Optional[Transition]]:
        """
        Ejecuta un único paso de computación.
        Retorna (True, transicion_aplicada) si se ejecutó un paso,
        o (False, None) si la máquina se detuvo (no hay transición aplicable).
        """
        if self.is_halted:
            return (False, None)

        read_symbol = self.tape.read(self.head_pos)
        key = (self.current_state, read_symbol)

        if key not in self.transiciones:
            self.is_halted = True
            self.halt_reason = f"Parada normal: No existe transición definida para ({self.current_state}, '{read_symbol}')"
            return (False, None)

        trans = self.transiciones[key]

        # Aplicar acción
        if trans.action_type == "MOVE":
            if trans.action == "R":
                self.head_pos += 1
            elif trans.action == "L":
                self.head_pos -= 1
            # 'S' se mantiene en el mismo lugar
        elif trans.action_type == "WRITE":
            self.tape.write(self.head_pos, trans.action)

        # Cambiar al estado siguiente
        self.current_state = trans.next_state
        self.step_count += 1

        return (True, trans)

    def get_result(self) -> str:
        """
        Extrae el resultado final escrito en la cinta.
        """
        content = self.tape.get_non_blank_content()
        return content if content else self.blanco

    def run(
        self,
        on_step: Optional[Callable[[int, str, str, Optional[Transition]], bool]] = None,
        max_steps: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Ejecuta la máquina hasta su parada o cancelación.

        Parámetros:
        - on_step: Función invocada en cada paso. Recibe (paso, id_formal, visual, transicion).
                   Si retorna False, la ejecución se cancela.
        - max_steps: Límite de pasos preventivo (opcional).

        Retorna un resumen de la computación.
        """
        # Registrar estado inicial
        initial_id = self.get_current_id()
        self.history_ids.append(initial_id)

        if on_step:
            continue_exec = on_step(0, initial_id, self.get_visual_tape(), None)
            if continue_exec is False:
                self.is_halted = True
                self.halt_reason = "Cancelado por el usuario antes de iniciar."
                return self._build_summary()

        try:
            while not self.is_halted:
                if max_steps is not None and self.step_count >= max_steps:
                    self.is_halted = True
                    self.halt_reason = f"Límite de pasos alcanzado ({max_steps})."
                    break

                prev_state = self.current_state
                prev_pos = self.head_pos
                applied, trans = self.step()

                if not applied:
                    break

                current_id = self.get_current_id()
                self.history_ids.append(current_id)

                if on_step:
                    continue_exec = on_step(self.step_count, current_id, self.get_visual_tape(), trans)
                    if continue_exec is False:
                        self.is_halted = True
                        self.halt_reason = "Cancelado por el usuario durante la ejecución."
                        break

        except KeyboardInterrupt:
            self.is_halted = True
            self.halt_reason = "Cancelado por el usuario mediante interrupción (Ctrl+C)."

        return self._build_summary()

    def _build_summary(self) -> Dict[str, Any]:
        """Construye el reporte resumen de la simulación."""
        return {
            "total_pasos": self.step_count,
            "estado_final": self.current_state,
            "posicion_cabezal": self.head_pos,
            "id_final": self.get_current_id(),
            "resultado_cinta": self.get_result(),
            "motivo_parada": self.halt_reason,
            "historial_ids": self.history_ids
        }
