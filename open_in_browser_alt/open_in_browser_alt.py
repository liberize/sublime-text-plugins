import sublime
import sublime_plugin
import subprocess
import tempfile


class OpenInBrowserAltCommand(sublime_plugin.ApplicationCommand):

    def run(self, **kwargs):
        browser = kwargs['browser']

        browser_cmd_map = {
            'safari': ['open', '-a', 'safari'],
            'firefox': ['open', '-a', 'firefox']
        }

        if browser in browser_cmd_map:
            cmd = browser_cmd_map[browser]
            view = sublime.Window.active_view(sublime.active_window())
            if view.file_name():
                cmd.append(view.file_name())
                subprocess.Popen(cmd)
            else:
                temp = tempfile.NamedTemporaryFile(delete=False)
                content = view.substr(sublime.Region(0, view.size()))
                temp.write(content.encode('utf-8'))
                temp.flush()
                cmd.append(temp.name)
                subprocess.Popen(cmd)
                temp.close()
