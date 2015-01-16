import redis
from backend import *
"""
Testing module for word agent's backend
"""
def backend_test():
    print("Begin backend testing")
    print()
    print('Connecting to redis server, using db 14... ')
    r_server = redis.Redis(db=14)

    if (r_server.ping()):
        print("server ping sucessful")
    else:
        print("server ping failed")

    print("flushing db 14")
    r_server.flushdb()
    print()

    print("init default_segment")
    default_seg = Segment.new()
    print("edits list after init: ", default_seg.edits_list)
    print("edits list length: ", len(default_seg.edits_list))
    print()

    words = ["first", "second", "third", "fourth"]
    test_edits = []
    for word in words:
        test_edits.append(word)
    print("test edits list: ", test_edits)
    print("test edits length: ", len(test_edits))
    print()

    for edit in test_edits:
        default_seg.add_edit(edit)

    print("edits list after adding test edits: ", default_seg.edits_list)
    print("edits list length: ", len(default_seg.edits_list))
    print()

    print("testing undo action...")
    for i in range(0,(len(words)-1)):
        default_seg.undo()
        print("Undo #", i, ": ", default_seg.edits_list)
        print("edits list length: ", len(default_seg.edits_list))
        print("base_edit: ", default_seg.base_edit)
        print("prev_edit: ", default_seg.prev_edit)
        print("curr_edit: ", default_seg.curr_edit)
        print()

    print("testing redo action")
    for i in range(0,(len(words)-3)):
        default_seg.redo()
        print("Redo #", i, ": ", default_seg.edits_list)
        print("edits list length: ", len(default_seg.edits_list))
        print("base_edit: ", default_seg.base_edit)
        print("prev_edit: ", default_seg.prev_edit)
        print("curr_edit: ", default_seg.curr_edit)
        print()

    print("add edit, should truncate old edits from list")
    default_seg.add_edit("fifth")
    print("edits list after adding new edit: ", default_seg.edits_list)
    print("edits list length: ", len(default_seg.edits_list))
    print("base_edit: ", default_seg.base_edit)
    print("prev_edit: ", default_seg.prev_edit)
    print("curr_edit: ", default_seg.curr_edit)
    print()
