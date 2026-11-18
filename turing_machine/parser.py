"""
Módulo de Análisis y Validación Defensiva de Especificaciones YAML para Máquina de Turing.
"""
from typing import Dict, List, Set, Tuple, Any
import yaml
import os


class SpecificationError(Exception):
    """Excepción lanzada cuando la especificación de la Máquina de Turing no es válida."""
    pass


class Transition:
    """Representa una transición en formato de cuádrupla."""

    def __init__(self, origin_state: str, read_symbol: str, action: str, action_type: str, next_state: str):
        self.origin_state = origin_state
        self.read_symbol = read_symbol
        self.action = action  # 'R', 'L', o símbolo a escribir
        self.action_type = action_type  # 'MOVE' o 'WRITE'
        self.next_state = next_state

    def __repr__(self):
        return f"Transition({self.origin_state} {self.read_symbol} {self.action} {self.next_state})"


def parse_and_validate_yaml(filepath: str) -> Dict[str, Any]:
    """
    Carga y valida defensivamente un archivo YAML de especificación de Máquina de Turing.

    Retorna un diccionario con:
    - 'estados': Set[str]
    - 'alfabeto': Set[str]
    - 'estado_inicial': str
    - 'blanco': str
    - 'transiciones': Dict[Tuple[str, str], Transition]
    - 'raw_data': Dict[str, Any]
    """
    if not os.path.exists(filepath):
        raise SpecificationError(f"El archivo especificado no existe: '{filepath}'")

    if not os.path.isfile(filepath):
        raise SpecificationError(f"La ruta especificada no es un archivo válido: '{filepath}'")

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as e:
        raise SpecificationError(f"Error de sintaxis YAML en '{filepath}':\n{e}")
    except Exception as e:
        raise SpecificationError(f"No se pudo leer el archivo '{filepath}': {e}")

    if not isinstance(data, dict):
        raise SpecificationError("El contenido del archivo YAML debe ser un objeto/mapeo de nivel superior.")

    # Permitir raíz 'mt' o claves directas
    if "mt" in data:
        mt_spec = data["mt"]
        if not isinstance(mt_spec, dict):
            raise SpecificationError("La clave 'mt' debe contener un mapeo con la configuración de la máquina.")
    else:
        mt_spec = data

    # 1. Validar claves obligatorias
    required_keys = ["estados", "alfabeto", "estado_inicial", "transiciones"]
    missing = [k for k in required_keys if k not in mt_spec]
    if missing:
        raise SpecificationError(f"Faltan claves obligatorias en la especificación: {', '.join(missing)}")

    # 2. Validar estados
    estados_raw = mt_spec.get("estados")
    if not isinstance(estados_raw, list) or len(estados_raw) == 0:
        raise SpecificationError("La clave 'estados' debe ser una lista no vacía de nombres de estados.")
    
    estados: Set[str] = set()
    for s in estados_raw:
        s_str = str(s).strip()
        if not s_str:
            raise SpecificationError("Se encontró un estado vacío o nulo en la lista de estados.")
        if s_str in estados:
            raise SpecificationError(f"Estado duplicado en la lista de estados: '{s_str}'")
        estados.add(s_str)

    # 3. Validar alfabeto
    alfabeto_raw = mt_spec.get("alfabeto")
    if not isinstance(alfabeto_raw, list) or len(alfabeto_raw) == 0:
        raise SpecificationError("La clave 'alfabeto' debe ser una lista no vacía de símbolos permitidos.")

    alfabeto: Set[str] = set()
    for a in alfabeto_raw:
        a_str = str(a)
        if len(a_str) != 1:
            raise SpecificationError(f"Cada símbolo del alfabeto debe ser de un solo carácter. Símbolo inválido: '{a_str}'")
        if a_str in alfabeto:
            raise SpecificationError(f"Símbolo duplicado en el alfabeto: '{a_str}'")
        alfabeto.add(a_str)

    # 4. Validar símbolo en blanco
    blanco = mt_spec.get("blanco")
    if blanco is not None:
        blanco_str = str(blanco)
        if len(blanco_str) != 1:
            raise SpecificationError(f"El símbolo de blanco debe ser un único carácter. Valor: '{blanco_str}'")
        if blanco_str not in alfabeto:
            raise SpecificationError(
                f"El símbolo de blanco '{blanco_str}' debe estar incluido explícitamente en el 'alfabeto'."
            )
        blank_symbol = blanco_str
    else:
        # Por convención, buscar 'B' o '_' en el alfabeto
        if "B" in alfabeto:
            blank_symbol = "B"
        elif "_" in alfabeto:
            blank_symbol = "_"
        else:
            raise SpecificationError(
                "No se especificó la clave 'blanco' y el alfabeto no incluye 'B' ni '_' como espacio en blanco."
            )

    # 5. Validar estado inicial
    estado_inicial_raw = str(mt_spec.get("estado_inicial")).strip()
    if estado_inicial_raw not in estados:
        raise SpecificationError(
            f"El estado inicial '{estado_inicial_raw}' no pertenece al conjunto de estados definidos: {sorted(list(estados))}"
        )
    estado_inicial = estado_inicial_raw

    # 6. Validar transiciones (cuádruplas)
    transiciones_raw = mt_spec.get("transiciones")
    if not isinstance(transiciones_raw, list):
        raise SpecificationError("La clave 'transiciones' debe ser una lista de cuádruplas.")

    transitions_map: Dict[Tuple[str, str], Transition] = {}

    for idx, item in enumerate(transiciones_raw, start=1):
        if isinstance(item, str):
            parts = item.strip().split()
        elif isinstance(item, list):
            parts = [str(p).strip() for p in item]
        else:
            raise SpecificationError(
                f"Transición #{idx} tiene formato inválido. Debe ser una cadena con 4 elementos o lista de 4 elementos: {item}"
            )

        if len(parts) != 4:
            raise SpecificationError(
                f"Transición #{idx} inválida: '{item}'. Se requieren exactamente 4 elementos "
                f"(estado_origen simbolo_leido accion estado_destino). Encontrados: {len(parts)}."
            )

        origin, read_sym, action, dest = parts[0], parts[1], parts[2], parts[3]

        # Validar estado origen
        if origin not in estados:
            raise SpecificationError(
                f"Transición #{idx} ('{item}'): El estado origen '{origin}' no está en la lista de estados."
            )

        # Validar símbolo leído
        if read_sym not in alfabeto:
            raise SpecificationError(
                f"Transición #{idx} ('{item}'): El símbolo leído '{read_sym}' no pertenece al alfabeto."
            )

        # Validar acción: puede ser movimiento ('R', 'L', 'S') o escritura (un símbolo del alfabeto)
        action_upper = action.upper()
        if action_upper in {"R", "L", "S"} and action not in (alfabeto - {"R", "L", "S"}):
            action_type = "MOVE"
            action_clean = action_upper
        elif action in alfabeto:
            action_type = "WRITE"
            action_clean = action
        elif action_upper in {"R", "L", "S"}:
            # Caso donde R o L está en el alfabeto pero se especifica movimiento
            action_type = "MOVE"
            action_clean = action_upper
        else:
            raise SpecificationError(
                f"Transición #{idx} ('{item}'): La acción '{action}' es inválida. "
                f"Debe ser un movimiento ('R', 'L') o un símbolo válido del alfabeto {sorted(list(alfabeto))}."
            )

        # Validar estado destino
        if dest not in estados:
            raise SpecificationError(
                f"Transición #{idx} ('{item}'): El estado destino '{dest}' no está en la lista de estados."
            )

        # Programación defensiva contra no-determinismo
        key = (origin, read_sym)
        if key in transitions_map:
            raise SpecificationError(
                f"Transición no-determinista o duplicada detectada: Ya existe una regla para "
                f"el estado '{origin}' leyendo el símbolo '{read_sym}':\n"
                f"  Existente: {transitions_map[key]}\n"
                f"  Duplicada: {item}"
            )

        transitions_map[key] = Transition(
            origin_state=origin,
            read_symbol=read_sym,
            action=action_clean,
            action_type=action_type,
            next_state=dest
        )

    return {
        "estados": estados,
        "alfabeto": alfabeto,
        "estado_inicial": estado_inicial,
        "blanco": blank_symbol,
        "transiciones": transitions_map,
        "raw_data": mt_spec
    }


def validate_input_string(input_str: str, alphabet: Set[str], blank_symbol: str) -> None:
    """
    Verifica que la cadena de entrada contenga únicamente caracteres del alfabeto.
    """
    for idx, char in enumerate(input_str):
        if char not in alphabet:
            raise SpecificationError(
                f"Carácter inválido '{char}' en la posición {idx} de la cadena de entrada. "
                f"No pertenece al alfabeto definido: {sorted(list(alphabet))}."
            )
