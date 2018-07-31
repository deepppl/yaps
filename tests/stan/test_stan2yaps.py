import yaps
from yaps.lib import *
import astor
import sys
from pathlib import Path

def roundtrip(path):
    with open(path, 'r') as fin:
        print(fin.read())
    print('--------------------------------')
    source = yaps.from_stan(code_file=path)
    print(source)
    print('--------------------------------')
    ast_ = yaps.from_string(source)
    yaps.print_stan(ast_)
    print('--------------------------------')


def run_test(dir):
    pathlist = Path(dir).glob('**/*.stan')
    nb_test = 0
    nb_success = 0
    for p in pathlist:
        path = str(p)
        nb_test += 1
        try:
            source = yaps.from_stan(code_file=path)
            ast_ = yaps.from_string(source)
            nb_success += 1
        except AttributeError:
            print("ATTRIBUTE\t", path)
        except SyntaxError:
            print("SYNTAX\t", path)
        except TypeError:
             print("TYPE\t", path)
    print("-------------------------")
    print("{}% of success on {} stan examples".format(nb_success/nb_test * 100, nb_test))

run_test('tests/stan')