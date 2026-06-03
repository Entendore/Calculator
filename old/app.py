# calculator_all_in_one.py
import streamlit as st
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

# ──────────────────────────────────────────────
# Page Configuration
# ──────────────────────────────────────────────
st.set_page_config(page_title="Multi-Function Calculator", layout="wide")
st.title("🧮 Multi-Function Calculator")

# ──────────────────────────────────────────────
# Session State: Calculation History
# ──────────────────────────────────────────────
if "history" not in st.session_state:
    st.session_state.history = []

# ──────────────────────────────────────────────
# Helper Functions
# ──────────────────────────────────────────────
def safe_eval(expr):
    """Safely evaluate a symbolic expression."""
    try:
        return sp.sympify(expr)
    except Exception:
        st.error(f"Invalid expression: {expr}")
        return None

def is_prime(n):
    """Check if n is a prime number."""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def parse_matrix(text):
    """Parse a text block into a numpy matrix."""
    return np.array([[float(x) for x in row.split()] for row in text.strip().split("\n")])

# ──────────────────────────────────────────────
# Sidebar: Operation Selector & Instructions
# ──────────────────────────────────────────────
operation = st.sidebar.selectbox("Choose Operation", [
    "Basic Arithmetic",
    "Exponentiation & Logs",
    "Calculus",
    "Factorization",
    "Solve Equation",
    "Statistics",
    "Matrix Operations",
    "Complex Arithmetic",
    "Plot Function",
    "Prime Checker/Generator",
    "Solve System of Equations",
])

with st.sidebar.expander("📖 Instructions"):
    st.markdown("""
    - Select an operation from the dropdown above.
    - Enter your inputs in the main panel.
    - Press the submit button to calculate.
    - Results and error messages appear below inputs.
    - Calculation history is tracked at the bottom.
    - Use `x` as the variable for calculus / plotting.
    - Complex numbers use Python syntax: `1+2j`
    - Matrices: rows on new lines, values separated by spaces.
    """)

# ──────────────────────────────────────────────
# 1. Basic Arithmetic
# ──────────────────────────────────────────────
if operation == "Basic Arithmetic":
    st.header("➕ Basic Arithmetic")

    with st.form("basic_arith_form"):
        col1, col2 = st.columns(2)
        with col1:
            expr1 = st.text_input("Expression 1", value="10",
                                  help="Enter a number or expression, e.g. 2*x + 3")
        with col2:
            expr2 = st.text_input("Expression 2", value="5",
                                  help="Enter a number or expression")

        op = st.radio("Operation", ["Add", "Subtract", "Multiply", "Divide"])
        submitted = st.form_submit_button("Calculate")

    if submitted:
        val1 = safe_eval(expr1)
        val2 = safe_eval(expr2)
        if val1 is not None and val2 is not None:
            result = None
            if op == "Add":
                result = val1 + val2
            elif op == "Subtract":
                result = val1 - val2
            elif op == "Multiply":
                result = val1 * val2
            elif op == "Divide":
                if val2 == 0:
                    st.error("Cannot divide by zero!")
                else:
                    result = val1 / val2
            if result is not None:
                st.success(f"Result: {result}")
                st.session_state.history.append(f"{expr1} {op} {expr2} = {result}")

# ──────────────────────────────────────────────
# 2. Exponentiation & Logs
# ──────────────────────────────────────────────
elif operation == "Exponentiation & Logs":
    st.header("🔢 Exponentiation & Logarithms")

    with st.form("exp_log_form"):
        sub_op = st.radio("Select Operation", ["Exponentiation", "Logarithm", "Square Root"])
        if sub_op == "Exponentiation":
            base = st.text_input("Base", value="2")
            exponent = st.text_input("Exponent", value="3")
        elif sub_op == "Logarithm":
            val = st.text_input("Value", value="10")
            base = st.text_input("Base (default e)", value="e")
        else:
            val = st.text_input("Value", value="9")
        submitted = st.form_submit_button("Calculate")

    if submitted:
        try:
            if sub_op == "Exponentiation":
                b = safe_eval(base)
                e = safe_eval(exponent)
                if b is not None and e is not None:
                    result = b ** e
                    st.success(f"Result: {result}")
                    st.session_state.history.append(f"{b} ** {e} = {result}")

            elif sub_op == "Logarithm":
                v = float(val)
                if v <= 0:
                    st.error("Value must be positive")
                else:
                    if base.lower() == "e":
                        res = sp.log(v)
                    else:
                        b = float(base)
                        if b <= 0 or b == 1:
                            st.error("Base must be positive and not 1")
                            res = None
                        else:
                            res = sp.log(v, b)
                    if res is not None:
                        res_eval = res.evalf()
                        st.success(f"Result: {res_eval}")
                        st.session_state.history.append(f"log base {base} of {v} = {res_eval}")

            else:  # Square Root
                v = float(val)
                if v < 0:
                    st.error("Value cannot be negative")
                else:
                    result = sp.sqrt(v)
                    st.success(f"Result: {result.evalf()}")
                    st.session_state.history.append(f"sqrt({v}) = {result.evalf()}")
        except Exception as exc:
            st.error(f"Error: {exc}")

