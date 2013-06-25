# Instructions

1. if you are on amd64 platform, copy the compiled library `libsublime-imfix.so` to your sublime text install directory.
or you can compile it on your own (need `libgtk2.0-dev` package installed):   
```bash
gcc -shared -o libsublime-imfix.so sublime_imfix.c  `pkg-config --libs --cflags gtk+-2.0` -fPIC
```
2. copy `subl` to `/user/bin/` to replace the original one.
3. copy `sublime_text.desktop` to `/usr/share/applications/` replace the original one.
4. test with your input method.
