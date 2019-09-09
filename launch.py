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

   -list      list out all applications in the /Applications folder
   -help      print out this help information
   -sources   view all sources being indexed'''

class Launch:
    def __init__(self):
        self.index = {}
        self.applications = []
        self.directories = []
        self.contents = []
        self.keys = [
                      '-help',
                      '-list',
                      '-sources'
                     ]

        self.sources = [
                         '/Applications',
                         '/Users/craigcarter/Applications'
                       ]
                       
    def crawl(self, path):
        self.contents = []
        for ls in os.listdir(path):
            ls = ls.replace(' ', '\ ')
            self.contents.append('{}/{}'.format(path, ls))

    def check_file_type(self, path):
        app = path.split('/')
        for a in app:
            if '.app' in a:
                a = a.replace('.app','')
                if a not in self.applications:
                    self.applications.append('{}'.format(a))
                if a.lower() not in self.index:
                    self.index[a.lower()] = path

        if os.path.isdir(path) and '.app' not in path:
            self.directories.append('{}'.format(path))

    def get_applications(self):
        for source in self.sources:
            self.crawl(source)
            for content in self.contents:
                self.check_file_type(content)
            for directory in self.directories:
                self.crawl(directory)
                for content in self.contents:
                    self.check_file_type(content)

    def check_sources(self):
        for source in self.sources:
            if not os.path.exists(source):
                print(' err: bad source given -> {}'.format(source))
                exit()

    def check_args(self, args):
        if args == '-list':
            self.list_applications()
            return True
        elif args == '-help':
            print(INFO)
            return True
        elif args == '-sources':
            for source in self.sources:
                print(' > {}'.format(source))
            return True
        
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
    if launch.check_args(found_args) == True:
        exit()
    
    found_args = found_args.lower()
    found_args = found_args.replace('.app', '')
    found_args = found_args.replace(' ','\ ')

    if found_args in launch.index:
        app = launch.index[found_args]
        launch.launch_application(app)
    else:
        print(' err: no application found -> {}'.format(found_args))


