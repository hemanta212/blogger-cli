from pathlib import Path
import jinja2
from bs4 import BeautifulSoup as BS
from blogger_cli.commands.feed_utils.feed_template import atom_entry, rss_entry


class FeedProcessor:
    def __init__(self, xml_file):
        self.xml_file = Path(xml_file)
        self.xml_soup = self.__xml_soup()
        self.feed_type = self.__feed_type()

    def __xml_soup(self):
        xml_data = self.xml_file.read_text(encoding="utf-8")
        soup = BS(xml_data, features="xml")
        return soup

    def __feed_type(self):
        soup = self.xml_soup
        rss = soup.find("rss")
        atom = soup.find("feed")
        if rss:
            return "rss"
        elif atom:
            return "atom"

        raise ValueError("Invalid feed file. Cannot determine if 'rss' or 'atom'")

    def add_entry(self, entry):
        # Check for duplicates and remove
        duplicate = self.get_feed_entry(entry["link"])
        if duplicate:
            # id should never change.
            entry_id = self.__get_entry_id(duplicate)
            if entry_id:
                entry["id"] = entry_id
            # delete previous entry for new updated entry
            duplicate.decompose()

        # Prepare entry to add to feed
        entry_template = rss_entry if self.feed_type == "rss" else atom_entry
        xml_entry_string = jinja2.Template(entry_template).render(entry=entry)

        # Convert xml string to bs4 xml element to append it.
        feed_entry = self.__gen_xml_entry(xml_entry_string)
        entries_holder = self.__get_entries_holder()

        # Add feed entry
        entries_holder.append(feed_entry)
        return self.xml_soup

    def __get_entry_id(self, entry):
        entry_id = None
        if self.feed_type == "rss":
            entry_id = entry.find("guid", attrs={"isPermaLink": "false"}).text
        else:
            entry_id = entry.find("id").text
        return entry_id

    def remove_entry(self, entry):
        """ Remove a bs4 element from the soup and write soup to file """
        entry.decompose()
        self.write_to_file()

    def __gen_xml_entry(self, entry):
        """ Genereates a beautifulsoup elemtent from a string"""
        entry_soup = BS(entry, features="xml")
        if self.feed_type == "rss":
            entry_tag = entry_soup.find("item")
        else:
            entry_tag = entry_soup.find("entry")
        return entry_tag

    def __get_entries_holder(self):
        if self.feed_type == "rss":
            entries_holder = self.xml_soup.find("channel")
        else:
            entries_holder = self.xml_soup.find("feed")
        return entries_holder

    def get_feed_entry(self, link):
        """'
        Returns a beautifulsoup element of matching xml entry
        Params
            link: A link of the entry [url] (link with rel=alternate for atom)
        """
        link_tags = self.xml_soup.find_all("link")
        if self.feed_type == "rss":
            link_tag = [i for i in link_tags if i.text.strip() == link]
            if link_tag:
                return link_tag[0].parent

        else:
            alt_links = []
            for tag in link_tags:
                if tag.get("rel") and tag["rel"].strip() == "alternate":
                    alt_links.append(tag)

            # Retrun None if no alt_links are there
            if not alt_links:
                return None

            for tag in alt_links:
                if tag.get("href") and tag["href"].strip() == link:
                    return tag.parent

    def write_to_file(self, xml, xml_file=None):
        if not xml_file:
            xml_file = self.xml_file
        xml_file = Path(xml_file)
        data = xml.prettify()
        xml_file.write_text(data, encoding="utf-8")
