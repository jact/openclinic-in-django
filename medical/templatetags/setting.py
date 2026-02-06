# Copyright (c) 2012-2022 Jose Antonio Chavarría <jachavar@gmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from django import template
from django.conf import settings

register = template.Library()


@register.tag
def setting(parser, token):
    try:
        _, option = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            f"{token.contents[0]} tag requires a single argument"
        )

    return SettingNode(option)


class SettingNode(template.Node):
    def __init__(self, option):
        self.option = option

    def render(self, context):
        # if FAILURE then FAIL silently
        try:
            return str(settings.__getattr__(self.option))
        except AttributeError:
            return ""
