import streamlit as st
import db
import analyser
import pandas as pd
"""makes the output in indian format"""
def money(x):
    n = int(round(x))
    s = str(abs(n))
    if len(s) > 3:
        head, tail = s[:-3], s[-3:]
        parts = []
        while len(head) > 2:
            parts.insert(0, head[-2:])
            head = head[:-2]
        if head:
            parts.insert(0, head)
        s = ",".join(parts) + "," + tail
    return ("-" if n < 0 else "") + "₹" + s


st.set_page_config(page_title="Salary Analyzer", page_icon="💰", layout="wide")
db.init_db()
if "flash" in st.session_state:
    st.success(st.session_state.pop("flash"))

st.title("Salary Analyzer")

choice = st.sidebar.selectbox("Department", ["All"] + db.list_departments())
dept = None if choice == "All" else choice

salaries = db.get_salaries(dept)
st.sidebar.header("Add employee")
with st.sidebar.form("add_form", clear_on_submit=True):
    name = st.text_input("Name")
    department = st.text_input("Department")
    role = st.text_input("Role")
    salary = st.number_input("Annual salary (₹)", min_value=0.0, step=10000.0)
    submitted = st.form_submit_button("Add")

if submitted:
    if not (name.strip() and department.strip() and role.strip()) or salary <= 0:
        st.sidebar.error("Fill every field and enter a salary above 0.")
    else:
        db.add_employee(name, department, role, salary)
        st.session_state["flash"] = f"Added {name.strip()}."
        st.rerun()
stats = analyser.summary(salaries)

if stats is None:
    st.info("No employees found.")
    st.stop()

tab1, tab2 = st.tabs(["Overview", "Employees"])

with tab1:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Employees", stats["count"])
    c2.metric("Average", money(stats["mean"]))
    c3.metric("Median", money(stats["median"]))
    c4.metric("Std deviation", money(stats["std"]))

    c5, c6, c7, c8 = st.columns(4)
    c5.metric("Lowest", money(stats["min"]))
    c6.metric("Highest", money(stats["max"]))
    c7.metric("25th percentile", money(stats["p25"]))
    c8.metric("75th percentile", money(stats["p75"]))

with tab2:
    employees = db.get_employees(dept)
    df = pd.DataFrame(employees)
    df["salary"] = df["salary"].apply(money)
    df.columns = ["ID", "Name", "Department", "Role", "Salary"]
    st.dataframe(df, hide_index=True)

    st.subheader("Delete an employee")
    options = {f"{e['id']} - {e['name']}": e["id"] for e in employees}
    pick = st.selectbox("Select employee", list(options))
    if st.button("Delete"):
        db.delete_employee(options[pick])
        st.session_state["flash"] = f"Deleted {pick}."
        st.rerun()
