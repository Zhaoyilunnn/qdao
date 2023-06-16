## QDAO: Quantum Data Access Optimization

### Redundancy

### Run-ahead

<p align="center">
    <img width="500" alt="image" src="https://user-images.githubusercontent.com/40353317/184477102-19d7f815-b7a7-452b-81a5-c38b3756bac8.png">
</p>

<p align="center">
    <img width="500" alt="image" src="https://user-images.githubusercontent.com/40353317/184477204-c16cfc2c-a845-4117-907c-921857273e06.png">
</p>

<p align="center">
    <img width="500" alt="image" src="https://user-images.githubusercontent.com/40353317/184477223-10270152-4339-4a6e-9cf3-2fe2ab18c9c0.png">
</p>

#### Work flow (High Level)
1. Consider a circuit that has $N$ qubits, $M$ gates.
2. Divide the gates into $G$ groups, each operating on $X$ qubits
3. Put the sub-statevector that contains $X$ qubits into primary storage
4. Finish a group of operations
5. Reorganize memory layout
6. Repeat step 3, until finishing all operations

The impact is **reduce memory traversal times from $M$ to $G$**

#### Work Flow (Low-level)

***Glossary***

- A ***segment*** is the least data block that is stored in secondary storage. Note that load and store is per-segment.
- A ***chunk*** is the data buffer that is stored in primary storage.

***The load and store***

1. We need to maintain a map from current qubit to original qubit

   - e.g., The original qubits are `[1,3,5,7]`, and in a sub-circuit this becomes `[0,1,2,3]`

2. The state vector is partitioned info many small segments, a small segment's size equals the `num_local` qubits. The segments are named with the suffix of index -- the original index if they are combined as the original state vector.

   - e.g., The original qubits are `[1,3,5,7]`, `num_qubits=8, num_local=2`, then although the operations act on like the qubits are `[0,1,2,3]`

   - | Segment No. (Logical) | Segment No. (Original) | Index Range (Logical)     | Index Range (Original)    |
     | --------------------- | ---------------------- | ------------------------- | ------------------------- |
     | 1                     | 2 (`1<<(3-2)`)         | **000001**00~**000001**11 | **000010**00~**000010**11 |

3. Based on 1 and 2, we can conclude the work flow as follows

   1. Get the *logical global* qubits. In the above example, it would be `[3-2,5-2,7-2]=[1,3,5]`
   2. Get the number of groups in primary memory. (Still use the above example)
      1. If the primary memory contain `8=2^3` segments, i.e., `num_primary=5` since the number of logical global qubits equals `num_primary - num_local`. The number of group is 1.
      2. If the primary memory contain `16=2^4` segments, i.e., `num_primary=6` since the number of logical global qubits is smaller than `num_primary - num_local`. The number of group is `1<<(num_primary - num_local - num_logical_global)=2`.
   3. Get the start group id. Note that the start group id depends on the chunk id, i.e. `start_group_id = chunk_id * num_groups`. Similarly, the `end_group_id` is simply the start plus number of groups
   4. For each group, get the corresponding indexes and save the segments with indexes as suffixes to secondary storage.

#### Examples

1. Simple Clustering

<img width="672" alt="image" src="https://user-images.githubusercontent.com/40353317/187071997-73d5e301-2e19-40f4-84fc-7a05152ac238.png">

2. Reordering opportunity

<img width="705" alt="image" src="https://user-images.githubusercontent.com/40353317/187072049-04a8f9ec-aaa2-44b8-ae5f-de9fbd9abf58.png">
