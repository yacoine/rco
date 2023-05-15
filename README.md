# rco


# Introduction
Find link to the article about this project:
https://www.linkedin.com/pulse/building-rock-climbing-pathfinder-pt-1-yassine-a%25C3%25A7oine/


Rock climbing optimizer (rock climbing optimizer). Creating a micro-service based application that helps people
find the optimal rock climbing path based on taking a picture or video. 


# Roadmap and Tasks

## Consolidated def functions with results 

#### Phase 1: Translating picture of rock climbing wall to x-y graph of invidual center holds
    1. Image is ingested
    2. Image is changed to RGB/RBG to HSV in order to better differentiate the holds/objects of interest
    3. Predisposed color ranges have been coded and can be chosen in order to help user 
    4. Additional sliders can be used to change the hue,saturation,and value in order to best isolate the color-specific holds of interest from all other holds and wall
    5. Once appropriate holds are isolated and result is appropriate to user, a k-means classificaiton is used to find the center of each hold
    6. The number of holds need to be inputted in order to properly determine the center (would be best to not have to do that)
    7. Centers of each hold is then visualized on a separate x-y axis in order to start phase.
    
#### Phase 2: Using the center holds and finding best hand and feet path based on human biomechanics 
    1. Create human body contraints
    2. What is the next step? Creating body constraints and creating object body
    3. Constraints:
        a.Two feet and two hands (4 points of contact possible),
    ignoring complexity of using other body parts as well (e.g.:knee)
        b. Feet can only be at the same height or lower than hands
    (to accomodate for lower levels of climbing and keep model simpler)
        c. Only one foot can be at the same level as the hands
        d. You can have two points on one hold (to start, keep complexity simple and not have feet and hands cross)
        e. start position is input value
        f. end position is input value (two hands)

    

# Recommended modules
# Installation
# Configuration
# Troubleshooting
# FAQ
# Maintainers
