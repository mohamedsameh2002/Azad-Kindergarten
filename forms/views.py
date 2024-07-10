from django.shortcuts import render
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
import io
from django.http import HttpResponse,FileResponse
from django.core.mail import EmailMessage
from bidi.algorithm import get_display
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from arabic_reshaper import reshape




def draw_one_sq(i,a,b,c,*args):
    text = b[0]
    text_reshaped = get_display(reshape(text))

    # تعيين عرض المستطيل (90% من عرض الصفحة)
    rect_width = letter[0] * 0.9
    rect_height = 30  # ارتفاع ثابت للمستطيل

    # حساب الموضع للمستطيل
    start_x = (letter[0] - rect_width) / 2  # نقطة البداية للمستطيل

    # حساب المسافة نحو اليمين لعنوان دينامكياً بناءً على عرض الكلمة
    title = a[0]
    title_reshaped = get_display(reshape(title))
    title_width = pdfmetrics.stringWidth(title_reshaped, "Arial-Regular", 20)
    offset_x = rect_width - title_width - 10  # المسافة نحو اليمين للعنوان

    # رسم المستطيل
    rect_y = (letter[1] - rect_height) / 2 + i * (rect_height + 0.6 * inch) - 320
    c.setFillColorRGB(0.9, 0.9, 0.9)  # اللون الرمادي الفاتح
    c.rect(start_x, rect_y, rect_width, rect_height, fill=1)

    # كتابة "عنوان" فوق المستطيل بحجم خط 17
    c.setFont("Arial-Regular", 17)  # حجم الخط للعنوان فوق المستطيل
    c.setFillColorRGB(0, 0, 0)  # اللون الأسود
    c.drawRightString(start_x + rect_width - 10, rect_y + rect_height - 45, title_reshaped)

    # حساب حجم الخط المناسب للنص "محمد" داخل المستطيل
    text_font_size = 16


    # تعديل موضع النص "محمد" داخل المستطيل
    text_height = pdfmetrics.getAscent("Arial-Regular", text_font_size) - pdfmetrics.getDescent("Arial-Regular", text_font_size)
    text_y = rect_y + (rect_height - text_height) / 1.5 + text_height / 2  # المركز العمودي للنص
    c.setFont("Arial-Regular", text_font_size)  # حجم الخط للنص
    c.setFillColorRGB(0, 0, 0)  # اللون الأسود
    c.drawRightString(start_x + rect_width - 10, text_y, text_reshaped)





def draw_tow_sq(i,a,b,c,*args):
    text1 = b[1]
    text1_reshaped = get_display(reshape(text1))
    text2 = b[0]
    text2_reshaped = get_display(reshape(text2))

    text_font_size = 16
    text1_width = pdfmetrics.stringWidth(text1_reshaped, "Arial-Regular", text_font_size)
    text2_width = pdfmetrics.stringWidth(text2_reshaped, "Arial-Regular", text_font_size)
    text_height = pdfmetrics.getAscent("Arial-Regular", text_font_size) - pdfmetrics.getDescent("Arial-Regular", text_font_size)

    # تعيين عرض كل مستطيل (40% من عرض الصفحة)
    rect_width = letter[0] * 0.4
    rect_height = text_height + 10  # إضافة بعض الحشو حول النص

    # حساب المواضع للمستطيلات
    gap = 30  # الفجوة بين المستطيلات
    total_width = rect_width * 2 + gap  # العرض الكلي للمستطيلات والفجوة
    start_x = (letter[0] - total_width) / 2  # نقطة البداية للمستطيل الأول

    # حساب المسافة نحو اليمين لعنوان دينامكياً بناءً على عرض الكلمة
    title_above_rect1 = a[1]
    title_above_rect1_reshaped = get_display(reshape(title_above_rect1))
    title1_width = pdfmetrics.stringWidth(title_above_rect1_reshaped, "Arial-Regular", 20)
    offset_x1 = (rect_width - title1_width) / 1  # المسافة نحو اليمين لعنوان الأول

    title_above_rect2 = a[0]
    title_above_rect2_reshaped = get_display(reshape(title_above_rect2))
    title2_width = pdfmetrics.stringWidth(title_above_rect2_reshaped, "Arial-Regular", 20)
    offset_x2 = (rect_width - title2_width) / 1  # المسافة نحو اليمين لعنوان الثاني

    # رسم 4 مجموعات من المستطيلات والنصوص
    if args:
        rect1_y = (letter[1] - rect_height) / 10 + i * (rect_height + 0.7 * inch) -25
    else:
        rect1_y = (letter[1] - rect_height) / 5.5 + i * (rect_height + 0.7 * inch) -25

    rect2_y = rect1_y

    # رسم المستطيل الأول
    c.setFillColorRGB(0.9, 0.9, 0.9)  # اللون الرمادي الفاتح
    c.rect(start_x, rect1_y, rect_width, rect_height, fill=1)
    # كتابة "عنوان" فوق المستطيل الأول بحجم خط 22
    c.setFont("Arial-Regular", 17)  # حجم الخط للعنوان فوق المستطيل
    c.setFillColorRGB(0, 0, 0)  # اللون الأسود
    c.drawString(start_x + offset_x1, rect1_y + rect_height - 35, title_above_rect1_reshaped)

    # رسم المستطيل الثاني
    rect2_x = start_x + rect_width + gap
    c.setFillColorRGB(0.9, 0.9, 0.9)  # اللون الرمادي الفاتح
    c.rect(rect2_x, rect2_y, rect_width, rect_height, fill=1)
    # كتابة "عنوان 2" فوق المستطيل الثاني بحجم خط 22
    c.setFont("Arial-Regular", 17)  # حجم الخط للعنوان فوق المستطيل
    c.setFillColorRGB(0, 0, 0)  # اللون الأسود
    c.drawString(rect2_x + offset_x2, rect2_y + rect_height - 35, title_above_rect2_reshaped)

    # تعديل موضع النص "محمد" و "عمرو"
    text_y = rect1_y + (rect_height - text_height) / 2 + 14  # زيادة 10 لتحريكه لأسفل قليلاً
    c.setFont("Arial-Regular", text_font_size)  # حجم الخط للنص
    c.setFillColorRGB(0, 0, 0)  # اللون الأسود
    c.drawString(start_x + (rect_width - text1_width) / 2, text_y, text1_reshaped)
    c.drawString(rect2_x + (rect_width - text2_width) / 2, text_y, text2_reshaped)



