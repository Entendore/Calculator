import streamlit as st
import sympy as sp
import matplotlib.pyplot as plt
import numpy as np

st.title("Multi-Function Calculator")

operation = st.selectbox("Choose operation:", [
    "Addition",
    "Subtraction",
    "Multiplication",
    "Division",
    "Exponentiation",
    "Logarithm",
    "Square Root",
    "Derivative",
    "Nth Derivative",
    "Integral (Indefinite)",
    "Integral (Definite)",
    "Factorization",
    "Solve Equation",
    "Statistics",
    "Complex Arithmetic",
    "Plot Function",
    "Matrix Operations",
    "Prime Checker/Generator",
    "Solve System of Equations"
])

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

def safe_eval(expr):
    try:
        return float(sp.sympify(expr))
    except Exception:
        st.error(f"Invalid expression: {expr}")
        return None

if operation in ["Addition", "Subtraction", "Multiplication", "Division", "Exponentiation"]:
    st.write("Enter two numbers or expressions:")
    expr1 = st.text_input("Expression 1:", value="0")
    expr2 = st.text_input("Expression 2:", value="0")

    val1 = safe_eval(expr1)
    val2 = safe_eval(expr2)

    if val1 is not None and val2 is not None:
        result = None
        if operation == "Addition":
            result = val1 + val2
        elif operation == "Subtraction":
            result = val1 - val2
        elif operation == "Multiplication":
            result = val1 * val2
        elif operation == "Division":
            if val2 == 0:
                st.error("Division by zero error")
            else:
                result = val1 / val2
        elif operation == "Exponentiation":
            result = val1 ** val2
        if result is not None:
            st.success(f"Result: {result}")

elif operation == "Logarithm":
    st.write("Compute logarithm")
    expr = st.text_input("Enter number (positive):", value="10")
    base = st.text_input("Enter base (default e):", value="e")
    try:
        num = float(expr)
        if num <= 0:
            st.error("Number must be positive")
        else:
            if base.lower() == 'e':
                result = sp.log(num)
            else:
                base_val = float(base)
                if base_val <= 0 or base_val == 1:
                    st.error("Base must be positive and not equal to 1")
                else:
                    result = sp.log(num, base_val)
            st.success(f"Result: {result.evalf()}")
    except Exception as e:
        st.error(f"Error: {e}")

elif operation == "Square Root":
    st.write("Compute square root")
    expr = st.text_input("Enter number:", value="9")
    try:
        num = float(expr)
        if num < 0:
            st.error("Cannot compute square root of negative number")
        else:
            result = sp.sqrt(num)
            st.success(f"Result: {result.evalf()}")
    except Exception as e:
        st.error(f"Error: {e}")

elif operation == "Derivative":
    st.write("Compute derivative with respect to x")
    expr = st.text_input("Enter expression in x:", value="x**2 + 3*x + 2")
    try:
        x = sp.symbols('x')
        f = sp.sympify(expr)
        derivative = sp.diff(f, x)
        st.success(f"Derivative: {derivative}")
    except Exception as e:
        st.error(f"Error: {e}")

elif operation == "Nth Derivative":
    st.write("Compute nth derivative with respect to x")
    expr = st.text_input("Enter expression in x:", value="x**3 + x")
    n = st.number_input("Enter derivative order (n):", min_value=1, value=1)
    try:
        x = sp.symbols('x')
        f = sp.sympify(expr)
        derivative = sp.diff(f, x, int(n))
        st.success(f"{n}th Derivative: {derivative}")
    except Exception as e:
        st.error(f"Error: {e}")

elif operation == "Integral (Indefinite)":
    st.write("Compute indefinite integral with respect to x")
    expr = st.text_input("Enter expression in x:", value="x**2 + 3*x + 2")
    try:
        x = sp.symbols('x')
        f = sp.sympify(expr)
        integral = sp.integrate(f, x)
        st.success(f"Integral: {integral} + C")
    except Exception as e:
        st.error(f"Error: {e}")

elif operation == "Integral (Definite)":
    st.write("Compute definite integral with respect to x")
    expr = st.text_input("Enter expression in x:", value="x**2")
    a = st.text_input("Lower limit (a):", value="0")
    b = st.text_input("Upper limit (b):", value="1")
    try:
        x = sp.symbols('x')
        f = sp.sympify(expr)
        a_val = float(sp.sympify(a))
        b_val = float(sp.sympify(b))
        definite_integral = sp.integrate(f, (x, a_val, b_val))
        st.success(f"Definite Integral from {a_val} to {b_val}: {definite_integral.evalf()}")
    except Exception as e:
        st.error(f"Error: {e}")

elif operation == "Factorization":
    st.write("Factorize expression in x")
    expr = st.text_input("Enter expression:", value="x**2 - 4")
    try:
        x = sp.symbols('x')
        f = sp.sympify(expr)
        factored = sp.factor(f)
        st.success(f"Factored form: {factored}")
    except Exception as e:
        st.error(f"Error: {e}")

elif operation == "Solve Equation":
    st.write("Solve equation f(x) = 0")
    expr = st.text_input("Enter expression in x:", value="x**2 - 4")
    try:
        x = sp.symbols('x')
        f = sp.sympify(expr)
        solutions = sp.solve(f, x)
        st.success(f"Solutions: {solutions}")
    except Exception as e:
        st.error(f"Error: {e}")