# ──────────────────────────────────────────────
# 3. Calculus
# ──────────────────────────────────────────────
elif operation == "Calculus":
    st.header("📐 Calculus Operations")

    with st.form("calculus_form"):
        calc_op = st.radio(
            "Operation",
            ["Derivative", "Nth Derivative", "Integral (Indefinite)", "Integral (Definite)"],
        )
        expr = st.text_input("Function in x", value="x**3 + 2*x")
        submitted = st.form_submit_button("Calculate")

    if submitted:
        x = sp.symbols("x")
        f = safe_eval(expr)
        if f is not None:
            try:
                if calc_op == "Derivative":
                    d = sp.diff(f, x)
                    st.success(f"Derivative: {d}")
                    st.session_state.history.append(f"d/dx({expr}) = {d}")

                elif calc_op == "Nth Derivative":
                    n = st.number_input("Derivative order (n)", min_value=1, value=1,
                                        key="nth_deriv_n")
                    d = sp.diff(f, x, int(n))
                    st.success(f"{n}th Derivative: {d}")
                    st.session_state.history.append(f"d^{n}/dx^{n}({expr}) = {d}")

                elif calc_op == "Integral (Indefinite)":
                    integ = sp.integrate(f, x)
                    st.success(f"Indefinite Integral: {integ} + C")
                    st.session_state.history.append(f"∫ {expr} dx = {integ} + C")

                else:  # Definite Integral
                    a = st.text_input("Lower limit (a)", value="0", key="def_a")
                    b = st.text_input("Upper limit (b)", value="1", key="def_b")
                    try:
                        a_val = float(sp.sympify(a))
                        b_val = float(sp.sympify(b))
                        integ = sp.integrate(f, (x, a_val, b_val))
                        st.success(f"Definite Integral from {a_val} to {b_val}: {integ.evalf()}")
                        st.session_state.history.append(
                            f"∫_{a_val}^{b_val} {expr} dx = {integ.evalf()}"
                        )
                    except Exception as exc:
                        st.error(f"Invalid limits: {exc}")
            except Exception as exc:
                st.error(f"Error: {exc}")

# ──────────────────────────────────────────────
# 4. Factorization  (from calculator_app.py)
# ──────────────────────────────────────────────
elif operation == "Factorization":
    st.header("✂️ Factorization")

    with st.form("factor_form"):
        expr = st.text_input("Enter expression in x", value="x**2 - 4")
        submitted = st.form_submit_button("Factorize")

    if submitted:
        x = sp.symbols("x")
        f = safe_eval(expr)
        if f is not None:
            try:
                factored = sp.factor(f)
                st.success(f"Factored form: {factored}")
                st.session_state.history.append(f"factor({expr}) = {factored}")
            except Exception as exc:
                st.error(f"Error: {exc}")

# ──────────────────────────────────────────────
# 5. Solve Equation  (from calculator_app.py)
# ──────────────────────────────────────────────
elif operation == "Solve Equation":
    st.header("🔍 Solve Equation  f(x) = 0")

    with st.form("solve_eq_form"):
        expr = st.text_input("Enter expression in x", value="x**2 - 4")
        submitted = st.form_submit_button("Solve")

    if submitted:
        x = sp.symbols("x")
        f = safe_eval(expr)
        if f is not None:
            try:
                solutions = sp.solve(f, x)
                st.success(f"Solutions: {solutions}")
                st.session_state.history.append(f"Solve {expr} = 0 → {solutions}")
            except Exception as exc:
                st.error(f"Error: {exc}")

