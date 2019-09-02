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

INFO = '''-- launch v.2
   Quickly index and launch applications in located in the /Applications folder
   in macOS. Applications nested within folders will not be found.

   --list    list out all applications in the /Applications folder
   --help    print out this help information'''

class Launch:
    def __init__(self):
        self.index = {}
        self.applications = []
        self.keys = ['-help',
                     '-list',
                     '-sources'
                     ]
        self.sources = ['/Applications',
                        '/Applications/Utilities'
                       ]

    def check_sources(self):
        for source in self.sources:
            if not os.path.exists(source):
                print(' err: bad source given -> {}'.format(source))
                exit()

    def check_args(self, args):
        if args == '-list':
            self.list_applications(); exit()
        elif args == '-help':
            print(INFO); exit()
        elif args == '-sources':
            for source in self.sources:
                print(' > {}'.format(source))
            exit()

    def get_applications(self, count=1):
        for source in self.sources:
            apps = os.listdir(source)
            for app in apps:
                if '.app' in app:
                    app = app.replace('.app', '')
                    self.applications.append(app)
                    app_lower = app.lower()
                    app_path = source + '/' + app
                    self.index[app.lower()] = app_path
                    count = count + 1
        return(self.applications)
        
    def list_applications(self, count=1):
        for app in self.applications:
            print(' > {}. {}'.format(count, app))
            count = count + 1

    def launch_application(self, app):
        cmd = '/usr/bin/open {}'.format(app)
        out = os.system(cmd)
        if out != 0:
            print(' err: error ({})\n err: could not launch -> {}'.format(out, app))

if __name__ == '__main__':
    launch = Launch()
    launch.check_sources()
    launch.get_applications()

# Check for and parse user input
    args = sys.argv
    if len(args[1:]) == 0: print(' try: --help'); quit()
    found_args = ' '.join(args[1:])
    launch.check_args(found_args)
            
    found_args = found_args.lower()
    found_args = found_args.replace('.app', '')
    if found_args in launch.index:
        app = launch.index[found_args]
        app = app.replace(' ', '\ ')
        app = app + '.app'
        launch.launch_application(app)
    else:
        print(' err: no application found -> {}'.format(found_args))





