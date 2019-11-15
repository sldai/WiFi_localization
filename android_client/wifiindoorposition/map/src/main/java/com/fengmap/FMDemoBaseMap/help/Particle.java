package com.fengmap.FMDemoBaseMap.help;

/**
 * Created by lenovo on 2017/11/12.
 */

public class Particle {
    public float x;
    public float y;
    public float stepLength;
    public double orientation;
    public Particle(float _x, float _y, float _stepLength, double _orientation){
        x=_x;
        y=_y;
        stepLength=_stepLength;
        orientation=_orientation;

    }
    public void move(float var){
        x+=(stepLength+var)* Math.cos(orientation);
        y+=(stepLength+var)* Math.sin(orientation);
        stepLength+=0.1* Math.random()-0.05f;
        orientation+=Math.random()*0.17-0.085+orientation;
    }
    public void move(double step,double angle){
        x+=step* Math.cos(angle);
        y+=step* Math.sin(angle);

    }
    public void constain(float xL,float xH,float yL,float yH){
        x=(x<=xH?x:xH);
        x=(x>=xL?x:xL);
        y=(y<=yH?y:yH);
        y=(y>=yL?y:yL);

    }
    public void copy(Particle particle){
        x=particle.x;
        y=particle.y;
        stepLength=particle.stepLength;
        orientation=particle.orientation;
    }
}
