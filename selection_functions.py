# <selection_functions.py>
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


def compute_selection_score(pair,
                            effectiveness,
                            correlations,
                            beta=1):
    eff1 = effectiveness[pair[0]]
    eff2 = effectiveness[pair[1]]
    cor = correlations[str(pair)]
    eff_score = (eff1*eff2)
    cor_score = (1 + cor)**beta
    return eff_score/cor_score


def compute_selection_for_pairs(parameters,
                                pairs,
                                effectiveness,
                                correlations):
    selection = {}
    print("\n Computing selection scores...")
    for pair in pairs:
        # print("\tComputing sel. score for", pair)
        selection[str(pair)] = compute_selection_score(
                                            pair,
                                            effectiveness,
                                            correlations,
                                            beta=parameters["beta"])
    print(" Done!")
    return selection
