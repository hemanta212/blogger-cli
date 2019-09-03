from pathlib import Path
import click
from spellchecker import SpellChecker
from misspellings_lib import Misspellings
from blogger_cli.converter.extractor import (
    extract_text_from_ipynb,
    extract_text_from_html,
)


@click.command("spellcheck", short_help="Check spelling errors")
@click.option("-f", "--force_suggestions", is_flag=True)
@click.argument("filename", type=click.Path(exists=True))
def cli(filename, force_suggestions):
    """
    This command will check spelling and point out the typos.
    """
    spellcheck = SpellChecker()
    checked = run_initial_check(filename)

    if Path(filename).suffix == ".ipynb":
        data = extract_text_from_ipynb(filename)
    elif Path(filename).suffix in (".htm", ".html"):
        data = extract_text_from_html(filename)
    else:
        data = Path(filename).read_text(encoding="utf-8")

    all_words = []
    space_split = (word.strip() for word in data.split(" "))
    for i in space_split:
        split_list = i.split("\n")
        if split_list:
            all_words += split_list
        else:
            all_words.append(i)

    all_words = (i for i in all_words if i)

    for word in all_words:
        if word in checked:
            continue
        try:
            unknown = spellcheck.unknown([word])
            if unknown and unknown != {""}:
                line_no = get_line(filename, word)
                checked.append(word)
                if force_suggestions:
                    suggestion = spellcheck.correction(word)
                    click.echo(
                        "At line: " + line_no + " | " + word + " | " + suggestion
                    )
                else:
                    click.echo("At line: " + line_no + " | " + word)

        except Exception as E:
            click.echo(str(E))
            click.echo("Skipping word " + word)


def get_line(filename, word):
    with open(filename, "r", encoding="utf-8") as rf:
        lines = rf.readlines()

    line_no = tuple()
    for index, line in enumerate(lines):
        line_words = (word.strip() for word in line.split(" "))
        all_words = []
        for i in line_words:
            split_list = i.split("\n")
            if split_list:
                all_words += split_list
            else:
                all_words.append(i)

        if word in all_words:
            line_no += (index + 1,)

    return str(line_no)


def run_initial_check(filename):
    checked = []
    misspelling = Misspellings(files=[filename])
    errors = misspelling.check()[1]
    if not errors:
        return checked
    for error in errors:
        unknown = error[2]
        if unknown in checked:
            continue
        checked.append(unknown)
        line = get_line(filename, unknown)
        suggestion = misspelling.suggestions(unknown)[0]
        click.echo("At line: " + line + " | " + unknown + " | " + suggestion)
    return checked
