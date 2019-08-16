"""
A collection of jinja2 templates of xml as python variables
    XML markups with basic tags for feed entries/items
        atom_entry
        rss_entry
"""


atom_entry = """
<entry>
    <id>
        {{entry.id}}
    </id>

    <title>
        {{entry.title}}
    </title>

    <summary>
        {{entry.content}}
    </summary>

    <link href='{{entry.link}}' rel='alternate'>

    <updated>
        {{entry.updated}}
    </updated>

</entry>"""

rss_entry = """
<item>
    <title>
        {{entry.title}}
    </title>

    <description>
        {{entry.content}}
    </description>

    <link>
    {{entry.link}}
    </link>

    <guid isPermaLink="false">
        {{entry.id}}
    </guid>

    <lastBuildDate>
        {{entry.updated}}
    </lastBuildDate>
</item>"""
