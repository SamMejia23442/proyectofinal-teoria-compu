# Simulador de Máquinas de Turing
**Universidad del Valle de Guatemala**  
**Facultad de Ingeniería — Departamento de Ciencias de la Computación**  
**CC2019: Teoría de la Computación — Proyecto Final #3**

---

## 📌 Descripción General

Este proyecto implementa un **Simulador Universal de Máquinas de Turing Deterministas (MT)** de una sola cinta infinita en ambas direcciones y un único cabezal de lectura/escritura. El simulador interpreta especificaciones formales definidas en archivos **YAML** utilizando la convención formal de **cuádruplas**:

$$\delta(q_{\text{actual}}, s_{\text{leído}}) = (\text{acción}, q_{\text{siguiente}})$$

donde la acción corresponde a un movimiento del cabezal ($R$ o $L$) o a la escritura de un símbolo del alfabeto sobre la cinta.

El motor ejecuta paso a paso la computación completa, genera el listado de **Descripciones Instantáneas (IDs)** formales $\alpha [q] \beta$, despliega una visualización gráfica de la cinta y extrae el resultado final.

---

## 🚀 Características Principales

- **Cinta Infinita Bidireccional:** Indexación dinámica para celdas a la izquierda ($< 0$) y a la derecha ($\ge 0$).
- **Sintaxis YAML en Cuádruplas:** Definición intuitiva y limpia de estados, alfabeto, símbolo de blanco y reglas de transición.
- **Programación Defensiva Rigurosa:** Validación exhaustiva de tipos, estados existentes, pertenencia de símbolos al alfabeto, no-determinismo y entradas no permitidas.
- **Control de Ejecución y Cancelación:** Capacidad de interrumpir la simulación en cualquier momento con `Ctrl+C` o mediante modo paso a paso, previniendo bucles infinitos en máquinas indecidibles.
- **Visualización Dual:** Salida formal con notación matemática estándar e interfaz en consola con colores y cabezal resaltado.
- **Modo CLI e Interactivo:** Permite ejecución por línea de comandos con argumentos o mediante un menú interactivo.

---

## 📂 Estructura del Repositorio

```text
.
├── main.py                     # Punto de entrada principal (CLI y menú interactivo)
├── requirements.txt            # Dependencias del proyecto (PyYAML)
├── .gitignore                  # Reglas de exclusión para Git
├── turing_machine/             # Módulo central del simulador
│   ├── __init__.py
│   ├── machine.py              # Motor de ejecución de la MT y control de parada
│   ├── parser.py               # Analizador sintáctico defensivo y validador de cuádruplas
│   └── tape.py                 # Abstracción de cinta infinita bidireccional y formato de IDs
├── ejemplos/                   # Máquinas de Turing de ejemplo en YAML
│   ├── predecesor_binario.yaml        # Máquina 1: Resta 1 a un número binario (O(n))
│   └── verificador_palindromos.yaml   # Máquina 2: Reconocedor de palíndromos (O(n²))
└── doc/                        # Documentación e informe académico
    └── informe.tex             # Informe completo en LaTeX
```

---

## ⚙️ Instalación y Requisitos

El proyecto requiere **Python 3.8+** y la biblioteca `PyYAML`.

```bash
# 1. Clonar el repositorio (si aplica)
git clone https://github.com/SamMejia23442/proyectofinal-teoria-compu.git
cd proyectofinal-teoria-compu

# 2. Instalar dependencias
pip install -r requirements.txt
```

---

## 💻 Manual de Uso

### 1. Modo Interactivo (Recomendado)
Ejecuta el programa sin argumentos para acceder al menú interactivo:
```bash
python3 main.py
```

### 2. Modo Línea de Comandos (CLI)

#### Ejecutar Máquina 1: Predecesor Binario ($n - 1$)
Calcula $1100_2 - 1 = 1011_2$:
```bash
python3 main.py ejemplos/predecesor_binario.yaml 1100
```

#### Ejecutar Máquina 2: Verificador de Palíndromos
Verifica si `10101` es palíndromo (Resultado: `Y`):
```bash
python3 main.py ejemplos/verificador_palindromos.yaml 10101
```

Verifica si `10110` es palíndromo (Resultado: `N`):
```bash
python3 main.py ejemplos/verificador_palindromos.yaml 10110
```

### 3. Opciones y Banderas Avanzadas
- `-s`, `--paso-a-paso`: Permite avanzar manualmente presionando Enter, terminar automáticamente (`t`) o cancelar (`c`).
- `--sin-visual`: Oculta la vista gráfica de la cinta, mostrando únicamente las IDs formales.
- `--limite <N>`: Establece un límite preventivo de $N$ pasos para evitar ciclos indefinidos.
- `--no-color`: Desactiva secuencias de escape ANSI.

---

## 🧪 Máquinas Implementadas

| Máquina | Alfabeto $\Sigma$ | Estados | Complejidad | Ejemplo |
| :--- | :---: | :---: | :---: | :--- |
| **Predecesor Binario** | `0, 1, B` | 5 | $O(n)$ | Entrada: `1100` $\to$ Salida: `1011` |
| **Verificador de Palíndromos** | `0, 1, B, Y, N` | 13 | $O(n^2)$ | Entrada: `10101` $\to$ Salida: `Y` |

---

## 👥 Integrantes y Enlaces
- **Repositorio:** [https://github.com/SamMejia23442/proyectofinal-teoria-compu.git](https://github.com/SamMejia23442/proyectofinal-teoria-compu.git)
- **Video Explicativo:** *[Colocar enlace a YouTube aquí]*
