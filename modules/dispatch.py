from modules.backend import Segment

def file_new(**kwargs):
    if kwargs is not None:
        designation = kwargs.pop("designation")
        content     = kwargs.pop("content")
        return Segment.new(designation=designation, content=content)
    else:
        return Segment.new()

def file_open(**kwargs):
    if kwargs is not None:
        designation = kwargs.pop("designation")
        content     = kwargs.pop("content")
        return Segment.open(designation=designation, content=content)
    else:
        return Segment.open()

def file_save():
    r_server.bgsave()

def edit_undo():
    segment.undo()

def edit_redo():
    segment.redo()

def edit_add(text):
    text = str(text)
    segment.add_edit(text)

dispatchers = {
    "file_new": file_new,
    "file_open": file_open,
    "file_save": file_save,
    "edit_undo": edit_undo,
    "edit_redo": edit_redo,
    "edit_add": edit_add,
    }
