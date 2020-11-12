# <load_data.py>
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


def list_descriptors(path):
    return [x[:-4] for x in sorted(os.listdir(path))]


def read_ranked_lists_file(parameters, descriptor, path_rks):
    file_path = os.path.join(path_rks, descriptor) + ".txt"
    print("\tReading file", file_path)
    with open(file_path, 'r') as f:
        return [[int(y) for y in x.strip().split(' ')][:parameters["top_k"]]
                for x in f.readlines()]


def load_ranked_lists(parameters, descriptors, path_rks):
    ranked_lists = {}
    print("\n Loading ranked lists...")
    for descriptor in descriptors:
        ranked_lists[descriptor] = read_ranked_lists_file(parameters,
                                                          descriptor,
                                                          path_rks)
    print(" Done!")
    return ranked_lists
