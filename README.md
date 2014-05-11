# Word Agent

Word Agent is a Python v3.x text editor that I'm building from scratch,
using Gtk+ for the GUI. This is my submission for the CS50x Final
Project and for LaunchCodeSTL consideration.

### Licence

I'm currently undecided if I want to licence this with a permissive
licence or GPL. This will be decided before v1.0. If you have interest
for proprietary use, please contact me.

### Instructions

Word Agent currently exists as a Python script run from the commandline.
It is based on Python 3.x and the Python GI API, so please have these
packages installed. So far, this is Linux only (including the CS50
Appliance v19). I claim no Windows, OSX, or BSD support.

To use the program, the `run.py` script will serve you best.
I plan on creating unit tests in the future, as well has proper
setup/installation scripts.

### Version Numbering

I will follow the convention of X.Y.Z version numbering.
* X numbers indicate project maturity and major revisions, including UX
changes.
* Even-numbered Y's will indicate work on improving existing features,
and odd-numbered Y's indicate work on new features. The idea is that a
new feature will be introduced in an odd number, and finalized in the
next even number in the sequence.
* Z increments for each revision.
It will likely contain the date of the revision

### Features & Roadmap

My mental roadmap for the project is outlined below,
but it can be changed depending upon Word Agent's userbase, if anyone.

##### Basic Features

Basic features include Cut/Copy/Paste, New/Open/Save(As), Undo/Redo,
and an About Dialog.

There are currently no keyboard shortcuts, nor is there any formatting.

##### Novel Project Management (starting v0.3):

These features will be similar to yWriter, Plume Creator, and others.

It will break the large document into smaller plaintext "segments" with
an internal database to keep track of where they belong in the scheme
of the larger document. Word Agent will "render" the larger document
by concatenating the segments together when the full project is needed.

These segments will be simple UTF-8 files with no implicit markup or
formatting, for compatiblity with external tools and other programs, at
 the user's option. Markdown and other tools will be supported for an
 internal formatting module. This formatting would be applied during the
 "project rendering" stage as mentioned above.

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

###### Distraction-free "Composition" mode

Modeled after FocusWriter and PyRoom, this feature is a fullscreen
"composition" mode that tries to keep the writing going. This feature
will have to get user imput on what works for them, and perhaps this
will support user-built plugins. The composition tools may be things
like timers, music, name generators, and other tools.

###### Project Scheduler

An alert system for users sent via email (or text chat, beginning in
v1.5) for actions decided among users. This could include things such as
benchmarks for peer editing, number of pages, and so on. This could
include a "segment locker" feature that prevents multiple users from
editing the same segment.

###### Visual Merge Conflict Resolution

In case of a merge conflict, the two files can be shown side by side so
that the users can negotiate how to solve the merge conflict. Because
this is creative writing, merge conflicts can be easier to solve
visually.

### Design and Development

Word Agent was inspired by programs such as yWriter and Plume Creator,
programs that help writers working on a long text document. The cloud
collaboration idea was also fueled by a need for creators to work
together in a way that is not based on a corporate service.

While thinking about which project to work on for CS50 and LaunchCode,
I decided that these two features could work together nicely, Thus,
I started work on Word Agent.

I decided upon Python, because it was the first language that I started
teaching myself successfully before CS50. I didn't get very far, but
having an English major background, I appreciated Python's focus on
readability. Also, because Python is multiparadigm, I figured that
I could use procedural, object-oriented, and functional approaches in my
toolbelt and my CV.

In the future, along with my feature roadmap above, I would like to
modularize my code, add in the ability for others to design new UI's for
the program, using different modules as backends for their projects.
I would also like to make a few stylesheets for Gtk+ and accessibility
options, as well.
