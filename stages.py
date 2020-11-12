# <stages.py>
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


import show_messages
import load_data
import parameters_estimation
import effectiveness_estimation_functions
import correlation_functions
import selection_functions
import tuples_processing
import rank_dictionaries
import evaluation_functions
import octave_calls
import execute_udlf
import numpy as np


def perform_loading_stage(parameters, dataset):
    print("\n\n---------------------------------")
    print(" LOADING STAGE")

    # Load all ranked lists into memory
    descriptors = load_data.list_descriptors(dataset["path_ranked_lists"])
    ranked_lists = load_data.load_ranked_lists(parameters,
                                               descriptors,
                                               dataset["path_ranked_lists"])
    return ranked_lists


def perform_pre_selection_stage(parameters, dataset, ranked_lists):
    print("\n\n---------------------------------")
    print(" PRE-SELECTION STAGE")

    # List descriptors to combine
    descriptors = load_data.list_descriptors(dataset["path_ranked_lists"])
    show_messages.show_available_descriptors(descriptors)

    # Show combinations
    pairs = tuples_processing.compute_possible_pairs(descriptors)
    if len(pairs) <= 15:
        show_messages.show_computed_pairs(pairs)
    # combinations = tuples_processing.compute_possible_tuples(descriptors)
    # show_messages.show_computed_combinations(combinations)

    # Compute effectiveness estimations and rank descriptors
    effectiveness_function = effectiveness_estimation_functions.\
        get_effectiveness_func(parameters["effectiveness_estimation_measure"])
    effectiveness = effectiveness_estimation_functions.\
        compute_descriptors_effectiveness(parameters,
                                          effectiveness_function,
                                          ranked_lists,
                                          descriptors,
                                          parameters["top_k"])
    effectiveness_rk = rank_dictionaries.\
        rank_descriptors_by_effec_estim(effectiveness)
    show_messages.show_effectiveness_results(effectiveness_rk)

    # Compute correlations for pairs and rank them
    correlation_function = correlation_functions.get_correlation_func(
                           parameters["correlation_measure"])
    correlations = correlation_functions.\
        compute_correlations_for_pairs(parameters,
                                       correlation_function,
                                       ranked_lists,
                                       pairs,
                                       parameters["top_k"])
    correlation_rk = rank_dictionaries.rank_pairs_by_correlation(correlations)
    show_messages.show_correlation_results(correlation_rk)

    # Estimate values for beta
    if parameters["estimate_expoents"]:
        beta = parameters_estimation.estimate_beta(parameters,
                                                   effectiveness,
                                                   correlations)
        parameters["beta"] = beta

    return pairs, effectiveness, correlations


def perform_selection_stage(parameters,
                            dataset,
                            pairs,
                            effectiveness,
                            correlations):
    print("\n\n---------------------------------")
    print(" SELECTION STAGE")

    # Compute selection measure for each pair and rank them
    selected_pairs_scores = selection_functions.\
        compute_selection_for_pairs(parameters,
                                    pairs,
                                    effectiveness,
                                    correlations)
    selected_pairs_rk = rank_dictionaries.\
        rank_pairs_by_selection(selected_pairs_scores)
    show_messages.show_pairs_selection_results(selected_pairs_rk)

    # Select tuples according to the specified selection mode
    selection_mode = parameters["selection_mode"]
    if selection_mode == "pairs_only":
        selected_tuples_rk = tuples_processing.\
            compute_tuples_pairs(parameters, selected_pairs_rk)
    elif selection_mode == "tuples_intersection":
        selected_tuples_rk = tuples_processing.\
            compute_tuples_intersection(parameters, selected_pairs_rk)
    else:
        print("\n ERROR: Unknown selection mode:", selection_mode)
        exit(1)

    show_messages.show_tuples_selection_results(selected_tuples_rk)

    return selected_pairs_scores, selected_tuples_rk


def perform_fusion_stage(parameters, dataset, selected_tuples):
    print("\n\n---------------------------------")
    print(" FUSION STAGE")

    top_tuples_fusion = parameters["top_tuples_fusion"]

    for tuple_size in selected_tuples:
        print("\n Executing tuples of", tuple_size, "elements...")
        combinations = [elem[0] for elem in selected_tuples[tuple_size]]
        combinations = combinations[:top_tuples_fusion]
        results = execute_udlf.execute_aggregation_cprr(parameters,
                                                        dataset,
                                                        combinations)
        print("\n", parameters["supervised_effectiveness"].upper(),
              "of the selected tuples (", tuple_size,
              "elements ) fused with CPRR:")

        result_list = []
        for result in results:
            result_list.append(results[result])
            print("\t", result, " = ", "%0.4f" % float(results[result]))
        avg = np.average(result_list)
        avg_weighted = np.average(result_list,
                                  weights=range(len(result_list), 0, -1))
        print("\t Average",
              parameters["supervised_effectiveness"].upper(),
              ":", "%0.4f" % avg)
        print("\t Weighted Average",
              parameters["supervised_effectiveness"].upper(),
              ":", "%0.4f" % avg_weighted)


def perform_evaluation_stage(parameters, dataset, pairs, selection_scores):
    print("\n\n---------------------------------")
    print(" EVALUATION STAGE")

    print(" WARNING: This mode only evaluates pairs!")

    # Compute supervised effectiveness measure for each descriptor
    descriptors_map = execute_udlf.\
        execute_eval_isolated_descriptors(parameters, dataset)
    descriptors_map_rk = rank_dictionaries.\
        rank_descriptors_by_map(descriptors_map)
    show_messages.show_descriptors_map_results(parameters, descriptors_map_rk)

    # Run CPRR for each pair and rank them
    pairs_map = execute_udlf.\
        execute_aggregation_cprr(parameters, dataset, pairs)
    pairs_map_rk = rank_dictionaries.rank_pairs_by_map(pairs_map)
    show_messages.show_pairs_map_results(parameters, pairs_map_rk)

    # Compute pearson correlation between map/prec and selection scores
    evaluation_functions.compute_pearson_for_scores(parameters,
                                                    selection_scores,
                                                    pairs_map)

    # Compute all the cases (our approach + the hypothetical/virtual baselines)
    selection_case = evaluation_functions.\
        compute_selection_case(selection_scores, pairs_map)
    (best_case,
     avg_case,
     worst_case) = evaluation_functions.compute_virtual_baselines(pairs_map)

    # Compute the average top-k lists for all the cases
    print("\n Computing average",
          parameters["supervised_effectiveness"].upper(), "top-k lists...")
    selection_avg_topk = evaluation_functions.\
        compute_avg_topk_list(selection_case)
    best_avg_topk = evaluation_functions.compute_avg_topk_list(best_case)
    average_avg_topk = evaluation_functions.compute_avg_topk_list(avg_case)
    worst_avg_topk = evaluation_functions.compute_avg_topk_list(worst_case)
    print(" Done!")

    # Show the first values of the average top-k lists
    show_messages.show_avg_topk_lists(parameters,
                                      selection_avg_topk,
                                      best_avg_topk,
                                      average_avg_topk,
                                      worst_avg_topk)

    # Export the octave line graph
    octave_calls.export_line_graph(parameters,
                                   dataset,
                                   selection_avg_topk,
                                   best_avg_topk,
                                   average_avg_topk,
                                   worst_avg_topk,
                                   descriptors_map_rk)

    # Export the octave dots graph
    octave_calls.export_dots_graph(parameters,
                                   dataset,
                                   selection_scores,
                                   pairs_map,
                                   descriptors_map_rk)
