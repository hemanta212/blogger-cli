import os
import shutil
from pathlib import Path
from bs4 import BeautifulSoup as BS

HOME = os.path.expanduser("~")


def get_docs():
    tmp = os.path.join(HOME, "tmp1234")
    os.mkdir(tmp)
    docs_path = os.path.join(tmp, "docs")
    readme = os.path.join(tmp, "README.md")
    licence = os.path.join(tmp, "LICENSE")
    get_blogger = os.path.join(tmp, "get_blogger.py")
    os.system("git clone https://github.com/hemanta212/blogger-cli " + tmp)
    shutil.copytree(docs_path, "tmp_docs")
    os.system("cp " + readme + " " + get_blogger + " " + licence + " tmp_docs/")
    shutil.rmtree(tmp)


def configure_and_convert():
    os.system("blogger rmblog blogger_cli")
    os.system("blogger addblog blogger_cli -s")
    os.system("blogger setdefault blogger_cli")
    os.system("blogger config -re blogger_cli.json")
    os.system("blogger convert tmp_docs/* --topic docs -no-ex")
    os.system("blogger convert tmp_docs/README.md -no-ex")
    os.system("cp tmp_docs/*.py tmp_docs/LICENSE .")
    os.system("mv README.html index.html")


def do_post_processing():
    os.system("rm -rf tmp_docs/")
    os.system("rm docs/*.md")
    os.system("rm docs/README.html")
    os.system("rm docs/index.html")

    readme = Path("index.html")
    readme_text = readme.read_text(encoding="utf-8")

    # Add total downloads badge from pepy.tech to index.html(readme)
    readme_soup = BS(readme_text, features="html.parser")
    badge_container = readme_soup.find("div", id="content").find("p")
    downloads_badge = """
<a href="https://pepy.tech/project/blogger-cli">
    <img alt="total downloads" src="https://pepy.tech/badge/blogger-cli"/>
</a>
"""
    new_badge_tag = BS(downloads_badge, features="html.parser").find("a")
    badge_container.insert(0, new_badge_tag)
    readme_text = readme_soup.prettify(formatter="html")

    modified_text = readme_text.replace(".md", ".html")
    readme.write_text(modified_text, encoding="utf-8")

    os.chdir("docs")
    for i in os.listdir():
        file = Path(i)
        soup = BS(file.read_text(encoding="utf-8"), features="html.parser")
        a_tags = soup.find_all("a")
        for a_tag in a_tags:
            a_tag_href = a_tag.attrs.get("href")
            if a_tag_href and ".md" in a_tag_href:
                new_href = a_tag_href.replace(".md", ".html")
                a_tag["href"] = new_href

        file.write_text(soup.prettify(formatter="html"), encoding="utf-8")

    print("DONE")


if __name__ == "__main__":
    get_docs()
    configure_and_convert()
    do_post_processing()
