import logging


## Logging configuration
#logging.basicConfig(filename='qvm_test.log', encoding='utf-8', level=logging.DEBUG,
#                format='%(asctime)s %(message)s')
#logger = logging.getLogger("qvm_pytest_logger")


def pytest_addoption(parser):
    parser.addoption("--qasm", action="store", default="")
    parser.addoption("--nq", action="store", default=10)
    parser.addoption("--np", action="store", default=0)
    parser.addoption("--nl", action="store", default=0)
    parser.addoption("--mode", action="store", default="QDAO")
    parser.addoption("--parallel", action="store", default=1)
    parser.addoption("--diff", action="store", default=1)
    parser.addoption("--sv_location", action="store", default="disk")
    parser.addoption("--device", action="store", default="CPU")


def pytest_generate_tests(metafunc):
    # This is called for every test. Only get/set command line arguments
    # if the argument is specified in the list of test "fixturenames".

    option_value = metafunc.config.option.qasm
    if 'qasm' in metafunc.fixturenames and option_value is not None:
        metafunc.parametrize("qasm", [option_value])

    option_value = metafunc.config.option.nq
    if 'nq' in metafunc.fixturenames and option_value is not None:
        metafunc.parametrize("nq", [option_value])

    option_value = metafunc.config.option.np
    if 'np' in metafunc.fixturenames and option_value is not None:
        metafunc.parametrize("np", [option_value])

    option_value = metafunc.config.option.nl
    if 'nl' in metafunc.fixturenames and option_value is not None:
        metafunc.parametrize("nl", [option_value])

    option_value = metafunc.config.option.mode
    if 'mode' in metafunc.fixturenames and option_value is not None:
        metafunc.parametrize("mode", [option_value])

    option_value = metafunc.config.option.parallel
    if 'parallel' in metafunc.fixturenames and option_value is not None:
        metafunc.parametrize("parallel", [option_value])

    option_value = metafunc.config.option.diff
    if 'diff' in metafunc.fixturenames and option_value is not None:
        metafunc.parametrize("diff", [option_value])

    option_value = metafunc.config.option.device
    if 'device' in metafunc.fixturenames and option_value is not None:
        metafunc.parametrize("device", [option_value])

    option_value = metafunc.config.option.sv_location
    if 'sv_location' in metafunc.fixturenames and option_value is not None:
        metafunc.parametrize("sv_location", [option_value])
