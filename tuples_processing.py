# <tuples_processing.py>
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


import itertools


def compute_possible_pairs(descriptors):
    return list(itertools.combinations(descriptors, 2))


def compute_possible_tuples(descriptors):
    combinations = []
    for i in range(1, len(descriptors)):
        comb = list(itertools.combinations(descriptors, i))
        for combination in comb:
            combinations.append(combination)
    return combinations


def compute_tuples_pairs(parameters, selected_pairs_rk):
    # Number of pairs to consider
    top_tuples_fusion = parameters["top_tuples_fusion"]

    # Get the first pairs converting the pair from string to tuple type
    top_tuples = [[eval(elem[0]), elem[1]]
                  for elem in selected_pairs_rk[:top_tuples_fusion]]

    # Add the best pairs to the selected tuples dictionary
    selected_tuples = {2: top_tuples}

    return selected_tuples


def compute_tuples_intersection(parameters, selected_pairs_rk):
    # Number of pairs to consider for computing the intersection
    top_tuples_intersection = parameters["top_tuples_intersection"]

    # Get the first pairs converting the pair from string to tuple type
    top_tuples = [[eval(elem[0]), elem[1]]
                  for elem in selected_pairs_rk[:top_tuples_intersection]]

    # Add the best pairs to the selected tuples dictionary
    selected_tuples = {2: top_tuples}

    # Select tuples through intersection
    max_tuple_size = parameters["max_tuple_size"]
    for current_tuple_size in range(3, max_tuple_size+1):
        # Init list to store the tuples of the current iteration
        current_tuples = []
        # This set is used to prevent the insertion of repeated tuples
        tuples_set = set()
        for i, elem1 in enumerate(top_tuples):
            # Get elements of the first tuple
            tuple1 = elem1[0]
            tuple1_score = elem1[1]
            for elem2 in top_tuples[i+1:]:
                # Get elements of the second tuple
                tuple2 = elem2[0]
                tuple2_score = elem2[1]
                # If there's intersection, compute a new tuple based on union
                intersection = set(tuple1) & set(tuple2)
                if len(intersection) >= current_tuple_size-2:
                    new_tuple = tuple(sorted(set(tuple1) | set(tuple2)))
                    # Check if the tuple is not repeated
                    if new_tuple not in tuples_set:
                        # Compute the selection score for the new tuple
                        new_tuple_score = tuple1_score + tuple2_score
                        # Add it to the tuple set (to prevent repetition)
                        tuples_set.add(new_tuple)
                        # Add it to the list of tuples of the current size
                        current_tuples.append([new_tuple, new_tuple_score])
        # If there are no new tuples, just stop
        if current_tuples == []:
            break
        # Sort tuples by score
        current_tuples = sorted(current_tuples,
                                key=lambda x: x[1],
                                reverse=True)
        # Crop the list to consider only the best tuples
        current_tuples = current_tuples[:top_tuples_intersection]
        # Update dictionary with the new tuples
        selected_tuples[current_tuple_size] = current_tuples
        # Set top tuples for the next iteration
        top_tuples = current_tuples

    return selected_tuples
