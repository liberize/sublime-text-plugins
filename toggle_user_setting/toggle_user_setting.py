import sublime
import sublime_plugin

class ToggleUserSettingCommand(sublime_plugin.ApplicationCommand):
	def run(self, **kwargs):
		name = kwargs['setting']
		
		setting_dict = {
			"draw_white_space" : ("all", "selection"),
			"gutter" : (False, True),
			"line_numbers" : (False, True),
			"draw_indent_guides" : (False, True)
			# add other settings here
		}

		if name in setting_dict:
			options = setting_dict[name]
			settings = sublime.load_settings("Preferences.sublime-settings")
			value = options[0] if settings.get(name, options[0]) != options[0] else options[1]
			settings.set(name, value)
			sublime.save_settings("Preferences.sublime-settings")
