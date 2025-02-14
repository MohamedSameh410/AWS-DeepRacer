# TrackAware-Optimized
**TrackAware-Optimized** is a refined version of **EdgeAware-SpeedOptimized**, introducing stricter penalties for off-track behavior while maintaining speed and control optimizations. This model keeps the edge awareness approach, rewarding the car for track positioning, but now explicitly penalizes off-track instances to reinforce better adherence. It continues to use square root scaling for smoother steering penalties and a quadratic function to encourage higher speeds. Progress tracking remains a key factor, ensuring efficient lap completion.
## Action space
Encourage the model to be faster.
| Steering angle (°) | Speed (m/s) |
|-|-|
| -30.0 | 1.10 |
| -30.0 | 1.30 |
| -20.0 | 1.50 |
| -20.0 | 1.70 |
| -10.0 | 1.90 |
| -10.0 | 2.10 |
| 0.0 | 3.70 |
| 0.0 | 3.00 |
| 10.0 | 2.10 |
| 10.0 | 1.90 |
| 20.0 | 1.70 |
| 20.0 | 1.50 |
| 30.0 | 1.30 |
| 30.0 | 1.10 |

## Reward function
This model adds a stricter off-track penalty, applying a soft reduction for minor deviations and a harsher one when fully off-track. It retains edge awareness, steering control, speed optimization, and progress rewards while improving track adherence.
```python
import math

def reward_function(params):
    # Read input parameters
    distance_from_center = params['distance_from_center']
    track_width = params['track_width']
    is_left_of_center = params['is_left_of_center']
    abs_steering = abs(params['steering_angle'])
    speed = params['speed']
    progress = params['progress']
    all_wheels_on_track = params['all_wheels_on_track']
    off_track = params['is_offtrack']

    # Calculate distance from the left edge
    if is_left_of_center:
        distance_from_left_side = (track_width / 2) - distance_from_center
    else:
        distance_from_left_side = (track_width / 2) + distance_from_center

    # Ensure non-negative values before applying sqrt
    distance_ratio = max(0, distance_from_left_side / track_width)
    distance_reward = 1 - math.sqrt(distance_ratio)

    steering_ratio = max(0, abs_steering / 30)
    steering_reward = 1 - math.sqrt(steering_ratio)

    speed_reward = (speed / 4.0) ** 2
    progress_reward = progress / 100

    # Combine rewards with weights
    reward = (2 * distance_reward + steering_reward + 2 * speed_reward + 2 * progress_reward) / 7

    # Penalize if the car goes off track
    if not all_wheels_on_track:
        reward *= 0.5  # to allow going outside the track by sense :)

    # Penalize if the car goes off track
    if off_track:
        reward *= 0.5

    return float(reward)

```

## Hyperparameters 
Decrease the Episodes between each iteration by 2.

| Hyperparameter | Value |
|-|-|
| Gradient descent batch size | 64 |
| Entropy | 0.01 |
| Discount factor | 0.999 |
| Loss type | Huber |
| Learning rate | 0.00001 |
| Episodes between each iteration | 16 |
| Number of epochs | 10 |

## Model Performance

### Training:
I trained the model with a maximum time of 45 minutes.

### Results:
This model obtained the following performance:
| Best lab time | Total time | Off-track |
|-|-|-|
| 00:09.534 | 00:30.464 | 0 |

This model achieves superior speed, stability, and overall lap efficiency.
