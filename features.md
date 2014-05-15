# Word Agent Features & Roadmap

My roadmap for the project is outlined below,
but it can be changed depending upon Word Agent's userbase, if anyone.

### Current Features for v0.2

##### Basic Editor Features

* Cut/Copy/Paste
* New/Open/Save(As)
* Undo/Redo
* About Dialog

There are currently no keyboard shortcuts, nor is there any formatting.

### Future Features, introduced in odd-numbered releases

##### Novel Project Management (starting v0.3):

* Segment centric

Your large text file is kept in smaller "segments" with an internal
database to keep track of where they belong in the scheme of the larger
document. These files will not contain implicit formatting or metadata

* Project rendering and formatting

Word Agent will "render" the larger document by concatenating
the segments together when the full project is needed. Additionally,
the document will be formatted at this stage, with either an internal
module using Markdown or other lightweight markup, or external tools
at the user's option.

* Export to eReader formats

Word Agent will export to eReader formats such as ePub and Mobi, as
well as PDF and related page formats.

* Character Database

Special segments that contain a character description, and each segment
of the project that includes a reference to that character. Another
idea is to support photographs and images to the character's entry.

* Novel support, others later

Up until Version 1.1, this program will have novels as the target
project type. Support for academic papers, stage/screenplays, and other
long works will be supported starting in version 1.1.

##### Version Control System Integration (starting v0.5)

VCS Integration will feature Git, Mercurial, and other VCS programs.
This will be useful for collaborative projects, and for a nice history
feature.

Mercurial will be the only one supported until version 1.3, since the
project will be written in Python, and I can include the Mercurial
scripts with the program as an additional module (I think). My
assumption is that many of the users of this program will not have VCS
programs on their machines by default. However, starting in version 1.3,
I will build support for the common ones, primarily Git.

##### Cloud Collaboration (starting v0.7)

This feature will use WebRTC technology, and possibly Node.js or some
similar technology if needed, that connects instances of the program, so
users can work on projects concurrently. This is where the VCS feature
will come in handy, as the deltas can be traded in a data channel.

Text chat support will begin in Version 1.5, and video and audio chat,
if supported, will appear some time in Version 2.

##### Possible other features for v1.0 and beyond

* Distraction-free "Composition" mode

Modeled after FocusWriter and PyRoom, this feature is a fullscreen
"composition" mode that tries to keep the writing going. This feature
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
