import sys
import math
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
    QFormLayout, QMessageBox, QGridLayout, QFrame, QSizePolicy,
    QStatusBar
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


# ═══════════════════════════════════════════════════════════════
# STYLESHEET — Professional dark theme
# ═══════════════════════════════════════════════════════════════
STYLESHEET = """
QMainWindow { background-color: #0f1021; }

QWidget { background-color: #0f1021; color: #d4d8e8; font-family: 'Segoe UI', Arial, sans-serif; font-size: 13px; }

/* ── Sidebar ── */
#sidebar { background-color: #151628; border-right: 1px solid #1e2040; }
#logo { color: #7b8cff; font-size: 26px; font-weight: 800; padding: 8px 4px 2px 4px; letter-spacing: 1px; }
#logoSub { color: #4a5080; font-size: 11px; padding: 0 4px 14px 4px; font-weight: 400; }

QListWidget { background-color: transparent; border: none; outline: none; font-size: 13px; padding: 4px; }
QListWidget::item { padding: 11px 14px; border-radius: 8px; margin: 2px 2px; color: #7a80a8; }
QListWidget::item:selected { background-color: #3b4cc0; color: #ffffff; font-weight: 600; }
QListWidget::item:hover:!selected { background-color: #1e2048; color: #c0c4e0; }

/* ── Labels ── */
#pageTitle { color: #a0b0ff; font-size: 20px; font-weight: 700; padding: 4px 0; }
#pageDesc  { color: #5a6080; font-size: 12px; padding: 2px 0 8px 0; }
#separator { background-color: #1e2040; max-height: 1px; }

/* ── Display ── */
#calcDisplayFrame { background-color: #0a0b18; border-radius: 14px; border: 1px solid #1a1c3a; }
#calcExprLabel { color: #4a5070; font-size: 15px; background: transparent; border: none; }
#calcResultLabel { color: #ffffff; font-size: 34px; font-weight: 700; background: transparent; border: none; }
#calcInputLine { background-color: #12132a; border: 1px solid #222450; border-radius: 8px; padding: 8px 12px; color: #9098c0; font-size: 14px; font-family: 'Consolas', 'Courier New', monospace; }

/* ── Inputs ── */
QLineEdit { background-color: #181a34; border: 1.5px solid #252850; border-radius: 8px; padding: 9px 13px; color: #d4d8e8; font-size: 13px; selection-background-color: #3b4cc0; }
QLineEdit:focus { border-color: #3b4cc0; }

QTextEdit { background-color: #181a34; border: 1.5px solid #252850; border-radius: 8px; padding: 9px 13px; color: #d4d8e8; font-size: 13px; selection-background-color: #3b4cc0; }

QComboBox { background-color: #181a34; border: 1.5px solid #252850; border-radius: 8px; padding: 8px 13px; color: #d4d8e8; min-width: 100px; }
QComboBox:focus { border-color: #3b4cc0; }
QComboBox::drop-down { border: none; width: 28px; }
QComboBox QAbstractItemView { background-color: #181a34; border: 1px solid #252850; color: #d4d8e8; selection-background-color: #3b4cc0; padding: 4px; }

QSpinBox, QDoubleSpinBox { background-color: #181a34; border: 1.5px solid #252850; border-radius: 8px; padding: 8px 13px; color: #d4d8e8; }
QSpinBox:focus, QDoubleSpinBox:focus { border-color: #3b4cc0; }

/* ── Buttons ── */
QPushButton#primaryBtn { background-color: #3b4cc0; border: none; border-radius: 10px; padding: 11px 28px; color: #fff; font-size: 14px; font-weight: 700; min-height: 18px; }
QPushButton#primaryBtn:hover { background-color: #5060e0; }
QPushButton#primaryBtn:pressed { background-color: #2a3aa0; }

QPushButton#secondaryBtn { background-color: #1e2048; border: 1px solid #2a2d60; border-radius: 8px; padding: 8px 18px; color: #7a80a8; font-size: 12px; }
QPushButton#secondaryBtn:hover { background-color: #2a2d60; color: #b0b8e0; }

QPushButton#dangerBtn { background-color: #3a1530; border: 1px solid #5a2040; border-radius: 8px; padding: 8px 18px; color: #f06090; font-size: 12px; }
QPushButton#dangerBtn:hover { background-color: #4a2040; }

/* ── Group Boxes ── */
QGroupBox { background-color: #13152a; border: 1px solid #1e2040; border-radius: 12px; margin-top: 18px; padding: 20px 16px 16px 16px; font-weight: 600; color: #6070c0; font-size: 13px; }
QGroupBox::title { subcontrol-origin: margin; left: 16px; padding: 0 8px; color: #6070c0; }

/* ── Slider ── */
QSlider::groove:horizontal { background: #1e2048; height: 5px; border-radius: 2px; }
QSlider::handle:horizontal { background: #3b4cc0; width: 16px; height: 16px; margin: -6px 0; border-radius: 8px; }
QSlider::sub-page:horizontal { background: #3b4cc0; border-radius: 2px; }

/* ── Scrollbar ── */
QScrollBar:vertical { background: #0f1021; width: 6px; border-radius: 3px; }
QScrollBar::handle:vertical { background: #2a2d60; border-radius: 3px; min-height: 30px; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }

/* ── Status Bar ── */
QStatusBar { background-color: #0c0d1a; color: #3a3e68; font-size: 11px; padding: 4px 14px; border-top: 1px solid #1a1c38; }
"""

# ═══════════════════════════════════════════════════════════════
# CALCULATOR BUTTON STYLES
# ═══════════════════════════════════════════════════════════════
BTN_NUM = """QPushButton{background:#1e2148;color:#e0e4ff;font-size:20px;font-weight:700;border-radius:10px;min-height:32px}
QPushButton:hover{background:#2a2e60}QPushButton:pressed{background:#363a78}"""

BTN_OP = """QPushButton{background:#2a1860;color:#c8b0ff;font-size:20px;font-weight:700;border-radius:10px;min-height:32px}
QPushButton:hover{background:#3a2880}QPushButton:pressed{background:#4a38a0}"""

BTN_FN = """QPushButton{background:#101838;color:#6090e0;font-size:12px;font-weight:700;border-radius:8px;min-height:22px}
QPushButton:hover{background:#182048}QPushButton:pressed{background:#202858}"""

BTN_EQ = """QPushButton{background:#3b4cc0;color:#fff;font-size:22px;font-weight:800;border-radius:10px;min-height:32px}
QPushButton:hover{background:#5060e0}QPushButton:pressed{background:#2a3aa0}"""

BTN_CLR = """QPushButton{background:#301828;color:#ff6090;font-size:16px;font-weight:700;border-radius:10px;min-height:28px}
QPushButton:hover{background:#402038}QPushButton:pressed{background:#502848}"""

BTN_MEM = """QPushButton{background:#141830;color:#5080b0;font-size:11px;font-weight:700;border-radius:8px;min-height:22px}
QPushButton:hover{background:#1e2448}QPushButton:pressed{background:#283060}"""


