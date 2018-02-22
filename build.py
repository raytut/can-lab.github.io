#!/usr/bin/env python

import os
import fnmatch
import codecs
import glob

from jinja2 import Environment, FileSystemLoader
from bs4 import BeautifulSoup


def _render_template(template_filename, context):
    TEMPLATE_ENVIRONMENT = Environment(autoescape=False,
                                       loader=FileSystemLoader('source'),
                                       trim_blocks=False)

    return TEMPLATE_ENVIRONMENT.get_template(template_filename).render(context)

def delete_html_files():
    files = glob.glob("*.html")
    for file_ in files:
        os.remove(file_)

def create_html_files():
    members = []
    files = []
    for root, dirnames, filenames in os.walk('source'):
            for filename in fnmatch.filter(filenames, '*.html'):
                        files.append(os.path.join(root, filename))
                        if "lab_members" in root:
                            with codecs.open(os.path.join(root, filename), 'r', "utf-8") as f:
                                source_code = f.read()
                            soup = BeautifulSoup(source_code)
                            members.append({"name": soup.h1.text,
                                            "function": soup.p.text,
                                            "url": "_".join(soup.h1.text.lower().split()) + ".html",
                                            "image": soup.span.img['src']})

    # Sort first by length of function (PI < Postdoc < PhD student < Master student), then by LAST name
    members.sort(key=lambda x: (len(x["function"]), x["name"].split(" ")[-1]))
    context = {
            'members': members
        }
    for file_ in files:
        file_ = file_.replace("source" + os.path.sep, "")
        if file_ == "base.html":
            continue
        with codecs.open(os.path.split(file_)[1], 'w', encoding='utf-8') as f:
            print file_
            html = _render_template(file_, context)
            f.write(html)

def main():
    delete_html_files()
    create_html_files()

if __name__ == "__main__":
    main()
