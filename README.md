# Word Agent

Word Agent is a Python text editor that I'm building from scratch, with modules from the version 3.3 of the Python Standard Library, version 3 of GTK+, and version 3 of the Glade UI designer.
This is my submission for the CS50x Final Project.

I'm currently undecided if I want to licence this with a permissive licence or GPL. This will be decided in v0.2

I will follow the convention of X.Y.Z version numbering.
* X numbers indicate project maturity and major revisions, including UX changes.
* Even-numbered Y's will indicate work on improving existing features, and odd-numbered Y's indicate work on new features. The idea is that a new feature will be introduced in an odd number, and finalized in the next even number in the sequence.
* Z increments for each revision. If there is going to be an additional version number after Z, it will indicate the date of the revision.

My mental roadmap for the project is outlined below, but it can be changed depending upon Word Agent's userbase.

### Basic Features (started in v0.1, finished by v0.2)

Currently, I'm working on some of the standard text editor features, which include File IO and cut/copy/paste. Text formatting will not be included in this version.

### Novel Project Management (starting v0.3):

These features will be similar to yWriter, Plume Creator, and others.

It will break the large document into smaller plaintext "segments" with an internal database to keep track of where they belong in the scheme of the larger document. Word Agent will "render" the larger document by concatenating the segments together when the full project is needed.

These segments will be simple UTF-8 files with no implicit markup or formatting, for compatiblity with external tools and other programs, at the user's option. Markdown and other tools will be supported for an internal formatting module. This formatting would be applied during the "project rendering" stage as mentioned above.

Up until Version 1.1, this program will have novels as the target project type. Support for academic papers, stage/screenplays, and other long works will be supported starting in version 1.1.


### Version Control System Integration (starting v0.5)

VCS Integration will feature Git, Mercurial, and other VCS programs. This will be useful for collaborative projects, and for a nice history feature.

Mercurial will be the only one supported until version 1.3, since the project will be written in Python, and I can include the Mercurial scripts with the program as an additional module. My assumption is that many of the users of this program will not have VCS programs on their machines by default. However, starting in version 1.3, I will build support for the common ones, primarily Git.

### Cloud Collaboration (starting v0.7)

This feature will use WebRTC technology, and possibly Node.js or some similar technology if needed, that connects instances of the program, so users can work on projects concurrently. This is where the VCS feature will come in handy, as the deltas can be traded in a data channel.

Text chat support will begin in Version 1.5, and video and audio chat, if supported, will appear some time in Version 2.

### Possible other features for v1.0 and beyond

##### Distraction-free "Composition" mode

Modeled after FocusWriter and PyRoom, this feature is a fullscreen "composition" mode that tries to keep the writing going. This feature will have to get user imput on what works for them, and perhaps this will support user-built plugins. The composition tools may be things like timers, music, name generators, and other things to keep things going

##### Project Scheduler

An alert system for users sent via email (or text chat, beginning in v1.5) for actions decided among users. This could include things such as benchmarks for peer editing, number of pages, and so on. This could include a "segment locker" feature that prevents multiple users from editing the same segment.

##### Visual Merge Conflict Resolution

In case of a merge conflict, the two files can be shown side by side so that the users can negotiate how to solve the merge conflict. Because this is creative writing, merge conflicts can be easier to solve visually.
