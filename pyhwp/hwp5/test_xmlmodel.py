from unittest import TestCase
from . import test_binmodel
from .utils import cached_property

class TestBase(test_binmodel.TestBase):

    @cached_property
    def hwp5file_xml(self):
        from .xmlmodel import Hwp5File
        return Hwp5File(self.olestg)

    hwp5file = hwp5file_xml


class TestModelEventStream(TestBase):

    @cached_property
    def docinfo(self):
        from .xmlmodel import ModelEventStream
        return ModelEventStream(self.hwp5file, 'DocInfo',
                                self.hwp5file.header.version)

    def test_modelevents(self):
        self.assertEquals(len(list(self.docinfo.models())) * 2,
                          len(list(self.docinfo.modelevents())))
        #print len(list(self.docinfo.modelevents()))


class TestDocInfo(TestBase):

    @cached_property
    def docinfo(self):
        from .xmlmodel import DocInfo
        return DocInfo(self.hwp5file, 'DocInfo',
                       self.hwp5file.header.version)

    def test_events(self):
        events = list(self.docinfo.events())
        self.assertEquals(112, len(events))
        #print len(events)


class TestHwp5File(TestBase):

    def test_docinfo_class(self):
        from .xmlmodel import DocInfo
        self.assertTrue(isinstance(self.hwp5file.docinfo, DocInfo))


from .xmlmodel import make_ranged_shapes, split_and_shape
class TestShapedText(TestCase):
    def test_make_shape_range(self):
        charshapes = [(0, 'A'), (4, 'B'), (6, 'C'), (10, 'D')]
        ranged_shapes = make_ranged_shapes(charshapes)
        self.assertEquals([((0, 4), 'A'), ((4, 6), 'B'), ((6, 10), 'C'), ((10, 0x7fffffff), 'D')], list(ranged_shapes))

    def test_split(self):
        chunks = [((0, 3), None, 'aaa'), ((3, 6), None, 'bbb'), ((6, 9), None, 'ccc'), ((9, 12), None, 'ddd')]
        charshapes = [(0, 'A'), (4, 'B'), (6, 'C'), (10, 'D')]
        shaped_chunks = split_and_shape(iter(chunks), make_ranged_shapes(charshapes))
        shaped_chunks = list(shaped_chunks)
        self.assertEquals([
            ((0,3), ('A',None), 'aaa'),
            ((3,4), ('A',None), 'b'),
            ((4,6), ('B',None), 'bb'),
            ((6,9), ('C',None), 'ccc'),
            ((9, 10), ('C',None), 'd'),
            ((10, 12), ('D',None), 'dd')],
                shaped_chunks)

        # split twice
        chunks = [((0, 112), None, 'x'*112)]
        charshapes = [(0, 'a'), (3, 'b'), (5,'c')]
        linesegs = [(0, 'A'), (51,'B'), (103,'C')]
        shaped = split_and_shape(iter(chunks), make_ranged_shapes(charshapes))
        shaped = list(shaped)
        self.assertEquals([((0, 3), ('a', None), 'xxx'), ((3, 5), ('b',None), 'xx'), ((5,112), ('c',None), 'x'*107)], shaped)
        lines = split_and_shape(iter(shaped), make_ranged_shapes(linesegs))
        lines = list(lines)
        self.assertEquals([
            ((0,3), ('A', ('a', None)), 'xxx'), 
            ((3,5), ('A', ('b', None)), 'xx'), 
            ((5,51), ('A', ('c', None)), 'x'*(51-5)), 
            ((51,103), ('B', ('c', None)), 'x'*(103-51)), 
            ((103,112), ('C', ('c', None)), 'x'*(112-103)), ], lines)

from .xmlmodel import line_segmented
class TestLineSeg(TestCase):
    def test_line_segmented(self):
        chunks = [((0, 3), None, 'aaa'), ((3, 6), None, 'bbb'), ((6, 9), None, 'ccc'), ((9, 12), None, 'ddd')]
        linesegs = [(0, 'A'), (4, 'B'), (6, 'C'), (10, 'D')]
        lines = line_segmented(iter(chunks), make_ranged_shapes(linesegs))
        lines = list(lines)
        self.assertEquals([ ('A', [((0, 3), None, 'aaa'), ((3,4), None, 'b')]), ('B', [((4,6),None,'bb')]), ('C', [((6,9),None,'ccc'), ((9,10),None,'d')]), ('D', [((10,12),None,'dd')]) ], lines)
