#!/usr/bin/env python
try:
    import os
    import sys
    import subprocess
except:
    print('module import error'); quit()

# ToDo:
#   Index multiple folders
#   Store index information in conf file
#   Create shortcuts for applications
#   Index/Re-Index/Delete Index options
#   Autocompletion of application names
#   oswalk

INFO = '''-- launch v.1
   Quickly index and launch applications in located in the /Applications folder
   in macOS. Applications nested within folders will not be found.

   --list    list out all applications in the /Applications folder
   --help    print out this help information'''

class Launch:
    def __init__(self):
        self.applications = []
        self.source = '/Applications'
        self.index = {}

    def get_applications(self, count=0):
        apps = os.listdir(self.source)
        for app in apps:
            if '.app' in app:
                app = app.replace('.app', '')
                self.applications.append(app)
                self.index[app.lower()] = app
                count = count + 1
        return(self.applications)
        
    def list_applications(self, count=1):
        for app in self.applications:
            print(' > {}. {}'.format(count, app))
            count = count + 1

    def launch_application(self, app):
        cmd = "/usr/bin/open " + self.source + '/' + app
        out = os.system(cmd)
        if out != 0:
            print('err: occured({})'.format(out))

if __name__ == '__main__':
    launch = Launch()
    launch.get_applications()

    args = sys.argv
    if len(args[1:]) == 0: print('try: --help'); quit()
    found_args = ' '.join(args[1:])
    
    if found_args == '--list':
        launch.list_applications()
    elif found_args == '--help':
        print(INFO)
        
    found_args = found_args.lower()
    found_args = found_args.replace('.app', '')
    if found_args in launch.index:
        app = launch.index[found_args]
        app = app.replace(' ', '\ ')
        app = app + '.app'
        launch.launch_application(app)
