import streamlit as st
import pandas as pd

# عنوان الموقع
st.title("نظام الاستعلام عن نتائج الطلاب")

# تحميل البيانات
@st.cache_data
def load_data():
    return pd.read_excel('students.xlsx')

df = load_data()

# خانة البحث
student_id = st.number_input("أدخل كود الطالب (student_ID):", min_value=0, step=1)

if st.button("بحث"):
    result = df[df['student_ID'] == student_id]
    
    if not result.empty:
        st.success("تم العثور على الطالب!")
        st.write(result.iloc[0])
    else:
        st.error("كود الطالب غير موجود، يرجى المحاولة مرة أخرى.")
