# Calculator

Calculator is a desktop scientific calculator application built with PySide6. It integrates SymPy for symbolic mathematics and NumPy/Matplotlib for numerical computations and data visualization. The application uses a sidebar navigation paradigm with a `QStackedWidget` to switch between 13 distinct mathematical modules, all rendered within a custom dark-themed UI.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Entendore/Calculator.git
   cd Calculator
   ```

2. Install dependencies:
   ```bash
   pip install PySide6 sympy numpy matplotlib
   ```

## Execution

Run the application from the command line:
```bash
python app.py
```

## Features

- **Standard Calculator:** On-screen numpad and direct keyboard input. Evaluates expressions using `sympify` with a restricted namespace (`CALC_NS`) supporting trigonometric, logarithmic, and constant functions. Includes a live expression preview, history tracking (last 15 entries), and memory registers (MC, MR, M+, M-).
- **Exponents & Logarithms:** Computes exponentiation, custom base logarithms, square roots, and Nth roots. Utilizes SymPy for exact symbolic results alongside 12-digit numerical evaluation.
- **Calculus:** Symbolic differentiation (1st and nth order) and integration (indefinite and definite). Requires `x` as the independent variable.
- **Factorization:** Symbolic polynomial factorization using `sp.factor` and `sp.expand`.
- **Equation Solver:** Finds roots for expressions set to zero (f(x) = 0) using `sp.solve`. Provides exact and approximate numerical solutions.
- **Statistics:** Processes comma-separated datasets. Outputs count, sum, mean, median, mode, sample variance (ddof=1), sample standard deviation, min/max, range, 25th/75th percentiles, and interquartile range (IQR).
- **Matrix Operations:** Input parsed from newline/space-separated strings into NumPy arrays. Supports addition, subtraction, dot product multiplication, transposition, determinant, inverse (with singularity check), and eigenvalue calculation.
- **Complex Numbers:** Arithmetic operations (add, subtract, multiply, divide, exponentiate) on Python complex types (e.g., `1+2j`). Calculates conjugate and magnitude, outputting real/imaginary parts and phase in radians.
- **Function Plotter:** Renders symbolic expressions using Matplotlib embedded via `FigureCanvasQTAgg`. Allows configuration of x-min, x-max, and sample resolution via a slider (100-2000 points).
- **Prime Tools:** Checks primality (optimized 6k±1 trial division), generates primes up to a specified limit, and computes prime factorization with exponent aggregation.
- **System of Equations:** Solves linear systems. Input requires equations formatted as `expr = expr`, which are parsed into `sp.Eq` objects.
- **Base Converter:** Converts integers between decimal, hexadecimal, octal, and binary formats.
- **Combinatorics:** Module for combinations, permutations, factorials, GCD, and LCM.

## Technical Stack

- **PySide6 (Qt for Python):** GUI framework. Uses `QMainWindow`, `QStackedWidget` for page routing, and `FigureCanvasQTAgg` for Matplotlib integration.
- **SymPy:** Symbolic computation backend. Handles calculus, algebra, equation solving, and exact arithmetic.
- **NumPy:** Numerical backend. Powers the statistics module, matrix operations, and complex number phase calculations.
- **Matplotlib:** Plotting backend (`QtAgg` renderer). Configured programmatically to match the application's dark theme.

## Usage Specifications

- **Variable Syntax:** The `x` variable is hardcoded for the Calculus, Equation Solver, System of Equations, and Plotting modules.
- **Complex Syntax:** Complex numbers must be entered using Python's native format with a `j` suffix (e.g., `3+4j`).
- **Matrix Syntax:** Matrices are entered as plain text. Rows are delimited by newlines, and column values within a row are delimited by spaces.
- **Equation Syntax:** The System of Equations module requires one equation per line, explicitly containing an equals sign (e.g., `2*x - y = 1`).
- **Keyboard Bindings:** When the Calculator module is active, the application intercepts keypresses for digits, operators (`+`, `-`, `*`, `/`, `^`), `Enter` (evaluate), `Backspace` (delete), and `Escape` (clear).
- **Evaluation Environment:** The calculator's expression parser maps specific tokens to SymPy functions via the `CALC_NS` dictionary (e.g., `log10` maps to `sp.log(x, 10)`, `sqrt` maps to `sp.sqrt`).