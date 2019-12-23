#!/usr/bin/python
import curses
import npyscreen

npyscreen.TEST_SETTINGS['TEST_INPUT'] = [ch for ch in 'This is a test']
npyscreen.TEST_SETTINGS['TEST_INPUT'].append(curses.KEY_DOWN)
npyscreen.TEST_SETTINGS['CONTINUE_AFTER_TEST_INPUT'] = True

class TestForm(npyscreen.Form):
    def create(self):
        self.myTitleText = self.add(npyscreen.TitleText,
                                    name="Events (Form Controlled):",
                                    editable=True)

    def afterEditing(self):
        '''
        next form is none so ends program
        :return:
        '''
        self.parentApp.setNextForm(None)


# what's the difference between NPSAppManaged and Standard App?
# class TestApp(npyscreen.StandardApp):
class TestApp(npyscreen.NPSAppManaged):
    def onStart(self):
        self.registerForm("MAIN", TestForm())
        # don't use self.addForm


if __name__ == '__main__':
    A = TestApp()
    A.run(fork=False)
    # 'This is a test' will appear in the first widget, as if typed by the user.