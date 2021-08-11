from vtk import *
from time import perf_counter


# str -> long
time_execution_data = {}


def timed_execution(name, func, args = ()):
    t_start = perf_counter()
    r = func(*args)
    time_execution_data[name] = perf_counter() - t_start
    return r


def main():
    reader = timed_execution("reader_inst", vtkStructuredGridReader)
    timed_execution("reader_setfile", reader.SetFileName, ("density.vtk",))
    timed_execution("reader_update", reader.Update)

    seeds = timed_execution("seeds_inst", vtkPointSource)
    timed_execution("seeds_setradius", seeds.SetRadius, (3.0,))
    timed_execution("seeds_setcenter_reader_getoutput_getcenter", seeds.SetCenter, (reader.GetOutput().GetCenter(),))
    timed_execution("seeds_setnumberofpoints", seeds.SetNumberOfPoints, (100,))

    streamer = timed_execution("streamer_inst", vtkStreamTracer)
    timed_execution("streamer_setinputconn_reader_getoutputport", streamer.SetInputConnection, (reader.GetOutputPort(0),))
    timed_execution("streamer_setsourceconn_seeds_getoutputport", streamer.SetSourceConnection, (seeds.GetOutputPort(0),))
    timed_execution("streamer_setmaxpropagation", streamer.SetMaximumPropagation, (1000,))
    timed_execution("streamer_setinitialintegstep", streamer.SetInitialIntegrationStep, (.1,))
    timed_execution("streamer_setintegdirboth", streamer.SetIntegrationDirectionToBoth)

    outline = timed_execution("outline_inst", vtkStructuredGridOutlineFilter)
    timed_execution("outline_setinputconn_reader_getoutputport", outline.SetInputConnection, (reader.GetOutputPort(0),))


if __name__ == '__main__':
    timed_execution("main", main)

    with open("py_native_vtk_benchmark.results", "w") as f:
        for name in time_execution_data:
            f.write(name + ", " + str(time_execution_data[name]) + "\n")
        f.close()