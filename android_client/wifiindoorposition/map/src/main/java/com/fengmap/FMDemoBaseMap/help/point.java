package com.fengmap.FMDemoBaseMap.help;

/**
 * Created by lenovo on 2017/7/18.
 */

public class point {
    public float x;
    public float y;
    public point(point father){
        x=father.x;
        y=father.y;
    }
    public point(float _x,float _y){ x=_x;
        y=_y;}

    public void copy(point father){
        x=father.x;
        y=father.y;
    }
    public void move(float dx,float dy){
        x+=dx;
        y+=dy;
    }
    public boolean equal(point compare){
        if(x==compare.x&&y==compare.y)return true;
        return false;

    }

    public void constain(float xL,float xH,float yL,float yH){
        x=(x<=xH?x:xH);
        x=(x>=xL?x:xL);
        y=(y<=yH?y:yH);
        y=(y>=yL?y:yL);

    }
    public void rotmatrix()
    {
        double Y,X;
        if (x!=0){Y=-Math.sqrt(2*x*x+2*y*y)*Math.cos((Math.atan(y/x)-0.26))+4719663;}
        else
        {
            Y=-Math.sqrt(2*x*x+2*y*y)*(Math.cos(Math.PI/2-0.26))+4719663;
        }
        if (x!=0){X=Math.sqrt(2*x*x+2*y*y)*Math.sin((Math.atan(y/x)-0.26))+13061769;}
        else
        {
            X=Math.sqrt(2*x*x+2*y*y)*(Math.sin(Math.PI/2-0.26))+13061769;
        }
        y=(float) Y;
        x=(float) X;
    }
}