# ═══════════════════════════════════════════════════════════════
# CALCULATOR EVALUATION NAMESPACE
# ═══════════════════════════════════════════════════════════════
CALC_NS = {
    'log10': lambda x: sp.log(x, 10),
    'factorial': sp.factorial,
    'sqrt': sp.sqrt,
    'Abs': sp.Abs,
    'sin': sp.sin, 'cos': sp.cos, 'tan': sp.tan,
    'asin': sp.asin, 'acos': sp.acos, 'atan': sp.atan,
    'log': sp.log, 'exp': sp.exp,
    'pi': sp.pi, 'E': sp.E, 'e': sp.E,
}


# ═══════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════
def safe_eval(expr):
    try:
        return sp.sympify(expr, locals=CALC_NS)
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


# ═══════════════════════════════════════════════════════════════
# MAIN WINDOW
# ═══════════════════════════════════════════════════════════════
class CalculatorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ProCalc — Advanced Scientific Calculator")
        self.resize(1120, 760)

        self.history = []
        self.memory = 0.0
        self.last_result = None

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # ─── Sidebar ─────────────────────────────
        sidebar = QWidget()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(230)
        sb_layout = QVBoxLayout(sidebar)
        sb_layout.setContentsMargins(12, 18, 12, 14)
        sb_layout.setSpacing(4)

        logo = QLabel("ProCalc")
        logo.setObjectName("logo")
        sb_layout.addWidget(logo)
        sub = QLabel("Advanced Scientific Calculator")
        sub.setObjectName("logoSub")
        sb_layout.addWidget(sub)

        self.nav_list = QListWidget()
        self.nav_list.addItems([
            "🧮  Calculator",
            "🔢  Exponents & Logs",
            "📐  Calculus",
            "✂️  Factorization",
            "🔍  Equation Solver",
            "📊  Statistics",
            "🔲  Matrix Operations",
            "🌀  Complex Numbers",
            "📈  Plot Function",
            "🔑  Prime Tools",
            "📝  System of Equations",
            "🔄  Base Converter",
            "🎲  Combinatorics",
        ])
        self.nav_list.currentRowChanged.connect(self.switch_page)
        sb_layout.addWidget(self.nav_list, 1)

        info = QLabel(
            "<small style='color:#3a4068'>Tip: Use <b>x</b> as variable for calculus / plotting. "
            "Complex numbers: <b>1+2j</b>. Matrices: rows on new lines, values space-separated.</small>"
        )
        info.setWordWrap(True)
        sb_layout.addWidget(info)

        main_layout.addWidget(sidebar)

        # ─── Content Area ────────────────────────
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(18, 14, 18, 10)
        content_layout.setSpacing(10)

        self.stack = QStackedWidget()
        content_layout.addWidget(self.stack, 5)

        # History panel
        hist_group = QGroupBox("⏱  Calculation History  (last 15)")
        hist_layout = QVBoxLayout(hist_group)
        self.history_text = QTextEdit()
        self.history_text.setReadOnly(True)
        self.history_text.setMaximumHeight(130)
        hist_layout.addWidget(self.history_text)
        hist_btns = QHBoxLayout()
        clear_h = QPushButton("🗑  Clear")
        clear_h.setObjectName("dangerBtn")
        clear_h.clicked.connect(self.clear_history)
        copy_h = QPushButton("📋  Copy All")
        copy_h.setObjectName("secondaryBtn")
        copy_h.clicked.connect(lambda: self._copy_text(self.history_text.toPlainText()))
        hist_btns.addWidget(clear_h)
        hist_btns.addWidget(copy_h)
        hist_btns.addStretch()
        hist_layout.addLayout(hist_btns)
        content_layout.addWidget(hist_group, 1)

        main_layout.addWidget(content, 1)

        # Status bar
        self.setStatusBar(QStatusBar())

        # Build all pages
        self.build_calculator_page()
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
        self.build_base_converter_page()
        self.build_combinatorics_page()

        self.nav_list.setCurrentRow(0)

    # ─── Navigation & History ────────────────────
    def switch_page(self, index):
        self.stack.setCurrentIndex(index)
        tips = [
            "Type or click buttons to enter expressions. Press = to evaluate.",
            "Compute powers, roots, and logarithms with precision.",
            "Derivatives and integrals — use x as the variable.",
            "Factor polynomial expressions symbolically.",
            "Solve f(x) = 0 for x.",
            "Mean, median, mode, variance, and more.",
            "Add, multiply, transpose, invert matrices.",
            "Arithmetic on complex numbers.",
            "Plot any function f(x) over a custom range.",
            "Check primality or generate lists of primes.",
            "Solve systems of linear equations simultaneously.",
            "Convert numbers between bases: decimal, hex, octal, binary.",
            "Combinations, permutations, factorials, GCD, and LCM.",
        ]
        if 0 <= index < len(tips):
            self.statusBar().showMessage(tips[index])

    def update_history(self, entry):
        self.history.append(entry)
        recent = self.history[-15:]
        self.history_text.setPlainText("\n".join(reversed(recent)))

    def clear_history(self):
        self.history.clear()
        self.history_text.clear()
        self.statusBar().showMessage("History cleared.", 2000)

    def _copy_text(self, text):
        if text:
            QApplication.clipboard().setText(text)
            self.statusBar().showMessage("Copied to clipboard!", 2000)

    def _make_page_header(self, layout, icon_title, desc):
        t = QLabel(icon_title)
        t.setObjectName("pageTitle")
        layout.addWidget(t)
        d = QLabel(desc)
        d.setObjectName("pageDesc")
        d.setWordWrap(True)
        layout.addWidget(d)
        line = QFrame()
        line.setObjectName("separator")
        line.setFixedHeight(1)
        layout.addWidget(line)

    def _add_result_area(self, layout, attr_name):
        rg = QGroupBox("Result")
        rl = QVBoxLayout(rg)
        te = QTextEdit()
        te.setReadOnly(True)
        te.setMinimumHeight(80)
        setattr(self, attr_name, te)
        rl.addWidget(te)
        cb = QPushButton("📋  Copy Result")
        cb.setObjectName("secondaryBtn")
        cb.clicked.connect(lambda: self._copy_text(getattr(self, attr_name).toPlainText()))
        rl.addWidget(cb)
        layout.addWidget(rg)
        layout.addStretch()

    # ═══════════════════════════════════════════════
    # 1. CALCULATOR  (numpad + display + memory)
    # ═══════════════════════════════════════════════
    def build_calculator_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(8)
        layout.setContentsMargins(8, 8, 8, 8)

        # ── Display ──
        disp = QFrame()
        disp.setObjectName("calcDisplayFrame")
        dl = QVBoxLayout(disp)
        dl.setContentsMargins(16, 12, 16, 8)
        dl.setSpacing(2)

        self.calc_expr_label = QLabel("")
        self.calc_expr_label.setObjectName("calcExprLabel")
        self.calc_expr_label.setAlignment(Qt.AlignRight)
        dl.addWidget(self.calc_expr_label)

        self.calc_result_label = QLabel("0")
        self.calc_result_label.setObjectName("calcResultLabel")
        self.calc_result_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.calc_result_label.setMinimumHeight(52)
        dl.addWidget(self.calc_result_label)

        self.calc_input = QLineEdit()
        self.calc_input.setObjectName("calcInputLine")
        self.calc_input.setPlaceholderText("Type expression or use buttons below…")
        self.calc_input.textChanged.connect(self._update_calc_preview)
        self.calc_input.returnPressed.connect(self._evaluate_calc)
        dl.addWidget(self.calc_input)

        layout.addWidget(disp)

        # ── Button Grid ──
        grid = QGridLayout()
        grid.setSpacing(5)

        buttons = [
            # row, col, text, type, span
            (0, 0, "MC", "mem"),  (0, 1, "MR", "mem"),  (0, 2, "M+", "mem"),  (0, 3, "M−", "mem"),  (0, 4, "C", "clr"),
            (1, 0, "sin", "fn"), (1, 1, "cos", "fn"), (1, 2, "tan", "fn"), (1, 3, "(", "op"),  (1, 4, ")", "op"),
            (2, 0, "ln", "fn"),  (2, 1, "log₁₀", "fn"), (2, 2, "√", "fn"), (2, 3, "^", "op"),  (2, 4, "⌫", "clr"),
            (3, 0, "7", "num"),  (3, 1, "8", "num"),  (3, 2, "9", "num"),  (3, 3, "÷", "op"),  (3, 4, "%", "fn"),
            (4, 0, "4", "num"),  (4, 1, "5", "num"),  (4, 2, "6", "num"),  (4, 3, "×", "op"),  (4, 4, "n!", "fn"),
            (5, 0, "1", "num"),  (5, 1, "2", "num"),  (5, 2, "3", "num"),  (5, 3, "−", "op"),  (5, 4, "π", "fn"),
            (6, 0, "±", "fn"),  (6, 1, "0", "num"),  (6, 2, ".", "num"),  (6, 3, "+", "op"),  (6, 4, "=", "eq"),
        ]

        style_map = {"num": BTN_NUM, "op": BTN_OP, "fn": BTN_FN, "eq": BTN_EQ, "clr": BTN_CLR, "mem": BTN_MEM}

        for r, c, text, btype in buttons:
            btn = QPushButton(text)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            btn.setStyleSheet(style_map[btype])
            btn.clicked.connect(lambda checked, t=text, bt=btype: self._on_calc_btn(t, bt))
            grid.addWidget(btn, r, c)

        layout.addLayout(grid, 1)
        self.stack.addWidget(page)

    def _on_calc_btn(self, text, btype):
        inp = self.calc_input
        cur = inp.text()

        if text == "C":
            inp.clear()
            self.calc_result_label.setText("0")
            self.calc_expr_label.clear()
            return
        if text == "⌫":
            inp.setText(cur[:-1])
            return
        if text == "=":
            self._evaluate_calc()
            return
        if text == "MC":
            self.memory = 0.0
            self.statusBar().showMessage("Memory cleared", 2000)
            return
        if text == "MR":
            inp.setText(cur + str(self.memory))
            return
        if text == "M+":
            self._evaluate_calc()
            if self.last_result is not None:
                try: self.memory += float(self.last_result)
                except: pass
                self.statusBar().showMessage(f"Memory: {self.memory}", 2000)
            return
        if text == "M−":
            self._evaluate_calc()
            if self.last_result is not None:
                try: self.memory -= float(self.last_result)
                except: pass
                self.statusBar().showMessage(f"Memory: {self.memory}", 2000)
            return
        if text == "±":
            if cur.startswith("(-"):
                inp.setText(cur[2:].rstrip(")"))
            elif cur.startswith("-"):
                inp.setText(cur[1:])
            else:
                inp.setText("(-" + cur + ")")
            return

        # Map display symbols → internal syntax
        insert_map = {
            "÷": "/", "×": "*", "−": "-", "^": "**",
            "π": "pi", "√": "sqrt(", "n!": "factorial(",
            "sin": "sin(", "cos": "cos(", "tan": "tan(",
            "ln": "log(", "log₁₀": "log10(", "%": "/100",
        }
        to_insert = insert_map.get(text, text)
        inp.setText(cur + to_insert)

    def _update_calc_preview(self):
        expr = self.calc_input.text()
        if not expr:
            self.calc_result_label.setText("0")
            self.calc_expr_label.clear()
            return
        pretty = expr.replace("*", "×").replace("/", "÷").replace("pi", "π").replace("sqrt(", "√(").replace("**", "^")
        self.calc_expr_label.setText(pretty)
        try:
            result = sp.sympify(expr, locals=CALC_NS)
            if result.is_number:
                self.calc_result_label.setText(str(result.evalf(12)))
            else:
                self.calc_result_label.setText(str(result))
        except Exception:
            self.calc_result_label.setText("…")

    def _evaluate_calc(self):
        expr = self.calc_input.text().strip()
        if not expr:
            return
        try:
            result = sp.sympify(expr, locals=CALC_NS)
            if result.is_number:
                val = result.evalf(12)
                self.calc_result_label.setText(str(val))
                self.last_result = float(val) if val.is_Float else val
            else:
                self.calc_result_label.setText(str(result))
                self.last_result = result
            pretty = expr.replace("*", "×").replace("/", "÷").replace("pi", "π").replace("**", "^")
            self.calc_expr_label.setText(pretty + " =")
            self.update_history(f"{pretty} = {self.last_result}")
            self.calc_input.setText(str(self.last_result))
        except Exception as e:
            self.calc_result_label.setText("Error")
            self.calc_expr_label.setText(expr)
            self.statusBar().showMessage(f"Evaluation error: {e}", 4000)

    # Keyboard support for calculator
    def keyPressEvent(self, event):
        if self.stack.currentIndex() == 0:
            key = event.text()
            if key in '0123456789.+-*/()^%':
                self.calc_input.setText(self.calc_input.text() + key)
                return
            if event.key() in (Qt.Key_Return, Qt.Key_Enter):
                self._evaluate_calc()
                return
            if event.key() == Qt.Key_Backspace:
                self.calc_input.setText(self.calc_input.text()[:-1])
                return
            if event.key() == Qt.Key_Escape:
                self.calc_input.clear()
                self.calc_result_label.setText("0")
                self.calc_expr_label.clear()
                return
        super().keyPressEvent(event)

    # ═══════════════════════════════════════════════
    # 2. Exponents & Logs
    # ═══════════════════════════════════════════════
    def build_exp_log_page(self):
        page = QWidget(); layout = QVBoxLayout(page)
        layout.setSpacing(10); layout.setContentsMargins(20, 18, 20, 14)
        self._make_page_header(layout, "🔢  Exponents & Logarithms", "Compute powers, roots, and logarithmic values with full precision.")

        self.explog_op = QComboBox()
        self.explog_op.addItems(["Exponentiation", "Logarithm", "Square Root", "Nth Root"])
        self.explog_op.currentIndexChanged.connect(lambda i: self.explog_stack.setCurrentIndex(i))
        layout.addWidget(QLabel("Operation:"))
        layout.addWidget(self.explog_op)

        self.explog_stack = QStackedWidget()
        # Exp
        w1 = QWidget(); f1 = QFormLayout(w1)
        self.exp_base = QLineEdit("2"); self.exp_pow = QLineEdit("10")
        f1.addRow("Base:", self.exp_base); f1.addRow("Exponent:", self.exp_pow)
        self.explog_stack.addWidget(w1)
        # Log
        w2 = QWidget(); f2 = QFormLayout(w2)
        self.log_val = QLineEdit("100"); self.log_base = QLineEdit("10")
        f2.addRow("Value:", self.log_val); f2.addRow("Base (or 'e'):", self.log_base)
        self.explog_stack.addWidget(w2)
        # Sqrt
        w3 = QWidget(); f3 = QFormLayout(w3)
        self.sqrt_val = QLineEdit("144")
        f3.addRow("Value:", self.sqrt_val)
        self.explog_stack.addWidget(w3)
        # Nth Root
        w4 = QWidget(); f4 = QFormLayout(w4)
        self.nrt_val = QLineEdit("27"); self.nrt_n = QLineEdit("3")
        f4.addRow("Value:", self.nrt_val); f4.addRow("Root n:", self.nrt_n)
        self.explog_stack.addWidget(w4)

        layout.addWidget(self.explog_stack)
        btn = QPushButton("Calculate"); btn.setObjectName("primaryBtn")
        btn.clicked.connect(self.calc_explog); layout.addWidget(btn)
        self._add_result_area(layout, "explog_out")
        self.stack.addWidget(page)

    def calc_explog(self):
        op = self.explog_op.currentText()
        try:
            if op == "Exponentiation":
                b, e = safe_eval(self.exp_base.text()), safe_eval(self.exp_pow.text())
                if b is None or e is None: raise ValueError("Invalid input")
                res = b ** e
                self.explog_out.setText(f"{b} ^ {e} = {res}\n\nNumerical: {res.evalf(12) if hasattr(res, 'evalf') else res}")
                self.update_history(f"{b}^{e} = {res}")
            elif op == "Logarithm":
                v = float(sp.sympify(self.log_val.text()))
                bt = self.log_base.text().strip().lower()
                if v <= 0: raise ValueError("Value must be positive")
                if bt == 'e':
                    res = sp.log(v); label = "ln"
                else:
                    b = float(sp.sympify(bt))
                    if b <= 0 or b == 1: raise ValueError("Base must be > 0 and ≠ 1")
                    res = sp.log(v, b); label = f"log_{b}"
                self.explog_out.setText(f"{label}({v}) = {res.evalf(12)}")
                self.update_history(f"{label}({v}) = {res.evalf(12)}")
            elif op == "Square Root":
                v = float(sp.sympify(self.sqrt_val.text()))
                if v < 0: raise ValueError("Cannot take square root of negative number")
                exact = sp.sqrt(v); num = exact.evalf(12)
                self.explog_out.setText(f"√{v} = {exact}\n\nNumerical: {num}")
                self.update_history(f"√{v} = {num}")
            else:  # Nth Root
                v = float(sp.sympify(self.nrt_val.text()))
                n = float(sp.sympify(self.nrt_n.text()))
                res = sp.real_root(v, n) if v < 0 else v ** (1/n)
                self.explog_out.setText(f"{n}√{v} = {res}\n\nNumerical: {float(res):.12g}" if isinstance(res, (int, float)) else f"{n}√{v} = {res.evalf(12)}")
                self.update_history(f"{n}√{v} = {res}")
        except Exception as e:
            self.explog_out.setText(f"❌ Error: {e}")

    # ═══════════════════════════════════════════════
    # 3. Calculus
    # ═══════════════════════════════════════════════
    def build_calculus_page(self):
        page = QWidget(); layout = QVBoxLayout(page)
        layout.setSpacing(10); layout.setContentsMargins(20, 18, 20, 14)
        self._make_page_header(layout, "📐  Calculus", "Symbolic differentiation and integration. Use x as the variable.")

        self.calc_op = QComboBox()
        self.calc_op.addItems(["Derivative", "Nth Derivative", "Integral (Indefinite)", "Integral (Definite)"])
        self.calc_op.currentIndexChanged.connect(lambda i: self.calc_stack.setCurrentIndex(i))
        layout.addWidget(QLabel("Operation:"))
        layout.addWidget(self.calc_op)

        self.calc_stack = QStackedWidget()
        # Derivative
        w1 = QWidget(); f1 = QFormLayout(w1)
        self.calc_deriv_expr = QLineEdit("x**3 + 2*x")
        f1.addRow("f(x):", self.calc_deriv_expr)
        self.calc_stack.addWidget(w1)
        # Nth Derivative
        w2 = QWidget(); f2 = QFormLayout(w2)
        self.calc_nth_expr = QLineEdit("x**4 - 3*x**2")
        self.calc_nth_n = QSpinBox(); self.calc_nth_n.setRange(1, 20); self.calc_nth_n.setValue(2)
        f2.addRow("f(x):", self.calc_nth_expr); f2.addRow("n:", self.calc_nth_n)
        self.calc_stack.addWidget(w2)
        # Indefinite
        w3 = QWidget(); f3 = QFormLayout(w3)
        self.calc_indef_expr = QLineEdit("x**3 + 2*x")
        f3.addRow("f(x):", self.calc_indef_expr)
        self.calc_stack.addWidget(w3)
        # Definite
        w4 = QWidget(); f4 = QFormLayout(w4)
        self.calc_def_expr = QLineEdit("x**2")
        self.calc_def_a = QLineEdit("0"); self.calc_def_b = QLineEdit("1")
        f4.addRow("f(x):", self.calc_def_expr); f4.addRow("Lower limit a:", self.calc_def_a); f4.addRow("Upper limit b:", self.calc_def_b)
        self.calc_stack.addWidget(w4)

        layout.addWidget(self.calc_stack)
        btn = QPushButton("Calculate"); btn.setObjectName("primaryBtn")
        btn.clicked.connect(self.calc_calc); layout.addWidget(btn)
        self._add_result_area(layout, "calc_out")
        self.stack.addWidget(page)

    def calc_calc(self):
        op = self.calc_op.currentText(); x = sp.symbols('x')
        try:
            if op == "Derivative":
                f = safe_eval(self.calc_deriv_expr.text())
                if f is None: raise ValueError("Invalid expression")
                res = sp.diff(f, x)
                self.calc_out.setText(f"d/dx ({f}) = {res}")
                self.update_history(f"d/dx({f}) = {res}")
            elif op == "Nth Derivative":
                f = safe_eval(self.calc_nth_expr.text())
                if f is None: raise ValueError("Invalid expression")
                n = self.calc_nth_n.value()
                res = sp.diff(f, x, n)
                self.calc_out.setText(f"d{n}/dx{n} ({f}) = {res}")
                self.update_history(f"d{n}/dx{n}({f}) = {res}")
            elif op == "Integral (Indefinite)":
                f = safe_eval(self.calc_indef_expr.text())
                if f is None: raise ValueError("Invalid expression")
                res = sp.integrate(f, x)
                self.calc_out.setText(f"∫ {f} dx = {res} + C")
                self.update_history(f"∫ {f} dx = {res} + C")
            else:
                f = safe_eval(self.calc_def_expr.text())
                if f is None: raise ValueError("Invalid expression")
                a = float(sp.sympify(self.calc_def_a.text()))
                b = float(sp.sympify(self.calc_def_b.text()))
                res = sp.integrate(f, (x, a, b))
                self.calc_out.setText(f"∫[{a}, {b}] {f} dx = {res}\n\nNumerical: {res.evalf(12)}")
                self.update_history(f"∫[{a}..{b}] {f} dx = {res.evalf(12)}")
        except Exception as e:
            self.calc_out.setText(f"❌ Error: {e}")

    # ═══════════════════════════════════════════════
    # 4. Factorization
    # ═══════════════════════════════════════════════
    def build_factorization_page(self):
        page = QWidget(); layout = QVBoxLayout(page)
        layout.setSpacing(10); layout.setContentsMargins(20, 18, 20, 14)
        self._make_page_header(layout, "✂️  Factorization", "Factor polynomial expressions symbolically.")
        form = QFormLayout()
        self.factor_expr = QLineEdit("x**2 - 4")
        form.addRow("Expression:", self.factor_expr)
        layout.addLayout(form)
        btn = QPushButton("Factorize"); btn.setObjectName("primaryBtn")
        btn.clicked.connect(self.calc_factor); layout.addWidget(btn)
        self._add_result_area(layout, "factor_out")
        self.stack.addWidget(page)

    def calc_factor(self):
        try:
            f = safe_eval(self.factor_expr.text())
            if f is None: raise ValueError("Invalid expression")
            res = sp.factor(f)
            expanded = sp.expand(f)
            self.factor_out.setText(f"Original:  {expanded}\nFactored:  {res}")
            self.update_history(f"factor({f}) = {res}")
        except Exception as e:
            self.factor_out.setText(f"❌ Error: {e}")

    # ═══════════════════════════════════════════════
    # 5. Equation Solver
    # ═══════════════════════════════════════════════
    def build_solve_eq_page(self):
        page = QWidget(); layout = QVBoxLayout(page)
        layout.setSpacing(10); layout.setContentsMargins(20, 18, 20, 14)
        self._make_page_header(layout, "🔍  Equation Solver", "Solve f(x) = 0 for x. Enter the expression equal to zero.")
        form = QFormLayout()
        self.solve_expr = QLineEdit("x**2 - 4")
        form.addRow("f(x) = 0 :", self.solve_expr)
        layout.addLayout(form)
        btn = QPushButton("Solve"); btn.setObjectName("primaryBtn")
        btn.clicked.connect(self.calc_solve); layout.addWidget(btn)
        self._add_result_area(layout, "solve_out")
        self.stack.addWidget(page)

    def calc_solve(self):
        try:
            x = sp.symbols('x')
            f = safe_eval(self.solve_expr.text())
            if f is None: raise ValueError("Invalid expression")
            res = sp.solve(f, x)
            lines = [f"Solving:  {f} = 0", ""]
            for i, sol in enumerate(res):
                lines.append(f"  x{i+1} = {sol}  (≈ {sol.evalf(10)})" if hasattr(sol, 'evalf') else f"  x{i+1} = {sol}")
            if not res:
                lines.append("No solutions found.")
            self.solve_out.setText("\n".join(lines))
            self.update_history(f"Solve {f}=0 → {res}")
        except Exception as e:
            self.solve_out.setText(f"❌ Error: {e}")

    # ═══════════════════════════════════════════════
    # 6. Statistics
    # ═══════════════════════════════════════════════
    def build_statistics_page(self):
        page = QWidget(); layout = QVBoxLayout(page)
        layout.setSpacing(10); layout.setContentsMargins(20, 18, 20, 14)
        self._make_page_header(layout, "📊  Statistics", "Compute descriptive statistics for a dataset.")
        form = QFormLayout()
        self.stats_data = QTextEdit("12, 15, 18, 22, 25, 18, 30")
        self.stats_data.setMaximumHeight(70)
        form.addRow("Numbers (comma-separated):", self.stats_data)
        layout.addLayout(form)
        btn = QPushButton("Calculate"); btn.setObjectName("primaryBtn")
        btn.clicked.connect(self.calc_stats); layout.addWidget(btn)
        self._add_result_area(layout, "stats_out")
        self.stack.addWidget(page)

    def calc_stats(self):
        try:
            data = [float(n.strip()) for n in self.stats_data.toPlainText().split(",") if n.strip()]
            if not data: raise ValueError("Empty dataset")
            arr = np.array(data)
            mean = np.mean(arr); median = np.median(arr)
            var = np.var(arr, ddof=1) if len(arr) > 1 else 0
            std = np.std(arr, ddof=1) if len(arr) > 1 else 0
            rng = np.ptp(arr)
            counts = {v: data.count(v) for v in set(data)}
            mode_val = max(counts, key=counts.get)
            q1, q3 = np.percentile(arr, [25, 75])
            iqr = q3 - q1

            result = (
                f"Count:       {len(data)}\n"
                f"Sum:         {np.sum(arr):.4f}\n"
                f"Mean:        {mean:.4f}\n"
                f"Median:      {median:.4f}\n"
                f"Mode:        {mode_val}\n"
                f"Variance:    {var:.4f}\n"
                f"Std Dev:     {std:.4f}\n"
                f"Min:         {np.min(arr):.4f}\n"
                f"Max:         {np.max(arr):.4f}\n"
                f"Range:       {rng:.4f}\n"
                f"Q1 (25%):    {q1:.4f}\n"
                f"Q3 (75%):    {q3:.4f}\n"
                f"IQR:         {iqr:.4f}"
            )
            self.stats_out.setText(result)
            self.update_history(f"Stats n={len(data)} → mean={mean:.4f}")
        except Exception as e:
            self.stats_out.setText(f"❌ Error: {e}")

    # ═══════════════════════════════════════════════
    # 7. Matrix Operations
    # ═══════════════════════════════════════════════
    def build_matrix_page(self):
        page = QWidget(); layout = QVBoxLayout(page)
        layout.setSpacing(10); layout.setContentsMargins(20, 18, 20, 14)
        self._make_page_header(layout, "🔲  Matrix Operations", "Operate on matrices. Enter rows on new lines, values separated by spaces.")

        form = QFormLayout()
        self.mat1 = QTextEdit("1 2\n3 4"); self.mat1.setMaximumHeight(60)
        self.mat2 = QTextEdit("5 6\n7 8"); self.mat2.setMaximumHeight(60)
        self.mat_op = QComboBox()
        self.mat_op.addItems(["Add", "Subtract", "Multiply", "Transpose (M1)", "Determinant (M1)", "Inverse (M1)", "Eigenvalues (M1)"])
        form.addRow("Matrix 1:", self.mat1); form.addRow("Matrix 2:", self.mat2)
        form.addRow("Operation:", self.mat_op)
        layout.addLayout(form)
        btn = QPushButton("Calculate"); btn.setObjectName("primaryBtn")
        btn.clicked.connect(self.calc_matrix); layout.addWidget(btn)
        self._add_result_area(layout, "mat_out")
        self.stack.addWidget(page)

    def calc_matrix(self):
        try:
            m1 = parse_matrix(self.mat1.toPlainText())
            m2_text = self.mat2.toPlainText().strip()
            m2 = parse_matrix(m2_text) if m2_text else None
            op = self.mat_op.currentText()
            res = None
            if op == "Add":
                if m2 is None: raise ValueError("Matrix 2 required")
                res = m1 + m2
            elif op == "Subtract":
                if m2 is None: raise ValueError("Matrix 2 required")
                res = m1 - m2
            elif op == "Multiply":
                if m2 is None: raise ValueError("Matrix 2 required")
                res = np.dot(m1, m2)
            elif op == "Transpose (M1)":
                res = m1.T
            elif op == "Determinant (M1)":
                res = np.linalg.det(m1)
                self.mat_out.setText(f"Determinant of M1:\n{res:.6f}")
                self.update_history(f"Mat Det = {res:.6f}")
                return
            elif op == "Inverse (M1)":
                det = np.linalg.det(m1)
                if abs(det) < 1e-12: raise ValueError("Singular matrix — no inverse exists")
                res = np.linalg.inv(m1)
            elif op == "Eigenvalues (M1)":
                eig = np.linalg.eigvals(m1)
                lines = "Eigenvalues of M1:\n"
                for i, v in enumerate(eig):
                    lines += f"  λ{i+1} = {v}\n"
                self.mat_out.setText(lines)
                self.update_history(f"Mat Eigenvalues = {eig}")
                return
            self.mat_out.setText(f"Result ({res.shape}):\n{res}")
            self.update_history(f"Mat {op} calculated")
        except Exception as e:
            self.mat_out.setText(f"❌ Error: {e}")

    # ═══════════════════════════════════════════════
    # 8. Complex Numbers
    # ═══════════════════════════════════════════════
    def build_complex_page(self):
        page = QWidget(); layout = QVBoxLayout(page)
        layout.setSpacing(10); layout.setContentsMargins(20, 18, 20, 14)
        self._make_page_header(layout, "🌀  Complex Number Arithmetic", "Arithmetic on complex numbers. Use Python syntax: 1+2j")
        form = QFormLayout()
        self.comp_e1 = QLineEdit("3+4j"); self.comp_e2 = QLineEdit("1-2j")
        self.comp_op = QComboBox()
        self.comp_op.addItems(["Add", "Subtract", "Multiply", "Divide", "Exponentiate", "Conjugate (z1)", "Magnitude (z1)"])
        form.addRow("z₁:", self.comp_e1); form.addRow("z₂:", self.comp_e2)
        form.addRow("Operation:", self.comp_op)
        layout.addLayout(form)
        btn = QPushButton("Calculate"); btn.setObjectName("primaryBtn")
        btn.clicked.connect(self.calc_complex); layout.addWidget(btn)
        self._add_result_area(layout, "comp_out")
        self.stack.addWidget(page)

    def calc_complex(self):
        try:
            c1 = complex(self.comp_e1.text())
            c2_text = self.comp_e2.text().strip()
            c2 = complex(c2_text) if c2_text else None
            op = self.comp_op.currentText()
            if op == "Add": res = c1 + c2
            elif op == "Subtract": res = c1 - c2
            elif op == "Multiply": res = c1 * c2
            elif op == "Divide":
                if c2 == 0: raise ValueError("Division by zero")
                res = c1 / c2
            elif op == "Exponentiate": res = c1 ** c2
            elif op == "Conjugate (z1)": res = c1.conjugate()
            elif op == "Magnitude (z1)":
                res = abs(c1)
                self.comp_out.setText(f"|z₁| = |{c1}| = {res:.6f}")
                self.update_history(f"|{c1}| = {res:.6f}")
                return
            self.comp_out.setText(
                f"z₁ = {c1}\nz₂ = {c2}\n\nResult: {res}\n\n"
                f"Real part:      {res.real:.6f}\nImaginary part: {res.imag:.6f}\nMagnitude:      {abs(res):.6f}\nPhase (rad):    {np.angle(res):.6f}"
            )
            self.update_history(f"{c1} {op} {c2} = {res}")
        except Exception as e:
            self.comp_out.setText(f"❌ Error: {e}")

    # ═══════════════════════════════════════════════
    # 9. Plot Function
    # ═══════════════════════════════════════════════
    def build_plot_page(self):
        page = QWidget(); layout = QVBoxLayout(page)
        layout.setSpacing(10); layout.setContentsMargins(20, 18, 20, 14)
        self._make_page_header(layout, "📈  Function Plotter", "Visualize any function f(x). Use x as the variable.")

        form = QFormLayout()
        self.plot_expr = QLineEdit("sin(x) * exp(-x/5)")
        self.plot_xmin = QDoubleSpinBox(); self.plot_xmin.setRange(-10000, 10000); self.plot_xmin.setValue(-10)
        self.plot_xmax = QDoubleSpinBox(); self.plot_xmax.setRange(-10000, 10000); self.plot_xmax.setValue(10)
        self.plot_pts = QSlider(Qt.Horizontal); self.plot_pts.setRange(100, 2000); self.plot_pts.setValue(500)
        self.plot_pts_label = QLabel("500")
        self.plot_pts.valueChanged.connect(lambda v: self.plot_pts_label.setText(str(v)))
        form.addRow("f(x):", self.plot_expr)
        h = QHBoxLayout(); h.addWidget(QLabel("x min:")); h.addWidget(self.plot_xmin)
        h.addWidget(QLabel("x max:")); h.addWidget(self.plot_xmax); layout.addLayout(h)
        ph = QHBoxLayout(); ph.addWidget(QLabel("Points:")); ph.addWidget(self.plot_pts); ph.addWidget(self.plot_pts_label)
        layout.addLayout(ph)

        btn = QPushButton("📈  Plot"); btn.setObjectName("primaryBtn")
        btn.clicked.connect(self.calc_plot); layout.addWidget(btn)

        self.fig, self.ax = plt.subplots()
        self.fig.patch.set_facecolor('#0f1021')
        self.ax.set_facecolor('#0f1021')
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setMinimumHeight(300)
        layout.addWidget(self.canvas, 1)
        self.stack.addWidget(page)

    def calc_plot(self):
        try:
            x = sp.symbols('x')
            f = sp.sympify(self.plot_expr.text(), locals=CALC_NS)
            f_np = sp.lambdify(x, f, modules=["numpy"])
            x_vals = np.linspace(self.plot_xmin.value(), self.plot_xmax.value(), self.plot_pts.value())
            y_vals = f_np(x_vals)

            self.ax.clear()
            self.ax.plot(x_vals, y_vals, linewidth=2.2, color="#6090ff", zorder=3)
            self.ax.set_title(f"y = {self.plot_expr.text()}", fontsize=14, color="#a0b0ff", pad=10)
            self.ax.grid(True, linestyle="--", alpha=0.2, color="#4060a0")
            self.ax.axhline(y=0, color="#304060", linewidth=0.8)
            self.ax.axvline(x=0, color="#304060", linewidth=0.8)
            self.ax.tick_params(colors='#6080a0')
            for spine in self.ax.spines.values():
                spine.set_color('#252860')
            self.fig.tight_layout()
            self.canvas.draw()
            self.update_history(f"Plotted: {self.plot_expr.text()}")
        except Exception as e:
            QMessageBox.warning(self, "Plot Error", str(e))

    # ═══════════════════════════════════════════════
    # 10. Prime Tools
    # ═══════════════════════════════════════════════
    def build_prime_page(self):
        page = QWidget(); layout = QVBoxLayout(page)
        layout.setSpacing(10); layout.setContentsMargins(20, 18, 20, 14)
        self._make_page_header(layout, "🔑  Prime Checker & Generator", "Test primality or generate prime numbers.")

        self.prime_op = QComboBox()
        self.prime_op.addItems(["Check Prime", "Generate Primes up to N", "Prime Factorization"])
        self.prime_op.currentIndexChanged.connect(lambda i: self.prime_stack.setCurrentIndex(i))
        layout.addWidget(QLabel("Operation:"))
        layout.addWidget(self.prime_op)

        self.prime_stack = QStackedWidget()
        w1 = QWidget(); f1 = QFormLayout(w1)
        self.prime_check_n = QSpinBox(); self.prime_check_n.setRange(1, 999999999); self.prime_check_n.setValue(97)
        f1.addRow("Integer:", self.prime_check_n)
        self.prime_stack.addWidget(w1)
        w2 = QWidget(); f2 = QFormLayout(w2)
        self.prime_gen_n = QSpinBox(); self.prime_gen_n.setRange(2, 9999999); self.prime_gen_n.setValue(100)
        f2.addRow("Limit:", self.prime_gen_n)
        self.prime_stack.addWidget(w2)
        w3 = QWidget(); f3 = QFormLayout(w3)
        self.prime_factor_n = QSpinBox(); self.prime_factor_n.setRange(2, 999999999); self.prime_factor_n.setValue(360)
        f3.addRow("Integer:", self.prime_factor_n)
        self.prime_stack.addWidget(w3)

        layout.addWidget(self.prime_stack)
        btn = QPushButton("Run"); btn.setObjectName("primaryBtn")
        btn.clicked.connect(self.calc_prime); layout.addWidget(btn)
        self._add_result_area(layout, "prime_out")
        self.stack.addWidget(page)

    def calc_prime(self):
        op = self.prime_op.currentText()
        try:
            if op == "Check Prime":
                n = self.prime_check_n.value()
                if is_prime(n):
                    self.prime_out.setText(f"✅  {n} is a prime number!")
                else:
                    # Find smallest factor
                    for d in range(2, int(n**0.5)+1):
                        if n % d == 0:
                            self.prime_out.setText(f"❌  {n} is NOT prime.\n\nSmallest factor: {d}\n{d} × {n//d} = {n}")
                            break
                self.update_history(f"Checked: {n} — {'prime' if is_prime(n) else 'not prime'}")
            elif op == "Generate Primes up to N":
                limit = self.prime_gen_n.value()
                primes = [i for i in range(2, limit + 1) if is_prime(i)]
                self.prime_out.setText(f"Primes up to {limit} ({len(primes)} found):\n\n{primes}")
                self.update_history(f"Generated {len(primes)} primes up to {limit}")
            else:  # Prime Factorization
                n = self.prime_factor_n.value()
                original = n
                factors = []
                d = 2
                while d * d <= n:
                    while n % d == 0:
                        factors.append(d)
                        n //= d
                    d += 1
                if n > 1:
                    factors.append(n)
                from collections import Counter
                counts = Counter(factors)
                factor_str = " × ".join(f"{p}^{c}" if c > 1 else str(p) for p, c in sorted(counts.items()))
                self.prime_out.setText(f"Prime factorization of {original}:\n\n{original} = {factor_str}")
                self.update_history(f"Factorized {original} = {factor_str}")
        except Exception as e:
            self.prime_out.setText(f"❌ Error: {e}")

    # ═══════════════════════════════════════════════
    # 11. System of Equations
    # ═══════════════════════════════════════════════
    def build_system_eq_page(self):
        page = QWidget(); layout = QVBoxLayout(page)
        layout.setSpacing(10); layout.setContentsMargins(20, 18, 20, 14)
        self._make_page_header(layout, "📝  System of Linear Equations", "Solve multiple equations simultaneously. One equation per line.")
        form = QFormLayout()
        self.sys_eqs = QTextEdit("x + y = 5\n2*x - y = 1")
        self.sys_eqs.setMaximumHeight(70)
        self.sys_vars = QLineEdit("x, y")
        form.addRow("Equations:", self.sys_eqs); form.addRow("Variables:", self.sys_vars)
        layout.addLayout(form)
        btn = QPushButton("Solve"); btn.setObjectName("primaryBtn")
        btn.clicked.connect(self.calc_system); layout.addWidget(btn)
        self._add_result_area(layout, "sys_out")
        self.stack.addWidget(page)

    def calc_system(self):
        try:
            eqns = []
            for line in self.sys_eqs.toPlainText().strip().split("\n"):
                if "=" not in line: raise ValueError(f"Missing '=' in: {line}")
                left, right = line.split("=", 1)
                eqns.append(sp.Eq(sp.sympify(left), sp.sympify(right)))
            variables = sp.symbols(self.sys_vars.text())
            sol = sp.solve(eqns, variables)
            if not sol:
                self.sys_out.setText("No solution found.")
            else:
                lines = ["Solution:\n"]
                if isinstance(sol, dict):
                    for var, val in sol.items():
                        lines.append(f"  {var} = {val}  (≈ {val.evalf(10)})" if hasattr(val, 'evalf') else f"  {var} = {val}")
                elif isinstance(sol, list):
                    for s in sol:
                        if isinstance(s, dict):
                            for var, val in s.items():
                                lines.append(f"  {var} = {val}")
                        else:
                            lines.append(f"  {s}")
                else:
                    lines.append(f"  {sol}")
                self.sys_out.setText("\n".join(lines))
            self.update_history(f"Solved system → {sol}")
        except Exception as e:
            self.sys_out.setText(f"❌ Error: {e}")

    # ═══════════════════════════════════════════════
    # 12. Base Converter  (NEW)
    # ═══════════════════════════════════════════════
    def build_base_converter_page(self):
        page = QWidget(); layout = QVBoxLayout(page)
        layout.setSpacing(10); layout.setContentsMargins(20, 18, 20, 14)
        self._make_page_header(layout, "🔄  Number Base Converter", "Convert numbers between decimal, hexadecimal, octal, and binary.")

        form = QFormLayout()
        self.base_input = QLineEdit("255")
        self.base_from = QComboBox()
        self.base_from.addItems(["Decimal (10)", "Hexadecimal (16)", "Octal (8)", "Binary (2)"])
        form.addRow("Value:", self.base_input); form.addRow("From Base:", self.base_from)
        layout.addLayout(form)

        btn = QPushButton("Convert"); btn.setObjectName("primaryBtn")
        btn.clicked.connect(self.calc_base_convert); layout.addWidget(btn)
        self._add_result_area(layout, "base_out")
        self.stack.addWidget(page)

    def calc_base_convert(self):
        try:
            val = self.base_input.text().strip()
            from_idx = self.base_from.currentIndex()
            bases = [10, 16, 8, 2]
            base_names = ["Decimal", "Hexadecimal", "Octal", "Binary"]
            prefixes = ["", "0x", "0o", "0b"]
            base = bases[from_idx]

            # Parse input
            n = int(val, base)

            lines = [f"Input:  {val}  (base {base})\n"]
            for i, (b, name, prefix) in enumerate(zip(bases, base_names, prefixes)):
                if i == from_idx:
                    continue
                if b == 10:
                    converted = str(n)
                elif b == 16:
                    converted = hex(n)
                elif b == 8:
                    converted = oct(n)
                else:
                    converted = bin(n)
                lines.append(f"{name:14s} (base {b:2d}):  {converted}")

            # Also show ASCII character if in range
            if 32 <= n <= 126:
                lines.append(f"\nASCII character:  '{chr(n)}'")

            self.base_out.setText("\n".join(lines))
            self.update_history(f"Base convert: {val} (base {base}) → decimal {n}")
        except Exception as e:
            self.base_out.setText(f"❌ Error: {e}\n\nMake sure the input is valid for the selected base.")

    # ═══════════════════════════════════════════════
    # 13. Combinatorics  (NEW)
    # ═══════════════════════════════════════════════
    def build_combinatorics_page(self):
        page = QWidget(); layout = QVBoxLayout(page)
        layout.setSpacing(10); layout.setContentsMargins(20, 18, 20, 14)
        self._make_page_header(layout, "🎲  Combinatorics & Number Theory", "Permutations, combinations, factorials, GCD, and LCM.")

        self.comb_op = QComboBox()
        self.comb_op.addItems(["Factorial (n!)", "Permutation (nPr)", "Combination (nCr)", "GCD", "LCM"])
        self.comb_op.currentIndexChanged.connect(lambda i: self.comb_stack.setCurrentIndex(i))
        layout.addWidget(QLabel("Operation:"))
        layout.addWidget(self.comb_op)

        self.comb_stack = QStackedWidget()
        # Factorial
        w1 = QWidget(); f1 = QFormLayout(w1)
        self.fact_n = QSpinBox(); self.fact_n.setRange(0, 1000); self.fact_n.setValue(10)
        f1.addRow("n:", self.fact_n)
        self.comb_stack.addWidget(w1)
        # nPr
        w2 = QWidget(); f2 = QFormLayout(w2)
        self.npr_n = QSpinBox(); self.npr_n.setRange(0, 500); self.npr_n.setValue(10)
        self.npr_r = QSpinBox(); self.npr_r.setRange(0, 500); self.npr_r.setValue(3)
        f2.addRow("n:", self.npr_n); f2.addRow("r:", self.npr_r)
        self.comb_stack.addWidget(w2)
        # nCr
        w3 = QWidget(); f3 = QFormLayout(w3)
        self.ncr_n = QSpinBox(); self.ncr_n.setRange(0, 1000); self.ncr_n.setValue(10)
        self.ncr_r = QSpinBox(); self.ncr_r.setRange(0, 1000); self.ncr_r.setValue(3)
        f3.addRow("n:", self.ncr_n); f3.addRow("r:", self.ncr_r)
        self.comb_stack.addWidget(w3)
        # GCD
        w4 = QWidget(); f4 = QFormLayout(w4)
        self.gcd_a = QSpinBox(); self.gcd_a.setRange(1, 999999999); self.gcd_a.setValue(48)
        self.gcd_b = QSpinBox(); self.gcd_b.setRange(1, 999999999); self.gcd_b.setValue(36)
        f4.addRow("a:", self.gcd_a); f4.addRow("b:", self.gcd_b)
        self.comb_stack.addWidget(w4)
        # LCM
        w5 = QWidget(); f5 = QFormLayout(w5)
        self.lcm_a = QSpinBox(); self.lcm_a.setRange(1, 999999999); self.lcm_a.setValue(12)
        self.lcm_b = QSpinBox(); self.lcm_b.setRange(1, 999999999); self.lcm_b.setValue(18)
        f5.addRow("a:", self.lcm_a); f5.addRow("b:", self.lcm_b)
        self.comb_stack.addWidget(w5)

        layout.addWidget(self.comb_stack)
        btn = QPushButton("Calculate"); btn.setObjectName("primaryBtn")
        btn.clicked.connect(self.calc_combinatorics); layout.addWidget(btn)
        self._add_result_area(layout, "comb_out")
        self.stack.addWidget(page)

    def calc_combinatorics(self):
        op = self.comb_op.currentText()
        try:
            if op == "Factorial (n!)":
                n = self.fact_n.value()
                res = math.factorial(n)
                self.comb_out.setText(f"{n}! = {res}")
                self.update_history(f"{n}! = {res}")
            elif op == "Permutation (nPr)":
                n, r = self.npr_n.value(), self.npr_r.value()
                if r > n: raise ValueError("r cannot be greater than n")
                res = math.perm(n, r)
                self.comb_out.setText(f"P({n}, {r}) = {n}! / ({n}-{r})! = {res}")
                self.update_history(f"P({n},{r}) = {res}")
            elif op == "Combination (nCr)":
                n, r = self.ncr_n.value(), self.ncr_r.value()
                if r > n: raise ValueError("r cannot be greater than n")
                res = math.comb(n, r)
                self.comb_out.setText(f"C({n}, {r}) = {n}! / ({r}! × ({n}-{r})!) = {res}")
                self.update_history(f"C({n},{r}) = {res}")
            elif op == "GCD":
                a, b = self.gcd_a.value(), self.gcd_b.value()
                res = math.gcd(a, b)
                self.comb_out.setText(f"GCD({a}, {b}) = {res}")
                self.update_history(f"GCD({a},{b}) = {res}")
            else:  # LCM
                a, b = self.lcm_a.value(), self.lcm
                res = math.lcm(a, b)
                self.comb_out.setText(f"LCM({a}, {b}) = {res}")
                self.update_history(f"LCM({a},{b}) = {res}")
        except Exception as e:
            self.comb_out.setText(f"❌ Error: {e}")


# ═══════════════════════════════════════════════════════════════
# ENTRY POINT
# ═══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet(STYLESHEET)
    
    # Set application-wide font
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    
    window = CalculatorApp()
    window.show()
    sys.exit(app.exec())