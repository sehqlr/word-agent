# Word Agent Features & Roadmap

My roadmap for the project is outlined below,
but it can be changed depending upon Word Agent's userbase, if anyone.

### Current Features for v0.2.x

##### Basic Editor Features

* Cut/Copy/Paste
* New/Open/Save(As)
* Undo/Redo
* About Dialog
* Help Dialog
* Keyboard shortcuts
* Toolbar with basic features as buttons, with the option of 
hiding it with F3. I call this "typewriter mode."

There are currently is no formatting tools. See below.

### Future Features, introduced in odd-numbered releases



##### Novel Project Management:

* Segment centric

Your large text file is kept in smaller "segments" with an internal
database to keep track of where they belong in the scheme of the larger
document. These files will not contain implicit formatting or metadata.

* Project rendering and formatting

Word Agent will "render" the larger document by concatenating
the segments together when the full project is needed. Additionally,
the document will be formatted at this stage, with either an internal
module or external tools (like Markdown) at the user's option.

* Export to eReader formats

Word Agent will export to eReader formats such as ePub and Mobi, as
well as PDF and related page formats.

* Character Database

Special segments that contain a character description, and each segment
of the project that includes a reference to that character. Another
idea is to support photographs and images to the character's entry.

* Novel support, others later

To begin with, this program will have novels as the target
project type. Support for academic papers, stage/screenplays, and other
long works will be supported later.

##### Version Control System

This feature will take ideas from programs like Git and Mercurial
for version control of the project. I will design a simple VCS module 
for internal use, using difflib. Integration with external tools will
come later.

##### Cloud Collaboration

This feature will connect instances of the program, so
users can work on projects concurrently. This is where the VCS feature
will come in handy, as the deltas can be traded in a data channel.

I think I may go as far as supporting text chat, but I will rely on
external web conferencing tools rather than build internally.

##### Possible other features

* Distraction-free "Composition" mode

Modeled after FocusWriter and PyRoom, this feature is a fullscreen
"composition" mode that tries to keep the writing going. This feature
will have to get user imput on what works for them, and perhaps this
will support user-built plugins. The composition tools may be things
like timers, music, name generators, and other tools.

This feature is implemented in part with "typewriter mode," but I will
need to expand upon it with the above features.

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

This is an experimental feature, inspired by the text editor, vim.
I love the command environment, but I feel like there is a learning
curve, and it's not easy to implement in a way that makes sense in 
a windowed environment. So, my idea is to create a Command Bar,
a TextEntry widget that parsing a command input, and performs 
operations. For example, type "Save file as ~/Documents/foo.txt" and
the program would set the filename as foo.txt with the path, and then
perform the File/Save operation. 

As I said, this is an experimental feature, and I have no idea how
useful this would be to anyone but me.
