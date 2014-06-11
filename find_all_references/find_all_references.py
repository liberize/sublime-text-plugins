import sublime
import sublime_plugin

BUILD_SYSTEM = "Packages/User/Find All References.sublime-build"


class FindAllReferencesCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        selections = self.view.sel()
        if len(selections) != 1:
            return
        pattern = self.view.substr(selections[0])
        lines = self.view.lines(selections[0])
        if pattern == '' or len(lines) != 1:
            return
        sublime.set_clipboard(pattern)

        window = self.view.window()
        window.run_command("set_build_system", {"file": BUILD_SYSTEM})
        window.run_command("build")
