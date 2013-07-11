#!/usr/bin/env python

import codecs
import jinja2
import markdown
import shutil
import errno
import sys
import glob
import os
import SimpleHTTPServer
import SocketServer
import mdx_tutorize

PORT = 8000
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def process_slides(slides_file):

    with codecs.open(slides_file.replace(".md", ".html"), 'w', encoding='utf8') as outfile:
        slides = []
        layout = os.path.join(BASE_DIR, "theme", "templates", "layout.html")
        md_file = codecs.open(slides_file, encoding='utf8').read()
        md_slides = md_file.split('\n---\n')
        md = markdown.Markdown(extensions=['meta', mdx_tutorize.PythonTutorExtension()])
        # Process each slide separately.
        for section in md_slides:
            slide_md = md.convert(section)
            slide = {
                'content': postprocess_html(slide_md, md.Meta)
            }
            slide.update(md.Meta)
            print md.Meta.get('title')
            slides.append(slide)

        with open(layout) as f:
            template = jinja2.Template(f.read())
            outfile.write(template.render(slides=slides))
        
        print 'Compiled %s slides.' % len(md_slides)

def postprocess_html(html, metadata):
    """Returns processed HTML to fit into the slide template format."""

    html = html.replace('<ul>', '<ul class="build">')
    html = html.replace('<ol>', '<ol class="build">')
    return html

def pack_slides():
    cwd = os.getcwd()
    try:
        shutil.copytree(os.path.join(BASE_DIR, "js"), os.path.join(cwd,"js"))
        shutil.copytree(os.path.join(BASE_DIR, "theme", "css"), os.path.join(cwd, "theme", "css"))
        shutil.copytree(os.path.join(BASE_DIR, "theme", "img"), os.path.join(cwd, "theme", "img"))
    except OSError as exc:
        if exc.errno == errno.EEXIST:
            pass

def main():
    sf = "slides.md"
    if len(sys.argv) == 2:
        sf = sys.argv[1]
    else:
        sf = glob.glob("*.md").pop()
    process_slides(sf)
    pack_slides()


def serve():
    Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
    httpd = SocketServer.TCPServer(("", PORT), Handler)
    httpd.serve_forever()
    print "Serving at port", PORT

if __name__ == '__main__':
    main()
    