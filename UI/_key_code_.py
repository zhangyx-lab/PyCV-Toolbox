KEYCODE = {
    "arrow_up": 0,
    "arrow_down": 1,
    "arrow_left": 2,
    "arrow_right": 3,

    "enter": 13,
    "escape": 27,
    "delete": 40,
    "backspace": 127,
}

if __name__ == "__main__":
    import cv2
    cv2.namedWindow("Press any key to get its code")
    cv2.startWindowThread()
    while True:
        key = cv2.waitKey(1)
        if key < 0: continue
        # if key == ord("q"): break
        c = None
        try:
            c = chr(key)
        except ValueError:
            pass
        print("code =", key, "\tcharacter =", c)
