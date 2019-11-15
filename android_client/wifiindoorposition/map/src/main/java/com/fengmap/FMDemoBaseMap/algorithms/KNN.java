package com.fengmap.FMDemoBaseMap.algorithms;

import android.content.Context;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.net.wifi.ScanResult;
import android.net.wifi.WifiManager;

import com.fengmap.FMDemoBaseMap.help.Db;
import com.fengmap.FMDemoBaseMap.help.Window;
import com.fengmap.FMDemoBaseMap.help.point;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;

import static android.content.Context.WIFI_SERVICE;

public class  KNN{
    public point tempcenter;
    private Db dbhelper;//数据库helper
    private SQLiteDatabase dbRead;//可读数据库
    private WifiManager wifiManager ;
    private List<ScanResult> nku;//online mac
    private List<wifi> near;

    private int xH=15,xL=0,yH=4,yL=0;
    private int NN=10,fineNN=3;
    private float var=3;
    private float coordinateX,coordinateY;
    public point coarsePoint;

    private float[][][] map;
    private String[] bssidList;
    private int macNum;
    private int locateNum=4;
    private int[] idStorage;
    private float[] wifiObserve;
    private class aaf{
        public float aver;
        public int freq;
        aaf(){
            aver=0;
            freq=0;
        }
    }
    aaf[] wifistore;
    //动态窗
    private List<Window> windowList;

    public KNN(Context context,
               String databaseName
    )
    {
        dbhelper=new Db(context,databaseName,null,1);
        dbRead=dbhelper.getReadableDatabase();
        wifiManager=(WifiManager) context.getSystemService(WIFI_SERVICE);;
        bssidList=new String[35];
        map=new float[100][100][35];
        wifistore=new aaf[35];
        for(int i=0;i<35;i++){
            wifistore[i]=new aaf();
        }

        windowList=new ArrayList<Window>();
    }


    public void importData(String positionName)
    {
        /*从数据库中对基本数据初始化
        *
        *
        * */
        Cursor cursor=dbRead.query(positionName, null,null,null,null,null,null);

        for(int i=0;i<35;i++){
            bssidList[i]=cursor.getColumnName(2+i);

        }
        while(cursor.moveToNext())
        {
            int x=(int)(cursor.getFloat(0));
            int y=(int)(cursor.getFloat(1));
            for(int i=0;i<35;i++)
            {
                map[x][y][i]=cursor.getFloat(2+i);

            }
        }

    }
    public boolean getOb(List<ScanResult> scanResultList)//获得观测信号
    {

        nku=new ArrayList<ScanResult>();
        macNum=0;

        for(ScanResult scanResult : scanResultList){//滤去非南开WIfi
            if(transBssidToNum(scanResult.BSSID)!=-1&&scanResult.level>=-60){
                nku.add(scanResult);
                macNum++;
            }
        }
        if(macNum==0)return false;

        /*Collections.sort(nku, new Comparator<ScanResult>() {
            public int compare(ScanResult a, ScanResult b) {//降序处理。。。
                if(a.level>b.level)return -1;
                return 1;
            }
        });
        */
        ///if(macNum>5)macNum=5;



        idStorage=new int[macNum];
        wifiObserve=new float[macNum];
        for(int i=0;i<macNum;i++)
        {
            //int temp=transBssidToNum(nku.get(i).BSSID);
            /*wifistore[temp].aver=(wifistore[temp].aver*wifistore[temp].freq+nku.get(i).level)/(wifistore[temp].freq+1);
            wifistore[temp].freq++;*/
            idStorage[i]=transBssidToNum(nku.get(i).BSSID);
            wifiObserve[i]=nku.get(i).level;
        }
        return true;
    }

    public int transBssidToNum(String bssid)
    {
        for(int i=0;i<35;i++)
        {
            if(bssid.equals(bssidList[i]))return i;
        }
        return -1;
    }

