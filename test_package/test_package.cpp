#include <stdio.h>
#include <mruby.h>
#include <mruby/compile.h>

int main() {
    printf("Compiled with %s\n", MRUBY_DESCRIPTION);
    mrb_state *mrb = mrb_open();
    const char* code = "printf('Using %s %s', RUBY_ENGINE, RUBY_VERSION)";
    mrb_load_string(mrb, code);
    mrb_close(mrb);
    return 0;
}
