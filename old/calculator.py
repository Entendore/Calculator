import streamlit as st
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(page_title="Multi-Function Calculator", layout="wide")

st.title("🧮 Multi-Function Calculator")

# Initialize history in session state
if "history" not in st.session_state:
    st.session_state.history = []

def safe_eval(expr):
    try:
        return sp.sympify(expr)
    except Exception:
        st.error(f"Invalid expression: {expr}")
        return None

operation = st.sidebar.selectbox("Choose Operation", [
    "Basic Arithmetic",
    "Exponentiation & Logs",
    "Calculus",
    "Statistics",
    "Matrix Operations",
    "Complex Arithmetic",
    "Plot Function",
    "Prime Checker/Generator",
    "Solve System of Equations"
])

with st.sidebar.expander("Instructions"):
    st.markdown("""
    - Select an operation.
    - Enter inputs in the main panel.
    - Press submit buttons to calculate.
    - Results and error messages will appear below inputs.
    - History of calculations is shown at the bottom.
    """)

# -------- Basic Arithmetic --------
if operation == "Basic Arithmetic":
    st.header("Basic Arithmetic")

    with st.form("basic_arith_form"):
        col1, col2 = st.columns(2)
        with col1:
            expr1 = st.text_input("Expression 1", value="10", help="Enter a number or expression, e.g. 2*x + 3")
        with col2:
            expr2 = st.text_input("Expression 2", value="5", help="Enter a number or expression")

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

# -------- Exponentiation & Logs --------
elif operation == "Exponentiation & Logs":
    st.header("Exponentiation & Logarithms")

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
                    result = b**e
                    st.success(f"Result: {result}")
                    st.session_state.history.append(f"{b} ** {e} = {result}")

            elif sub_op == "Logarithm":
                v = float(val)
                if v <= 0:
                    st.error("Value must be positive")
                else:
                    if base.lower() == 'e':
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
                    result = np.sqrt(v)
                    st.success(f"Result: {result}")
                    st.session_state.history.append(f"sqrt({v}) = {result}")
        except Exception as e:
            st.error(f"Error: {e}")

# -------- Calculus --------
elif operation == "Calculus":
    st.header("Calculus Operations")

    with st.form("calculus_form"):
        calc_op = st.radio("Operation", ["Derivative", "Nth Derivative", "Integral (Indefinite)", "Integral (Definite)"])
        expr = st.text_input("Function in x", value="x**3 + 2*x")
        submitted = st.form_submit_button("Calculate")

        x = sp.symbols('x')
        f = safe_eval(expr)

        if submitted:
            if f is not None:
                try:
                    if calc_op == "Derivative":
                        d = sp.diff(f, x)
                        st.success(f"Derivative: {d}")
                        st.session_state.history.append(f"d/dx({expr}) = {d}")

                    elif calc_op == "Nth Derivative":
                        n = st.number_input("Derivative order (n)", min_value=1, value=1)
                        d = sp.diff(f, x, int(n))
                        st.success(f"{n}th Derivative: {d}")
                        st.session_state.history.append(f"d^{n}/dx^{n}({expr}) = {d}")

                    elif calc_op == "Integral (Indefinite)":
                        integ = sp.integrate(f, x)
                        st.success(f"Indefinite Integral: {integ} + C")
                        st.session_state.history.append(f"∫ {expr} dx = {integ} + C")

                    else:
                        a = st.text_input("Lower limit (a)", value="0")
                        b = st.text_input("Upper limit (b)", value="1")
                        try:
                            a_val = float(sp.sympify(a))
                            b_val = float(sp.sympify(b))
                            integ = sp.integrate(f, (x, a_val, b_val))
                            st.success(f"Definite Integral from {a_val} to {b_val}: {integ.evalf()}")
                            st.session_state.history.append(f"∫_{a_val}^{b_val} {expr} dx = {integ.evalf()}")
                        except Exception as e:
                            st.error(f"Invalid limits: {e}")
                except Exception as e:
                    st.error(f"Error: {e}")

# -------- Statistics --------
elif operation == "Statistics":
    st.header("Statistics")

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
                counts = {val:data.count(val) for val in set(data)}
                mode = max(counts, key=counts.get) if counts else None

                st.write(f"Mean: {mean}")
                st.write(f"Median: {median}")
                st.write(f"Mode: {mode}")
                st.write(f"Variance: {variance}")
                st.write(f"Standard Deviation: {std_dev}")
                st.write(f"Range: {data_range}")

                st.session_state.history.append(f"Stats on {data_str}: mean={mean}, median={median}, mode={mode}")
        except Exception as e:
            st.error(f"Error parsing numbers: {e}")

