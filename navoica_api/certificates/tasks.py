import logging
from functools import partial

from celery import task
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.test.client import RequestFactory
from django.utils.translation import ugettext_noop
from lms.djangoapps.certificates.views import render_cert_by_uuid
from lms.djangoapps.instructor_task.tasks_base import BaseInstructorTask
from lms.djangoapps.instructor_task.tasks_helper.runner import run_main_task

from navoica_api.certificates.functions import render_pdf, merging_all_course_certificates

TASK_LOG = logging.getLogger('edx.celery.task')

@task()
def render_pdf_cert_by_uuid(certificate_uuid):
    factory = RequestFactory()
    fake_request = factory.get("")
    fake_request.user = AnonymousUser()
    fake_request.session = {}

    output = render_cert_by_uuid(fake_request, certificate_uuid)
    render_pdf(html=output.content,certificate_uuid=certificate_uuid)

@task(base=BaseInstructorTask, routing_key=settings.GRADES_DOWNLOAD_ROUTING_KEY)
def merge_all_certificates(entry_id, xmodule_instance_args):
    """
    Grade students and generate certificates.
    """
    # Translators: This is a past-tense verb that is inserted into task progress messages as {action}.
    action_name = ugettext_noop('merge all certificates')
    TASK_LOG.info(
        u"Task: %s, InstructorTask ID: %s, Task type: %s, Preparing for task execution",
        xmodule_instance_args.get('task_id'), entry_id, action_name
    )

    task_fn = partial(merging_all_course_certificates, xmodule_instance_args)
    return run_main_task(entry_id, task_fn, action_name)