import sys
import sympy as sp
import numpy as np
import matplotlib
matplotlib.use('QtAgg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QTextEdit, QPushButton, QComboBox, QListWidget,
    QStackedWidget, QSpinBox, QDoubleSpinBox, QSlider, QGroupBox,
    QFormLayout, QMessageBox
)
from PySide6.QtCore import Qt

# ──────────────────────────────────────────────
# Helper Functions
# ──────────────────────────────────────────────
def safe_eval(expr):
    try:
        return sp.sympify(expr)
    except Exception:
        return None

def is_prime(n):
    if n <= 1: return False
    if n <= 3: return True
    if n % 2 == 0 or n % 3 == 0: return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0: return False
        i += 6
    return True

def parse_matrix(text):
    rows = [row for row in text.strip().split("\n") if row.strip()]
    return np.array([[float(x) for x in row.split()] for row in rows])

# ──────────────────────────────────────────────
# Main Window Class
# ──────────────────────────────────────────────
class CalculatorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🧮 Multi-Function Calculator")
        self.resize(1000, 700)

        self.history = []

        # Main UI Setup
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # Left Sidebar (Navigation)
        sidebar = QVBoxLayout()
        self.nav_list = QListWidget()
        self.nav_list.addItems([
            "Basic Arithmetic", "Exponentiation & Logs", "Calculus",
            "Factorization", "Solve Equation", "Statistics",
            "Matrix Operations", "Complex Arithmetic", "Plot Function",
            "Prime Checker/Generator", "Solve System of Equations"
        ])
        self.nav_list.currentRowChanged.connect(self.switch_page)
        sidebar.addWidget(QLabel("<h2>Operations</h2>"))
        sidebar.addWidget(self.nav_list)
        
        # Sidebar Instructions
        info_label = QLabel(
            "<small><b>Instructions:</b><br>"
            "- Select an operation from above.<br>"
            "- Enter inputs in the right panel.<br>"
            "- Press Calculate to see results.<br>"
            "- Use 'x' as the variable for calculus/plotting.<br>"
            "- Complex numbers use Python syntax: 1+2j<br>"
            "- Matrices: rows on new lines, values separated by spaces.</small>"
        )
        info_label.setWordWrap(True)
        sidebar.addWidget(info_label)
        
        main_layout.addLayout(sidebar, 1)

        # Right Panel (Content & History)
        right_panel = QVBoxLayout()
        
        self.stack = QStackedWidget()
        right_panel.addWidget(self.stack, 3)

        # History Section
        hist_group = QGroupBox("🕘 Calculation History (Last 10)")
        hist_layout = QVBoxLayout(hist_group)
        self.history_text = QTextEdit()
        self.history_text.setReadOnly(True)
        hist_layout.addWidget(self.history_text)
        
        clear_hist_btn = QPushButton("🗑️ Clear History")
        clear_hist_btn.clicked.connect(self.clear_history)
        hist_layout.addWidget(clear_hist_btn)
        
        right_panel.addWidget(hist_group, 1)
        main_layout.addLayout(right_panel, 3)

        # Build Pages
        self.build_basic_arithmetic_page()
        self.build_exp_log_page()
        self.build_calculus_page()
        self.build_factorization_page()
        self.build_solve_eq_page()
        self.build_statistics_page()
        self.build_matrix_page()
        self.build_complex_page()
        self.build_plot_page()
        self.build_prime_page()
        self.build_system_eq_page()

        self.nav_list.setCurrentRow(0)

    def switch_page(self, index):
        self.stack.setCurrentIndex(index)

    def update_history(self, entry):
        self.history.append(entry)
        recent = self.history[-10:]
        self.history_text.setPlainText("\n".join(reversed(recent)))

    def clear_history(self):
        self.history = []
        self.history_text.clear()

    # ──────────────────────────────────────────
    # 1. Basic Arithmetic
    # ──────────────────────────────────────────
    def build_basic_arithmetic_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        
        layout.addWidget(QLabel("<h3>➕ Basic Arithmetic</h3>"))
        
        form = QFormLayout()
        self.basic_e1 = QLineEdit("10")
        self.basic_e2 = QLineEdit("5")
        self.basic_op = QComboBox()
        self.basic_op.addItems(["Add", "Subtract", "Multiply", "Divide"])
        form.addRow("Expression 1:", self.basic_e1)
        form.addRow("Expression 2:", self.basic_e2)
        form.addRow("Operation:", self.basic_op)
        layout.addLayout(form)

        btn = QPushButton("Calculate")
        btn.clicked.connect(self.calc_basic)
        layout.addWidget(btn)

        self.basic_out = QTextEdit()
        self.basic_out.setReadOnly(True)
        layout.addWidget(self.basic_out)
        
        self.stack.addWidget(page)

    def calc_basic(self):
        v1, v2 = safe_eval(self.basic_e1.text()), safe_eval(self.basic_e2.text())
        op = self.basic_op.currentText()
        if v1 is None or v2 is None:
            self.basic_out.setText("Error: Invalid expression")
            return
        
        result = None
        if op == "Add": result = v1 + v2
        elif op == "Subtract": result = v1 - v2
        elif op == "Multiply": result = v1 * v2
        elif op == "Divide":
            if v2 == 0:
                self.basic_out.setText("Error: Cannot divide by zero!")
                return
            result = v1 / v2
            
        self.basic_out.setText(f"Result: {result}")
        self.update_history(f"{self.basic_e1.text()} {op} {self.basic_e2.text()} = {result}")

    # ──────────────────────────────────────────
    # 2. Exponentiation & Logs
    # ──────────────────────────────────────────
    def build_exp_log_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(QLabel("<h3>🔢 Exponentiation & Logarithms</h3>"))
        
        self.explog_op = QComboBox()
        self.explog_op.addItems(["Exponentiation", "Logarithm", "Square Root"])
        self.explog_op.currentIndexChanged.connect(self.toggle_explog_inputs)
        layout.addWidget(self.explog_op)

        self.explog_stack = QStackedWidget()
        layout.addWidget(self.explog_stack)

        # Exp
        w1 = QWidget(); f1 = QFormLayout(w1)
        self.exp_base = QLineEdit("2"); self.exp_pow = QLineEdit("3")
        f1.addRow("Base:", self.exp_base); f1.addRow("Exponent:", self.exp_pow)
        self.explog_stack.addWidget(w1)

        # Log
        w2 = QWidget(); f2 = QFormLayout(w2)
        self.log_val = QLineEdit("10"); self.log_base = QLineEdit("e")
        f2.addRow("Value:", self.log_val); f2.addRow("Base:", self.log_base)
        self.explog_stack.addWidget(w2)

        # Sqrt
        w3 = QWidget(); f3 = QFormLayout(w3)
        self.sqrt_val = QLineEdit("9")
        f3.addRow("Value:", self.sqrt_val)
        self.explog_stack.addWidget(w3)

        btn = QPushButton("Calculate"); btn.clicked.connect(self.calc_explog)
        layout.addWidget(btn)

        self.explog_out = QTextEdit(); self.explog_out.setReadOnly(True)
        layout.addWidget(self.explog_out)
        self.stack.addWidget(page)

    def toggle_explog_inputs(self, idx):
        self.explog_stack.setCurrentIndex(idx)

    def calc_explog(self):
        op = self.explog_op.currentText()
        try:
            if op == "Exponentiation":
                b, e = safe_eval(self.exp_base.text()), safe_eval(self.exp_pow.text())
                if b is None or e is None: raise ValueError("Invalid input")
                res = b**e
                self.explog_out.setText(f"Result: {res}")
                self.update_history(f"{b} ** {e} = {res}")
            elif op == "Logarithm":
                v = float(self.log_val.text())
                b_text = self.log_base.text()
                if v <= 0: raise ValueError("Value must be positive")
                if b_text.lower() == 'e':
                    res = sp.log(v).evalf()
                else:
                    b = float(b_text)
                    if b <= 0 or b == 1: raise ValueError("Base must be >0 and !=1")
                    res = sp.log(v, b).evalf()
                self.explog_out.setText(f"Result: {res}")
                self.update_history(f"log base {b_text} of {v} = {res}")
            else:
                v = float(self.sqrt_val.text())
                if v < 0: raise ValueError("Value cannot be negative")
                res = sp.sqrt(v).evalf()
                self.explog_out.setText(f"Result: {res}")
                self.update_history(f"sqrt({v}) = {res}")
        except Exception as e:
            self.explog_out.setText(f"Error: {e}")

    # ──────────────────────────────────────────
    # 3. Calculus
    # ──────────────────────────────────────────
    def build_calculus_page(self):
        page = QWidget(); layout = QVBoxLayout(page)
        layout.addWidget(QLabel("<h3>📐 Calculus Operations</h3>"))
        
        self.calc_op = QComboBox()
        self.calc_op.addItems(["Derivative", "Nth Derivative", "Integral (Indefinite)", "Integral (Definite)"])
        self.calc_op.currentIndexChanged.connect(self.toggle_calc_inputs)
        layout.addWidget(self.calc_op)

        self.calc_stack = QStackedWidget(); layout.addWidget(self.calc_stack)

        # Deriv
        w1 = QWidget(); f1 = QFormLayout(w1)
        self.calc_deriv_expr = QLineEdit("x**3 + 2*x")
        f1.addRow("f(x):", self.calc_deriv_expr)
        self.calc_stack.addWidget(w1)

        # Nth Deriv
        w2 = QWidget(); f2 = QFormLayout(w2)
        self.calc_nth_expr = QLineEdit("x**3 + 2*x")
        self.calc_nth_n = QSpinBox(); self.calc_nth_n.setValue(1); self.calc_nth_n.setMinimum(1)
        f2.addRow("f(x):", self.calc_nth_expr); f2.addRow("n:", self.calc_nth_n)
        self.calc_stack.addWidget(w2)

        # Indef
        w3 = QWidget(); f3 = QFormLayout(w3)
        self.calc_indef_expr = QLineEdit("x**3 + 2*x")
        f3.addRow("f(x):", self.calc_indef_expr)
        self.calc_stack.addWidget(w3)

        # Def
        w4 = QWidget(); f4 = QFormLayout(w4)
        self.calc_def_expr = QLineEdit("x**3 + 2*x")
        self.calc_def_a = QLineEdit("0"); self.calc_def_b = QLineEdit("1")
        f4.addRow("f(x):", self.calc_def_expr)
        f4.addRow("Lower Limit (a):", self.calc_def_a); f4.addRow("Upper Limit (b):", self.calc_def_b)
        self.calc_stack.addWidget(w4)

        btn = QPushButton("Calculate"); btn.clicked.connect(self.calc_calc)
        layout.addWidget(btn)

        self.calc_out = QTextEdit(); self.calc_out.setReadOnly(True)
        layout.addWidget(self.calc_out)
        self.stack.addWidget(page)

    def toggle_calc_inputs(self, idx):
        self.calc_stack.setCurrentIndex(idx)

    def calc_calc(self):
        op = self.calc_op.currentText()
        x = sp.symbols('x')
        try:
            if op == "Derivative":
                f = safe_eval(self.calc_deriv_expr.text())
                if f is None: raise ValueError("Invalid expression")
                res = sp.diff(f, x)
                self.calc_out.setText(f"Derivative: {res}")
                self.update_history(f"d/dx({f}) = {res}")
            elif op == "Nth Derivative":
                f = safe_eval(self.calc_nth_expr.text())
                if f is None: raise ValueError("Invalid expression")
                n = self.calc_nth_n.value()
                res = sp.diff(f, x, n)
                self.calc_out.setText(f"{n}th Derivative: {res}")
                self.update_history(f"d^{n}/dx^{n}({f}) = {res}")
            elif op == "Integral (Indefinite)":
                f = safe_eval(self.calc_indef_expr.text())
                if f is None: raise ValueError("Invalid expression")
                res = sp.integrate(f, x)
                self.calc_out.setText(f"Indefinite Integral: {res} + C")
                self.update_history(f"∫ {f} dx = {res} + C")
            else:
                f = safe_eval(self.calc_def_expr.text())
                if f is None: raise ValueError("Invalid expression")
                a_val = float(sp.sympify(self.calc_def_a.text()))
                b_val = float(sp.sympify(self.calc_def_b.text()))
                res = sp.integrate(f, (x, a_val, b_val))
                self.calc_out.setText(f"Definite Integral from {a_val} to {b_val}: {res.evalf()}")
                self.update_history(f"∫_{a_val}^{b_val} {f} dx = {res.evalf()}")
        except Exception as e:
            self.calc_out.setText(f"Error: {e}")

    # ──────────────────────────────────────────
    # 4. Factorization
    # ──────────────────────────────────────────
    def build_factorization_page(self):
        page = QWidget(); layout = QVBoxLayout(page)
        layout.addWidget(QLabel("<h3>✂️ Factorization</h3>"))
        form = QFormLayout()
        self.factor_expr = QLineEdit("x**2 - 4")
        form.addRow("Expression:", self.factor_expr)
        layout.addLayout(form)
        
        btn = QPushButton("Factorize"); btn.clicked.connect(self.calc_factor)
        layout.addWidget(btn)
        
        self.factor_out = QTextEdit(); self.factor_out.setReadOnly(True)
        layout.addWidget(self.factor_out)
        self.stack.addWidget(page)

    def calc_factor(self):
        try:
            x = sp.symbols('x')
            f = safe_eval(self.factor_expr.text())
            if f is None: raise ValueError("Invalid expression")
            res = sp.factor(f)
            self.factor_out.setText(f"Factored form: {res}")
            self.update_history(f"factor({f}) = {res}")
        except Exception as e:
            self.factor_out.setText(f"Error: {e}")

    # ──────────────────────────────────────────
    # 5. Solve Equation
    # ──────────────────────────────────────────
    def build_solve_eq_page(self):
        page = QWidget(); layout = QVBoxLayout(page)
        layout.addWidget(QLabel("<h3>🔍 Solve Equation f(x) = 0</h3>"))
        form = QFormLayout()
        self.solve_expr = QLineEdit("x**2 - 4")
        form.addRow("Expression:", self.solve_expr)
        layout.addLayout(form)
        
        btn = QPushButton("Solve"); btn.clicked.connect(self.calc_solve)
        layout.addWidget(btn)
        
        self.solve_out = QTextEdit(); self.solve_out.setReadOnly(True)
        layout.addWidget(self.solve_out)
        self.stack.addWidget(page)

    def calc_solve(self):
        try:
            x = sp.symbols('x')
            f = safe_eval(self.solve_expr.text())
            if f is None: raise ValueError("Invalid expression")
            res = sp.solve(f, x)
            self.solve_out.setText(f"Solutions: {res}")
            self.update_history(f"Solve {f} = 0 → {res}")
        except Exception as e:
            self.solve_out.setText(f"Error: {e}")

    # ──────────────────────────────────────────
    # 6. Statistics
    # ──────────────────────────────────────────
    def build_statistics_page(self):
        page = QWidget(); layout = QVBoxLayout(page)
        layout.addWidget(QLabel("<h3>📊 Statistics</h3>"))
        form = QFormLayout()
        self.stats_data = QTextEdit("1, 2, 3, 4, 5")
        self.stats_data.setMaximumHeight(80)
        form.addRow("Numbers (comma separated):", self.stats_data)
        layout.addLayout(form)

        btn = QPushButton("Calculate"); btn.clicked.connect(self.calc_stats)
        layout.addWidget(btn)

        self.stats_out = QTextEdit(); self.stats_out.setReadOnly(True)
        layout.addWidget(self.stats_out)
        self.stack.addWidget(page)

    def calc_stats(self):
        try:
            data = [float(n.strip()) for n in self.stats_data.toPlainText().split(",") if n.strip()]
            if not data: raise ValueError("Empty data")
            arr = np.array(data)
            mean = np.mean(arr); median = np.median(arr)
            variance = np.var(arr, ddof=1) if len(arr) > 1 else 0
            std_dev = np.std(arr, ddof=1) if len(arr) > 1 else 0
            data_range = np.ptp(arr)
            counts = {v: data.count(v) for v in set(data)}
            mode = max(counts, key=counts.get) if counts else None

            result = (
                f"Mean: {mean:.4f}\n"
                f"Median: {median:.4f}\n"
                f"Mode: {mode}\n"
                f"Variance: {variance:.4f}\n"
                f"Std Deviation: {std_dev:.4f}\n"
                f"Range: {data_range:.4f}"
            )
            self.stats_out.setText(result)
            self.update_history(f"Stats on {data} → mean={mean:.4f}")
        except Exception as e:
            self.stats_out.setText(f"Error: {e}")

    # ──────────────────────────────────────────
    # 7. Matrix Operations
    # ──────────────────────────────────────────
    def build_matrix_page(self):
        page = QWidget(); layout = QVBoxLayout(page)
        layout.addWidget(QLabel("<h3>🔲 Matrix Operations</h3>"))
        
        form = QFormLayout()
        self.mat1 = QTextEdit("1 2\n3 4"); self.mat1.setMaximumHeight(60)
        self.mat2 = QTextEdit("5 6\n7 8"); self.mat2.setMaximumHeight(60)
        self.mat_op = QComboBox()
        self.mat_op.addItems(["Add", "Multiply", "Transpose (M1)", "Determinant (M1)", "Inverse (M1)"])
        form.addRow("Matrix 1:", self.mat1); form.addRow("Matrix 2:", self.mat2)
        form.addRow("Operation:", self.mat_op)
        layout.addLayout(form)

        btn = QPushButton("Calculate"); btn.clicked.connect(self.calc_matrix)
        layout.addWidget(btn)

        self.mat_out = QTextEdit(); self.mat_out.setReadOnly(True)
        layout.addWidget(self.mat_out)
        self.stack.addWidget(page)

    def calc_matrix(self):
        try:
            m1 = parse_matrix(self.mat1.toPlainText())
            m2_text = self.mat2.toPlainText().strip()
            m2 = parse_matrix(m2_text) if m2_text else None
            op = self.mat_op.currentText()
            
            res = None
            if op == "Add":
                if m2 is None: raise ValueError("M2 required")
                res = m1 + m2
            elif op == "Multiply":
                if m2 is None: raise ValueError("M2 required")
                res = np.dot(m1, m2)
            elif op == "Transpose (M1)": res = m1.T
            elif op == "Determinant (M1)":
                res = np.linalg.det(m1)
                self.mat_out.setText(f"Determinant: {res}")
                self.update_history(f"Mat Det = {res}")
                return
            elif op == "Inverse (M1)":
                det = np.linalg.det(m1)
                if abs(det) < 1e-12: raise ValueError("Singular matrix")
                res = np.linalg.inv(m1)
            
            self.mat_out.setText(f"Result:\n{res}")
            self.update_history(f"Mat {op} calculated")
        except Exception as e:
            self.mat_out.setText(f"Error: {e}")

    # ──────────────────────────────────────────
    # 8. Complex Arithmetic
    # ──────────────────────────────────────────
    def build_complex_page(self):
        page = QWidget(); layout = QVBoxLayout(page)
        layout.addWidget(QLabel("<h3>🌀 Complex Number Arithmetic</h3>"))
        form = QFormLayout()
        self.comp_e1 = QLineEdit("1+2j"); self.comp_e2 = QLineEdit("3-4j")
        self.comp_op = QComboBox()
        self.comp_op.addItems(["Add", "Subtract", "Multiply", "Divide", "Exponentiate"])
        form.addRow("Number 1:", self.comp_e1); form.addRow("Number 2:", self.comp_e2)
        form.addRow("Operation:", self.comp_op)
        layout.addLayout(form)

        btn = QPushButton("Calculate"); btn.clicked.connect(self.calc_complex)
        layout.addWidget(btn)

        self.comp_out = QTextEdit(); self.comp_out.setReadOnly(True)
        layout.addWidget(self.comp_out)
        self.stack.addWidget(page)

    def calc_complex(self):
        try:
            c1, c2 = complex(self.comp_e1.text()), complex(self.comp_e2.text())
            op = self.comp_op.currentText()
            if op == "Add": res = c1 + c2
            elif op == "Subtract": res = c1 - c2
            elif op == "Multiply": res = c1 * c2
            elif op == "Divide":
                if c2 == 0: raise ValueError("Div by zero")
                res = c1 / c2
            else: res = c1 ** c2
            
            self.comp_out.setText(f"Result: {res}")
            self.update_history(f"{c1} {op} {c2} = {res}")
        except Exception as e:
            self.comp_out.setText(f"Error: {e}")

    # ──────────────────────────────────────────
    # 9. Plot Function
    # ──────────────────────────────────────────
    def build_plot_page(self):
        page = QWidget(); layout = QVBoxLayout(page)
        layout.addWidget(QLabel("<h3>📈 Function Plotter</h3>"))
        
        form = QFormLayout()
        self.plot_expr = QLineEdit("sin(x)")
        self.plot_xmin = QDoubleSpinBox(); self.plot_xmin.setRange(-10000, 10000); self.plot_xmin.setValue(-10)
        self.plot_xmax = QDoubleSpinBox(); self.plot_xmax.setRange(-10000, 10000); self.plot_xmax.setValue(10)
        self.plot_pts = QSlider(Qt.Horizontal); self.plot_pts.setRange(100, 1000); self.plot_pts.setValue(500)
        self.plot_pts_label = QLabel("500")
        self.plot_pts.valueChanged.connect(lambda v: self.plot_pts_label.setText(str(v)))

        form.addRow("f(x):", self.plot_expr)
        form.addRow("x min:", self.plot_xmin); form.addRow("x max:", self.plot_xmax)
        form.addRow("Points:", self.plot_pts)
        layout.addLayout(form)

        btn = QPushButton("Plot"); btn.clicked.connect(self.calc_plot)
        layout.addWidget(btn)

        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.fig)
        layout.addWidget(self.canvas)
        
        self.stack.addWidget(page)

    def calc_plot(self):
        try:
            x = sp.symbols('x')
            f = sp.sympify(self.plot_expr.text())
            f_np = sp.lambdify(x, f, modules=["numpy"])
            
            x_vals = np.linspace(self.plot_xmin.value(), self.plot_xmax.value(), self.plot_pts.value())
            y_vals = f_np(x_vals)

            self.ax.clear()
            self.ax.plot(x_vals, y_vals, linewidth=2, color="#1f77b4")
            self.ax.set_title(f"Plot of {self.plot_expr.text()}", fontsize=14)
            self.ax.grid(True, linestyle="--", alpha=0.7)
            self.ax.axhline(y=0, color="k", linewidth=0.5)
            self.ax.axvline(x=0, color="k", linewidth=0.5)
            self.canvas.draw()
            self.update_history(f"Plotted: {self.plot_expr.text()}")
        except Exception as e:
            QMessageBox.warning(self, "Plot Error", str(e))

    # ──────────────────────────────────────────
    # 10. Prime Checker / Generator
    # ──────────────────────────────────────────
    def build_prime_page(self):
        page = QWidget(); layout = QVBoxLayout(page)
        layout.addWidget(QLabel("<h3>🔑 Prime Checker & Generator</h3>"))

        self.prime_op = QComboBox()
        self.prime_op.addItems(["Check Prime", "Generate Primes up to N"])
        self.prime_op.currentIndexChanged.connect(self.toggle_prime_inputs)
        layout.addWidget(self.prime_op)

        self.prime_stack = QStackedWidget(); layout.addWidget(self.prime_stack)

        w1 = QWidget(); f1 = QFormLayout(w1)
        self.prime_check_n = QSpinBox(); self.prime_check_n.setRange(1, 999999999)
        f1.addRow("Integer:", self.prime_check_n)
        self.prime_stack.addWidget(w1)

        w2 = QWidget(); f2 = QFormLayout(w2)
        self.prime_gen_n = QSpinBox(); self.prime_gen_n.setRange(2, 999999999)
        f2.addRow("Limit:", self.prime_gen_n)
        self.prime_stack.addWidget(w2)

        btn = QPushButton("Run"); btn.clicked.connect(self.calc_prime)
        layout.addWidget(btn)

        self.prime_out = QTextEdit(); self.prime_out.setReadOnly(True)
        layout.addWidget(self.prime_out)
        self.stack.addWidget(page)

    def toggle_prime_inputs(self, idx):
        self.prime_stack.setCurrentIndex(idx)

    def calc_prime(self):
        op = self.prime_op.currentText()
        if op == "Check Prime":
            n = self.prime_check_n.value()
            if is_prime(n):
                self.prime_out.setText(f"✅ {n} is prime!")
                self.update_history(f"Checked: {n} is prime")
            else:
                self.prime_out.setText(f"❌ {n} is not prime.")
                self.update_history(f"Checked: {n} not prime")
        else:
            limit = self.prime_gen_n.value()
            primes = [i for i in range(2, limit + 1) if is_prime(i)]
            self.prime_out.setText(f"Primes up to {limit}:\n{primes}")
            self.update_history(f"Generated primes up to {limit}")

    # ──────────────────────────────────────────
    # 11. Solve System of Equations
    # ──────────────────────────────────────────
    def build_system_eq_page(self):
        page = QWidget(); layout = QVBoxLayout(page)
        layout.addWidget(QLabel("<h3>📝 Solve System of Linear Equations</h3>"))
        form = QFormLayout()
        self.sys_eqs = QTextEdit("x + y = 2\nx - y = 0")
        self.sys_eqs.setMaximumHeight(80)
        self.sys_vars = QLineEdit("x,y")
        form.addRow("Equations:", self.sys_eqs); form.addRow("Variables:", self.sys_vars)
        layout.addLayout(form)

        btn = QPushButton("Solve"); btn.clicked.connect(self.calc_system)
        layout.addWidget(btn)

        self.sys_out = QTextEdit(); self.sys_out.setReadOnly(True)
        layout.addWidget(self.sys_out)
        self.stack.addWidget(page)

    def calc_system(self):
        try:
            eqns = []
            for line in self.sys_eqs.toPlainText().strip().split("\n"):
                if "=" not in line: raise ValueError(f"Missing '=' in: {line}")
                left, right = line.split("=")
                eqns.append(sp.Eq(sp.sympify(left), sp.sympify(right)))
            
            variables = sp.symbols(self.sys_vars.text())
            sol = sp.solve(eqns, variables)
            self.sys_out.setText(f"Solution:\n{sol}")
            self.update_history(f"Solved system → {sol}")
        except Exception as e:
            self.sys_out.setText(f"Error: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CalculatorApp()
    window.show()
    sys.exit(app.exec())