class Exporter:
    def __init__(self, textName):
        self.CLIPBOARD_OPTION = "clipboard"
        self.FILE_OPTION = "file"
        self.EXPORT_OPTIONS = [self.CLIPBOARD_OPTION, self.FILE_OPTION]

        self.filename = None
        self.exportTo = None
        self.textName = textName

    def addArgumentsToParser(self, parser):
        parser.add_argument('--export-to', required=True, help=" or ".join(["'"+option+"'" for option in self.EXPORT_OPTIONS]))
        parser.add_argument('--file-name', help='filename if you choose "%s" for exporting' % self.FILE_OPTION)


    def parseArguments(self, args):
        self.exportTo = args.export_to
        self.filename = None

        if self.exportTo not in self.EXPORT_OPTIONS:
            print "option has to be in "+str(self.EXPORT_OPTIONS)
            return False

        if self.exportTo == self.FILE_OPTION:
            if args.file_name != None:
                self.filename = args.file_name
            else:
                print "you have to specify a filename using --file-name"
                return False
        return True


    def exportText(self, text):
        if self.exportTo == self.FILE_OPTION:
            try:
                with open(self.filename, 'w') as file:
                    file.write(text)
            except Exception as e:
                print "Could not print to file"
                print e
                print "Press enter to print %s here:" % self.textName
                raw_input()
                print text

        elif self.exportTo == self.CLIPBOARD_OPTION:
            import pyperclip
            pyperclip.copy(text)
            print "%s is in your clipboard now" % self.textName