# -------- Matrix Operations --------
elif operation == "Matrix Operations":
    st.header("Matrix Operations")

    with st.form("matrix_form"):
        mat1_str = st.text_area("Matrix 1 (rows separated by newlines, values by spaces)", value="1 2\n3 4")
        mat2_str = st.text_area("Matrix 2 (optional for Add/Multiply)", value="5 6\n7 8")
        mat_op = st.selectbox("Select operation", ["Add", "Multiply", "Transpose (Matrix 1)", "Determinant (Matrix 1)", "Inverse (Matrix 1)"])
        submitted = st.form_submit_button("Calculate")

    def parse_matrix(text):
        return np.array([[float(x) for x in row.split()] for row in text.strip().split("\n")])

    if submitted:
        try:
            mat1 = parse_matrix(mat1_str)
            mat2 = parse_matrix(mat2_str) if mat2_str.strip() else None

            if mat_op == "Add":
                if mat2 is None:
                    st.error("Matrix 2 needed for addition")
                else:
                    res = mat1 + mat2
                    st.write(res)
                    st.session_state.history.append(f"Matrix Add result:\n{res}")

            elif mat_op == "Multiply":
                if mat2 is None:
                    st.error("Matrix 2 needed for multiplication")
                else:
                    res = np.dot(mat1, mat2)
                    st.write(res)
                    st.session_state.history.append(f"Matrix Multiply result:\n{res}")

            elif mat_op == "Transpose (Matrix 1)":
                res = mat1.T
                st.write(res)
                st.session_state.history.append(f"Matrix Transpose result:\n{res}")

            elif mat_op == "Determinant (Matrix 1)":
                det = np.linalg.det(mat1)
                st.write(det)
                st.session_state.history.append(f"Matrix Determinant: {det}")

            elif mat_op == "Inverse (Matrix 1)":
                det = np.linalg.det(mat1)
                if det == 0:
                    st.error("Matrix is singular, no inverse")
                else:
                    inv = np.linalg.inv(mat1)
                    st.write(inv)
                    st.session_state.history.append(f"Matrix Inverse result:\n{inv}")
        except Exception as e:
            st.error(f"Matrix input error: {e}")

# -------- Complex Arithmetic --------
elif operation == "Complex Arithmetic":
    st.header("Complex Number Arithmetic")

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
        except Exception as e:
            st.error(f"Error: {e}")

# -------- Plot Function --------
elif operation == "Plot Function":
    st.header("Function Plotter")

    with st.form("plot_form"):
        expr = st.text_input("Enter function of x", value="sin(x)")
        x_min = st.number_input("x min", value=-10.0)
        x_max = st.number_input("x max", value=10.0)
        points = st.slider("Number of points", min_value=100, max_value=1000, value=500)
        submitted = st.form_submit_button("Plot")

    if submitted:
        try:
            x = sp.symbols('x')
            f = sp.sympify(expr)
            f_np = sp.lambdify(x, f, "numpy")

            x_vals = np.linspace(x_min, x_max, points)
            y_vals = f_np(x_vals)

            fig, ax = plt.subplots()
            ax.plot(x_vals, y_vals)
            ax.set_title(f"Plot of {expr}")
            ax.grid(True)
            st.pyplot(fig)
            st.session_state.history.append(f"Plotted function: {expr}")
        except Exception as e:
            st.error(f"Error plotting function: {e}")

# -------- Prime Checker/Generator --------
elif operation == "Prime Checker/Generator":
    st.header("Prime Checker & Generator")

    def is_prime(n):
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

    with st.form("prime_form"):
        choice = st.radio("Select mode", ["Check Prime", "Generate Primes up to N"])
        if choice == "Check Prime":
            num = st.number_input("Enter integer", min_value=1, step=1)
        else:
            limit = st.number_input("Generate primes up to", min_value=2, step=1)
        submitted = st.form_submit_button("Run")

    if submitted:
        if choice == "Check Prime":
            if is_prime(num):
                st.success(f"{num} is prime!")
                st.session_state.history.append(f"Checked prime: {num} is prime")
            else:
                st.warning(f"{num} is not prime.")
                st.session_state.history.append(f"Checked prime: {num} is not prime")
        else:
            primes = [i for i in range(2, limit + 1) if is_prime(i)]
            st.write(f"Primes up to {limit}:")
            st.write(primes)
            st.session_state.history.append(f"Generated primes up to {limit}")

# -------- Solve System of Equations --------
elif operation == "Solve System of Equations":
    st.header("Solve System of Linear Equations")

    with st.form("solve_form"):
        eqns_text = st.text_area("Enter equations (one per line, e.g. x + y = 2)", value="x + y = 2\nx - y = 0")
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
            variables = sp.symbols(vars_text)
            sol = sp.solve(eqns, variables)
            st.write("Solution:")
            st.write(sol)
            st.session_state.history.append(f"Solved system: {sol}")
        except Exception as e:
            st.error(f"Error solving system: {e}")

# -------- History Display --------
st.markdown("---")
st.write("### 🕘 Calculation History (Last 10)")
if len(st.session_state.history) == 0:
    st.write("No history yet.")
else:
    for item in reversed(st.session_state.history[-10:]):
        st.write(item)
