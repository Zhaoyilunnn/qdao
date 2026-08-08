

[![Tests](https://github.com/Zhaoyilunnn/qdao/actions/workflows/unit_test.yml/badge.svg?branch=main)](https://github.com/Zhaoyilunnn/qdao/actions/workflows/unit_test.yml)
[![qiskit](https://img.shields.io/badge/qiskit%20community-8A2BE2)](https://qiskit.org/ecosystem)

- [¿Qué es QDAO](#what-is-qdao)
- [Instalación](#install)
- [Pruebas](#testing)
- [Uso](#usage)
  * [Uso Básico](#basic-usage)
  * [Simulación en GPU](#gpu-simulation)
  * [Backends](#backends)
  * [Obtener Resultados de la Simulación](#get-simulation-results)
- [Cita](#citation)
- [Desarrollo](#development)
- [Características](#features)
- [Limitaciones](#limitations)
  * [Soluciones a Corto Plazo](#short-term-solutions)
  * [A Largo Plazo](#long-term)
- [Problemas (Issues)](#issues)


# ¿Qué es qdao
qdao es un **marco de optimización de acceso de datos** cuánticos. Aprovecha el almacenamiento secundario para simular circuitos cuánticos a gran escala y minimiza el movimiento de datos entre la memoria y el almacenamiento secundario. El requisito de memoria para la simulación completa del estado de un circuito cuántico crece exponencialmente con el número de qubits. Por ejemplo, en una PC típica, simular un circuito con más de 30 qubits puede provocar fácilmente un error de falta de memoria (out-of-memory). Con qdao, la ocupación de memoria de la simulación está completamente bajo tu control.

# Instalación

```BASH
git clone https://github.com/Zhaoyilunnn/qdao.git
cd qdao
pip install .
```

# Pruebas
```BASH
pytest tests/
```

# Uso

## Uso Básico

El siguiente ejemplo se puede encontrar en el directorio `examples/` y se añadirán más ejemplos en el futuro.

El siguiente fragmento de código muestra el uso básico de qdao. Puedes configurar el parámetro `num_primary` para reducir la ocupación de memoria.

$\text{memory consumption} = 2^{\text{num-primary}} * 16 \text{ Byte}$

```Python
from qdao import Engine
from qiskit.circuit.random import random_circuit
from qiskit import transpile
from qiskit_aer import Aer

num_qubits = 12
num_primary = 10
num_local = 8

# Create a qiskit quantum circuit `circ`
circ = random_circuit(num_qubits, 10, measure=False, max_operands=2)
backend = Aer.get_backend("aer_simulator")
circ = transpile(circ, backend=backend)

# `num_primary`: size of a compute unit, i.e., $m$ in QDAO paper
# `num_local`: size of a storage unit, i.e., $t$ in QDAO paper
eng = Engine(circuit=circ, num_primary=num_primary, num_local=num_local)
eng.run()
```

## Simulación en GPU

Para utilizar la GPU para la simulación y usar la memoria del host para almacenar el vector de estado completo, prueba la siguiente configuración.

Primero, debes instalar `qiskit-aer-gpu`. Consulta el [documento oficial](https://github.com/Qiskit/qiskit-aer).

```Python
eng = Engine(circuit=circ, num_primary=num_primary, num_local=num_local, sv_location="memory", device="GPU")
```


## Backends

Puedes especificar un simulador de backend utilizando la opción `backend`, actualmente solo se admiten qiskit y pyquafu.

```Python
# First transform qiskit circuit to a quafu circuit
from quafu import QuantumCircuit
quafu_circ = QuantumCircuit(1)

# For qiskit < 1.0
quafu_circ.from_openqasm(circ.qasm())

# For qiskit >= 1.0, `qasm()` api has been deprecated.
from qiskit.qasm2 import dumps
quafu_circ.from_openqasm(dumps(circ))

# Create a new engine using quafu backend
eng = Engine(circuit=quafu_circ, num_primary=num_primary, num_local=num_local, backend="quafu")
eng.run()
```

## Obtener Resultados de la Simulación

Estamos trabajando para admitir mediciones en qdao; por ahora, obtén el vector de estado después de la simulación de la siguiente manera.

```Python
from qdao.util import retrieve_sv
res = retrieve_sv(num_qubits, num_local=num_local)
print(res)
```

# Cita
Si consideras que nuestro trabajo es útil, por favor cita nuestro artículo como se muestra a continuación.
```bib
@inproceedings{qdao2023,
  title={Full State Quantum Circuit Simulation Beyond Memory Limit},
  author={Zhao, Yilun and Chen, Yu and Li, He and Wang, Ying and Chang, Kaiyan and Wang, Bingmeng and Li, Bing and Han, Yinhe},
  booktitle={2023 IEEE/ACM International Conference on Computer-Aided Design (ICCAD)},
  year={2023},
  organization={IEEE}
}
```

# Desarrollo

Consulta el archivo [CONTRIBUTING.md](https://github.com/Zhaoyilunnn/qdao/blob/main/CONTRIBUTING.md).

# Características
Hay algunas características clave que se admitirán en el futuro

 - [x] Simulación en GPU
 - [ ] Simulación con ruido

# Limitaciones

Al utilizar el backend de qiskit, establecer un vector de estado inicial en qiskit genera una sobrecarga significativa debido a:
1. Qiskit trata el vector de estado como parámetros e implementa lógica de validación que consume mucho tiempo, consulta https://github.com/Zhaoyilunnn/qdao/issues/14.
2. Existe una copia de datos adicional al enviar el circuito con el vector de estado inicial a Aer. Por ejemplo, si estableces un vector de estado inicial de 1 GB, en realidad consume 2 GB de memoria durante la simulación.


## Soluciones a Corto Plazo

1. Puedes utilizar la versión estable etiquetada, que requiere qiskit < 1.0 y en la que realizamos modificacionesmodificaciones técnicas_ en qiskit para eliminar la sobrecarga de validación.

```bash

git checkout stable/0.1
pip install .
```

2. Puedes utilizar el backend `quafu`. Aunque en sí es más lento que Qiskit, no presenta los problemas de qiskit al usar QDAO. De hecho, QDAO-PyQuafu es más rápido que QDAO-Qiskit para circuitos grandes (>=28 Qubits).

3. Dado que la sobrecarga adicional de qiskit es completamente un problema de implementación, es posible que desees medir el rendimiento ideal de QDAO-Qiskit. Para hacerlo, podrías comentar [esta línea](https://github.com/Zhaoyilunnn/qdao/blob/v0.1.0/qdao/qiskit/circuit.py#L58), aunque esto conducirá a resultados de simulación incorrectos.


## A Largo Plazo

- Implementaremos un backend personalizado de alto rendimiento en C++ y lo integraremos en QDAO. Por favor, estad atentos.


# Problemas (Issues)
Por favor, abre un issue o contacta a zyilun8@gmail.com si encuentras algún problema.