    private class wifi{
        public float x;
        public float y;
        public double weigth;
        wifi(float x,float y,double _weigh){
            this.x=x;
            this.y=y;
            weigth=_weigh;
        }
    }
    public point getcoarse(){
        float temp;
        near=new ArrayList<wifi>();

        for(int x=xL;x<=xH;x++)
            for(int y=yL;y<=yH;y++)
            {
                temp=0;
                boolean isUseful =true;
                /*
                for(int i=0;i<macNum-1;i++)
                    for(int j=i+1;j<macNum;j++)
                {
                    temp+=Math.pow((map[x][y][idStorage[i]]-map[x][y][idStorage[j]]-wifiObserve[i]+wifiObserve[j]),2);
                }
                */

                for(int i=0;i<macNum;i++) {
                    if(Math.abs(map[x][y][idStorage[i]]-wifiObserve[i])>15){isUseful=false;break;}
                    temp+=Math.pow((map[x][y][idStorage[i]]-wifiObserve[i]),2);
                }

                if(isUseful==false)continue;
                temp=(float) Math.exp((-temp/2/(var*var)/macNum));

                wifi candidate=new wifi(x,y,temp);
                near.add(candidate);
            }
        Collections.sort(near, new Comparator<wifi>() {
            public int compare(wifi a, wifi b) {//降序。。。
                if(a.weigth>b.weigth)return -1;
                return 1;
            }
        });
        float sum=0;
        int actualNum=NN<near.size()?NN:near.size();
        for(int i=0;i<actualNum;i++) {
            sum += near.get(i).weigth;
        }
        //calculate the coordinate

        coordinateY=0;
        coordinateX=0;

        for(int i=0;i<actualNum;i++){
            coordinateX+=near.get(i).x*near.get(i).weigth/sum;
            coordinateY+=near.get(i).y*near.get(i).weigth/sum;
        }


        coarsePoint=new point(coordinateX,coordinateY);
        return coarsePoint;
    }
    public point getfine_1(point tcenter,float radius){
        List<wifi> tnear=new ArrayList<wifi>();
        float temp;
        int xTop,xBot,yTop,yBot;
        xTop=(tcenter.x+radius<=xH?(int)(tcenter.x+radius):xH);
        xBot=(tcenter.x-radius>=xL?(int)(tcenter.x-radius):xL);
        yTop=(tcenter.y+radius<=yH?(int)(tcenter.y+radius):yH);
        yBot=(tcenter.y-radius>=yL?(int)(tcenter.y-radius):yL);
        for(int x=xBot;x<=xTop;x++)
            for(int y=yBot;y<=yTop;y++)
            {
                temp=0;
                boolean isUseful =true;
                for(int i=0;i<macNum-1;i++) {
                    if(Math.abs(map[x][y][idStorage[i]]-wifiObserve[i])>15){isUseful=false;break;}
                    for (int j = i + 1; j < macNum; j++) {
                        temp += Math.pow((map[x][y][idStorage[i]] - map[x][y][idStorage[j]] - wifiObserve[i] + wifiObserve[j]), 2);
                    }
                }
                /*for(int i=0;i<macNum;i++) {

                    temp+=Math.pow((map[x][y][idStorage[i]]-wifiObserve[i]),2);
                }*/
                if(isUseful==false)continue;
                temp=(float) Math.exp((-temp/2/3.15/3.15));
                //double weigth=dis;
                //dis=100.0/dis;
                wifi candidate=new wifi(x,y,temp);
                tnear.add(candidate);
            }
        if(tnear.size()>=2) {
            Collections.sort(tnear, new Comparator<wifi>() {
                public int compare(wifi a, wifi b) {//降序。。。
                    if (a.weigth > b.weigth) return -1;
                    if(a.weigth == b.weigth) return 0;
                    return 1;
                }
            });
        }
        float fineX=0;
        float fineY=0;

        float sum=0;
        int actualNum=fineNN<tnear.size()?fineNN:tnear.size();
        for(int i=0;i<actualNum;i++) {
            sum += tnear.get(i).weigth;
        }
        for(int i=0;i<actualNum;i++){
            fineX+=tnear.get(i).x*tnear.get(i).weigth/sum;
            fineY+=tnear.get(i).y*tnear.get(i).weigth/sum;
        }

        point p=new point(fineX,fineY);

        return p;

    }