elif operation == "Complex Arithmetic":
    st.write("Enter two complex numbers (e.g. 1+2j, 3-4j)")
    expr1 = st.text_input("Complex Number 1:", value="1+2j")
    expr2 = st.text_input("Complex Number 2:", value="3-4j")
    comp_op = st.selectbox("Operation", ["Add", "Subtract", "Multiply", "Divide", "Exponentiate"])

    try:
        c1 = complex(expr1)
        c2 = complex(expr2)
        result = None
        
        if comp_op == "Add":
            result = c1 + c2
        elif comp_op == "Subtract":
            result = c1 - c2
        elif comp_op == "Multiply":
            result = c1 * c2
        elif comp_op == "Divide":
            if c2 == 0:
                st.error("Division by zero")
            else:
                result = c1 / c2
        elif comp_op == "Exponentiate":
            result = c1 ** c2
        
        if result is not None:
            st.success(f"Result: {result}")
    except Exception as e:
        st.error(f"Error: {e}")

elif operation == "Statistics":
    st.write("Enter a list of numbers separated by commas (e.g. 1, 2, 3, 4)")
    data_str = st.text_area("Numbers:", value="1, 2, 3, 4, 5")
    try:
        data = [float(i.strip()) for i in data_str.split(",") if i.strip() != ""]
        if len(data) == 0:
            st.warning("Please enter at least one number")
        else:
            arr = np.array(data)
            mean = np.mean(arr)
            median = np.median(arr)
            variance = np.var(arr, ddof=1) if len(arr) > 1 else 0
            std_dev = np.std(arr, ddof=1) if len(arr) > 1 else 0
            mode = None
            try:
                counts = {i:data.count(i) for i in set(data)}
                mode = max(counts, key=counts.get)
            except:
                mode = "N/A"
            data_range = np.ptp(arr)

            st.write(f"Mean: {mean}")
            st.write(f"Median: {median}")
            st.write(f"Mode: {mode}")
            st.write(f"Variance: {variance}")
            st.write(f"Standard Deviation: {std_dev}")
            st.write(f"Range: {data_range}")
    except Exception as e:
        st.error(f"Error parsing input: {e}")
elif operation == "Prime Checker/Generator":
    choice = st.radio("Choose:", ["Check if a number is prime", "Generate primes up to N"])
    if choice == "Check if a number is prime":
        num = st.number_input("Enter integer:", min_value=1, step=1)
        if st.button("Check"):
            if is_prime(num):
                st.success(f"{num} is a prime number.")
            else:
                st.warning(f"{num} is not a prime number.")
    else:
        limit = st.number_input("Generate primes up to:", min_value=2, step=1)
        if st.button("Generate"):
            primes = [i for i in range(2, limit + 1) if is_prime(i)]
            st.write(f"Primes up to {limit}:")
            st.write(primes)

elif operation == "Solve System of Equations":
    st.write("Enter system of linear equations (one per line), variables separated by commas")
    eqns_text = st.text_area("Equations:", value="x + y = 2\nx - y = 0")
    vars_text = st.text_input("Variables (comma separated):", value="x,y")

    try:
        eqns = [sp.sympify(eq.replace("=", "-(") + ")") for eq in eqns_text.strip().split("\n")]
        variables = sp.symbols(vars_text)
        sol = sp.linsolve(eqns, variables)
        st.write("Solution:")
        st.write(sol)
    except Exception as e:
        st.error(f"Error solving system: {e}")

elif operation == "Plot Function":
    st.write("Plot a function f(x)")
    expr = st.text_input("Enter function in x:", value="sin(x)")
    x_min = st.number_input("x min:", value=-10.0)
    x_max = st.number_input("x max:", value=10.0)
    num_points = st.slider("Number of points", min_value=100, max_value=1000, value=500)
    
    try:
        x = sp.symbols('x')
        f = sp.sympify(expr)
        f_lambdified = sp.lambdify(x, f, modules=["numpy"])
        
        x_vals = np.linspace(x_min, x_max, num_points)
        y_vals = f_lambdified(x_vals)
        
        fig, ax = plt.subplots()
        ax.plot(x_vals, y_vals)
        ax.set_title(f"Plot of {expr}")
        ax.grid(True)
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Error plotting function: {e}")
elif operation == "Matrix Operations":
    st.write("Matrix Operations: addition, multiplication, transpose, determinant, inverse")
    mat1_str = st.text_area("Matrix 1 (rows separated by new lines, values by spaces):", value="1 2\n3 4")
    mat2_str = st.text_area("Matrix 2 (optional for addition/multiplication):", value="5 6\n7 8")
    mat_op = st.selectbox("Matrix Operation", ["Add", "Multiply", "Transpose (Matrix 1)", "Determinant (Matrix 1)", "Inverse (Matrix 1)"])

    def parse_matrix(text):
        return np.array([[float(num) for num in row.split()] for row in text.strip().split("\n")])
    
    try:
        mat1 = parse_matrix(mat1_str)
        mat2 = parse_matrix(mat2_str) if mat2_str.strip() else None
        
        if mat_op == "Add":
            if mat2 is None:
                st.error("Matrix 2 required for addition")
            else:
                res = mat1 + mat2
                st.write("Result:")
                st.write(res)
        elif mat_op == "Multiply":
            if mat2 is None:
                st.error("Matrix 2 required for multiplication")
            else:
                res = np.dot(mat1, mat2)
                st.write("Result:")
                st.write(res)
        elif mat_op == "Transpose (Matrix 1)":
            st.write(mat1.T)
        elif mat_op == "Determinant (Matrix 1)":
            det = np.linalg.det(mat1)
            st.write(f"Determinant: {det}")
        elif mat_op == "Inverse (Matrix 1)":
            if np.linalg.det(mat1) == 0:
                st.error("Matrix is singular, inverse does not exist")
            else:
                inv = np.linalg.inv(mat1)
                st.write("Inverse:")
                st.write(inv)
    except Exception as e:
        st.error(f"Error processing matrices: {e}")
else:
    st.write("Please select an operation")
