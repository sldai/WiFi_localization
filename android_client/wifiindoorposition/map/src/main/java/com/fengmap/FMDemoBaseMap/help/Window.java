package com.fengmap.FMDemoBaseMap.help;

/**
 * Created by lenovo on 2017/11/5.
 */

public class Window {
    public point center;
    public int confidence;
    public float radius=3;
    public Window(point _center){
        center=new point(_center.x,_center.y);
        confidence=1;
    }

}