    public point getfine_2(point tcenter,float radius,int num){
        List<wifi> tnear=new ArrayList<wifi>();
        float temp;
        int xTop,xBot,yTop,yBot;
        xTop=(tcenter.x+radius<=xH?(int)(tcenter.x+radius):xH);
        xBot=(tcenter.x-radius>=xL?(int)(tcenter.x-radius):xL);
        yTop=(tcenter.y+radius<=yH?(int)(tcenter.y+radius):yH);
        yBot=(tcenter.y-radius>=yL?(int)(tcenter.y-radius):yL);
        for(int x=xBot;x<=xTop;x++)
            for(int y=yBot;y<=yTop;y++)
            {
                temp=0;
                boolean isUseful =true;
                for(int i=0;i<macNum;i++) {
                    if(Math.abs(map[x][y][idStorage[i]]-wifiObserve[i])>15){isUseful=false;break;}
                    temp+=Math.pow((map[x][y][idStorage[i]]-wifiObserve[i]),2);
                }
                if(isUseful==false)continue;
                temp=(float) Math.exp((-temp/2/var/var/macNum));

                wifi candidate=new wifi(x,y,temp);
                tnear.add(candidate);
            }
        Collections.sort(tnear, new Comparator<wifi>() {
            public int compare(wifi a, wifi b) {//降序。。。
                if(a.weigth>b.weigth)return -1;
                return 1;
            }
        });
        float fineX=0;
        float fineY=0;
        float sum=0;
        int actualNum=num<tnear.size()?num:tnear.size();
        for(int i=0;i<actualNum;i++) {
            sum += tnear.get(i).weigth;
        }
        for(int i=0;i<actualNum;i++){
            fineX+=tnear.get(i).x*tnear.get(i).weigth/sum;
            fineY+=tnear.get(i).y*tnear.get(i).weigth/sum;
        }
        point p=new point(fineX,fineY);
        return p;
    }

    public boolean include(Window window,point p){
        if((window.center.x+window.radius>=p.x)&&(window.center.x-window.radius<=p.x)
                 &&(window.center.y+window.radius>=p.y)&&(window.center.y-window.radius<=p.y))
            return true;
        return false;

    }

    public void windowMove(double stepLength,double orientation){
        for (Window window : windowList){
            window.center.move( (float)(stepLength*Math.cos(orientation)),(float)(stepLength*Math.sin(orientation)));
            window.center.constain(xL,xH,yL,yH);
        }
    }

    public void windowUpdate(point updata) {

        boolean exist = false;
        int maxConfidence=0;
        for (Window window : windowList) {
            window.center.move(0.5f,0);
            if (include(window, updata)) {
                window.confidence++;
                window.center.copy(getfine_2(window.center, window.radius,1));
                exist = true;
                maxConfidence=maxConfidence>window.confidence?maxConfidence:window.confidence;
            }
            else {
                window.confidence/=2;
                window.center.copy(getfine_2(window.center,window.radius,3));
            }
        }
        if(exist==false){
            Window window=new Window(updata);
            windowList.add(window);
        }
        else {

        }

        for(int i=0;i<windowList.size();i++)
        {
            //删去不可信的
            if(windowList.get(i).confidence<=0){
                windowList.remove(i);
                i--;
                continue;
            }

        }
    }

    public Window getBestWindow()
    {
        Collections.sort(windowList, new Comparator<Window>() {
            public int compare(Window a, Window b) {//降序。。。
                if(a.confidence>b.confidence)return -1;
                return 1;
            }
        });
        Window mwindow=new Window(windowList.get(0).center);
        mwindow.confidence=windowList.get(0).confidence;
        return mwindow;

    }


}


