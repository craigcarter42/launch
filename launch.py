#!/usr/bin/env python
try:
    import os
    import sys
    import fnmatch
    import subprocess
except:
    print('module import error'); quit()

# ToDo:
#   Index multiple folders
#   Store index information in conf file
#   Create shortcuts for applications
#   Index/Re-Index/Delete Index options
#   Autocompletion of application names
#   Allow for importing

INFO = '''-- launch v.1
   Quickly index and launch applications in located in the /Applications folder
   in macOS. Applications nested within folders will not be found.

   --list    list out all applications in the /Applications folder
   --help    print out this help information'''

class Launch:
    def __init__(self):
        self.applications = []
        self.source = '/Applications'
        self.index = []

    def get_applications(self, count=0):
        apps = os.listdir(self.source)
        for app in apps:
            if fnmatch.fnmatch(app, '*.app'):
                self.applications.append(app)
                count = count + 1
        return(self.applications)
        
    def list_applications(self, count=1):
        for app in self.applications:
            print(' > {}. {}'.format(count, app))
            count = count + 1

    def index_applications(self):
        for app in self.applications:
            if ' ' in app:
                app = app.replace(' ', '\ ')
                self.index.append(app)
            else:
                self.index.append(app)
        return(self.index)

    def launch_application(self, app):
        cmd = "/usr/bin/open " + self.source + '/' + app
        out = os.system(cmd)
        if out != 0:
            print('err: occured({})'.format(out))

if __name__ == '__main__':
    launch = Launch()
    launch.get_applications()
    launch.index_applications()

    args = sys.argv
    if len(args[1:]) == 0: print('try: --help'); quit()
    found_args = ' '.join(args[1:])
    
    if found_args == '--list':
        launch.list_applications()
    elif found_args == '--help':
        print(INFO)
        
    found_args = found_args.replace(' ', '\ ')
    if '.app' not in found_args:
        found_args = found_args + '.app'
    if found_args in launch.index:
        launch.launch_application(found_args)
