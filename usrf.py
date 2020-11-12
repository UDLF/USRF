#!/usr/bin/env python
# <usrf.py>
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


import sys
import stages
import show_messages
from multiprocessing import cpu_count
from config import parameters, select_dataset


def check_sys_args(args):
    if len(args) < 2:
        print(" Call me like this:", args[0], " dataset_name")
        exit(1)


if __name__ == "__main__":
    # Check call and load dataset info/parameters
    check_sys_args(sys.argv)
    dataset = select_dataset(sys.argv[1])

    # Set number of pools
    if parameters["multithreading_pools"] == 0:
        parameters["multithreading_pools"] = cpu_count()

    # For holidays, only MAP can be used
    if dataset["name"] == "holidays":
        parameters["supervised_effectiveness"] = "map"

    # Set the neighborhood size (top_k)
    if parameters["top_k"] == 0:
        parameters["top_k"] = dataset["top_k"]

    # Show program header and parameters info
    show_messages.show_usraf_header()
    show_messages.show_settings(parameters, dataset)

    # Loading stage
    ranked_lists = stages.perform_loading_stage(parameters, dataset)

    # Pre-selection stage
    # (compute cor., eff., and estimate the parameters)
    (pairs,
     effectiveness,
     correlations) = stages.perform_pre_selection_stage(parameters,
                                                        dataset,
                                                        ranked_lists)

    # Selection stage
    (selected_pairs_scores,
     selected_tuples_rk) = stages.perform_selection_stage(parameters,
                                                          dataset,
                                                          pairs,
                                                          effectiveness,
                                                          correlations)

    # Fusion stage
    if parameters["perform_fusion"]:
        stages.perform_fusion_stage(parameters,
                                    dataset,
                                    selected_tuples_rk)

    # Evaluation stage
    if parameters["perform_evaluation"]:
        stages.perform_evaluation_stage(parameters,
                                        dataset,
                                        pairs,
                                        selected_pairs_scores)
