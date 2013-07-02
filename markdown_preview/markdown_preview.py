#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sublime, sublime_plugin
import os, tempfile

class MarkdownPreviewCommand(sublime_plugin.TextCommand):
	
	def __init__(self, p):
		settings = sublime.load_settings('Markdown (GFM).sublime-settings')
		self.file_types = tuple(settings.get('extensions') or [".md", ".markdown", ".mdown"])
		super(MarkdownPreviewCommand, self).__init__(p)

	def run(self, edit):
		file_name = self.view.file_name()
		if file_name and file_name.endswith(self.file_types):
			selection = self.view.substr(self.view.sel()[0])
			if selection.strip() != '':
				contents = selection
			else:
				region = sublime.Region(0, self.view.size())
				contents = self.view.substr(region)
			redcarpet = os.path.join(sublime.packages_path(), "SublimeMarkdown", "redcarpet.rb")
			temp_file = os.path.join(tempfile.gettempdir(), 'markdown_%s.md' % self.view.id())
			open(temp_file, 'w').write(contents)
			os.system('ruby "%s" "%s" &' % (redcarpet, temp_file))
