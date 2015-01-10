# Word Agent Features & Roadmap

My roadmap for the project is outlined below,
but it can be changed depending upon the userbase, if anyone.

### Current Features for v0.2.2

##### Basic Editor Features

* Cut/Copy/Paste
* New/Open/Save(As)
* Undo/Redo
* About Dialog
* Help Dialog
* Toolbar with all features
* Keyboard shortcuts
* "Typewriter" mode (F3)

There are currently is no formatting tools. See below.

### Future Features

##### Web App:

This is the feature that I'm currently working on, using Flask.
I plan on focusing on including as few microframeworks as possible.

##### Novel Project Management:

* Segment centric

Your large text file is kept in smaller "segments" with a
database to keep track of where they belong in the scheme of the larger
document. These files will be non-formatted plaintext, for maximum
compatibility across systems.

* Project rendering and formatting

Word Agent will "render" the larger document by concatenating
the segments together when the file is needed. The web interface will
feature an infinite scroll type interface, so the segmented files can be
invisible to the user.

Formatting for the document will be a different step, with either an internal
module or external tools (like Markdown) at the user's option. I want to
build it this way so that the composition of text is not distracted by the
formatting of text.

* Export to eReader formats

Word Agent will eventually export to eReader formats such as ePub and Mobi, as
well as PDF and related page formats.

* Resource Database

A Resource is a special segments that contain metadata about characters,
places, source materials, and other research. The idea is to be able to
track where important resources are located in the segments
of the project. Another idea is to support image.

* Novel support, others later

To begin with, this program will have novels as the target
project type. Support for academic papers, stage/screenplays, and other
long works will be supported later.

##### Versioning

This feature ideas from programs like Git and Mercurial
for version control of the project. The internal version of this module
will simply store diffs of the segments as separate files. Integration with
external tools shouldn't be too complex.

##### Cloud Collaboration

This feature will connect instances of the program, so
users can work on projects concurrently. This is where the VCS feature
will come in handy, as the deltas can be traded in a data channel.

I think I may go as far as supporting text chat, but I will rely on
external web conferencing tools rather than build internally.

##### Possible other features

* Expanded Typewriter mode

Modeled after FocusWriter and PyRoom, this feature
will have to get user imput on what works for them, and perhaps this
will support user-built plugins. The composition tools may be things
like timers, music, name generators, and other tools.

* Project Scheduler

An alert system for users sent via email (or text chat, beginning in
v1.5) for actions decided among users. This could include things such as
benchmarks for peer editing, number of pages, and so on. This could
include a "segment locker" feature that prevents multiple users from
editing the same segment.

* Visual Merge Conflict Resolution

In case of a merge conflict, the two files can be shown side by side so
that the users can negotiate how to solve the merge conflict. Because
this is creative writing, merge conflicts can be easier to solve
visually.

* Command Bar:

This would be experimental feature, inspired by the text editor, vim.
I love the command environment, but I feel like there is a learning
curve, and it's not easy to implement in a way that makes sense in
a windowed environment. So, my idea is to create a Command Bar,
a widget that parses a command input, and performs
operations. For example, type "Save file as ~/Documents/foo.txt" and
the program would set the filename as foo.txt with the path, and then
perform the File/Save operation.

Probably what will happen is that I would just build out a VIM plugin
to interface with the web app.
