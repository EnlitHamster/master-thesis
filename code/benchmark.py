import vtk

import inspect

import time


def test_SetCenter(source_name, source_class, itl, ntl):
    # Inspect version
    start = time.perf_counter()
    source_obj = lookup_classes[source_name]()
    dict(inspect.getmembers(source_obj))['SetCenter'](0.1, 0.1, 0.1)
    end = time.perf_counter()
    itl.append((end - start))

    # Native version
    start = time.perf_counter()
    source_obj = source_class()
    source_obj.SetCenter(0.1, 0.1, 0.1)
    end = time.perf_counter()
    ntl.append((end - start))


def test_SetTipLength(source_name, source_class, itl, ntl):
    # Inspect version
    start = time.perf_counter()
    source_obj = lookup_classes[source_name]()
    dict(inspect.getmembers(source_obj))['SetTipLength'](0.1)
    end = time.perf_counter()
    itl.append((end - start))

    # Native version
    start = time.perf_counter()
    source_obj = source_class()
    source_obj.SetTipLength(0.1)
    end = time.perf_counter()
    ntl.append((end - start))


def test_SetInnerRadius(source_name, source_class, itl, ntl):
    # Inspect version
    start = time.perf_counter()
    source_obj = lookup_classes[source_name]()
    dict(inspect.getmembers(source_obj))['SetInnerRadius'](0.1)
    end = time.perf_counter()
    itl.append((end - start))

    # Native version
    start = time.perf_counter()
    source_obj = source_class()
    source_obj.SetInnerRadius(0.1)
    end = time.perf_counter()
    ntl.append((end - start))


def test_SetRadius(source_name, source_class, itl, ntl):
    # Inspect version
    start = time.perf_counter()
    source_obj = lookup_classes[source_name]()
    dict(inspect.getmembers(source_obj))['SetRadius'](0.1)
    end = time.perf_counter()
    itl.append((end - start))

    # Native version
    start = time.perf_counter()
    source_obj = source_class()
    source_obj.SetRadius(0.1)
    end = time.perf_counter()
    ntl.append((end - start))


def test_SetLinesLength(source_name, source_class, itl, ntl):
    # Inspect version
    start = time.perf_counter()
    source_obj = lookup_classes[source_name]()
    dict(inspect.getmembers(source_obj))['SetLinesLength'](0.1)
    end = time.perf_counter()
    itl.append((end - start))

    # Native version
    start = time.perf_counter()
    source_obj = source_class()
    source_obj.SetLinesLength(0.1)
    end = time.perf_counter()
    ntl.append((end - start))


def test_SetResolution(source_name, source_class, itl, ntl):
    # Inspect version
    start = time.perf_counter()
    source_obj = lookup_classes[source_name]()
    dict(inspect.getmembers(source_obj))['SetResolution'](100)
    end = time.perf_counter()
    itl.append((end - start))

    # Native version
    start = time.perf_counter()
    source_obj = source_class()
    source_obj.SetResolution(100)
    end = time.perf_counter()
    ntl.append((end - start))


def test_SetBounds(source_name, source_class, itl, ntl):
    # Inspect version
    start = time.perf_counter()
    source_obj = lookup_classes[source_name]()
    dict(inspect.getmembers(source_obj))['SetBounds'](0.1, 0.1, 0.1, 0.1, 0.1, 0.1)
    end = time.perf_counter()
    itl.append((end - start))

    # Native version
    start = time.perf_counter()
    source_obj = source_class()
    source_obj.SetBounds(0.1, 0.1, 0.1, 0.1, 0.1, 0.1)
    end = time.perf_counter()
    ntl.append((end - start))


# Each of the sources first generates the inspected version
# and applies the method with the param, then the native version
# is run doing the same thing, the timing results are appended
# to the respective lists; this is then repeated n_iter times
# and the average is computed. The function finally returns the
# average of both, the overhead factor of inspect and the two lists
def test_source(source_name, source_class, n_iter, test_func):
    inspect_time_list = []
    native_time_list = []

    for i in range(n_iter):
        print('Iteration', i, 'of', source_name)
        test_func(source_name, source_class, inspect_time_list, native_time_list)

    inspect_time_avg = sum(inspect_time_list) / n_iter
    native_time_avg = sum(native_time_list) / n_iter
    overhead_factor_avg = inspect_time_avg / native_time_avg

    return (inspect_time_avg, native_time_avg, overhead_factor_avg, inspect_time_list, native_time_list)


def main():
    global lookup_classes

    # Creating the introspection lookup
    start = time.perf_counter()
    lookup_classes = dict(inspect.getmembers(vtk, inspect.isclass))
    end = time.perf_counter()

    time_lookup_classes_generation = end - start;

    # All filter sources to test, the average overhead factor will be considered the
    # introspection overhead factor
    sources = [
        ('vtkArrowSource', vtk.vtkArrowSource, test_SetTipLength), 
        ('vtkConeSource', vtk.vtkConeSource, test_SetCenter), 
        ('vtkCubeSource', vtk.vtkCubeSource, test_SetCenter), 
        ('vtkCylinderSource', vtk.vtkCylinderSource, test_SetCenter), 
        ('vtkDiskSource', vtk.vtkDiskSource, test_SetInnerRadius), 
        ('vtkEarthSource', vtk.vtkEarthSource, test_SetRadius), 
        ('vtkFrustumSource', vtk.vtkFrustumSource, test_SetLinesLength), 
        ('vtkLineSource', vtk.vtkLineSource, test_SetResolution), 
        ('vtkSphereSource', vtk.vtkSphereSource, test_SetCenter), 
        ('vtkTessellatedBoxSource', vtk.vtkTessellatedBoxSource, test_SetBounds)
    ]

    output = open('results.log', 'w')
    output.write('Results of Introspection Python VTK run\n\n')
    output.write('Class Lookup generation time: {}\n'.format(time_lookup_classes_generation))

    for source_name, source_class, test_func in sources:
        ita, nta, ofa, itl, ntl = test_source(source_name, source_class, 10, test_func)
        output.write('\nResults for {}\n'.format(source_name))
        output.write('\tInspect average time: {}\n'.format(ita))
        output.write('\tNative average time: {}\n'.format(nta))
        output.write('\tOverhead average factor: {}\n'.format(ofa))
        output.write('\tInspect times: {}\n'.format(itl))
        output.write('\tNative times: {}\n'.format(ntl))

    output.close()


if __name__ == '__main__':
    main()