# CenterTrack-Stable
**CenterTrack-Stable** is designed to keep the car near the track center while reducing sharp steering, ensuring smooth and efficient laps.

## Action space
This action space balances speed and control by allowing higher speeds when steering is minimal and reducing speed during sharp turns. Lower speeds at extreme angles (-30° and 30°) help prevent skidding or off-tracks, while the highest speed (2.50 m/s) is reserved for straight paths (0° steering) to maximize efficiency on straight sections. This setup ensures stability while optimizing lap times.
| Steering angle (°) | Speed (m/s) |
|-|-|
| -30.0 | 0.80 |
| -30.0 | 1.00 |
| -20.0 | 1.30 |
| -20.0 | 1.50 |
| -10.0 | 1.70 |
| -10.0 | 1.90 |
| 0.0 | 2.20 |
| 0.0 | 2.50 |
| 10.0 | 1.90 |
| 10.0 | 1.70 |
| 20.0 | 1.50 |
| 20.0 | 1.30 |
| 30.0 | 1.00 |
| 30.0 | 0.80 |

## Reward function
I used the default reward function from AWS:
```python
def reward_function(params):

    # Read input parameters
    distance_from_center = params['distance_from_center']
    track_width = params['track_width']
    abs_steering = abs(params['steering_angle']) # Only need the absolute steering angle

    # Calculate 3 marks that are farther and father away from the center line
    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.5 * track_width

    # Give higher reward if the car is closer to center line and vice versa
    if distance_from_center <= marker_1:
        reward = 1.0
    elif distance_from_center <= marker_2:
        reward = 0.5
    elif distance_from_center <= marker_3:
        reward = 0.1
    else:
        reward = 1e-3  # likely crashed/ close to off track

    # Steering penality threshold, change the number based on your action space setting
    ABS_STEERING_THRESHOLD = 15

    # Penalize reward if the car is steering too much
    if abs_steering > ABS_STEERING_THRESHOLD:
        reward *= 0.8
    return float(reward)
```
This reward function encourages the car to stay near the track center while penalizing excessive steering to maintain stability.

## Hyperparameters 

| Hyperparameter | Value | Reason |
|-|-|-|
| Gradient descent batch size | 64 | Ensures efficient updates while maintaining stability. |
| Entropy | 0.01 | Encourages exploration without excessive randomness. |
| Discount factor | 0.999 | Prioritizes long-term rewards for better decision-making. |
| Loss type | Huber | Handles outliers effectively for stable training. |
| Learning rate | 0.0003 | Provides steady convergence without overshooting. |
| Episodes between each iteration | 18 | Ensures sufficient experience is gathered before updates. |
| Number of epochs | 10 | Optimizes training while preventing overfitting. |

## Model Performance

### Training:
I trained the model with a maximum time of 60 minutes.

### Results:
This model obtained the following performance:
| Best lab time | Total time | Off-track |
|-|-|-|
| 00:12.130 | 00:43.460 | 5 |

The model does not perform well but it will be a good start to fine-tune.
