# WiFi_localization
Indoor localization system for people using WiFi signal received by smart phones, since GPS is hard to use indoors. And localization accuracy is 1m.

Method: first build the fingerprint map of WiFi, then match fingerprints received by users with the fingerprint map to find the position. Also fuse the inertial measurement unit and the WiFi sensor to get better performance by the particle filter.  

Automatic system: the robot is adopted to autonomously build and maintain the fingerprint map, so it's easy to use. The detail of this design is introduced in this paper.