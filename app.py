import streamlit as st
import pandas as pd
import plotly.express as px

# 1. إعداد الصفحة وتنسيقها (النقطة 3)
st.set_page_config(page_title="نظام النتائج", page_icon="🎓")
st.title("🎓 نظام الاستعلام عن نتائج الطلاب")
st.subheader("مرحباً بك في بوابة نتائج المدرسة")

@st.cache_data
def load_data():
    return pd.read_excel('students.xlsx')

df = load_data()

# 2. تحسين العرض (النقطة 1)
student_id = st.number_input("أدخل كود الطالب:", min_value=0, step=1)

if st.button("عرض النتيجة"):
    result = df[df['student_ID'] == student_id]
    
    if not result.empty:
        student_data = result.iloc[0]
        st.success(f"مرحباً {student_data['Student_Name']}!")
        
        # عرض البيانات بشكل منظم بدون العمود الإضافي 0
        display_df = result.drop(columns=['student_ID', 'Student_Name']).T
        display_df.columns = ['الدرجة']
        st.table(display_df)
        
        # 3. الرسوم البيانية (النقطة 2)
        st.write("### 📊 تحليل مستوى الطالب")
        chart_data = display_df.reset_index().rename(columns={'index': 'المادة'})
        fig = px.bar(chart_data, x='المادة', y='الدرجة', color='الدرجة', color_continuous_scale='Viridis')
        st.plotly_chart(fig)
        
    else:
        st.error("كود الطالب غير موجود، يرجى التأكد من الرقم.")
    
    if not result.empty:
        st.success("تم العثور على الطالب!")
        st.write(result.iloc[0])
    else:
        st.error("كود الطالب غير موجود، يرجى المحاولة مرة أخرى.")
