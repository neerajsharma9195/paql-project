# paql-project
PaQL Package Query Results Recreation

1) Requirements:
     - Install cplex (https://www.ibm.com/docs/en/icos/12.7.1.0?topic=v1271-installing-cplex-optimization-studio)
        We are using cplex academic initative project for this implementation.
     - Download tpch.csv from http://avid.cs.umass.edu/courses/645/s2021/project/paql_data/tpch.csv and put in data folder inside src directory.
     - pip install -r requirements.txt
     - setup.py file and cplex folder in src directory are copied from Applications folder to run with cplex. 

2) Direct Method:
   - Implementation of direct method using cplex is in src/direct.py
   
3) Offline partitioning:
    - Implementation of partitioning is in src/partitioning.py
    - run src/run_offline_partitioning.py (recommend running overnight since it takes a significant amount of time)
    - run src/k_means_clustering.py to create partitions with K Means clustering. (recommend running overnight since it takes a significant amount of time)
 
4) Sketch Refine:
    - Implementation for SketchRefine is in src/SketchRefine.py
    - Implementation for SketchRefine with greedy backtracking is in src/SketchRefineWithBT.py (this is we use for our experiments)

5) Generate results:
    - run dataset_size_analysis.py to get results of Direct and SketchRefine (includes both k-dim Quad tree and kmeans partitioning) for different dataset sizes
    - run partition_threshhold_analysis.py to get results of SketchRefine with different partition threshold sizes.



