# Word Agent

Word Agent is a Python v3.x text editor that I'm building from scratch,
using Gtk+ for the GUI. This is my submission for the CS50x Final
Project and for LaunchCodeSTL consideration.

### Licence

I'm currently undecided if I want to licence this with a permissive
licence or GPL. This will be decided before v1.0. If you have interest
for proprietary use, please contact me.

### Instructions

To use the program, run `python3 word-agent.py` on the commandline. The
console should have debugging output like "Text autosaved."

It is based on Python 3.x and the Python GI API, so please have these
packages installed. So far, this is Linux only, including the CS50
Appliance. I claim no Windows, OSX, or BSD support. (However, a
good friend has told me it will run from Windows.)

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

In the future, along with my feature roadmap included in `features.md`,
I would like to modularize my code, add in the ability for others to
design new UI's for the program, using different modules as backends
for their projects. I would also like to make a few stylesheets for
Gtk+ and accessibility options, as well.
