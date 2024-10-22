import cv2
import numpy as np
import math

# Video configuration
width, height = 1920, 1080
fps = 1
total_seconds = 12 * 60 * 60  # 12 hours = 43200 seconds
video_filename = "clock_video.mp4"

# Clock configuration
center = (width // 2, height // 2)
radius_sec = height // 2 - 50
radius_min = height // 2 - 150
radius_hour = height // 2 - 250

# Create a video writer
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(video_filename, fourcc, fps, (width, height))

# Drawing clock
def draw_hand(img, angle, radius, thickness, color):
    x = int(center[0] + math.cos(angle - math.pi/2) * radius)
    y = int(center[1] + math.sin(angle - math.pi/2) * radius)
    cv2.line(img, center, (x, y), color, thickness)

# Function to draw clock face
def draw_clock_face(img):
    # Draw hour marks
    for hour in range(12):
        angle = (hour / 12) * 2 * math.pi
        x1 = int(center[0] + math.cos(angle - math.pi/2) * (radius_sec - 30))
        y1 = int(center[1] + math.sin(angle - math.pi/2) * (radius_sec - 30))
        x2 = int(center[0] + math.cos(angle - math.pi/2) * (radius_sec + 30))
        y2 = int(center[1] + math.sin(angle - math.pi/2) * (radius_sec + 30))
        cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 15)

    # Draw minute marks
    for minute in range(60):
        angle = (minute / 60) * 2 * math.pi
        x1 = int(center[0] + math.cos(angle - math.pi/2) * (radius_sec - 20))
        y1 = int(center[1] + math.sin(angle - math.pi/2) * (radius_sec - 20))
        x2 = int(center[0] + math.cos(angle - math.pi/2) * (radius_sec + 20))
        y2 = int(center[1] + math.sin(angle - math.pi/2) * (radius_sec + 20))
        cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 7)

# Main loop for generating video
for seconds in range(total_seconds):
    # Create black image for each frame
    img = np.zeros((height, width, 3), dtype=np.uint8)

    # Calculate hand positions
    sec_angle = (seconds % 60) / 60 * 2 * math.pi
    min_angle = (seconds % 3600) / 3600 * 2 * math.pi
    hour_angle = (seconds % (12 * 3600)) / (12 * 3600) * 2 * math.pi

    # Draw clock face
    draw_clock_face(img)

    # Draw hour, minute, and second hands
    draw_hand(img, sec_angle, radius_sec, 5, (0, 0, 255))     # Second hand
    draw_hand(img, min_angle, radius_min, 15, (0, 255, 0))    # Minute hand
    draw_hand(img, hour_angle, radius_hour, 25, (255, 0, 0))  # Hour hand

    # Draw center circle
    cv2.circle(img, center, 25, (255, 255, 255), -1)

    # Write frame to video
    out.write(img)

    # Display frame (optional)
    # cv2.imshow("Clock", img)
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break

# Release the video writer and close windows
out.release()
cv2.destroyAllWindows()

print(f"Video saved as {video_filename}")
