#! /usr/bin/env python3

from gi.repository import Gtk

class CommandBar:
    """
    For this class, Command = input, Operation = output
    """
    def __init__(self):
        start_text = "Enter commands here"
        self._buffer = Gtk.EntryBuffer.new(start_text, len(start_text))
        self._entry = Gtk.Entry.new_with_buffer(self._buffer)

        self.words = ["new", "open", "save", "as", "undo", "redo", 
                        "cut", "copy", "paste", "delete", "help", "about", 
                        "typewriter"]

    ## TODO: find out what I can do here to make it parse commands
    @property
    def buffer(self):
        return self._buffer

    @property
    def entry(self):
        return self._entry

    @property
    def input(self):
        return self._buffer.get_text()

    @input.setter
    def input(self, value):
        self._buffer.set_text(value, len(value))
    
    def parse_command(self):
        """
        Gets the commands and processes them into operations
        """
        
        # semicolon is used like in C, separating multiple commands
        command_words = self.input.split()
        
        print(command_words)

        for word in command_words:
            if word in self.words:
                print(word)

if __name__ == "__main__":
    print("Starting basic test")
    cmd = CommandBar()
    cmd.input = "save a new file as untitled.txt"
    cmd.parse_command()

else:
    print("Imported command_bar")
