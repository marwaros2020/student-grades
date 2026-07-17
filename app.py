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
            # تجهيز البيانات لحفظها
            new_submission = pd.DataFrame({
                'National_ID': [user['National_ID']],
                'Video_URL': [video_url],
                'Comment_Text': [comment],
                'Status': ['Pending'] # الحالة الافتراضية
            })
            
            # محاولة قراءة الملف وإضافة السطر الجديد
            try:
                # قراءة ورقة المشاركات
                book = pd.read_excel('school_data.xlsx', sheet_name='Submissions')
                # إضافة المشاركة الجديدة
                updated_book = pd.concat([book, new_submission], ignore_index=True)
                # حفظ الملف
                with pd.ExcelWriter('school_data.xlsx', engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                    updated_book.to_excel(writer, sheet_name='Submissions', index=False)
                
                st.success("✅ تم استلام مشاركتك بنجاح، وهي قيد المراجعة.")
            except Exception as e:
                st.error(f"حدث خطأ أثناء حفظ المشاركة: {e}")
        else:
            st.warning("يرجى إدخال رابط الفيديو أولاً.")
    if st.button("خروج"):
        st.session_state['logged_in'] = False
        st.rerun()
# --- لوحة تحكم الإدارة ---
st.write("---")
if st.checkbox("دخول لوحة التحكم (خاص بالمسؤول)"):
    password = st.text_input("أدخل كلمة المرور:", type="password")
    if password == "1234": # يمكنك تغيير كلمة المرور هنا
        st.subheader("لوحة تحكم المسابقة")
        
        # قراءة المشاركات
        try:
            subs_df = pd.read_excel('school_data.xlsx', sheet_name='Submissions')
            st.dataframe(subs_df)
            
            # خيار بسيط لتغيير الحالة
            target_id = st.text_input("أدخل الرقم القومي للطالب لتعديل حالته:")
            new_status = st.selectbox("اختر الحالة الجديدة:", ["Approved", "Rejected"])
            
            if st.button("تحديث الحالة"):
                # منطق تحديث الحالة في الإكسيل
                subs_df.loc[subs_df['National_ID'].astype(str) == target_id, 'Status'] = new_status
                with pd.ExcelWriter('school_data.xlsx', engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                    subs_df.to_excel(writer, sheet_name='Submissions', index=False)
                st.success("تم تحديث الحالة بنجاح!")
                st.rerun()
        except Exception as e:
            st.error(f"لا توجد مشاركات بعد أو حدث خطأ: {e}")
    else:
        st.warning("كلمة مرور خاطئة.")
