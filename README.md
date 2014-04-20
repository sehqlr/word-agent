word-agent
==========

Word Agent is a Python3 text editor that I'm building with modules from the Python Standard Library.
This is my submission for the CS50x Final Project. 

Currently, I'm working on the save/undo/redo feature. File IO is coming next.

After that, features will include novel project management, integrated version control, and cloud collaboration tools.

Novel Project management will feature tools similar to yWriter, Plume Creator, and others. 
It will break the large document into smaller plaintext "segments" with a database to keep track of them.
The project is not just for novels, other long-form projects will be supported. 

Version Control System integration will feature Git, Mercurial, and other VCS programs. I'm not predicting that
more advanced features on these will not be used. Because of this, and the fact that the program is written in Python, 
I think that Mercurial will be the default. I will most certainly support Git thought, because I'm not a git myself.

Cloud Collaboration will feature WebRTC technology that connects instances of the program, so users can work on projects
concurrently. This is where the VCS feature will come in handy.

Other features could include Segment Lock Scheduler (people can access certain files on a schedule list during online sessions), 
WebRTC Conferencing (for discussion among collaborators), and Visual Merge Conflict Resolution (basically, drag and drop)

I'm planning on making this a long term project after CS50x is over, because I participate in NaNoWriMo and do other
writings, and I like to collaborate with others online on creative projects. 
