

def load_admin():
    from django.contrib import admin
    from app.models import Payment

    from app.admin.models.course import CourseAdmin
    from app.admin.models.teachers import TeacherAdmin
    from app.admin.models.categories import CategoryAdmin
    from app.admin.models.payment import PaymentAdmin
    from app.models import Teacher, Course, Category

    admin.site.register(Course, CourseAdmin)
    admin.site.register(Teacher, TeacherAdmin)
    admin.site.register(Category, CategoryAdmin)
    admin.site.register(Payment, PaymentAdmin)