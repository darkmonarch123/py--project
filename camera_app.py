import cv2

# Connect to your webcam (0 is usually the default built-in camera)
camera = cv2.VideoCapture(0)

print("Controls:")
print("-> Press 'g' to turn the Grayscale filter ON/OFF")
print("-> Press 's' to snap and save a photo")
print("-> Press 'q' to quit the app")

grayscale_mode = False

while True:
    # Capture the live video frame-by-frame
    ret, frame = camera.read()
    
    if not ret:
        print("Error: Could not access your webcam.")
        break

    # If grayscale mode is active, convert the image to black and white
    if grayscale_mode:
        display_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    else:
        display_frame = frame

    # Show the live feed in a window named 'My Camera App'
    cv2.imshow('My Camera App', display_frame)

    # Wait 1 millisecond for a key press
    key = cv2.waitKey(1) & 0xFF

    # 'g' toggles the filter
    if key == ord('g'):
        grayscale_mode = not grayscale_mode
        
    # 's' saves the current frame as an image file
    elif key == ord('s'):
        filename = "my_awesome_snapshot.png"
        cv2.imwrite(filename, display_frame)
        print(f"📸 Saved photo as {filename}!")
        
    # 'q' breaks the loop and closes the app
    elif key == ord('q'):
        break

# When everything is done, release the camera and close windows
camera.release()
cv2.destroyAllWindows()