import sublime, sublime_plugin

class CopyWithLineNumbersCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		view = sublime.Window.active_view(sublime.active_window())
		# replace the following line with `output = ''` if you don't want file name copied.
		output = view.file_name() + "\n"
		for selection in view.sel():
			for line in view.lines(selection):
				output = output + str(view.rowcol(line.begin())[0] + 1) + ": " + view.substr(line) + "\n"
		sublime.set_clipboard(output)
