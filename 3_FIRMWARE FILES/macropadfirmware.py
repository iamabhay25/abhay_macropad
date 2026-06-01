# ============================================================
# (ONLY ADDITION: LED ANIMATION ENGINE)
# ============================================================

class LEDAnimator:
    def __init__(self, rgb):
        self.rgb = rgb
        self.active_idx = -1
        self.target_idx = -1
        self.direction = 1   # 1 = fill up, -1 = clear down
        self.running = False
        self.last_update = 0
        self.step_delay = 30  # ms between LED steps
        self.current = 0
        self.color = (255, 255, 255)

    def start_fill(self, idx, color):
        self.target_idx = idx
        self.active_idx = 0
        self.current = 0
        self.direction = 1
        self.color = color
        self.running = True

    def start_clear(self, idx):
        self.target_idx = idx
        self.current = idx
        self.direction = -1
        self.running = True

    def tick(self):
        if not self.running:
            return

        now = supervisor.ticks_ms()
        if now - self.last_update < self.step_delay:
            return

        self.last_update = now

        # FILL ANIMATION
        if self.direction == 1:
            if self.current <= self.target_idx:
                self.rgb[self.current] = self.color
                self.current += 1
            else:
                self.running = False

        # CLEAR ANIMATION
        else:
            if self.current >= 0:
                self.rgb[self.current] = (0, 0, 0)
                self.current -= 1
            else:
                self.running = False


# ============================================================
# INIT LED ANIMATOR (AFTER rgb SETUP)
# ============================================================

led_anim = LEDAnimator(rgb)


# ============================================================
# MODIFY KEY WRAPPER ONLY (REPLACE FUNCTION)
# ============================================================

def _make_wrapped(idx):
    raw = KEY_DEFS[idx]["action"]
    color = KEY_DEFS[idx]["color"]

    def _pressed(key, keyboard, *args, **kwargs):
        animator.trigger(idx)

        # start LED animation (non-blocking)
        rgb.fill((0, 0, 0))
        led_anim.start_fill(idx, color)

        keyboard.hid_pending = True
        keyboard.tap_key(raw)

    def _released(key, keyboard, *args, **kwargs):
        led_anim.start_clear(idx)

    return make_key(
        names=("AK{:d}".format(idx),),
        on_press=_pressed,
        on_release=_released,
    )


# ============================================================
# MODIFY OLED TICK EXTENSION (ADD LED TICK)
# ============================================================

class _OledTickExtension:
    def during_bootup(self, keyboard):
        pass

    def before_hid_send(self, keyboard):
        animator.tick()
        led_anim.tick()   # <-- ADD THIS LINE

    def after_hid_send(self, keyboard):
        pass

    def before_hid_receive(self, keyboard):
        pass

    def after_hid_receive(self, keyboard):
        pass

    def on_powersave_enable(self, keyboard):
        pass

    def on_powersave_disable(self, keyboard):
        pass
