"""Configurations"""
import os


WORK_DIR = os.getcwd()

QASMBENCH_SMALL_DIR = os.path.join(WORK_DIR, "QASMBench/small/")

SMALL_BENCHES = [
    "adder_n4",
    "basis_change_n3",
    "basis_test_n4",
    "basis_trotter_n4",
    "bell_n4",
    "cat_state_n4",
    "deutsch_n2",
    "dnn_n2",
    "error_correctiond3_n5",
    "fredkin_n3",
    "grover_n2",
    "hs4_n4",
    "inverseqft_n4",
    "ipea_n2",
    "iswap_n2",
    "linearsolver_n3",
    "lpn_n5",
    "pea_n5",
    "qaoa_n3",
    "qec_en_n5",
    "qec_sm_n5",
    "qft_n4",
    "qrng_n4",
    "quantumwalks_n2",
    "shor_n5",
    "teleportation_n3",
    "toffoli_n3",
    "variational_n4",
    "vqe_uccsd_n4",
    "wstate_n3"
]

QASMBENCH_LARGE_DIR = os.path.join(WORK_DIR, "QASMBench/large/")

LARGE_BENCHES = [
    "bigadder_n18",
    "bv_n19",
    "bwt_n21",
    "cat_state_n22",
    "cc_n18",
    "class_number_n60045",
    "dnn_n16",
    "ghz_state_n23",
    "ising_model_n1000",
    "ising_model_n500",
    "ising_n26",
    "multiplier_n25",
    "qft_n20",
    "square_root_n18",
    "swap_test_n25",
    "vqe_n24",
    "wstate_n27"
]

QCS_URL = "https://github.com/Zhaoyilunnn/qcs.git"
QCS_BENCHMARKS_DIR = os.path.join(WORK_DIR, "qcs/benchmarks/qasm/")
