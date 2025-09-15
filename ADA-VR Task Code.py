import time
import numpy as np
import msvcrt

def capture_keystroke_timings(prompt, expected_password):
    print(prompt, end="", flush=True)
    pressed_times = []
    captured_text = []

    while True:
        key = msvcrt.getwch()

        # Enter = end input
        if key == '\r':
            print()
            break

        # Backspace handling
        if key in ('\b', '\x08'):
            if captured_text:  # only if something to delete
                captured_text.pop()
                if pressed_times:
                    pressed_times.pop()
                # move cursor back, overwrite with space, move back again
                print('\b \b', end="", flush=True)
            continue

        # Normal character
        captured_text.append(key)
        pressed_times.append(time.time())
        print(key, end="", flush=True)  # show typed character

    typed = "".join(captured_text)
    if typed != expected_password:
        print("Password mismatch. Try again.")
        return None

    # intervals between consecutive keystrokes
    intervals = [t2 - t1 for t1, t2 in zip(pressed_times, pressed_times[1:])]
    return intervals


def main():
    expected_password = input("Set your password for enrollment: ").strip()
    enrollment_data = []

    print("\nEnrollment Phase: Type your password 5 times.")
    while len(enrollment_data) < 5:
        attempt = capture_keystroke_timings(f"Attempt {len(enrollment_data)+1}: ", expected_password)
        if attempt:
            enrollment_data.append(attempt)
            print("Time vector:", [round(t, 3) for t in attempt])

    # compute average timing vector
    avg_vector = np.mean(enrollment_data, axis=0)
    print("\nAverage timing vector:", [float(round(t, 3)) for t in avg_vector])

    print("\nLogin Phase:")
    login_attempt = None
    while login_attempt is None:
        login_attempt = capture_keystroke_timings("Enter your password: ", expected_password)
        if login_attempt:
            print("Time vector (login attempt):", [round(t, 3) for t in login_attempt])

    # compute the Euclidean distance between the login attempt vector and the average vector
    distance = np.linalg.norm(np.array(login_attempt) - avg_vector)
    threshold = 0.6  

    print(f"Distance from average: {distance:.4f}")
    if distance < threshold:
        print("Access granted!")
    else:
        print("Access denied!")


if __name__ == "__main__":
    main()

