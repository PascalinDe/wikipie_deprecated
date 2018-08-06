#    This file is part of WikiPie.
#    Copyright (C) 2017  Carine Dengler
#
#    WikiPie is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.


"""
:synopsis: Tests magic words parser elements.
"""


# standard library imports

# third party imports
import pyparsing

# library specific imports
import src.wpdata


_BEHAVIOR_SWITCHES = list(src.wpdata.BEHAVIOR_SWITCHES)
_BEHAVIOR_SWITCHES.sort(key=len, reverse=True)
BEHAVIOR_SWITCH = pyparsing.MatchFirst(
)
