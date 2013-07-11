from markdown.treeprocessors import Treeprocessor
from markdown.extensions import Extension
from pythontutor import pg_logger
import json


json.encoder.FLOAT_REPR = lambda f: ('%.3f' % f)


def json_finalizer(input_code, output_trace):
    ret = dict(code=input_code, trace=output_trace)
    json_output = json.dumps(ret, indent=4)
    return json_output


class PythonTutorTreeprocessor(Treeprocessor):
    """ Hilight source code in code blocks. """

    def run(self, root):
        """ Find code blocks and store in htmlStash. """
        blocks = root.getiterator('pre')
        for block in blocks:
            children = block.getchildren()
            tutor_code = pg_logger.exec_script_str_local(children[0].text,
                False, False, False, json_finalizer
            )
            block.clear()
            block.text = tutor_code


class PythonTutorExtension(Extension):

    def __init__(self, configs = None):
        if configs is None:
            self.config = {}
        else:
            self.config.update(configs)

    def extendMarkdown(self, md, md_globals):
        """ Add HilitePostprocessor to Markdown instance. """
        tutor = PythonTutorTreeprocessor(md)
        tutor.config = self.getConfigs()
        md.treeprocessors.add("tutor", tutor, "<inline")
        md.registerExtension(self)


def makeExtension(configs={}):
  return PythonTutorExtension(configs=configs)