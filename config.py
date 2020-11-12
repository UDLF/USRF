# <config.py>
#
#  Parameters for each dataset.
#
#  @Author: Lucas Pascotti Valem <lucas.valem@unesp.br>
#
#-------------------------------------------------------------------------------
#
# This file is part of Unsupervised Selective Rank Fusion Framework (USRF).
#
# USRF is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# USRF is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with USRF.  If not, see <http://www.gnu.org/licenses/>.
#


# general parameters
parameters = {# "pairs_only" or "tuples_intersection"
              "selection_mode": "tuples_intersection",
              # "authority" or "reciprocal"
              "effectiveness_estimation_measure": "reciprocal",
              # "jaccard", "jaccard_k", "rbo", "kendalltau", "spearman",
              # "kendallw", "kappa", "fleiss", "alpha", "scotts"
              "correlation_measure": "rbo",
              # top_k = 0 to use the dataset default
              "top_k": 0,
              "beta": -1,
              "estimate_expoents": False,
              # "map" or "precision"
              "supervised_effectiveness": "map",
              # number of top tuples to run with UDLF in fusion stage
              "top_tuples_fusion": 5,
              # number of top tuples to compute the "tuples_intersection"
              "top_tuples_intersection": 100,
              # maximum size for the selected tuples
              "max_tuple_size": 6,
              "perform_fusion": True,
              # evaluation stage executes and evaluates all pairs
              "perform_evaluation": False,
              # 0 to use the number of CPUs; 1 for serial execution
              "multithreading_pools": 0}

# mpeg7
dataset_mpeg7 = {"name": "mpeg7",
                 "size": 1400,
                 "rk_size": 1400,
                 "top_k": 20,
                 "path_ranked_lists": "datasets/mpeg7/ranked_lists/",
                 "path_lists_file": "datasets/mpeg7/mpeg7_lists.txt",
                 "path_classes_file": "datasets/mpeg7/mpeg7_classes.txt"}

# flowers
dataset_flowers = {"name": "flowers",
                   "size": 1360,
                   "rk_size": 1360,
                   "top_k": 50,
                   "path_ranked_lists": "datasets/flowers/ranked_lists/",
                   "path_lists_file": "datasets/flowers/flowers_lists.txt",
                   "path_classes_file": "datasets/flowers/flowers_classes.txt"}

# corel5k
dataset_corel5k = {"name": "corel5k",
                   "size": 5000,
                   "rk_size": 3000,
                   "top_k": 50,
                   "path_ranked_lists": "datasets/corel5k/ranked_lists/",
                   "path_lists_file": "datasets/corel5k/corel5k_lists.txt",
                   "path_classes_file": "datasets/corel5k/corel5k_classes.txt"}

# ukbench
dataset_ukbench = {"name": "ukbench",
                   "size": 10200,
                   "rk_size": 200,
                   "top_k": 5,
                   "path_ranked_lists": "datasets/ukbench/ranked_lists/",
                   "path_lists_file": "datasets/ukbench/ukbench_lists.txt",
                   "path_classes_file": "datasets/ukbench/ukbench_classes.txt"}

# soccer
dataset_soccer = {"name": "soccer",
                  "size": 280,
                  "rk_size": 280,
                  "top_k": 50,
                  "path_ranked_lists": "datasets/soccer/ranked_lists/",
                  "path_lists_file": "datasets/soccer/soccer_lists.txt",
                  "path_classes_file": "datasets/soccer/soccer_classes.txt"}

# brodatz
dataset_brodatz = {"name": "brodatz",
                   "size": 1776,
                   "rk_size": 1776,
                   "top_k": 20,
                   "path_ranked_lists": "datasets/brodatz/ranked_lists/",
                   "path_lists_file": "datasets/brodatz/brodatz_lists.txt",
                   "path_classes_file": "datasets/brodatz/brodatz_classes.txt"}

# dataset options
datasets = {"mpeg7": dataset_mpeg7,
            "corel5k": dataset_corel5k,
            "soccer": dataset_soccer,
            "brodatz": dataset_brodatz,
            "flowers": dataset_flowers,
            "ukbench": dataset_ukbench}


def select_dataset(dataset_name):
    dataset_name = dataset_name.lower()
    dataset = datasets.get(dataset_name)
    if dataset is not None:
        return dataset
    print(" ERROR: Unknown dataset", dataset_name)
    print(" Available datasets:")
    for key in datasets:
        print("\t", key)
    exit(1)
