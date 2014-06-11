import sublime
import sublime_plugin


class SelectRectAreaCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        regions = self.view.sel()
        if len(regions) == 1 and len(self.view.lines(regions[0])) > 1:
            begin = self.view.rowcol(regions[0].begin())
            end = self.view.rowcol(regions[0].end())
        elif len(regions) == 2 and regions[0].empty() and regions[1].empty():
            begin = self.view.rowcol(regions[0].begin())
            end = self.view.rowcol(regions[1].begin())
        else:
            return
        row_range = (begin[0], end[0]) if begin[0] <= end[0] else (end[0], begin[0])
        regions.clear()
        for row in range(row_range[0], row_range[1] + 1):
            begin_point = self.view.text_point(row, begin[1])
            end_point = self.view.text_point(row, end[1])
            if self.view.rowcol(begin_point)[0] == row and self.view.rowcol(end_point)[0] == row:
                regions.add(sublime.Region(begin_point, end_point))
