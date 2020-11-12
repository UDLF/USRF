# <octave_calls.py>
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
import sys


def export_line_graph(parameters,
                      dataset,
                      selection_avg_topk,
                      best_avg_topk,
                      average_avg_topk,
                      worst_avg_topk,
                      descriptors_map_rk):
    filename = "evaluation_graph_" + dataset["name"]

    print("\n Exporting " + filename + ".m and generating " +
          filename + ".pdf...")

    # Create octave file to export data and redirect output to it
    f = open(filename + ".m", "w+")
    sys.stdout = f

    # Export average map/prec top-k lists
    print("selection_case =", selection_avg_topk)
    print("best_case =", best_avg_topk)
    print("avg_case =", average_avg_topk)
    print("worst_case =", worst_avg_topk)

    # Font settings
    print("set(0, 'defaultaxesfontname', 'Helvetica');")
    print("set(0, 'defaultaxesfontsize', 18);")
    print("set(0, 'defaulttextfontname', 'Helvetica');")
    print("set(0, 'defaulttextfontsize', 18);")

    # Keep graph to plot multiple lines
    print("hold on")
    print("grid on")

    # Labels
    print("title('Selection Results on " +
          dataset["name"].upper() + " Dataset')")
    print("xlabel('Number of selected combinations')")
    print("ylabel('Average",
          parameters["supervised_effectiveness"].upper(), "')")

    # Limit x interval
    print("xlim([1 " + str(len(selection_avg_topk)) + "])")

    # Plot our approach
    print("plot(selection_case,'color',[0 0 0.85],'-o','LineWidth',2)")

    # Plot virtual baselines
    print("plot(best_case,'color',[0 0.85 0],'--x','LineWidth',2)")
    print("plot(avg_case,'color',[0.85 0.55 0],'--x','LineWidth',2)")
    print("plot(worst_case,'color',[0.85 0 0],'--x','LineWidth',2)")

    # Plot best isolated descriptor
    print("inter = " + str(descriptors_map_rk[0][1]))
    print("plot([0," + str(len(selection_avg_topk)) +
          "], [inter,inter],'color',[0 0 0],'--','LineWidth',2.2)")

    # Legend settings
    print("legend('USRAF', 'Best Case', 'Average Case', " +
          "'Worst Case', 'Best Descriptor')")
    print("legend('location', 'northeastoutside')")

    # Export to pdf
    print("print -dpdfwrite " + filename + ".pdf")

    # Close file and restore stdout to default
    f.close()
    sys.stdout = sys.__stdout__

    # Generate .pdf with octave and call pdf viewer
    os.system("octave " + filename + ".m > /dev/null")
    # os.system("xdg-open " + filename + ".pdf > /dev/null")

    print(" Done!")


def export_dots_graph(parameters,
                      dataset,
                      selection_scores,
                      pairs_map,
                      descriptors_map_rk):
    filename = "dots_graph_" + dataset["name"]

    print("\n Exporting " + filename + ".m and generating " +
          filename + ".pdf...")

    # Create octave file to export data and redirect output to it
    f = open(filename + ".m", "w+")
    sys.stdout = f

    # Process necessary data
    pairs_labels = []
    map_axis = []
    selection_axis = []
    for pair in selection_scores:
        pair_label = eval(pair)[0] + "+" + eval(pair)[1]
        pairs_labels.append(pair_label)
        map_axis.append(pairs_map[pair])
        selection_axis.append(selection_scores[pair])

    # Font settings
    print("set(0, 'defaultaxesfontname', 'Helvetica');")
    print("set(0, 'defaultaxesfontsize', 18);")
    print("set(0, 'defaulttextfontname', 'Helvetica');")
    print("set(0, 'defaulttextfontsize', 18);")

    # Export data to file
    print('x =', selection_axis)
    print('y =', map_axis)
    print('labels = ["', end='')
    print(*pairs_labels, sep='"; "', end='')
    print('"]')

    # Plot dots
    print("scatter(x, y, 85, [0 0 0.9], 'd', 'filled');")

    # Plot text labels to dots
    print("text(x+0.0002, y+0.0001, labels, 'fontsize', 10);")

    # Keep graph to plot multiple lines
    print("hold on;")
    print("grid on;")

    # Plot best isolated descriptor
    print("inter = " + str(descriptors_map_rk[0][1]))
    print("plot([" + str(min(selection_axis)) + "," +
          str(max(selection_axis)) +
          "], [inter,inter],'color',[0 0 0],'--','LineWidth', 2.2);")
    print("xlim([" + str(min(selection_axis)) + ", " +
          str(max(selection_axis)) + "]);")

    # Labels
    print("title('Visualization of Pairs Selection on " +
          dataset["name"].upper() + " Dataset')")
    print("xlabel('Proposed Selection Measure')")
    print("ylabel('",
          parameters["supervised_effectiveness"].upper(), "')")

    # Export to pdf
    print("print -dpdfwrite " + filename + ".pdf")

    # Close file and restore stdout to default
    f.close()
    sys.stdout = sys.__stdout__

    # Generate .pdf with octave and call pdf viewer
    os.system("octave " + filename + ".m > /dev/null")
    os.system("xdg-open " + filename + ".pdf > /dev/null")

    print(" Done!")
