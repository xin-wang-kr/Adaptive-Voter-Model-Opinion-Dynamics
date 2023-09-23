# Opinion Ecology Based on Social Network and Textual Sentiment of Twitter Tweets

### Introduction

Textual sentiment is important when we consider social influence on social media. To understand
the ecology of political opinions on social media (i.e., Twitter), an adaptive voter model, which
employs a weighted majority rule and adaptive edge removal, is introduced in this study. The
model is used to investigate the extent to which a network constructed based on textual sentiment
from social media and user geographic location aligns with the opinion formation patterns in realworld
data. The simulation results by the adaptive voter model can successfully show salient
clustering patterns. The whole simulation can achieve a stable stage without any change in the
number of edges and the average shortest path length when the nodes with different opinion states
are perfectly separated. The comparison between the simulated results and the real US election
situation indicates that there remain some challenges that prevent the model from achieving its full
potential due to the lack of actual network connection data among Twitter users. Future research
agenda is discussed to remove some of the current limitations.

### Data Source
Zhao, P., Chen, X., & Wang, X. (2021). Classifying COVID-19-related hate Twitter users using
deep neural networks with sentiment-based features and geopolitical factors. International
Journal of Society Systems Science, 13(2), 125–139.

### Weighted Majority Decision Rule
<img width="595" alt="image" src="https://github.com/xin-wang-kr/Adaptive-Voter-Model-Opinion-Dynamics/assets/28020765/3b3cc7bd-7551-46f5-951e-2c57e79cf9a1">

### Adaptive Voter Model
I designed this adaptive voter model:
<img width="780" alt="image" src="https://github.com/xin-wang-kr/Adaptive-Voter-Model-Opinion-Dynamics/assets/28020765/e45a707c-4b11-4f01-88af-bb504f50d24c">

### Simulation Process
The Republican (red dots), Neutral(white dots), and Democrat (blue dots) can be perfectly sepatated in the end of the simulation.

![](https://github.com/xin-wang-kr/Adaptive-Voter-Model-Opinion-Dynamics/animation-ny.mp4)

### Comparison between the Simulation Results and the Actual Results
![image](https://github.com/xin-wang-kr/Adaptive-Voter-Model-Opinion-Dynamics/assets/28020765/d87b5976-9771-495e-a792-49e3cb0e479d)

