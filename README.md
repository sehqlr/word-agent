# Word Agent

Word Agent is a Python v3.x text editor that I'm building from scratch.
This is my submission for the CS50x Final
Project and for LaunchCodeSTL consideration.

### Licence

More than likely, I'm going to dual licence this with a GPL-compatible
licence, and a permissive licence. Which ones in particular is the
question. It's not pressing issue, because no one is going to want to
use this just yet.

### Instructions

##### STABLE
The current stable version is v0.2.2. Checkout that tag, or download
the tarball or zip to get the source.

To use the program, run `python3 word_agent.py` or `./word_agent.py`
on the commandline. The console should have debugging output, such as
"Text autosaved."

It is based on Python 3.x and the Python GI API, so please have these
packages installed. I have tested this on Linux only, including the CS50
Appliance. I claim no Windows, OSX, or BSD support. (However, a
good friend has told me it will run from Windows.)

##### DEVELOPMENT
Word Agent is getting Flaskified, and eventually containerized,
so in this version, GTK+ is no longer a dependency, and once the
containerization is complete, that container will be the only
dependency. Because I'm turning the front end into a web app,
I could deploy it some time.

In order to run the most recent state of the dev code, checkout
the `flask` branch, and run `./server.py` For debugging,
run `./app.py` instead.

The `backend` module is the most stable part of the app,
and if you run `./modules/backend.py` you will see it's
(simple!) testing script.

### Version Numbering

Once this app reaches v1.0, I might have established a good habit
for numbering things. Before then, version numbers are at my whim.

### Design and Development

Word Agent was inspired by programs such as yWriter and Plume Creator,
programs that help writers working on a long text document. At the time,
I also saw a need for collaboration not based on a corporate service.

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
for their projects. I would also like to add accessibility as well.
