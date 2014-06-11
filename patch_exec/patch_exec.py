#!/usr/bin/env python3

"""This module patches the built in ExecCommand used by build systems to allow input via a keyboard shortcut"""

import os
import sys
import threading
import subprocess
import time
import sublime_plugin
import Default

execmodule = getattr(Default, 'exec')


def Monkeypatcher(name, bases, namespace):
    """http://mail.python.org/pipermail/python-dev/2008-January/076194.html"""
    base = bases[0]
    if hasattr(base, '__patched__'):
        return
    for name, value in namespace.items():
        if name != "__metaclass__":
            setattr(base, name, value)
    base.__bases__ += bases[1:]
    setattr(base, '__patched__', True)
    return base


class PatchedAsyncProcess(execmodule.AsyncProcess, metaclass=Monkeypatcher):

    def __init__(self, cmd, shell_cmd, env, listener,
                 # "path" is an option in build systems
                 path="",
                 # "shell" is an options in build systems
                 shell=False):

        if not shell_cmd and not cmd:
            raise ValueError("shell_cmd or cmd is required")

        if shell_cmd and not isinstance(shell_cmd, str):
            raise ValueError("shell_cmd must be a string")

        self.listener = listener
        self.killed = False

        self.start_time = time.time()

        # Hide the console window on Windows
        startupinfo = None
        if os.name == "nt":
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        # Set temporary PATH to locate executable in cmd
        if path:
            old_path = os.environ["PATH"]
            # The user decides in the build system whether he wants to append $PATH
            # or tuck it at the front: "$PATH;C:\\new\\path",
            # "C:\\new\\path;$PATH"
            os.environ["PATH"] = os.path.expandvars(path)

        proc_env = os.environ.copy()
        proc_env.update(env)
        for k, v in proc_env.items():
            proc_env[k] = os.path.expandvars(v)

        # Patched here
        if shell_cmd and sys.platform == "win32":
            # Use shell=True on Windows, so shell_cmd is passed through with
            # the correct escaping
            self.proc = subprocess.Popen(
                shell_cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                stderr=subprocess.PIPE, startupinfo=startupinfo, env=proc_env, shell=True)
        elif shell_cmd and sys.platform == "darwin":
            # Use a login shell on OSX, otherwise the users expected env vars
            # won't be setup
            self.proc = subprocess.Popen(
                ["/bin/bash", "-l", "-c", shell_cmd], stdout=subprocess.PIPE,
                stdin=subprocess.PIPE, stderr=subprocess.PIPE, startupinfo=startupinfo, env=proc_env, shell=False)
        elif shell_cmd and sys.platform == "linux":
            # Explicitly use /bin/bash on Linux, to keep Linux and OSX as
            # similar as possible. A login shell is explicitly not used for
            # linux, as it's not required
            self.proc = subprocess.Popen(
                ["/bin/bash", "-c", shell_cmd], stdout=subprocess.PIPE,
                stdin=subprocess.PIPE, stderr=subprocess.PIPE, startupinfo=startupinfo, env=proc_env, shell=False)
        else:
            # Old style build system, just do what it asks
            self.proc = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                stderr=subprocess.PIPE, startupinfo=startupinfo, env=proc_env, shell=shell)

        if path:
            os.environ["PATH"] = old_path

        if self.proc.stdout:
            threading.Thread(target=self.read_stdout).start()

        if self.proc.stderr:
            threading.Thread(target=self.read_stderr).start()

    # And patched here
    def give_input(self, value):
        os.write(self.proc.stdin.fileno(), value)
        if self.listener:
            self.listener.on_data(self, value)

if hasattr(execmodule, 'old_run_method'):
    oldRun = execmodule.old_run_method
else:
    oldRun = execmodule.ExecCommand.run
    execmodule.old_run_method = oldRun

# easy way of associating windows with their output panels, without
# causing strange bugs
panelsByWindow = {}


class PatchedExecCommand(execmodule.ExecCommand, metaclass=Monkeypatcher):

    def on_input_complete(self, value=None):
        """Show the output (which gets hidden) after taking the input"""
        if value is not None:
            self.proc.give_input(
                (value + '\n').encode(sys.getfilesystemencoding()))

        self.window.run_command("show_panel", {"panel": "output.exec"})
        self.window.focus_view(self.output_view)

    def run(self, give_input=False, **kwargs):
        """intercept a `give_input` argument before delegating to the real exec"""

        if give_input and hasattr(self, 'output_view'):
            lastline = self.output_view.substr(
                self.output_view.line(len(self.output_view)))
            self.window.show_input_panel(
                lastline or "", "", self.on_input_complete, None, self.on_input_complete)
            return

        oldRun(self, **kwargs)

        panelsByWindow[self.window.id()] = self.output_view.id()


class ExecInputListener(sublime_plugin.EventListener):

    """Accept input when output panel is focused"""

    def on_query_context(self, view, key, operator, operand, match_all):
        if key == 'build_selected':
            return view.id() == panelsByWindow[view.window().id()]
        else:
            return None
