"""
Navoica API URLs.
"""
from navoica_api.api.v1 import views
from django.conf import settings
from django.conf.urls import include, url

PROGRESS_URLS = [
    url(r'^{username}/courses/{course_id}/$'.format(
        username=settings.USERNAME_PATTERN,
        course_id=settings.COURSE_ID_PATTERN,
        ),
        views.CourseProgressApiView.as_view(),
        name='detail')
]

CERTIFICATES_URLS = [
    url(
        r'^courses/{course_id}/$'.format(
            course_id=settings.COURSE_ID_PATTERN
        ),
        views.CertificatesListView.as_view(), name='list'
    ),
]

urlpatterns = [
    url(r'^progress/', include(PROGRESS_URLS, namespace='progress')),
    url(r'^certificates/', include(CERTIFICATES_URLS, namespace='certificates')),
]
