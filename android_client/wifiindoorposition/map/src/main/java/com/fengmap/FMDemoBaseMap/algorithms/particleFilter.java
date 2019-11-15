package com.fengmap.FMDemoBaseMap.algorithms;

import android.content.Context;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.net.wifi.ScanResult;
import android.net.wifi.WifiManager;
import android.os.Handler;

import com.fengmap.FMDemoBaseMap.help.Db;
import com.fengmap.FMDemoBaseMap.help.Particle;
import com.fengmap.FMDemoBaseMap.help.point;

import java.util.ArrayList;
import java.util.List;

import static android.content.Context.WIFI_SERVICE;

/**
 * Created by lenovo on 2017/7/17.
 */

public class particleFilter {
    public float[][][] map;
    private Db dbhelper;//数据库helper
    String databaseName;
    private SQLiteDatabase dbRead;//可读数据库
    private WifiManager wifiManager;
    private List<ScanResult> nku;//online mac
    private float[] wifiObserve;
    private String[] bssidList;
    private Particle[] particles;
    private float length;
    private float width;
    private int xNum=13,yNum=1;
    private float interval=1;
    private double[] weighs;
    private float noiseR=4;
    private float noiseQ=(float)0.01;
    private float compareRate=20;
    private int N=100;//粒子数
    private int macNum;//选用节点个数
    private int[] idStorage;//储存mac编号
    private point center;
    private Handler handler;
    private Context context;
    public double maxWeigh=0;
    private int xH=15,xL=0,yH=4,yL=0;
    public particleFilter(Context _context,
                          String name
    )
    {
        /*初始化
        *
        *
        * */
        length=(float) 12;
        width=(float)0;
        xNum=(int)length+1;
        yNum=(int)width+1;
        map=new float[100][100][35];

        databaseName=name;
        context=_context;
        dbhelper=new Db(context,databaseName,null,1);
        dbRead=dbhelper.getReadableDatabase();
        wifiManager=(WifiManager) context.getSystemService(WIFI_SERVICE);
        bssidList=new String[35];
        wifiObserve=new float[35];
        particles=new Particle[N];
        weighs=new double[N];


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
    public int transBssidToNum(String bssid)
    {
        for(int i=0;i<35;i++)
        {
            if(bssid.equals(bssidList[i]))return i;
        }
        return -1;
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

    public void initialParticles(float x,float y,float stepLength,double orientation)
    {
        /*
        * 初始化粒子
        *
        * */
        for(int i=0;i<N;i++)
        {
            particles[i]=new Particle(x,y,(float) Math.random()*0.1f-0.05f+stepLength,Math.random()*0.17-0.085+orientation);
            weighs[i]=1.0/N;
        }
    }
    public void turn(double orientation){
        for(int i=0;i<N;i++){
            particles[i].orientation=Math.random()*0.17-0.085+orientation;
        }
    }
    public void move(float var)
    {
        for(int i=0;i<N;i++)
        {

            particles[i].move(var);
            particles[i].constain(xL,xH,yL,yH);
            //weighs[i]*=Math.exp(-exNoise*exNoise/2/noiseQ);
        }
    }
    public void move(double step,double angle){
        for(int i=0;i<N;i++)
        {

            particles[i].move(step+ Math.random()*0.1f-0.05f,angle+Math.random()*0.17-0.085);
            particles[i].constain(xL,xH,yL,yH);
            //weighs[i]*=Math.exp(-exNoise*exNoise/2/noiseQ);
        }
    }

    public void update()
    {

        /*
        * 权值计算
        * 多维高斯乘积
        * 余弦
        * 距离倒数
        * */
        for(int i=0;i<N;i++)
        {
            if(macNum==0)return;
            double temp=0;


            double dis=0;
            for(int j=0;j<macNum;j++) {
                temp+=Math.pow((map[Math.round(particles[i].x)][Math.round(particles[i].y)][idStorage[j]]-wifiObserve[j]),2);
            }

            temp=Math.exp((-temp/2/(3*3)/macNum));
            //if(dis==0)dis=0.00001;
            //dis=1.0/Math.sqrt(dis);距离倒数
            //weighs[i]*=N*dis;
            weighs[i]*=temp;
        }

        double sumw=0;
        for(int i=0;i<N;i++)
        {
            sumw+=weighs[i];
        }
        for(int i=0;i<N;i++)
        {
            weighs[i]/=sumw;
        }
        maxWeigh=getMax(weighs);
    }

    /*
    * 插值法得到更精确的强度
    * */
    public float chazhi(float x,float y,int id){
        float result;
        float tempx=x;
        float tempy=y;
        float[] similar=new float[4];
        if(Math.floor(x)==Math.ceil(tempx)&&Math.floor(y)==Math.ceil(tempy))return map[(int)x][(int)y][id];
        similar[0]=1/(float) Math.sqrt((Math.ceil(tempx)-x)*(Math.ceil(tempx)-x)+(Math.ceil(tempy)-y)*(Math.ceil(tempy)-y));
        similar[1]=1/(float) Math.sqrt((Math.floor(tempx)-x)*(Math.floor(tempx)-x)+(Math.ceil(tempy)-y)*(Math.ceil(tempy)-y));
        similar[2]=1/(float) Math.sqrt((Math.ceil(tempx)-x)*(Math.ceil(tempx)-x)+(Math.floor(tempy)-y)*(Math.floor(tempy)-y));
        similar[3]=1/(float) Math.sqrt((Math.floor(tempx)-x)*(Math.floor(tempx)-x)+(Math.floor(tempy)-y)*(Math.floor(tempy)-y));
        float all=similar[0]+similar[1]+similar[2]+similar[3];
        result=similar[0]/all*map[(int)Math.ceil(tempx)][(int)Math.ceil(tempy)][id]+
                similar[1]/all*map[(int)Math.floor(tempx)][(int)Math.ceil(tempy)][id]+
                similar[2]/all*map[(int)Math.ceil(tempx)][(int)Math.floor(tempy)][id]+
                similar[3]/all*map[(int)Math.floor(tempx)][(int)Math.floor(tempy)][id];
        return result;
    }

    public void resample(){
        for(int i=0;i<N;i++)
        {
            double wmax= 2*getMax(weighs) * Math.random();
            int index=(int)(Math.random()*100);
            while(wmax > weighs[index])
            {
                wmax = wmax - weighs[index];
                index = index + 1;
                if (index>= N) index = 0;
            }

            particles[i].copy(particles[index]);    //得到新粒子
        }
        for(int i=0;i<N;i++)
        {
            weighs[i]=1.0/N;
        }
    }
    public double getMax(double[] arr){
        double max=arr[0];
        for(int i=1;i<arr.length;i++){
            if(arr[i]>max)
            {
                max=arr[i];
            }
        }
        return max;
    }

    public boolean ifresample(){
        double temp=0;

        for(int i=0;i<N;i++)
        {
            temp+=weighs[i]*weighs[i];
        }
        float rate=(float)(1.0/temp);
        return  rate<compareRate;
    }

    public point makeCenter(){
        float x=0,y=0;
        for(int i=0;i<N;i++)
        {
            x+=particles[i].x*weighs[i];
            y+=particles[i].y*weighs[i];
        }
        center=new point(x,y);
        return center;
    }


}

