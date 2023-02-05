# -*- coding: utf-8 -*-
from django import forms
from django.urls import patterns, re_path, include
from django.urls import reverse
from django.views.generic import TemplateView
from django.views.generic.edit import BaseFormView

from djangojs.views import JasmineView, QUnitView


def unnamed(request, **kwargs):
    return None


class TestForm(forms.Form):
    message = forms.CharField()


class TestFormView(BaseFormView):
    form_class = TestForm

    def get_success_url(self):
        return reverse('opt')


class DjangoJsTestView(JasmineView):
    template_name = 'djangojs/test/djangojs-test-runner.html'
    js_files = 'js/test/django.specs.js'
    django_js = True

    def get_context_data(self, **kwargs):
        context = super(DjangoJsTestView, self).get_context_data(**kwargs)
        context['form'] = TestForm()
        return context


class JasmineTestView(JasmineView):
    js_files = 'js/test/jasmine/*Spec.js'


class QUnitTestView(QUnitView):
    template_name = 'djangojs/test/qunit-test-runner.html'
    js_files = 'js/test/qunit/qunit-*.js'


fake_patterns = patterns('',
    re_path(r'^fake$', TestFormView.as_view(), name='fake'),
)

nested_patterns = patterns('',
    re_path(r'^nested/', include(fake_patterns, namespace="nested", app_name="appnested")),
)

other_fake_patterns = patterns('',
    re_path(r'^fake$', TestFormView.as_view(), name='fake'),
)

test_patterns = patterns('',
    re_path(r'^form$', TestFormView.as_view(), name='test_form'),
    re_path(r'^unamed$', 'djangojs.test_urls.unnamed'),
    re_path(r'^unnamed-class$', TestFormView.as_view()),
    re_path(r'^arg/(\d+)$', TemplateView.as_view(template_name='djangojs/test/test1.html'), name='test_arg'),
    re_path(r'^arg/(\d+)/(\w)$', TemplateView.as_view(template_name='djangojs/test/test1.html'), name='test_arg_multi'),
    re_path(r'^named/(?P<test>\w+)$', TemplateView.as_view(template_name='djangojs/test/test1.html'), name='test_named'),
    re_path(r'^named/(?P<str>\w+)/(?P<num>\d+)$',
        TemplateView.as_view(template_name='djangojs/test/test1.html'),
        name='test_named_multi'),
    re_path(r'^named/(?P<test>\d+(?:,\d+)*)$',
        TemplateView.as_view(template_name='djangojs/test/test1.html'),
        name='test_named_nested'),
    re_path(r'^optionnals?$', TemplateView.as_view(template_name='djangojs/test/test1.html'), name="opt"),
    re_path(r'^optionnal/?$', TemplateView.as_view(template_name='djangojs/test/test1.html'), name="opt-trailing-slash"),
    re_path(r'^many?/optionnals?$', TemplateView.as_view(template_name='djangojs/test/test1.html'), name="opt_multi"),
    re_path(r'^optionnal/(?:capturing)?group$',
        TemplateView.as_view(template_name='djangojs/test/test1.html'),
        name="opt_grp"),
    re_path(r'^first/$', TemplateView.as_view(template_name='djangojs/test/test1.html'), name='twice'),
    re_path(r'^last/$', TemplateView.as_view(template_name='djangojs/test/test1.html'), name='twice'),
    re_path(r'^namespace1/', include(fake_patterns, namespace="ns1", app_name="app1")),
    re_path(r'^namespace2/', include(nested_patterns, namespace="ns2", app_name="app2")),
    re_path(r'^namespace3/', include(fake_patterns, namespace="ns3")),
    re_path(r'^test\.json$', TestFormView.as_view(), name='escaped'),
)

urlpatterns = patterns('',
    re_path(r'^$', DjangoJsTestView.as_view(), name='djangojs_tests'),

    re_path(r'^djangojs/', include('djangojs.urls')),

    re_path(r'^jasmine/$', JasmineTestView.as_view(), name='djangojs_jasmine_tests'),
    re_path(r'^qunit/$', QUnitTestView.as_view(), name='djangojs_qunit_tests'),

    re_path(r'^test/', include(test_patterns)),
)