def draw_three_sq (i,a,b,c,*args):
    text1 = b[2]
    text1_reshaped = get_display(reshape(text1))
    text2 = b[0]
    text2_reshaped = get_display(reshape(text2))
    text3 = b[1]
    text3_reshaped = get_display(reshape(text3))

    text_font_size = 16
    text1_width = pdfmetrics.stringWidth(text1_reshaped, "Arial-Regular", text_font_size)
    text2_width = pdfmetrics.stringWidth(text2_reshaped, "Arial-Regular", text_font_size)
    text3_width = pdfmetrics.stringWidth(text3_reshaped, "Arial-Regular", text_font_size)
    text_height = pdfmetrics.getAscent("Arial-Regular", text_font_size) - pdfmetrics.getDescent("Arial-Regular", text_font_size)

    # تعيين عرض كل مستطيل (25% من عرض الصفحة)
    rect_width = letter[0] * 0.25
    rect_height = text_height + 10  # إضافة بعض الحشو حول النص

    # حساب المواضع للمستطيلات
    gap = 20  # الفجوة بين المستطيلات
    total_width = rect_width * 3 + gap * 2  # العرض الكلي للمستطيلات والفجوتين
    start_x = (letter[0] - total_width) / 2  # نقطة البداية للمستطيل الأول

    if args:
        rect_y = (letter[1] - rect_height) / 5.5 + i * (rect_height + 0.7 * inch)-90
    else:
        rect_y = (letter[1] - rect_height) / 5.5 + i * (rect_height + 0.7 * inch)-25

    # رسم المستطيل الأول
    rect1_x = start_x
    c.setFillColorRGB(0.9, 0.9, 0.9)  # اللون الرمادي الفاتح
    c.rect(rect1_x, rect_y, rect_width, rect_height, fill=1)

    # كتابة "الجنسية" فوق المستطيل الأول بحجم خط 22
    title_above_rect1 = a[2]
    title_above_rect1_reshaped = get_display(reshape(title_above_rect1))
    title1_width = pdfmetrics.stringWidth(title_above_rect1_reshaped, "Arial-Regular", 17)
    offset_x1 = (rect_width - title1_width) / 1  # المسافة نحو اليمين ديناميكية
    c.setFont("Arial-Regular", 17)  # حجم الخط للعنوان فوق المستطيل
    c.setFillColorRGB(0, 0, 0)  # اللون الأسود
    c.drawString(rect1_x + offset_x1, rect_y + rect_height - 35, title_above_rect1_reshaped)

    # رسم المستطيل الثاني
    rect2_x = start_x + rect_width + gap
    c.setFillColorRGB(0.9, 0.9, 0.9)  # اللون الرمادي الفاتح
    c.rect(rect2_x, rect_y, rect_width, rect_height, fill=1)

    # كتابة "المرحلة الدراسية" فوق المستطيل الثاني بحجم خط 22
    title_above_rect2 = a[1]
    title_above_rect2_reshaped = get_display(reshape(title_above_rect2))
    title2_width = pdfmetrics.stringWidth(title_above_rect2_reshaped, "Arial-Regular", 17)
    offset_x2 = (rect_width - title2_width) / 1  # المسافة نحو اليمين ديناميكية
    c.setFont("Arial-Regular", 17)  # حجم الخط للعنوان فوق المستطيل
    c.setFillColorRGB(0, 0, 0)  # اللون الأسود
    c.drawString(rect2_x + offset_x2, rect_y + rect_height - 35, title_above_rect2_reshaped)

    # رسم المستطيل الثالث
    rect3_x = rect2_x + rect_width + gap
    c.setFillColorRGB(0.9, 0.9, 0.9)  # اللون الرمادي الفاتح
    c.rect(rect3_x, rect_y, rect_width, rect_height, fill=1)

    # كتابة "هل سبق له الدراسة" فوق المستطيل الثالث بحجم خط 22
    title_above_rect3 = a[0]
    title_above_rect3_reshaped = get_display(reshape(title_above_rect3))
    title3_width = pdfmetrics.stringWidth(title_above_rect3_reshaped, "Arial-Regular", 17)
    offset_x3 = (rect_width - title3_width) / 1  # المسافة نحو اليمين ديناميكية
    c.setFont("Arial-Regular", 17)  # حجم الخط للعنوان فوق المستطيل
    c.setFillColorRGB(0, 0, 0)  # اللون الأسود
    c.drawString(rect3_x + offset_x3, rect_y + rect_height - 35, title_above_rect3_reshaped)

    text_y = rect_y + (rect_height - text_height) / 2 + 14  # زيادة 10 لتحريكه لأسفل قليلاً
    c.setFont("Arial-Regular", text_font_size)  # حجم الخط للنصوص
    c.setFillColorRGB(0, 0, 0)  # اللون الأسود
    c.drawString(rect1_x + (rect_width - text1_width) / 2, text_y, text1_reshaped)
    c.drawString(rect2_x + (rect_width - text2_width) / 2, text_y, text2_reshaped)
    c.drawString(rect3_x + (rect_width - text3_width) / 2, text_y, text3_reshaped)









