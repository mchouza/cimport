import sys
sys.path.append('..')
import cimport
import c
import b
import d.a
import d.b
b.foo()
try:
	print d.a.foo()
	assert 0
except AttributeError:
	pass
assert d.a.bar() == 42