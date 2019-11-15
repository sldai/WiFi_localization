package com.fengmap.FMDemoBaseMap.algorithms;

import com.fengmap.FMDemoBaseMap.help.Window;
import com.fengmap.FMDemoBaseMap.help.point;

import java.util.ArrayList;
import java.util.List;

/**
 * Created by lenovo on 2017/11/5.
 */

public class MoveWindow {
    private List<Window> windowList;

    public MoveWindow(){
        windowList=new ArrayList<Window>();

    }


    public boolean include(Window window,point p){
        if((window.center.x+window.radius>=p.x)&&(window.center.x-window.radius<=p.x)
                &&(window.center.y+window.radius>=p.y)&&(window.center.y-window.radius<=p.y))
            return true;
        return false;
    }


    public void windowUpdate(point updata){

        boolean exist=false;
        for(Window window:windowList)
        {
            if(include(window,updata)) {
                window.confidence++;
                window.center.copy(updata);
                exist=true;
            }
            else
            {
                window.confidence--;

            }
        }


    }


}
