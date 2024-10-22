import cv2
import numpy as np
import math
import random
import time
import os

# Video configuration
width, height = 1920, 1080
fps = 1
total_seconds = 12 * 60 * 60  # 12 hours = 43200 seconds

# Create the "videos" directory if it doesn't exist
if not os.path.exists('videos'):
    os.makedirs('videos')

# Prepend the epoch time to the file name
epoch_time = int(time.time())
video_filename = f"videos/{epoch_time}_clock_video_random_colors.mp4"

# Clock configuration
center = (width // 2, height // 2)
radius_sec = height // 2 - 50
radius_min = height // 2 - 150
radius_hour = height // 2 - 250

# Create a video writer
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(video_filename, fourcc, fps, (width, height))

# Function to generate random color
def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

# Function to format time (hours, minutes, seconds)
def format_time(seconds):
    hrs = seconds // 3600
    mins = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{int(hrs):02}:{int(mins):02}:{int(secs):02}"

# Drawing clock hands
def draw_hand(img, angle, radius, thickness, color):
    x = int(center[0] + math.cos(angle - math.pi/2) * radius)
    y = int(center[1] + math.sin(angle - math.pi/2) * radius)
    cv2.line(img, center, (x, y), color, thickness)

# Function to draw the clock face
def draw_clock_face(img, hour_color, minute_color):
    # Draw hour marks
    for hour in range(12):
        angle = (hour / 12) * 2 * math.pi
        x1 = int(center[0] + math.cos(angle - math.pi/2) * (radius_sec - 30))
        y1 = int(center[1] + math.sin(angle - math.pi/2) * (radius_sec - 30))
        x2 = int(center[0] + math.cos(angle - math.pi/2) * (radius_sec + 30))
        y2 = int(center[1] + math.sin(angle - math.pi/2) * (radius_sec + 30))
        cv2.line(img, (x1, y1), (x2, y2), hour_color, 15)

    # Draw minute marks
    for minute in range(60):
        angle = (minute / 60) * 2 * math.pi
        x1 = int(center[0] + math.cos(angle - math.pi/2) * (radius_sec - 20))
        y1 = int(center[1] + math.sin(angle - math.pi/2) * (radius_sec - 20))
        x2 = int(center[0] + math.cos(angle - math.pi/2) * (radius_sec + 20))
        y2 = int(center[1] + math.sin(angle - math.pi/2) * (radius_sec + 20))
        cv2.line(img, (x1, y1), (x2, y2), minute_color, 7)

# Main loop for generating the video
start_time = time.time()

for seconds in range(total_seconds):
    # Create a random background color
    background_color = random_color()
    
    # Create a blank image with random background color
    img = np.full((height, width, 3), background_color, dtype=np.uint8)

    # Calculate hand positions
    sec_angle = (seconds % 60) / 60 * 2 * math.pi
    min_angle = (seconds % 3600) / 3600 * 2 * math.pi
    hour_angle = (seconds % (12 * 3600)) / (12 * 3600) * 2 * math.pi

    # Generate random colors for clock face and hands
    hour_mark_color = random_color()
    minute_mark_color = random_color()
    sec_hand_color = random_color()
    min_hand_color = random_color()
    hour_hand_color = random_color()
    center_circle_color = random_color()

    # Draw clock face with random colors for hour and minute marks
    draw_clock_face(img, hour_mark_color, minute_mark_color)

    # Draw hour, minute, and second hands with random colors
    draw_hand(img, sec_angle, radius_sec, 5, sec_hand_color)     # Second hand
    draw_hand(img, min_angle, radius_min, 15, min_hand_color)    # Minute hand
    draw_hand(img, hour_angle, radius_hour, 25, hour_hand_color)  # Hour hand

    # Draw center circle with random color
    cv2.circle(img, center, 25, center_circle_color, -1)

    # Write the frame to the video
    out.write(img)

    # Every 60 seconds, show statistics
    if seconds % 60 == 0:
        time_passed = seconds
        time_remaining = total_seconds - seconds
        percentage_done = (seconds / total_seconds) * 100

        # Format time passed and remaining
        formatted_passed = format_time(time_passed)
        formatted_remaining = format_time(time_remaining)

        # Print statistics
        print(f"Time passed: {formatted_passed}, Time remaining: {formatted_remaining}, Completion: {percentage_done:.2f}%")

    # Optional: display the frame in real-time (disable for longer runs)
    # cv2.imshow("Clock", img)
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break

# Release the video writer and close any open windows
out.release()
cv2.destroyAllWindows()

print(f"Video saved as {video_filename}")