# ──────────────────────────────────────────────
# 6. Statistics
# ──────────────────────────────────────────────
elif operation == "Statistics":
    st.header("📊 Statistics")

    with st.form("stats_form"):
        data_str = st.text_area("Enter numbers separated by commas", value="1, 2, 3, 4, 5")
        submitted = st.form_submit_button("Calculate")

    if submitted:
        try:
            data = [float(n.strip()) for n in data_str.split(",") if n.strip()]
            if len(data) == 0:
                st.warning("Please enter at least one number")
            else:
                arr = np.array(data)
                mean = np.mean(arr)
                median = np.median(arr)
                variance = np.var(arr, ddof=1) if len(arr) > 1 else 0
                std_dev = np.std(arr, ddof=1) if len(arr) > 1 else 0
                data_range = np.ptp(arr)

                counts = {v: data.count(v) for v in set(data)}
                mode = max(counts, key=counts.get) if counts else None

                # Display results
                col1, col2, col3 = st.columns(3)
                col1.metric("Mean", f"{mean:.4f}")
                col2.metric("Median", f"{median:.4f}")
                col3.metric("Mode", f"{mode}")

                col4, col5, col6 = st.columns(3)
                col4.metric("Variance", f"{variance:.4f}")
                col5.metric("Std Deviation", f"{std_dev:.4f}")
                col6.metric("Range", f"{data_range:.4f}")

                st.session_state.history.append(
                    f"Stats on [{data_str.strip()}]: mean={mean:.4f}, median={median:.4f}, mode={mode}"
                )
        except Exception as exc:
            st.error(f"Error parsing numbers: {exc}")

# ──────────────────────────────────────────────
# 7. Matrix Operations
# ──────────────────────────────────────────────
elif operation == "Matrix Operations":
    st.header("🔲 Matrix Operations")

    with st.form("matrix_form"):
        mat1_str = st.text_area(
            "Matrix 1 (rows on new lines, values separated by spaces)",
            value="1 2\n3 4",
        )
        mat2_str = st.text_area(
            "Matrix 2 (needed for Add / Multiply)",
            value="5 6\n7 8",
        )
        mat_op = st.selectbox(
            "Operation",
            ["Add", "Multiply", "Transpose (Matrix 1)", "Determinant (Matrix 1)", "Inverse (Matrix 1)"],
        )
        submitted = st.form_submit_button("Calculate")

    if submitted:
        try:
            mat1 = parse_matrix(mat1_str)
            mat2 = parse_matrix(mat2_str) if mat2_str.strip() else None

            if mat_op == "Add":
                if mat2 is None:
                    st.error("Matrix 2 is required for addition")
                else:
                    res = mat1 + mat2
                    st.write("Result:")
                    st.write(res)
                    st.session_state.history.append(f"Matrix Add → {res.tolist()}")

            elif mat_op == "Multiply":
                if mat2 is None:
                    st.error("Matrix 2 is required for multiplication")
                else:
                    res = np.dot(mat1, mat2)
                    st.write("Result:")
                    st.write(res)
                    st.session_state.history.append(f"Matrix Multiply → {res.tolist()}")

            elif mat_op == "Transpose (Matrix 1)":
                res = mat1.T
                st.write("Transpose:")
                st.write(res)
                st.session_state.history.append(f"Matrix Transpose → {res.tolist()}")

            elif mat_op == "Determinant (Matrix 1)":
                det = np.linalg.det(mat1)
                st.write(f"Determinant: {det}")
                st.session_state.history.append(f"Matrix Determinant = {det}")

            elif mat_op == "Inverse (Matrix 1)":
                det = np.linalg.det(mat1)
                if abs(det) < 1e-12:
                    st.error("Matrix is singular — inverse does not exist")
                else:
                    inv = np.linalg.inv(mat1)
                    st.write("Inverse:")
                    st.write(inv)
                    st.session_state.history.append(f"Matrix Inverse → {inv.tolist()}")
        except Exception as exc:
            st.error(f"Matrix input error: {exc}")

# ──────────────────────────────────────────────
# 8. Complex Arithmetic
# ──────────────────────────────────────────────
elif operation == "Complex Arithmetic":
    st.header("🌀 Complex Number Arithmetic")

    with st.form("complex_form"):
        c1 = st.text_input("Complex number 1", value="1+2j")
        c2 = st.text_input("Complex number 2", value="3-4j")
        comp_op = st.selectbox("Operation", ["Add", "Subtract", "Multiply", "Divide", "Exponentiate"])
        submitted = st.form_submit_button("Calculate")

    if submitted:
        try:
            num1 = complex(c1)
            num2 = complex(c2)
            result = None
            if comp_op == "Add":
                result = num1 + num2
            elif comp_op == "Subtract":
                result = num1 - num2
            elif comp_op == "Multiply":
                result = num1 * num2
            elif comp_op == "Divide":
                if num2 == 0:
                    st.error("Division by zero")
                else:
                    result = num1 / num2
            elif comp_op == "Exponentiate":
                result = num1 ** num2
            if result is not None:
                st.success(f"Result: {result}")
                st.session_state.history.append(f"{c1} {comp_op} {c2} = {result}")
        except Exception as exc:
            st.error(f"Error: {exc}")

