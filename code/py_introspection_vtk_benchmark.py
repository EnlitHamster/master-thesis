from vtk import *
from time import perf_counter
from Introspector import Introspector

# str -> long
time_execution_data = {}


def timed_execution(name, func, args = ()):
    t_start = perf_counter()
    r = func(*args)
    time_execution_data[name] = perf_counter() - t_start
    return r


def main():
    introspector = timed_execution("introspector_inst", Introspector)

    reader = timed_execution("reader_inst", introspector.createVtkObject, ("vtkStructuredGridReader",))
    timed_execution("reader_setfile", introspector.setVtkObjectAttribute, (reader, "FileName", "s", "density.vtk"))
    timed_execution("reader_update", introspector.updateVtkObject, (reader,))

    seeds = timed_execution("seeds_inst", introspector.createVtkObject, ("vtkPointSource",))
    timed_execution("seeds_setradius", introspector.setVtkObjectAttribute, (seeds, "Radius", "f", 3.0))
    center = timed_execution("reader_getoutputgetcenter", introspector.genericCall, (introspector.vtkInstanceCall(reader, "GetOutput", ()), "GetCenter", ()))
    timed_execution("seeds_setcenter_reader_getoutput_getcenter", introspector.setVtkObjectAttribute, (seeds, "Center", "f3", introspector.outputFormat(center)))
    timed_execution("seeds_setnumberofpoints", introspector.setVtkObjectAttribute, (seeds, "NumberOfPoints", "d", 100))

    streamer = timed_execution("streamer_inst", introspector.createVtkObject, ("vtkStreamTracer",))
    timed_execution("streamer_setinputconn_reader_getoutputport", introspector.vtkInstanceCall, (streamer, "SetInputConnection", (introspector.getVtkObjectOutputPort(reader),)))
    timed_execution("streamer_setsourceconn_seeds_getoutputport", introspector.vtkInstanceCall, (streamer, "SetSourceConnection", (introspector.getVtkObjectOutputPort(seeds),)))
    timed_execution("streamer_setmaxpropagation", introspector.setVtkObjectAttribute, (streamer, "MaximumPropagation", "d", 1000))
    timed_execution("streamer_setinitialintegstep", introspector.setVtkObjectAttribute, (streamer, "InitialIntegrationStep", "f", .1))
    timed_execution("streamer_setintegdirboth", introspector.vtkInstanceCall, (streamer, "SetIntegrationDirectionToBoth", ()))

    outline = timed_execution("outline_inst", introspector.createVtkObject, ("vtkStructuredGridOutlineFilter",))
    timed_execution("outline_setinputconn_reader_getoutputport", introspector.vtkInstanceCall, (outline, "SetInputConnection", (introspector.getVtkObjectOutputPort(reader),)))


if __name__ == '__main__':
    timed_execution("main", main)

    with open("py_introspection_vtk_benchmark.results", "w") as f:
        for name in time_execution_data:
            f.write(name + ", " + str(time_execution_data[name]) + "\n")
        f.close()