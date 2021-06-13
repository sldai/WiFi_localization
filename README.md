# WiFi_localization
Indoor localization system for people using WiFi signal received by smart phones, since GPS is hard to use indoors. And localization accuracy is 1m. [video](https://youtu.be/FdbGS7_Mi3Y)

Method: first build the fingerprint map of WiFi, then match fingerprints received by users with the fingerprint map to find the position. Also fuse the inertial measurement unit and the WiFi sensor to get better performance by the particle filter.  

Automatic system: the robot is adopted to autonomously build and maintain the fingerprint map, so it's easy to use. The detail of this design is introduced in this paper.

-----------------------

Formal Introduction
-------------------

---
title: "Autonomous Robots Based Indoor WiFi Localization System"
permalink: /publication/2019-08-01-WiFi-localization
paperurl: 'https://arxiv.org/pdf/1911.11825'
---
Indoor localization is a key technique to provide services about interaction with the indoor environment such as Virtual Reality and airport navigation. However, GPS can hardly be used in the indoor space, due to the obstruction from buildings itself. WiFi, which are widely used, are rich and accurate signal sources for localization. Much like using lidar or camera for mapping and localzation, we first build the WiFi signal strength map, then localize the users' smartphone according to their received signal strength. 

Signal strength: Wireless signal gradually become weak during propagation, thus it can reflects the distance from the receiver to the emitter, which are the smartphone and the WiFi access point in our context. Suppose there are $n$ access points in the indoor space, the smartphone can acquire $n$ signal strengths, thus we can represent all information as a $n$ dimensional vector. And in different locations, the vector are supposed to be different, that's how we can do localization.

Mapping stage: for localization, we first need a high quality map, which represents the WiFi signal strength at each location. A mobile robot is used to survey the environment, and a smartphone mounted on it collects the information. After collection completed, we build a Gaussian process model from the data, which maps each location to the signal strength vector. You can refer to the paper for more detail. Finally, we get the following map:

![WiFi signal map](http://sldai.github.io/images/WiFi_localization/heatmap_nosojourn.png) 

Localization stage: when the smartphone receives the signals, we search over the map to find locations whose signals match the received signals best. Also we use step detector built in the phone and compass to inference the person's motion state. A particle filter fuses these two information and estimates the localization. The following video shows the result:

<iframe width="1046" height="404" src="https://www.youtube.com/embed/FdbGS7_Mi3Y" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>



