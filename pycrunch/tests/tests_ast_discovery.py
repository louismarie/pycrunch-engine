from pathlib import Path

from pycrunch.discovery.ast_discovery import AstTestDiscovery
from pycrunch.session.configuration import Configuration


def test_simple_discovery():
    actual = run_dogfood_discovery()

    found_flag = False
    for t in actual.tests:
        if t.filename.endswith('test_discovery_specs_demo.py'):
            if t.name == 'test_regular':
                found_flag = True
                break

    assert found_flag


class TestProblem():
    def test_sample(self):
        self.assertEqual(1, 1)


def test_only_methods_are_discovered_not_variables():
    actual = run_dogfood_discovery()
    test_names = list(map(lambda _: _.name, actual.tests))
    assert len(test_names) > 0
    assert 'test_variable' not in test_names

def test_classes_with_unit_tests_are_discoverable():
    actual = run_dogfood_discovery()
    test_names = list(map(lambda _: _.name, actual.tests))
    assert len(test_names) > 0
    assert 'SomeClassInhereted::test_1' in test_names
    assert 'TestX::test_1' in test_names
    assert 'MyClass::test_method1' in test_names
    assert 'MyClass::test_method2' in test_names
    assert 'TestForDummies::test_method1' in test_names
    assert 'TestForDummies::test_method2' in test_names
    assert 'TestForDummies::helper_method' not in test_names


def run_dogfood_discovery():
    root_folder = Path('.')
    current_folder = root_folder.joinpath('pycrunch', 'tests', 'dogfood').absolute()
    sut = AstTestDiscovery(str(root_folder.absolute()), Configuration())
    search_only_in = ['/Users/gleb/code/PyCrunch/pycrunch/tests/dogfood/test_class_base.py']
    actual = sut.find_tests_in_folder(
        str(current_folder.absolute()),
        # search_only_in
    )
    return actual


