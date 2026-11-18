#!/usr/bin/env python3
"""
Simulador de Máquinas de Turing
Teoría de la Computación - CC2019
Universidad del Valle de Guatemala
"""

import sys
import os
import argparse
from typing import Optional

from turing_machine import (
    parse_and_validate_yaml,
    validate_input_string,
    SpecificationError,
    TuringMachine
)

# Códigos de color ANSI para presentación en consola
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"


def disable_colors():
    global CYAN, GREEN, YELLOW, RED, BOLD, DIM, RESET
    CYAN = GREEN = YELLOW = RED = BOLD = DIM = RESET = ""


def print_banner():
    banner = f"""{CYAN}{BOLD}
╔════════════════════════════════════════════════════════════════╗
║             SIMULADOR DE MÁQUINAS DE TURING                    ║
║      Teoría de la Computación (CC2019) - Proyecto #3           ║
╚════════════════════════════════════════════════════════════════╝{RESET}"""
    print(banner)


def run_simulation(
    yaml_path: str,
    input_str: str,
    step_by_step: bool = False,
    show_visual: bool = True,
    max_steps: Optional[int] = None
):
    print(f"\n{BOLD}Cargando especificación:{RESET} {yaml_path}")
    try:
        spec = parse_and_validate_yaml(yaml_path)
    except SpecificationError as e:
        print(f"\n{RED}{BOLD}[ERROR DE ESPECIFICACIÓN]{RESET} {e}")
        return False
    except Exception as e:
        print(f"\n{RED}{BOLD}[ERROR INESPERADO]{RESET} {e}")
        return False

    print(f"{GREEN}✓ Archivo YAML validado correctamente.{RESET}")
    print(f"  • Estados ({len(spec['estados'])}): {sorted(list(spec['estados']))}")
    print(f"  • Alfabeto ({len(spec['alfabeto'])}): {sorted(list(spec['alfabeto']))}")
    print(f"  • Estado inicial: {spec['estado_inicial']}")
    print(f"  • Símbolo blanco: '{spec['blanco']}'")
    print(f"  • Total de transiciones: {len(spec['transiciones'])}")

    print(f"\n{BOLD}Cadena de entrada:{RESET} '{input_str}' (Longitud: {len(input_str)})")
    try:
        tm = TuringMachine(spec, input_str)
    except SpecificationError as e:
        print(f"\n{RED}{BOLD}[ERROR EN CADENA DE ENTRADA]{RESET} {e}")
        return False

    print(f"\n{YELLOW}{BOLD}Iniciando computación...{RESET}")
    print(f"{DIM}Presiona Ctrl+C en cualquier momento para cancelar la ejecución.{RESET}\n")
    print(f"{BOLD}COMPUTACIÓN COMPLETA (Descripciones Instantáneas):{RESET}")
    print("=" * 64)

    auto_finish = not step_by_step

    def step_handler(step_num: int, id_str: str, visual_str: str, trans) -> bool:
        nonlocal auto_finish

        trans_str = ""
        if trans:
            if trans.action_type == "MOVE":
                action_desc = f"Mover {trans.action}"
            else:
                action_desc = f"Escribir '{trans.action}'"
            trans_str = f"  {DIM}→ δ({trans.origin_state}, '{trans.read_symbol}') = ({action_desc}, {trans.next_state}){RESET}"

        # Imprimir Descripción Instantánea formal
        print(f"{CYAN}Paso {step_num:4d}:{RESET}  {BOLD}{id_str}{RESET}{trans_str}")
        if show_visual:
            print(f"           {DIM}{visual_str}{RESET}")

        if not auto_finish:
            try:
                prompt = f"{YELLOW}[Enter: siguiente paso | 't': terminar automático | 'c': cancelar]: {RESET}"
                choice = input(prompt).strip().lower()
                if choice == "c":
                    return False
                elif choice == "t":
                    auto_finish = True
            except (KeyboardInterrupt, EOFError):
                print()
                return False

        return True

    res = tm.run(on_step=step_handler, max_steps=max_steps)

    print("=" * 64)
    print(f"\n{BOLD}RESUMEN FINAL DE LA SIMULACIÓN:{RESET}")
    print(f"  • Total de pasos ejecutados: {BOLD}{res['total_pasos']}{RESET}")
    print(f"  • Estado final:             {BOLD}{res['estado_final']}{RESET}")
    print(f"  • Posición final cabezal:   {BOLD}{res['posicion_cabezal']}{RESET}")
    print(f"  • Descripción final:        {BOLD}{res['id_final']}{RESET}")
    print(f"  • Motivo de parada:         {DIM}{res['motivo_parada']}{RESET}")
    print(f"\n{GREEN}{BOLD}RESULTADO EXTRAÍDO DE LA CINTA:{RESET} {BOLD}'{res['resultado_cinta']}'{RESET}\n")
    return True


