#!/bin/bash
# Clusters files
python3.4 recommend.py clusters_data_jaccard_distance_average.npy > rec_jacc_average.txt
python3.4 recommend.py clusters_data_jaccard_distance_complete.npy > rec_jacc_complete.txt
python3.4 recommend.py clusters_data_jaccard_distance_single.npy > rec_jacc_single.txt
python3.4 recommend.py clusters_data_jaccard_distance_ward.npy > rec_jacc_ward.txt
python3.4 recommend.py clusters_data_masi_distance_average.npy > rec_masi_average.txt
python3.4 recommend.py clusters_data_masi_distance_complete.npy > rec_masi_complete.txt
python3.4 recommend.py clusters_data_masi_distance_single.npy > rec_masi_single.txt
python3.4 recommend.py clusters_data_masi_distance_ward.npy > rec_masi_ward.txt
