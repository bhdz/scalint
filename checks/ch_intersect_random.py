from scalint.scalar_comparator import NativeComparator
from scalint.indexed_cursor import IndexedCursor as IC
from scalint.indexed_cursor import IndexedLoopCursor as ILC
from scalint.intersect import Intersect

def pick_one(min, max, **opts):
    noffset = 0
    
    if 'offset' in opts:
        noffset = opts.pop('offset')

    return noffset + random.randint(min, max)

def pick_series(min, max, count, **opts):
    opts2 = opts.copy()
    for x in xrange(0, count):
        yield pick_one(min, max, **opts2)

def pick_series_growing(nrange, nsubseries, ncount, **opts):
    nrange_ = nrange
    ncount_ = ncount
    nsubseries_ = nsubseries
    
    opts2 = opts.copy()
    
    if 'fixed_range' in opts:
        if opts.pop('fixed_range') == False:
            nrange_ = pick_one(0, range, **opts2)
        else:
            raise Exception("Be careful / type : fixed_range")
                        
    if 'fixed_count' in opts:
        if opts.pop('fixed_count') == False:
            ncount = pick_one(0, count, **opts2)
        else:
            raise Exception("Be careful / type : fixed_count")
            
    if 'random_subseries' in opts:
        nsubseries_ = pick_one(0, nsubseries, **opts2)
    elif 'fixed_subseries' in opts:
        nsubseries_ = nsubseries
        
    old = 0
    for _ in xrange(0, nsubseries_):
        for n in pick_series(old, old+nrange_, ncount_, **opts2):
            yield n
        old += nrange_

def check_pick_series_growing():
    print "pick_series_growing -from series_count=1 -with range_max=5 (Five numbers tops)"
    for x in pick_series_growing(5, 1, 1):
        print x,
    print ""
    print
    
    print "pick_series_growing -from series_count=5 -with range_max=5 (five series with five numbers tops each)"
    for x in pick_series_growing(5, 5, 5):
        print x,
    print ""
    print

    print "pick_series_growing -from series_count=5 -with range_max=5 -with fixed_count=True (five series with five numbers tops each)"
    c = 0
    for x in pick_series_growing(5, 5, 5, fixed_count=True):
        print x,
        c+=1
    print "count? {c}".format(c=c)
    print
    print
    
if __name__ == "__main__":
    print "Here I am testing the test code... :-) {{ test_wave? 1-1 }}"
    check_pick_series_growing()

    '''
    sets_cursor = ILC( IC ( (
                             IC ( ( 1,2,3,4,5,6,100,101,102,105 ) ), #0
                             IC ( (1,3,6,12,19,50,60,99,101,105 ) ),    #1
                             IC( (1,3,6,41,50,101,105) ), #2
                             IC( (1,3,6,8,9,10,11,12,50,51,90,101,105 )) #3
                             ) ) )
    expected_result =  [1, 3, 6, 101, 105]
    '''
    
def sets_gen(nsamples, ncount, **opts):
    # I am making some good code that takes random arguments data thru {{opts}}.
    # Thats why the remaining ?
    samples_ = nsamples
    ncount_ = ncount
    rang, subseriesn, count = None, None, None
    
    opts2 = opts.copy()
    
    if 'range' in opts:
        rang = opts.pop('range')
    if 'subseries' in opts:
        subseriesn = opts.pop('subseries')
    if 'ncount' in opts:
        count = opts.pop('ncount')
         
    sets = []
    for isample in xrange(0, samples_):
        sample_row = []
        for number in pick_series_growing(rang, subseriesn, count, **opt2):
            sample_row.append(number)
        sets.append(sample_row)
    return sets
    
def sets_cursor_gen(nsamples, ncount, rang, subseriesn, ncount):
    sets = sets_gen(nsamples, ncount, range=rang, subseries=subseriesn, ncount=ncount)
    sets_cursor = None

    for row in sets:
        rows.append(IC( tuple(*row) ))
    sets_cursor = ILC(IC(tuple(*rows)))
    return sets_cursor

'''
sets_cursor = ILC( IC ( (
IC ( ( 1,2,3,4,5,6,100,101,102,105 ) ), #0
IC ( (1,3,6,12,19,50,60,99,101,105 ) ),    #1
IC( (1,3,6,41,50,101,105) ), #2
IC( (1,3,6,8,9,10,11,12,50,51,90,101,105 )) #3
) ) )
'''

expected_result =  [1, 3, 6, 101, 105]
comparator = NativeComparator()

class ResultHandler(object):
    def __init__(self):
        self.store=list()
    def on_result(self,intersector,item):
        self.store.append( item )


r_handler = ResultHandler()
sect = Intersect( sets_cursor= sets_cursor , 
                  comparator=comparator, 
                  result_handler=r_handler )

try:
    sect()
except Exception, e:
    if type(e) is IndexError:
        print "sect done"
        print r_handler.store
        assert expected_result == r_handler.store
    else:
        raise e    


