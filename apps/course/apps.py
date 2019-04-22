from django.apps import AppConfig


class CourseConfig(AppConfig):
    name = 'course'
    verbose_name = "课程管理"

    def ready(self):
        import course.signals
