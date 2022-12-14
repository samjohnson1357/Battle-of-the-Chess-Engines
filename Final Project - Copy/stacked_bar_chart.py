"""
File Summary: Draw a stacked bar chart to display results between Leela Zero and other engines.
"""

import matplotlib.pyplot as plt
import read_pgn_files

def drawStackedBarChart(labels, data1, data2, title, xLabel, yLabel):
    fig, ax = plt.subplots()
    ax.bar(labels, data1, label='Leela Zero Points')
    ax.bar(labels, data2, bottom=data1, label='Other Engine Points')
    ax.legend()
    ax.set_title(title)
    ax.set_xlabel(xLabel)
    ax.set_ylabel(yLabel)
    plt.savefig(title + '.png')
    plt.show()


class StackedBarChartPlotter:
    def __init__(self):
        self.df = read_pgn_files.readAllPgnFilesIntoDf(saveFile=False)

    def drawWhitePlot(self):
        drawStackedBarChart(self.df.index, self.df['Leela White Points'], self.df['Leela White Missed Points'], 'Leela Zero (White) Against Other Engines',
                            'Other Chess Engine & Color', 'Points')

    def drawBlackPlot(self):
        drawStackedBarChart(self.df.index, self.df['Leela Black Points'], self.df['Leela Black Missed Points'], 'Leela Zero (Black) Against Other Engines',
                            'Other Chess Engine & Color', 'Points')

if __name__ == '__main__':
    plotter = StackedBarChartPlotter()
    plotter.drawWhitePlot()
    plotter.drawBlackPlot()

