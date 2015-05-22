import ctypes
import imp
import os
import os.path
import pycparser
import subprocess
import sys


def _get_imp_funcs(c_fpath):
    """Gets the functions that can be imported from a C file."""

    # gets the path of the fake system headers
    fsh_path = os.path.join(__path__[0], 'fake_libc_include')

    # TODO: USE THE cpp.py MODULE TO PREPROCESS THE FILE

    # gets the AST
    ast = pycparser.parse_file(c_fpath, use_cpp=c_fpath, cpp_args=['-I', fsh_path])
    
    # function definition info collector class
    class FuncDefVisitor(pycparser.c_ast.NodeVisitor):
        def __init__(self):
            pycparser.c_ast.NodeVisitor.__init__(self)
            self.func_names = []
        def visit_FuncDef(self, node):
            self.func_names.append(node.decl.name)

    # gets the function definition info
    v = FuncDefVisitor()
    v.visit(ast)

    # returns the function definition info
    return v.func_names


def _get_ctypes_cdll(src_path):
    """Gets the CDLL object associated with a given source file."""

    directory, filename = os.path.split(src_path)
    #obj_path = os.path.join(directory, '._cimport_.%s.so' % filename)
    obj_path = os.path.join(directory, '_cimport_.%s.so' % filename)
    # FIXME: AVOID ALWAYS COMPILING
    subprocess.check_output(['gcc', '-shared', '-fPIC', src_path, '-o', obj_path])
    return ctypes.CDLL(obj_path)


class CFinderLoader(object):
    def __init__(self, src_path):
        self.src_path = src_path

    @classmethod
    def find_module(cls, fullname, path):
        filename = '%s.c' % fullname.rsplit('.', 1)[-1]
        if path is None:
            src_path = os.path.join(os.getcwd(), filename)
        else:
            src_path = os.path.join(path[0], filename)
        if os.path.exists(src_path):
            return cls(src_path)
        else:
            return None

    def load_module(self, fullname):
        mod = sys.modules.setdefault(fullname, imp.new_module(fullname))
        list_of_funcs = _get_imp_funcs(self.src_path)
        cdll = _get_ctypes_cdll(self.src_path)
        for fn in list_of_funcs:
            mod.__dict__[fn] = cdll[fn]
        return mod

sys.path.append(__path__[0])
sys.meta_path.append(CFinderLoader)