
from numpy import linspace, sin

from chaco.api import ArrayPlotData, Plot
from chaco.tools.api import PanTool, ZoomTool
from enable.component_editor import ComponentEditor
from traits.api import Enum, HasTraits, Instance
from traitsui.api import Item, Group, View

class PlotEditor(HasTraits):

    plot = Instance(Plot)
    plot_type = Enum("scatter", "line")
    orientation = Enum("horizontal", "vertical")
    traits_view = View(Item('orientation', label="Orientation"),
                       Item('plot', editor=ComponentEditor(), show_label=False), 
                       width=500, height=500, resizable=True)

    def _plot_default(self):
        # Create the data and the PlotData object
        x = linspace(-14, 14, 100)
        y = sin(x) * x**3
        plotdata = ArrayPlotData(x = x, y = y)
        # Create the scatter plot
        plot = Plot(plotdata)
        plot.plot(("x", "y"), type=self.plot_type, color="blue")
        plot.tools.append(PanTool(plot))
        plot.tools.append(ZoomTool(plot))
        return plot
    
    def _orientation_changed(self):
        if self.orientation == "vertical":
            self.plot.orientation = "v"
        else:
            self.plot.orientation = "h"
        self.plot.request_redraw()
        

class Demo(HasTraits):
    
    # Scatter plot.
    scatter_plot = Instance(PlotEditor)
    
    # Line plot.
    line_plot = Instance(PlotEditor)
    
    traits_view = View(Group(Item('scatter_plot', show_label=False),
                             label='Scatter', style='custom'),
                       Group(Item('line_plot', show_label= False),
                             label='Line', style='custom'),
                       title='Chaco Plot',
                       resizable=True)
    
        
    def _scatter_plot_default(self):
        p = PlotEditor(plot_type="scatter")
        # Hook up this plot's ranges to the line plot's ranges.
        p.plot.range2d = self.line_plot.plot.range2d
        return p
    
    def _line_plot_default(self):
        return PlotEditor(plot_type="line")

    
demo = Demo()

if __name__ == "__main__":
    demo.configure_traits()