def interactive_menu():
    print_banner()
    while True:
        print("\nSeleccione una opción:")
        print("  1) Ejecutar Máquina 1: Predecesor Binario (resta 1)")
        print("  2) Ejecutar Máquina 2: Verificador de Palíndromos")
        print("  3) Cargar Máquina personalizada (archivo YAML)")
        print("  4) Salir")

        try:
            choice = input(f"\n{BOLD}Opción [1-4]: {RESET}").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nSaliendo del simulador.")
            break

        if choice == "1":
            yaml_path = "ejemplos/predecesor_binario.yaml"
            default_in = "1100"
            inp = input(f"Ingrese cadena binaria (Enter para defecto '{default_in}'): ").strip()
            if not inp:
                inp = default_in
            mode = input("¿Ejecutar paso a paso interactivo? (s/N): ").strip().lower() == "s"
            run_simulation(yaml_path, inp, step_by_step=mode)

        elif choice == "2":
            yaml_path = "ejemplos/verificador_palindromos.yaml"
            default_in = "10101"
            inp = input(f"Ingrese cadena binaria (Enter para defecto '{default_in}'): ").strip()
            if not inp:
                inp = default_in
            mode = input("¿Ejecutar paso a paso interactivo? (s/N): ").strip().lower() == "s"
            run_simulation(yaml_path, inp, step_by_step=mode)

        elif choice == "3":
            yaml_path = input("Ruta al archivo YAML: ").strip()
            if not os.path.exists(yaml_path):
                print(f"{RED}Archivo no encontrado: {yaml_path}{RESET}")
                continue
            inp = input("Cadena de entrada: ").strip()
            mode = input("¿Ejecutar paso a paso interactivo? (s/N): ").strip().lower() == "s"
            run_simulation(yaml_path, inp, step_by_step=mode)

        elif choice == "4":
            print("¡Hasta luego!")
            break
        else:
            print(f"{RED}Opción no válida.{RESET}")


def main():
    parser = argparse.ArgumentParser(
        description="Simulador de Máquinas de Turing (CC2019 - Proyecto #3 - UVG)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python3 main.py ejemplos/predecesor_binario.yaml 1100
  python3 main.py ejemplos/verificador_palindromos.yaml 10101 --paso-a-paso
  python3 main.py  (Inicia en modo interactivo)
"""
    )
    parser.add_argument("archivo_yaml", nargs="?", help="Ruta al archivo YAML con la especificación de la MT")
    parser.add_argument("cadena_entrada", nargs="?", default="", help="Cadena de entrada para la cinta")
    parser.add_argument("-s", "--paso-a-paso", action="store_true", help="Avanzar manualmente paso por paso")
    parser.add_argument("--sin-visual", action="store_true", help="Ocultar la vista gráfica de la cinta")
    parser.add_argument("--limite", type=int, default=None, help="Límite máximo de pasos para evitar bucles infinitos")
    parser.add_argument("--no-color", action="store_true", help="Desactivar colores en la consola")

    args = parser.parse_args()

    if args.no_color or not sys.stdout.isatty():
        disable_colors()

    if not args.archivo_yaml:
        interactive_menu()
    else:
        print_banner()
        run_simulation(
            yaml_path=args.archivo_yaml,
            input_str=args.cadena_entrada,
            step_by_step=args.paso_a_paso,
            show_visual=not args.sin_visual,
            max_steps=args.limite
        )


if __name__ == "__main__":
    main()
