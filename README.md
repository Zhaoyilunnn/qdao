# qdao
Quantum Data Access Optimizaton

# Install

1. Install an utility module.
```SHELL
git clone https://github.com/Zhaoyilunnn/qutils.git
cd qutils
python -m build
cd dist
pip install qutils-0.0.1*.whl
cd ../../
```

2. Install prerequisites.

Currently we use dev branch, see [pr11](https://github.com/ScQ-Cloud/pyquafu/pull/11)

```SHELL
git clone https://github.com/ScQ-Cloud/pyquafu.git
cd pyquafu
git checkout dev
pip install -r requirements.txt
python setup.py install
cd -
```

3. Install QDAO.
```SHELL
git clone https://github.com/Zhaoyilunnn/qdao.git
cd qdao
pip install -r requirements.txt
python setup.py install
cd -
```
