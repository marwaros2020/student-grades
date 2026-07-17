import streamlit as st
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="مسابقة التحدث بالإنجليزية", layout="centered")

# 2. تحميل البيانات
@st.cache_data
def load_data():
    df = pd.read_excel('school_data.xlsx', sheet_name='Students_List')
    
    df.columns = df.columns.str.strip()
    return df

try:
    students_df = load_data()
except Exception as e:
    st.error(f"خطأ في تحميل ملف البيانات: {e}")
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
        match = students_df[
            (students_df['National_ID'].astype(str) == input_national_id.strip()) & 
            (students_df['Student_ID'].astype(str) == input_student_id.strip())
        ]
        if not match.empty:
            st.session_state['logged_in'] = True
            st.session_state['user_data'] = match.iloc[0]
            st.rerun()
        else:
            st.error("بيانات غير صحيحة.")
else:
    user = st.session_state['user_data']
    st.write(f"### مرحباً {user['Student_Name']}")
    
    # رفع المشاركة
    video_url = st.text_input("ضعي رابط فيديو OneDrive:")
    comment = st.text_area("تعليقك (اختياري):")

    if st.button("إرسال المشاركة"):
        if video_url:
            new_sub = pd.DataFrame({'National_ID': [user['National_ID']], 'Video_URL': [video_url], 'Status': ['pending'], 'Comment': [comment]})
            try:
                book = pd.read_excel('school_data.xlsx', sheet_name='Submissions')
                updated_book = pd.concat([book, new_sub], ignore_index=True)
                with pd.ExcelWriter('school_data.xlsx', engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                    updated_book.to_excel(writer, sheet_name='Submissions', index=False)
                st.success("تم إرسال مشاركتك!")
            except Exception as e:
                st.error(f"خطأ في الحفظ: {e}")
        else:
            st.warning("يرجى إدخال الرابط.")

    if st.button("خروج"):
        st.session_state['logged_in'] = False
        st.rerun()

    # لوحة تحكم الإدارة (النسخة الموحدة والنهائية)
    st.write("---")
    if st.checkbox("دخول لوحة التحكم (للمسؤول)"):
        password = st.text_input("كلمة المرور:", type="password")
        if password == "1234":
            st.subheader("لوحة تحكم المسابقة")
            try:
                # قراءة البيانات
                subs_df = pd.read_excel('school_data.xlsx', sheet_name='Submissions')
                subs_df['Status'] = subs_df['Status'].astype(str)
                # تنظيف البيانات
                subs_df = subs_df.dropna(subset=['National_ID'])
                
                # عرض الجدول
                st.dataframe(subs_df[['National_ID', 'Video_URL', 'Status', 'Comment']])
                
                # إدخال بيانات التحديث
                target_id = st.text_input("أدخل الرقم القومي لتعديل الحالة:")
                new_status = st.selectbox("اختر الحالة:", ["Approved", "Rejected"])
                
                if st.button("تحديث الحالة"):
                    subs_df['National_ID'] = subs_df['National_ID'].astype(float).astype(int).astype(str)
                    search_id = target_id.strip()
                    st.write(f"البحث عن: '{search_id}' في: {subs_df['National_ID'].tolist()}")

                    mask = subs_df['National_ID'] == search_id
                    
                    if mask.any():
                        subs_df.loc[mask, 'Status'] = new_status
                        with pd.ExcelWriter('school_data.xlsx', engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                            subs_df.to_excel(writer, sheet_name='Submissions', index=False)
                        st.success(f"تم تحديث حالة الطالب {search_id} إلى {new_status}")
                        st.rerun()
                    else:
                        st.error("لم يتم العثور على طالب بهذا الرقم القومي.")
            except Exception as e:
                st.error(f"حدث خطأ أثناء المعالجة: {e}")
