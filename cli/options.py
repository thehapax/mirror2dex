#!/usr/bin/env python
# encoding: utf-8

# The system here is an experimental one. See documentation for details.
import npyscreen

DEFAULT_CONFIG_FILE  = 'tmp/test'

class TestApp(npyscreen.NPSApp):

    def __init__(self, config=None):
        super().__init__()
        if config:
            self.default_file = config
        else:
            self.default_file = DEFAULT_CONFIG_FILE

    def main(self):
        Options = npyscreen.OptionList()
        
        # just for convenience so we don't have to keep writing Options.options
        options = Options.options
        
        options.append(npyscreen.OptionFreeText('FreeText', value='', documentation="This is some documentation."))
        options.append(npyscreen.OptionMultiChoice('Multichoice', choices=['Choice 1', 'Choice 2', 'Choice 3']))
        options.append(npyscreen.OptionFilename('Filename', self.default_file))
        options.append(npyscreen.OptionDate('Date', ))
        options.append(npyscreen.OptionMultiFreeText('Multiline Text', value=''))
        options.append(npyscreen.OptionMultiFreeList('Multiline List'))
        
        try:
            Options.reload_from_file('/tmp/test')
        except FileNotFoundError:
            pass        
        
        F  = npyscreen.Form(name = "Welcome to Npyscreen",)

        ms = F.add(npyscreen.OptionListDisplay, name="Option List", 
                values = options, 
                scroll_exit=True,
                max_height=None)
        
        F.edit()

        Options.write_to_file(self.default_file)


if __name__ == "__main__":
    App = TestApp()
    App.run()   
