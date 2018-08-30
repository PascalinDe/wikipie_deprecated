#    This file is part of WikiPie 0.x.
#    Copyright (C) 2017  Carine Dengler, Heidelberg University (DBS)
#
#    WikiPie 0.x is free software: you can redistribute it and/or modify
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
.. _`Version`: https://en.wikipedia.org/wiki/Special:Version
.. _`List of Wikipedias`: https://meta.wikimedia.org/wiki/List_of_Wikipedias
.. _`Help:Interwiki linking`: \
https://en.wikipedia.org/wiki/Help:Interwiki_linking
.. _`Wikipedia:Namespace`: \
https://en.wikipedia.org/wiki/Wikipedia:Namespace
.. _`Help:Magic words`: https://www.mediawiki.org/wiki/Help:Magic_words
.. _`Help:Templates`: \
https://www.mediawiki.org/wiki/Special:MyLanguage/Help:template#Usage
.. _`Manual:Magic words`: \
https://www.mediawiki.org/wiki/Special:MyLanguage/Manual:Magic_words
.. _`Help:Extension:ParserFunctions`: \
https://www.mediawiki.org/wiki/Special:MyLanguage/Help:Extension:ParserFunctions

:synopsis: Data module, holds MediaWiki software information.

See `List of Wikipedias`_, `Help:Interwiki linking`_,
`Wikipedia:Namespace`_, `Help:Magic words`_,
`Help:Templates`_, `Manual:Magic words`_ and `Help:Extension:ParserFunctions`_
for further information.
"""


# standard library imports
# third party imports
# library specific imports


# case sensitive OR case insensitive
PARSER_EXTENSIONS = [
    "categorytree", "ce", "charinsert", "chem", "gallery", "graph",
    "hiero", "imagemap", "indicator", "inputbox", "maplink", "math",
    "poem", "pre", "ref", "references", "score", "section", "source",
    "syntaxhighlight", "templatedata", "timeline"
]

#: 1 000 000+ articles
#: Statistics at 00:00, 19 September 2017 (UTC)
LANGUAGE_CODES = [
    "en", "ceb", "sv", "de", "nl", "fr", "ru", "it", "es", "war"
]

# case insensitive
PROJECTS = [
    "wikipedia", "wiktionary", "wikinews", "wikibooks", "wikiquote",
    "wikisource", "oldwikisource", "wikispecies", "wikiversity",
    "wikivoyage", "wikimedia", "foundation", "commons", "metawikipedia",
    "meta", "incubator", "strategy", "mediawikiwiki", "mediazilla",
    "bugzilla", "phabricator", "testwiki", "wikidata", "wikitech",
    "toollabs", "w", "wikt", "n", "b", "q", "s", "species", "v", "voy",
    "wmf", "c", "m", "mw", "phab", "d"
]

# case insensitive
NAMESPACES = {
    "0": [""],
    "2": ["User"],
    "4": ["Wikipedia", "WP", "Project"],
    "6": ["File", "Image"],
    "8": ["MediaWiki"],
    "10": ["Template"],
    "12": ["Help"],
    "14": ["Category"],
    "100": ["Portal"],
    "108": ["Book"],
    "118": ["Draft"],
    "446": ["Education Program"],
    "710": ["TimedText"],
    "828": ["Module"],
    "2300": ["Gadget"],
    "2302": ["Gadget definition"],
    "-1": ["Special"],
    "-2": ["Media"]
}

# case sensitive OR case insensitive
MODIFIERS = [
    "int", "msg", "raw", "msgnw", "subst", "safesubst"
]

# case sensitive OR case insensitive
BEHAVIOR_SWITCHES = [
    "__NOTOC__", "__FORCETOC__", "__TOC__", "__NOEDITSECTION__",
    "__NEWSECTIONLINK__", "__NONEWSECTIONLINK__", "__NOGALLERY__",
    "__HIDDENCAT__", "__NOCONTENTCONVERT__", "__NOCC__",
    "__NOTITLECONVERT__", "__NOTC__", "__START__", "__END__",
    "__INDEX__", "__NOINDEX__", "__STATICREDIRECT__", "__NOGLOBAL__"
]

# case sensitive OR case insensitive
VARIABLES = [
    "CURRENTYEAR", "CURRENTMONTH", "CURRENTMONTH1", "CURRENTMONTHNAME",
    "CURRENTMONTHNAMEGEN", "CURRENTMONTHABBREV", "CURRENTDAY",
    "CURRENTDAY2", "CURRENTDOW", "CURRENTDAYNAME", "CURRENTTIME",
    "CURRENTHOUR", "CURRENTWEEK", "CURRENTTIMESTAMP", "LOCALYEAR",
    "LOCALMONTH", "LOCALMONTH1", "LOCALMONTHNAME", "LOCALMONTHNAMEGEN",
    "LOCALMONTHABBREV", "LOCALDAY", "LOCALDAY2", "LOCALDOW", "LOCALDAYNAME",
    "LOCALTIME", "LOCALHOUR", "LOCALWEEK", "LOCALTIMESTAMP", "SITENAME",
    "SERVER", "SERVERNAME", "DIRMARK", "DIRECTIONMARK", "SCRIPTPATH",
    "STYLEPATH", "CURRENTVERSION", "CONTENTLANGUAGE", "CONTENTLANG",
    "PAGEID", "PAGELANGUAGE", "PROTECTIONLEVEL", "PROTECTIONEXPIRY",
    "CASCADINGSOURCES", "REVISIONID", "REVISIONDAY", "REVISIONDAY2",
    "REVISIONMONTH", "REVISIONMONTH1", "REVISIONYEAR", "REVISIONTIMESTAMP",
    "REVISIONUSER", "REVISIONSIZE", "DISPLAYTITLE", "DEFAULTSORT",
    "DEFAULTSORTKEY", "DEFAULTCATEGORYSORT", "NUMBEROFPAGES",
    "NUMBEROFARTICLES", "NUMBEROFFILES", "NUMBEROFEDITS", "NUMBEROFVIEWS",
    "NUMBEROFUSERS", "NUMBEROFADMINS", "NUMBEROFACTIVEUSERS",
    "PAGESINCATEGORY", "PAGESINCAT", "NUMBERINGROUP", "PAGESINNS",
    "PAGESINNAMESPACE", "FULLPAGENAME", "PAGENAME", "BASEPAGENAME",
    "SUBPAGENAME", "SUBJECTPAGENAME", "ARTICLEPAGENAME", "TALKPAGENAME",
    "ROOTPAGENAME", "FULLPAGENAMEE", "PAGENAMEE", "BASEPAGENAMEE",
    "SUBPAGENAMEE", "SUBJECTPAGENAMEE", "ARTICLEPAGENAMEE", "TALKPAGENAMEE",
    "ROOTPAGENAMEE", "NAMESPACE", "NAMESPACENUMBER", "SUBJECTSPACE",
    "ARTICLESPACE", "TALKSPACE", "NAMESPACEE", "SUBJECTSPACEE",
    "ARTICLESPACEE", "TALKSPACEE", "!"
]

# case sensitive OR case insensitive
PARSER_FUNCTIONS = [
    "localurl", "fullurl", "canonicalurl", "filepath", "urlencode",
    "anchorencode", "ns", "nse", "formatnum", "#dateformat", "#formatdate",
    "lc", "lcfirst", "uc", "ucfirst", "padleft", "padright", "plural",
    "grammar", "gender", "int", "#language", "#special", "#speciale",
    "#tag", "#invoke", "#expr", "#if", "#ifeq", "#iferror", "#ifexpr",
    "#ifexist", "#rel2abs", "#switch", "#time", "#timel", "#titleparts"
]
