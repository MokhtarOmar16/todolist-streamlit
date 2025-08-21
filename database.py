import streamlit as st

st.title("تجربة مع الاكستنشن")

with st.form("my_form"):
    name = st.text_input("اسمك")
    age = st.number_input("عمرك", min_value=0, max_value=120, step=1)
    feedback = st.text_area("رأيك")

    submitted = st.form_submit_button("إرسال")
    if submitted:
        st.write("📌 القيم اللي اتملاّت:")
        st.write({"name": name, "age": age, "feedback": feedback})
