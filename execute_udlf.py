# <execute_udlf.py>
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


import os
import load_data
from multiprocessing import Pool
from udlf.udlf_calls import eval_supervised_effectiveness, fuse_tuple_cprr


def aggregate_pair_cprr(parameters, dataset, pair, exec_num):
    # print("\tExecuting fusion for", pair)
    effectiveness_measure = parameters["supervised_effectiveness"]
    return fuse_tuple_cprr(pair,
                           dataset["path_ranked_lists"],
                           dataset["path_lists_file"],
                           dataset["path_classes_file"],
                           dataset["size"],
                           num_iterations=1,
                           l_size=dataset["rk_size"],
                           top_k=parameters["top_k"],
                           effectiveness_measure=effectiveness_measure,
                           exec_num=exec_num)


def execute_aggregation_cprr(parameters, dataset, pairs):
    pairs_map = {}
    print("\n Running CPRR (through UDLF) for each tuple...")
    n_pools = parameters["multithreading_pools"]
    pool_params = list(zip(pairs, [x for x in range(len(pairs))]))
    pool_params = [(parameters, dataset) + param for param in pool_params]
    with Pool(n_pools) as p:
        # Some print messages may not be reported while running pool map
        output_pairs_map = p.starmap(aggregate_pair_cprr, pool_params)
    # Remove all the config files generated by the executions in parallel
    script_path = os.path.dirname(__file__)
    os.system("rm " + os.path.join(script_path, "udlf/bin/config*"))
    # Parse dictionary with the results and return it
    pairs_map = dict(zip([str(pair) for pair in pairs], output_pairs_map))
    print(" Done!")
    return pairs_map


def eval_descriptor(parameters, dataset, descriptor, exec_num):
    # print("\tComputing for", descriptor)
    path_file = os.path.join(dataset["path_ranked_lists"], descriptor) + ".txt"
    return eval_supervised_effectiveness(
            path_file,
            dataset["path_lists_file"],
            dataset["path_classes_file"],
            dataset["size"],
            effectiveness_measure=parameters["supervised_effectiveness"],
            top_k=parameters["top_k"],
            l_size=dataset["rk_size"],
            exec_num=exec_num)


def execute_eval_isolated_descriptors(parameters, dataset):
    descriptors_map = {}
    print("\n Evaluating MAP for each descriptor...")
    n_pools = parameters["multithreading_pools"]
    descriptors = load_data.list_descriptors(dataset["path_ranked_lists"])
    pool_params = list(zip(descriptors, [x for x in range(len(descriptors))]))
    pool_params = [(parameters, dataset) + param for param in pool_params]
    with Pool(n_pools) as p:
        # Some print messages may not be reported while running pool map
        output_descriptors_map = p.starmap(eval_descriptor, pool_params)
    # Remove all the config files generated by the executions in parallel
    script_path = os.path.dirname(__file__)
    os.system("rm " + os.path.join(script_path, "udlf/bin/config*"))
    # Parse dictionary with the results and return it
    descriptors_map = dict(zip([str(desc) for desc in descriptors],
                               output_descriptors_map))
    print(" Done!")
    return descriptors_map
