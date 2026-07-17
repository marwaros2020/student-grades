import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="مسابقة التحدث بالإنجليزية", layout="centered")

# 2. تحميل البيانات
@st.cache_data
def load_data():
    # نقوم بقراءة ملف الإكسيل من ورقة العمل المحددة
    df = pd.read_excel('school_data.xlsx', sheet_name='Students_List')
    # تنظيف أسماء الأعمدة من أي مسافات زائدة
    df.columns = df.columns.str.strip()
    return df

try:
    students_df = load_data()
except Exception as e:
    st.error(f"خطأ في تحميل ملف البيانات: {e}. تأكدي من وجود ملف 'school_data.xlsx' ووجود ورقة عمل باسم 'Students_List'.")
    st.stop()

# 3. واجهة بوابة الدخول
st.title("🛡️ بوابة مسابقة التحدث باللغة الإنجليزية")

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    st.subheader("تسجيل الدخول")
    input_national_id = st.text_input("أدخل الرقم القومي:")
    input_student_id = st.text_input("أدخل كود الطالب:")

    if st.button("دخول"):
        # تحويل المدخلات لنصوص لضمان المطابقة
        match = students_df[
            (students_df['National_ID'].astype(str) == input_national_id.strip()) & 
            (students_df['Student_ID'].astype(str) == input_student_id.strip())
        ]
        
        if not match.empty:
            st.session_state['logged_in'] = True
            st.session_state['user_data'] = match.iloc[0]
            st.success(f"أهلاً بكِ {match.iloc[0]['Student_Name']}!")
            st.rerun()
        else:
            st.error("بيانات غير صحيحة. يرجى التأكد من الرقم القومي وكود الطالب.")
else:
    # 4. واجهة المشارك بعد الدخول
    user = st.session_state['user_data']
    st.write(f"### مرحباً {user['Student_Name']}")
    st.write(f"**المدرسة:** {user['School_Name']} | **الفصل:** {user['Supervisor_Teacher']}")
    
    st.write("---")
    st.write("### صفحة رفع المشاركة")
    video_url = st.text_input("ضعي رابط فيديو OneDrive هنا:")
    comment = st.text_area("أضيفي تعليقك (اختياري):")

    if st.button("إرسال المشاركة"):
        if video_url:
            st.info("تم استلام مشاركتك، وهي الآن قيد المراجعة من قبل الإدارة.")
            # هنا سنضيف لاحقاً كود حفظ البيانات في ورقة Submissions
        else:
            st.warning("يرجى إدخال رابط الفيديو أولاً.")

    if st.button("خروج"):
        st.session_state['logged_in'] = False
        st.rerun()
