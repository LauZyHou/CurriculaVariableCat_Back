from subject.models import Subject

import xadmin


class SubjectAdmin(object):
    """课程"""
    list_display = ["id", "name", "logic_id", "category"]


xadmin.site.register(Subject, SubjectAdmin)
