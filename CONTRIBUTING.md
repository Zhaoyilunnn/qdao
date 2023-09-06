# Contributing Guide

# Test
```bash
cd qutils/
pip install .
cd -
```

Pass the following case
```bash
cd qcs/
pytest -s -k test_run_quafu_any_qasm tst/qdao/engine.py --nq 12 --np 10 --nl 8 --qasm random_12_9_max_operands_2_gen.qasm
```