def generate_pdf(l,v,*args, **kwargs):
    # تهيئة المخزن المؤقت و القماش
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    pdfmetrics.registerFont(TTFont('Arial-Bold', 'static/fonts/Arial-Bold.ttf'))
    pdfmetrics.registerFont(TTFont('Arial-Regular', 'static/fonts/Arial-Regular.ttf'))

    title = "بيانات الطالب"
    title_reshaped = get_display(reshape(title))
    title_font_size = 23
    title_width = pdfmetrics.stringWidth(title_reshaped, "Arial-Bold", title_font_size)

    # رسم العنوان في المنتصف
    title_x = (letter[0] - title_width) / 2
    title_y = .6 * inch  # ارتفاع العنوان مع التخفيض
    c.setFont("Arial-Bold", title_font_size)
    c.setFillColorRGB(0, 0, 0)  # اللون الأسود
    c.drawString(title_x, title_y, title_reshaped)

    # رسم خط تحت العنوان
    line_y = title_y + 15  # ارتفاع الخط تحت العنوان
    c.setStrokeColorRGB(0, 0, 0)  # اللون الأسود للخط
    c.line(title_x, line_y, title_x + title_width, line_y)  # خط تحت العنوان

    c.setStrokeColorRGB(117, 117, 117)  # اللون الرمادي

    # حساب الأبعاد للمستطيلات بناءً على النص "محمد"
    for i,a,b, in zip([z for z in range(100)],l,v):
        if len(a) == 3 and len(b) == 3:
            draw_three_sq(i,a,b,c)
        elif len(a) == 2 and len(b) == 2 :
            draw_tow_sq(i,a,b,c)
        elif len(a) == 1 and len(b) == 1 :
            draw_one_sq(i,a,b,c)
        
    if args:
        c.showPage()
        c.setStrokeColorRGB(117, 117, 117) 
        for i,a,b, in zip([z for z in range(100)],args[0],args[1]):
            if len(a) == 3 and len(b) == 3:
                draw_three_sq(i,a,b,c,'more')
            elif len(a) == 2 and len(b) == 2 :
                draw_tow_sq(i,a,b,c,'more')
            elif len(a) == 1 and len(b) == 1 :
                draw_one_sq(i,a,b,c)


    c.showPage()
    c.save()

    buf.seek(0)
    # return buf
    response = HttpResponse(buf, content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report.svg"'
    return response



def send_email_with_pdf(column_1_lable,column_2_lable,column_1_value,column_2_value,three_val,email):
    subject = "PDF Attachment"
    body = "Please find the PDF attached."
    from_email = 'sistar32.m@gmail.com'

    pdf_buffer = generate_pdf(column_1_lable,column_2_lable,column_1_value,column_2_value,three_val)
    email = EmailMessage(subject, body, from_email, ['mohamed.403.sameh@gmail.com'])
    email.attach('hello.pdf', pdf_buffer.getvalue(), 'application/pdf')

    try:
        email.send()
        return HttpResponse("Email sent successfully")
    except Exception as e:
        return HttpResponse(f"Failed to send email: {str(e)}")













def registration_in_school (request):
    if request.method == 'POST':
        stud_name=request.POST['student_name']
        id_number=request.POST['id_number']
        mother_name=request.POST['mother_name']
        place_birth=request.POST['place_birth']
        date_of_birth=request.POST['date_of_birth']
        nationality=request.POST['nationality']
        gender=request.POST['gender']
        parentstudent_relations=request.POST['parentstudent_relations']
        guardian_name=request.POST['guardian_name']
        health_status=request.POST['health_status']
        father_edu_lvl=request.POST['father_edu_lvl']
        mother_edu_lvl=request.POST['mother_edu_lvl']
        father_job=request.POST['father_job']
        mothre_job=request.POST['mothre_job']
        number_family=request.POST['number_family']
        Stud_ranking=request.POST['Stud_ranking']
        family_income=request.POST['family_income']
        guardian_phone=request.POST['guardian_phone']
        living=request.POST['living']
        relief_card_page=request.POST['relief_card_page']
        mother_phone=request.POST['mother_phone']
        father_phone=request.POST['father_phone']
        #transport
        would_subscribe=request.POST['would_subscribe']
        transport_type=request.POST['transport_type']
        residence_area=request.POST['residence_area']
        stret_name=request.POST['stret_name']
        #stud_informition
        who_student_attend=request.POST['who_student_attend']
        Who_accompany_student=request.POST['Who_accompany_student']
        Who_student_live_with=request.POST['Who_student_live_with']
        student_have_talent=request.POST['student_have_talent']
        can_child_use_bathroom=request.POST['can_child_use_bathroom']
        child_suffer_food_medicine=request.POST['child_suffer_food_medicine']
        son_suffer_diseases=request.POST['son_suffer_diseases']
        emergency_number=request.POST['emergency_number']
        nearest_address=request.POST['nearest_address']
        There_special_circumstances=request.POST['There_special_circumstances']
        other_comments=request.POST['other_comments']


        

        lables=[
            ['اسم الطالب' ,'الرقم الوطني'],
            ['اسم الأم' ,'مكان الميلاد'],
            ['تاريخ الميلاد' ,'الجنسية'],
            ['الجنس' ,'الوضع الصحي للطالب','علاقة ولي الامر بالطالب'],
            ['عدد افراد الأسرة(مع الوالدين)' ,'ترتيب الطالب بين اخوته','دخل الأسرة الشهري'],
            ['المستوى التعليمي للأب' ,'المستوى التعليمي للأم'],
            ['عمل الأب' ,'عمل الأم'],
            ['هاتف الأب' ,'هاتف الأم'],
            ['اسم ولي الامر' ,'هاتف ولي الأمر'],
            ['اسم ولي الامر' ,'هاتف ولي الأمر'],
            ]
        lables_2=[
            ['مكان السكن' ,'صفحة بطاقة الغوث'],
            ['هل ترغب بالاشتراك في النقل؟' ,'صفة النقل'],
            ['منطقة السكن' ,'اسم الشارع'],
            ['من سيحضر الطالب؟' ,'من سيصحب الطالب؟','مع من يعيش الطالب؟'],
            ['هل يعاني طفلك من حساسية تجاه غذاء او دواء معين؟'],
            ['هل يعاني ابنك من امراض معينة؟'],
            ['رقم الطوارئ , مع ذكر درجة القرابة'],
            ['اقرب عنوان في حال حدوث اي طارئ'],
            ['هل يوجد اي ضروف خاصة تتعلق بطفلك يجب مراعتها بالروضة؟'],
            ['ملاحظات اخرى تحب اطلاعنا عليها'],
            ]
        

        values=[
            [stud_name ,id_number],
            [mother_name ,place_birth],
            [date_of_birth ,nationality],
            [health_status ,gender,parentstudent_relations],
            [number_family ,Stud_ranking,family_income],
            [mother_edu_lvl ,father_edu_lvl],
            [father_job ,mothre_job],
            [father_phone ,mother_phone],
            [guardian_phone ,guardian_name],

            ]
        values_2=[
            [living ,relief_card_page],
            [would_subscribe ,transport_type],
            [residence_area ,stret_name],
            [who_student_attend ,Who_accompany_student,Who_student_live_with],
            [child_suffer_food_medicine],
            [son_suffer_diseases],
            [emergency_number],
            [nearest_address],
            [There_special_circumstances],
            [other_comments],
            ]
        return generate_pdf(lables,values,lables_2,values_2)
    # return send_email_with_pdf(column_1_lable,column_2_lable,column_1_value,column_2_value,three_val,email)
    return render(request,'forms/registration_in_school.html')






