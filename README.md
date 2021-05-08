# paql-project
PaQL Package Query Results Recreation

1) Requirements:
     - Install cplex (https://www.ibm.com/docs/en/icos/12.7.1.0?topic=v1271-installing-cplex-optimization-studio)
        We are using cplex academic initative project for this implementation.
     - pip install -r requirements.txt

2) Direct Method:
   To run the direct method approach:
   - Implementation of direct method using cplex is in src/direct.py
   - run src/test_direct.py for our results
   
3) Offline partitioning:
    - Implementation of partitioning is in src/partitioning.py
    - run src/run_offline_partitioning.py (recommend running overnight since it takes a significant amount of time)
 
4) Sketch Refine:
    - Implementation for SketchRefine is in src/SketchRefine.py
    - Implementation for SketchRefine with greedy backtracking is in src/SketchRefineWithBT.py
    - run src/test_backtracking_1.py for our results

5) Generate results:
    - run dataset_size_analysis.py to get results of Direct and SketchRefine (includes both k-dim Quad tree and kmeans partitioning) for different dataset sizes
    - run partition_threshhold_analysis.py to get results of SketchRefine with different partition threshold sizes.



