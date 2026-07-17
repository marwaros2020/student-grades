import streamlit as st
import pandas as pd
# تعديل تحميل البيانات للتأكد من قراءة الورقة الصحيحة
@st.cache_data
def load_data():
    # تأكدي أن اسم الملف في المجلد هو school_data.xlsx
    df = pd.read_excel('school_data.xlsx', sheet_name='Students_List')
    # تنظيف أسماء الأعمدة من أي مسافات مخفية قد تسبب مشاكل
    df.columns = df.columns.str.strip()
    return df

students_df = load_data()


st.title("🛡️ بوابة مسابقة التحدث باللغة الإنجليزية")

# بوابة الدخول
st.subheader("تسجيل الدخول للمشاركة")
input_national_id = st.text_input("أدخل الرقم القومي:")
input_student_id = st.text_input("أدخل كود الطالب:")

if st.button("دخول"):
    # البحث عن الطالب في الملف
    user = students_df[
        (students_df['National_ID'].astype(str) == input_national_id) & 
        (students_df['Student_ID'].astype(str) == input_student_id)
    ]
    
    if not user.empty:
        st.session_state['logged_in'] = True
        st.session_state['user_data'] = user.iloc[0]
        st.success(f"أهلاً بكِ {user.iloc[0]['Student_Name']}! يمكنك الآن البدء.")
        st.rerun() # تحديث الصفحة للدخول للمرحلة التالية
    else:
        st.error(" بيانات غير صحيحة أو غير مسجلة في قاعدة البيانات. برجاء التواصل مع معلمك لتسجيل بياناتك")

# ما بعد الدخول
if 'logged_in' in st.session_state and st.session_state['logged_in']:
    st.write("---")
    st.write("### مرحباً بك في صفحة المشاركة")
    st.write(f"المدرسة: {st.session_state['user_data']['School_Name']}")
    # هنا سنضيف لاحقاً زر رفع رابط الفيديو
    if not result.empty:
        st.success("تم العثور على الطالب!")
        st.write(result.iloc[0])
    else:
        st.error("كود الطالب غير موجود، يرجى المحاولة مرة أخرى.")
        # أضيفي هذا السطر بعد تحميل البيانات مباشرة
st.write("بيانات الطلاب المكتشفة:", students_df.head())
st.write("أنواع البيانات في الملف:", students_df.dtypes)
