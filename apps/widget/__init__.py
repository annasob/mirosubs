# Universal Subtitles, universalsubtitles.org
# 
# Copyright (C) 2010 Participatory Culture Foundation
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see 
# http://www.gnu.org/licenses/agpl-3.0.html.

from uuid import uuid4
from videos import models as video_models
from django.conf import settings
from django.conf.global_settings import LANGUAGES
from django.contrib.sites.models import Site
import simplejson as json

LANGUAGES_MAP = dict(LANGUAGES)

def full_path(js_file):
    return "{0}js/{1}".format(settings.MEDIA_URL, js_file)

def add_offsite_js_files(context):
    """ Adds variables necessary for _js_dependencies.html """
    return add_js_files(context, settings.JS_USE_COMPILED, 
                        settings.JS_OFFSITE, 
                        'mirosubs-offsite-compiled.js')

def add_onsite_js_files(context):
    """ Adds variables necessary for _js_onsite_dependencies.html """
    return add_js_files(context, settings.JS_USE_COMPILED, 
                        settings.JS_ONSITE, 
                        'mirosubs-onsite-compiled.js')

def add_widgetize_js_files(context):
    js_files = []
    js_files.append('http://{0}/widget/widgetizerconfig.js'.format(
            Site.objects.get_current().domain))
    js_files.append('{0}js/widgetizer/widgetizer.js'.format(settings.MEDIA_URL))
    return add_js_files(context, settings.JS_USE_COMPILED,
                        settings.JS_OFFSITE, 
                        'mirosubs-widgetizer.js',
                        full_path_js_files=js_files)

def add_js_files(context, use_compiled, js_files, compiled_file_name=None, full_path_js_files=[]):
    context["js_use_compiled"] = use_compiled
    if use_compiled:
        # might change in future when using cdn to serve static js
        context["js_dependencies"] = [full_path(compiled_file_name)]
    else:
        context["js_dependencies"] = [full_path(js_file) for js_file in js_files] + full_path_js_files
    context["site"] = Site.objects.get_current()
    return context;    

def language_to_map(code, name):
    return { 'code': code, 'name': name };
