# Copyright (c) 2012-2026 Jose Antonio Chavarría <jachavar@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

"""Tests for template tags."""

import pytest
from django.template import Template, Context, TemplateSyntaxError
from django.conf import settings


@pytest.mark.django_db
class TestSettingTemplateTag:
    """Tests for the setting template tag."""

    def test_setting_tag_valid(self):
        """Test that setting tag renders setting value."""
        template = Template('{% load setting %}{% setting DEBUG %}')
        context = Context({})
        result = template.render(context)
        assert result == str(settings.DEBUG)

    def test_setting_tag_static_url(self):
        """Test setting tag with STATIC_URL."""
        template = Template('{% load setting %}{% setting STATIC_URL %}')
        context = Context({})
        result = template.render(context)
        assert result == settings.STATIC_URL

    def test_setting_tag_invalid_setting(self):
        """Test that setting tag returns empty string for invalid setting."""
        template = Template('{% load setting %}{% setting NONEXISTENT_SETTING %}')
        context = Context({})
        result = template.render(context)
        assert result == ''

    def test_setting_tag_no_arguments(self):
        """Test that setting tag raises error without arguments."""
        with pytest.raises(TemplateSyntaxError) as exc_info:
            Template('{% load setting %}{% setting %}')
        assert 'requires a single argument' in str(exc_info.value)

    def test_setting_tag_too_many_arguments(self):
        """Test that setting tag raises error with too many arguments."""
        with pytest.raises(TemplateSyntaxError) as exc_info:
            Template('{% load setting %}{% setting DEBUG OTHER %}')
        assert 'requires a single argument' in str(exc_info.value)
