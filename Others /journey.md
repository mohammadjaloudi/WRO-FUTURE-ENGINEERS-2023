This file is about our journey.

First, we started a club in July with our teachers through the Ministry of Education. They taught us how to use Raspberry Pi and told us about this competition.

Initially, our team used a regular car (without a real servo; it had a DC motor with gears to control left and right turns). It took a long time to prepare it because, after a few days of using Raspberry Pi, it stopped working. The first stage was approaching in two days, so we decided to use Arduino instead of Raspberry Pi.

After we entered the second stage, we received new training, which was about cameras and some beneficial algorithms. It was the best training we had ever received. However, there was a problem for us: Raspberry Pi wasn't working, we didn't have a car with a real servo motor, and our car motors had broken down. We were about to give up, but we remembered that the primary goal of this competition for us was learning. So, we bought a new car with a real servo motor this time and also acquired a camera.

After that, we fixed the Raspberry Pi. It turned out to be a simple problem; we needed to download the latest update for it, though we weren't sure why. Then we began working. Our team consisted of two participants: my brother and me. We divided the work—my brother handled hardware wiring and Arduino programming, while I focused on Raspberry Pi programming, circuit design, and documentation.

but for no reason arduino is not working so we changed to raspbberry pi.

Now that I've summarized our journey, I'll explain a few things about the car. I'll start with the coding:

Raspberry Pi:
We used cv2, numpy, serial, imutils, time, gpiozero, imutils.video, collections and gpiozero libraries
 
Now, let's talk about the hardware. I'll mention the parts we used:

Servo motor
DC motor
Three ultrasonic sensors
Raspberry Pi
Wires
Breadboard
Motor driver
Raspberry Pi camera
Our robot operates like this: It starts working, detects if there's any block in front of it, turns left or right depending on the situation, and completes three rotations around the arena.


For me, this competition was amazing. It was the first time I participated in a competition with my primary goal being learning, and I'm sure my brother shared the same sentiment. This was a summarized journey and information about us and our robot. I hope you enjoyed reading this.