# ──────────────────────────────────────────────
# 9. Plot Function
# ──────────────────────────────────────────────
elif operation == "Plot Function":
    st.header("📈 Function Plotter")

    with st.form("plot_form"):
        expr = st.text_input("Enter function of x", value="sin(x)")
        x_min = st.number_input("x min", value=-10.0)
        x_max = st.number_input("x max", value=10.0)
        points = st.slider("Number of points", min_value=100, max_value=1000, value=500)
        submitted = st.form_submit_button("Plot")

    if submitted:
        try:
            x = sp.symbols("x")
            f = sp.sympify(expr)
            f_np = sp.lambdify(x, f, modules=["numpy"])

            x_vals = np.linspace(x_min, x_max, points)
            y_vals = f_np(x_vals)

            fig, ax = plt.subplots()
            ax.plot(x_vals, y_vals, linewidth=2, color="#1f77b4")
            ax.set_title(f"Plot of {expr}", fontsize=14)
            ax.set_xlabel("x")
            ax.set_ylabel("f(x)")
            ax.grid(True, linestyle="--", alpha=0.7)
            ax.axhline(y=0, color="k", linewidth=0.5)
            ax.axvline(x=0, color="k", linewidth=0.5)
            st.pyplot(fig)
            st.session_state.history.append(f"Plotted: {expr}")
        except Exception as exc:
            st.error(f"Error plotting function: {exc}")

# ──────────────────────────────────────────────
# 10. Prime Checker / Generator
# ──────────────────────────────────────────────
elif operation == "Prime Checker/Generator":
    st.header("🔑 Prime Checker & Generator")

    with st.form("prime_form"):
        choice = st.radio("Select mode", ["Check Prime", "Generate Primes up to N"])
        if choice == "Check Prime":
            num = st.number_input("Enter integer", min_value=1, step=1)
        else:
            limit = st.number_input("Generate primes up to", min_value=2, step=1)
        submitted = st.form_submit_button("Run")

    if submitted:
        if choice == "Check Prime":
            if is_prime(int(num)):
                st.success(f"✅ {int(num)} is prime!")
                st.session_state.history.append(f"Checked prime: {int(num)} → prime")
            else:
                st.warning(f"❌ {int(num)} is not prime.")
                st.session_state.history.append(f"Checked prime: {int(num)} → not prime")
        else:
            primes = [i for i in range(2, int(limit) + 1) if is_prime(i)]
            st.write(f"**Primes up to {int(limit)}:**")
            st.write(primes)
            st.session_state.history.append(f"Generated primes up to {int(limit)} ({len(primes)} found)")

# ──────────────────────────────────────────────
# 11. Solve System of Equations
# ──────────────────────────────────────────────
elif operation == "Solve System of Equations":
    st.header("📝 Solve System of Linear Equations")

    with st.form("solve_form"):
        eqns_text = st.text_area(
            "Enter equations (one per line, e.g. x + y = 2)",
            value="x + y = 2\nx - y = 0",
        )
        vars_text = st.text_input("Variables (comma separated)", value="x,y")
        submitted = st.form_submit_button("Solve")

    if submitted:
        try:
            eqns = []
            for eqn in eqns_text.strip().split("\n"):
                if "=" not in eqn:
                    st.error(f"Invalid equation (missing '='): {eqn}")
                    break
                left, right = eqn.split("=")
                eqn_expr = sp.Eq(sp.sympify(left), sp.sympify(right))
                eqns.append(eqn_expr)
            else:
                variables = sp.symbols(vars_text)
                sol = sp.solve(eqns, variables)
                st.success(f"Solution: {sol}")
                st.session_state.history.append(f"Solved system → {sol}")
        except Exception as exc:
            st.error(f"Error solving system: {exc}")

# ──────────────────────────────────────────────
# Calculation History
# ──────────────────────────────────────────────
st.markdown("---")
st.write("### 🕘 Calculation History (Last 10)")

if len(st.session_state.history) == 0:
    st.info("No calculations yet — start computing above!")
else:
    for item in reversed(st.session_state.history[-10:]):
        st.write(f"- {item}")

    if st.button("🗑️ Clear History"):
        st.session_state.history = []
        st.rerun()