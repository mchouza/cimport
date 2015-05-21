import imp
import os.path
import sys

class CFinderLoader(object):
    def find_module(self, fullname, path):
        filename = '%s.c' % fullname.rsplit('.', 1)[-1]
        if path is None:
            src_path = filename
        else:
            src_path = os.path.join(path[0], filename)
        if os.path.exists(src_path):
            return self
        else:
            return None

    def load_module(self, fullname):
        mod = sys.modules.setdefault(fullname, imp.new_module(fullname))
        mod.__dict__['foo'] = lambda : 'returns %s' % fullname
        return mod

sys.meta_path.append(CFinderLoader())