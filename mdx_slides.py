from markdown.treeprocessors import Treeprocessor
from markdown.extensions import Extension
import json


json.encoder.FLOAT_REPR = lambda f: ('%.3f' % f)


class SlidesTreeprocessor(Treeprocessor):
    """ Hilight source code in code blocks. """

    def run(self, root):
        """ Find code blocks and store in htmlStash. """
        blocks = root.getiterator('pre')
        for block in blocks:
            #TODO guess language and append class="prettyprint" data-lang="css"
            pass

            
class SlidesExtension(Extension):

    def __init__(self, configs = None):
        if configs is None:
            self.config = {}
        else:
            self.config.update(configs)

    def extendMarkdown(self, md, md_globals):
        """ Add HilitePostprocessor to Markdown instance. """
        slides = SlidesTreeprocessor(md)
        slides.config = self.getConfigs()
        md.treeprocessors.add("slides", slides, "<inline")
        md.registerExtension(self)


def makeExtension(configs={}):
  return SlidesExtension(configs=configs)