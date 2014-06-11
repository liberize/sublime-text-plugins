import sublime
import sublime_plugin


class FilterLinesCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        selections = self.view.sel()
        if len(selections) != 1:
            return
        pattern = self.view.substr(selections[0])
        lines = self.view.lines(selections[0])
        if pattern == '' or len(lines) != 1:
            return

        region = sublime.Region(0, self.view.size())
        lines = self.view.split_by_newlines(region)

        for line in reversed(lines):
            if pattern not in self.view.substr(line):
                self.view.erase(edit, self.view.full_line(line))
