package com.fengmap.FMDemoBaseMap;

import android.app.Activity;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.hardware.Sensor;
import android.hardware.SensorManager;
import android.net.wifi.ScanResult;
import android.net.wifi.WifiManager;
import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.os.PowerManager;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.LinearLayout;
import android.widget.TextView;

import com.fengmap.FMDemoBaseMap.algorithms.KNN;
import com.fengmap.FMDemoBaseMap.algorithms.KalmanFilter;
import com.fengmap.FMDemoBaseMap.algorithms.particleFilter;
import com.fengmap.FMDemoBaseMap.help.DeviceAttitudeHandle;
import com.fengmap.FMDemoBaseMap.help.PdrCall;
import com.fengmap.FMDemoBaseMap.help.Window;
import com.fengmap.FMDemoBaseMap.help.pdr;
import com.fengmap.FMDemoBaseMap.help.point;
import com.fengmap.FMDemoBaseMap.utils.FileUtils;
import com.fengmap.FMDemoBaseMap.utils.ViewHelper;
import com.fengmap.android.FMErrorMsg;
import com.fengmap.android.analysis.navi.FMNaviAnalyser;
import com.fengmap.android.analysis.navi.FMNaviResult;
import com.fengmap.android.data.OnFMDownloadProgressListener;
import com.fengmap.android.exception.FMObjectException;
import com.fengmap.android.map.FMMap;
import com.fengmap.android.map.FMMapUpgradeInfo;
import com.fengmap.android.map.FMMapView;
import com.fengmap.android.map.FMPickMapCoordResult;
import com.fengmap.android.map.FMViewMode;
import com.fengmap.android.map.event.OnFMMapClickListener;
import com.fengmap.android.map.event.OnFMMapInitListener;
import com.fengmap.android.map.geometry.FMMapCoord;
import com.fengmap.android.map.layer.FMImageLayer;
import com.fengmap.android.map.layer.FMLineLayer;
import com.fengmap.android.map.marker.FMImageMarker;
import com.fengmap.android.map.marker.FMLineMarker;
import com.fengmap.android.map.marker.FMSegment;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketException;
import java.net.UnknownHostException;
import java.util.ArrayList;
import java.util.List;
import java.util.Timer;

import static android.content.ContentValues.TAG;
import static com.fengmap.FMDemoBaseMap.R.id.d2;
import static com.loopj.android.http.AsyncHttpClient.LOG_TAG;

/**
 * @Email hezutao@fengmap.com
 * @Version 2.0.0
 * @Description 主页面
 * <p>在Android6.0以上版本使用fengmap地图之前，应注意android.permission.WRITE_EXTERNAL_STORAGE、
 * permission:android.permission.READ_EXTERNAL_STORAGE权限申请</p>
 */

/**
 * @Email hezutao@fengmap.com
 * @Version 2.0.0
 * @Description 2D 3D显示切换
 * <p>地图为2D模式时候,将会禁用手势倾斜功能</p>
 */
public class MapApiDemoMain extends Activity  implements OnFMMapInitListener, View.OnClickListener, OnFMMapClickListener {
    private FMMapView mMapView;
    private FMMap mFMMap;
    private Button[] mButtons = new Button[2];
    private int mPosition = 1;
    private FMImageLayer mImageLayer;
    private FMImageMarker mImageMarker;
    private Bitmap bitmap;
    private TextView show;
    //wifi类参数
    private Handler handler;
    private particleFilter pF;
    private WifiManager wifiManager;
    private SensorManager mSensorManager;
    private Sensor stepDetect;
    private DeviceAttitudeHandle device;
    int bssidNum = 20;
    private String[] bssidList={"d4:94:e8:1e:af:20",
            "d4:94:e8:1e:ac:a0",
            "d4:94:e8:1e:ae:80",
            "d4:94:e8:1a:0f:e0",
            "d4:94:e8:1a:33:80",
            "d4:94:e8:1a:11:40",
            "d4:94:e8:1e:a5:e0",
            "d4:94:e8:21:6a:20",
            "d4:94:e8:21:6b:00",
            "d4:94:e8:21:6a:80",
            "d4:94:e8:1e:af:30",
            "d4:94:e8:1e:ac:b0",
            "d4:94:e8:1e:ae:90",
            "d4:94:e8:1a:0f:f0",
            "d4:94:e8:1a:33:90",
            "d4:94:e8:1a:11:50",
            "d4:94:e8:1e:a5:f0",
            "d4:94:e8:21:6a:30",
            "d4:94:e8:21:6b:10",
            "d4:94:e8:21:6a:90"};
    private int[] levelList=new int[bssidNum];
    private int scanNum=0;

    private KNN knn;
    private Timer timer;
    private point center=new point(0,0),center1,center2,finalcenter;
    private Window mwindow;
    //滤波器参数
    private KalmanFilter filter;
    //private float x,y;
    //传感器参数
    private pdr mpdr;
    private String databaseName="wifistorage.db";
    private int renum;
    private float stepLength=0,orientation=0;
    //通信参数
    DatagramSocket socket;
    InetAddress serverAddress,robAddress;

    int port=8080;
    int servicePort=8081;
    TextView ip, ipService ;


    //ui
    boolean ifStart = false;
    Button control;

    //放锁屏
    PowerManager pManager;
    PowerManager.WakeLock mWakeLock;
    private BroadcastReceiver mReceiver = new BroadcastReceiver() {

        @Override
        public void onReceive(Context context, Intent intent) {
            final String action = intent.getAction();
            // wifi已成功扫描到可用wifi。
            if (action.equals(WifiManager.SCAN_RESULTS_AVAILABLE_ACTION)) {
                if(!ifStart) {return;}
                List<ScanResult> scanList = new ArrayList<ScanResult>(wifiManager.getScanResults());
                for(ScanResult scanResult : scanList){//滤去非南开WIfi
                    if(scanResult.SSID.equals("NKU_WLAN")){
                        int temp =transBssidToNum(scanResult.BSSID);
                        if(temp!=-1)
                        {
                            levelList[temp]=scanResult.level;

                        }

                    }
                }
                scanNum++;
                new Thread(sendWifi).start();
                Message msg=new Message();
                //msg.what=num;
                //handler.sendMessage(msg);
                try {
                    Thread.currentThread().sleep(500);//阻断0.5秒
                } catch (InterruptedException e) {
                    e.printStackTrace();
                }
                wifiManager.startScan();


            }
        }
    };

    public int transBssidToNum(String bssid)
    {
        for(int i=0;i<bssidNum;i++)
        {
            if(bssid.equals(bssidList[i]))return i;
        }
        return -1;
    }

    private class pdrSend implements PdrCall{
        public void OnStepDetected(float stepLengthGet,float orientationGet){
            if(!ifStart) {return;}
            stepLength=stepLengthGet;
            orientation=orientationGet;
            new Thread(sendPdr).start();

        }
    }
    pdrSend mpdrSend=new pdrSend();

    class MyThread implements Runnable{
        @Override
        public void run() {
            while (true) {
                byte data[] = new byte[1024];
                DatagramPacket packet = new DatagramPacket(data, data.length);
                try {
                    socket.receive(packet);
                } catch (IOException e) {
                    e.printStackTrace();
                }
                String result = new String(packet.getData(), packet.getOffset(), packet.getLength());
                //if(result.equals("over"))return;
                String[] location = result.split(",");
                //System.out.println(location[0] + "," + location[1]);
                float x=Float.parseFloat(location[0]);
                float y=Float.parseFloat(location[1]);
                center=new point(x,y);
                Message msg=new Message();
                handler.sendMessage(msg);
            }
        }
    }



    Runnable sendPdr = new Runnable() {

        @Override
        public void run() {
            // TODO
            // 在这里进行 http request.网络请求相关操作
            if(serverAddress==null){return;}
            //发送给pc端
            String str = "1,";

            str=str+stepLength+","+orientation;
            byte dataSend[] = str.getBytes();
            DatagramPacket packetSend = new DatagramPacket(dataSend, dataSend.length, serverAddress, port);
            try {

                socket.send(packetSend);
            } catch (Exception e) {
                Log.e(LOG_TAG, e.toString());
            }
        }
    };
    Runnable sendOK = new Runnable() {

        @Override
        public void run() {
            // TODO
            // 在这里进行 http request.网络请求相关操作
            if(serverAddress==null){return;}
            //发送给pc端
            String str = "start";
            byte dataSend[] = str.getBytes();
            DatagramPacket packetSend = new DatagramPacket(dataSend, dataSend.length, serverAddress, port);
            try {

                socket.send(packetSend);
            } catch (Exception e) {
                Log.e(LOG_TAG, e.toString());
            }
        }
    };
    Runnable sendOver = new Runnable() {

        @Override
        public void run() {
            // TODO
            // 在这里进行 http request.网络请求相关操作
            if(serverAddress==null){return;}
            //发送给pc端
            String str = "over";
            byte dataSend[] = str.getBytes();
            DatagramPacket packetSend = new DatagramPacket(dataSend, dataSend.length, serverAddress, port);
            try {

                socket.send(packetSend);
            } catch (Exception e) {
                Log.e(LOG_TAG, e.toString());
            }
            serverAddress=null;
        }
    };

    Runnable sendWifi = new Runnable() {

        @Override
        public void run() {
            // TODO
            // 在这里进行 http request.网络请求相关操作
            if(serverAddress==null){return;}
            //发送给pc端
            String str = "0,";
            str=str+levelList[0];
            for(int i = 1;i<20;i++){
                str=str+","+levelList[i];
            }
            byte dataSend[] = str.getBytes();
            DatagramPacket packetSend = new DatagramPacket(dataSend, dataSend.length, serverAddress, port);
            try {

                socket.send(packetSend);
            } catch (Exception e) {
                Log.e(LOG_TAG, e.toString());
            }
            for(int i=0;i<20;i++)
            {
                levelList[i]=-100;
            }
        }
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_2d3d);

        show=(TextView) findViewById(R.id.show);

        openMapByPath();
        mFMMap.setOnFMMapClickListener(this);

        //wifi的初始化
        imporDatabase();
        wifiManager=(WifiManager)getSystemService(WIFI_SERVICE);

        //控件初始化
        ip =(TextView)findViewById(R.id.ip);
        ipService = (TextView)findViewById(R.id.ipService);
        control = (Button) findViewById(R.id.control);

        try {
            socket = new DatagramSocket(8080);
            socket.setBroadcast(true);
        }
        catch (SocketException e)
        {
            e.printStackTrace();
        }
        for(int i=0;i<bssidNum;i++)
        {
            levelList[i]=-100;
        }


        handler = new Handler() {

            @Override
            public void handleMessage(Message msg) {
                point tempCenter=new point(center);
                Drew(tempCenter);
            }


        };
        mpdr=new pdr((SensorManager) getSystemService(Context.SENSOR_SERVICE));
        //pdr回调声明
        mpdr.registerCall(mpdrSend);
        MyThread myThread=new MyThread();
        new Thread(myThread).start();

    }

    @Override
    protected void onResume() {
        super.onResume();
        registerWifiBroadcast();
        mpdr.register();
        pManager = ((PowerManager) getSystemService(POWER_SERVICE));
        mWakeLock = pManager.newWakeLock(PowerManager.SCREEN_BRIGHT_WAKE_LOCK
                | PowerManager.ON_AFTER_RELEASE, TAG);
        mWakeLock.acquire();
    }
    @Override
    protected void onStop()
    {
        unregisterReceiver(mReceiver);
        new Thread(sendOver).start();
        super.onStop();
    }
    public void imporDatabase() {
        //存放数据库的目录
        String dirPath="/data/data/"+getPackageName()+"/databases";
        File dir = new File(dirPath);
        if(!dir.exists()) {
            dir.mkdir();
        }
        //数据库文件
        File file = new File(dir, databaseName);
        try {
            if(!file.exists()) {
                file.createNewFile();
            }
            //加载需要导入的数据库
            InputStream is = this.getApplicationContext().getResources().openRawResource(R.raw.wifistorage);
            FileOutputStream fos = new FileOutputStream(file);
            byte[] buffere=new byte[is.available()];
            is.read(buffere);
            fos.write(buffere);
            is.close();
            fos.close();
        }catch(FileNotFoundException e){
            e.printStackTrace();
        }catch(IOException e) {
            e.printStackTrace();
        }
    }

    private void registerWifiBroadcast() {
        IntentFilter filter = new IntentFilter();
        filter.addAction(WifiManager.SCAN_RESULTS_AVAILABLE_ACTION);
        registerReceiver(mReceiver, filter);
    }
    /*
    * 注册计步传感器
    *用来给予粒子控制量
    *
    * */

    //按钮
    public void StartOrStop(View view){

        if(ifStart==false) {

            try {
                serverAddress = InetAddress.getByName(""+ip.getText());
            }
            catch (UnknownHostException e)
            {
                e.printStackTrace();
            }

            wifiManager.startScan();
            control.setText("stop");
            ifStart=true;
            new Thread(sendOK).start();

        }
        else {
            control.setText("start");
            ifStart=false;

            new Thread(sendOver).start();
        }
    }

    Runnable sendRequ = new Runnable() {

        @Override
        public void run() {
            // TODO
            //请求发送给pc端
            String str = "service request";
            byte dataSend[] = str.getBytes();
            DatagramPacket packetSend = new DatagramPacket(dataSend, dataSend.length, serverAddress, port);
            try {
                socket.send(packetSend);
            } catch (Exception e) {
                Log.e(LOG_TAG, e.toString());
            }
        }
    };
    public void sendPose(View view){

        new Thread(sendRequ).start();
    }



    /**
     * 加载地图数据
     */
    private void openMapByPath() {
        mMapView = (FMMapView) findViewById(R.id.map_view);
        mFMMap = mMapView.getFMMap();
        mFMMap.setOnFMMapInitListener(this);
        //加载离线数据
        String path = FileUtils.getDefaultMapPath(this);
        mFMMap.openMapByPath(path);
    }

    /**
     * 地图加载成功回调事件
     *
     * @param path 地图所在sdcard路径
     */
    @Override
    public void onMapInitSuccess(String path) {
        //加载离线主题
        mFMMap.loadThemeByPath(FileUtils.getDefaultThemePath(this));
        mFMMap.setZoomLevel(20, false);
        //线图层
        mLineLayer = mFMMap.getFMLayerProxy().getFMLineLayer();
        mFMMap.addLayer(mLineLayer);

        mFMMap.setZoomLevel(20, false);
        setViewMode();
        LinearLayout view = ViewHelper.getView(MapApiDemoMain.this, R.id.layout_mode);
        for (int i = 0; i < view.getChildCount(); i++) {
            mButtons[i] = (Button) view.getChildAt(i);
            mButtons[i].setTag(i);
            mButtons[i].setEnabled(true);
            mButtons[i].setOnClickListener(this);
        }
        mButtons[mPosition].setEnabled(false);

        int groupId = mFMMap.getFocusGroupId();
        //获取图片图层
        mImageLayer = mFMMap.getFMLayerProxy().createFMImageLayer(groupId);
        mFMMap.addLayer(mImageLayer);



        //导航分析
        try {
            mNaviAnalyser = FMNaviAnalyser.getFMNaviAnalyserById(FileUtils.DEFAULT_MAP_ID);
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (FMObjectException e) {
            e.printStackTrace();
        }

    }

    public void Drew(point m) { //FMMapCoord 坐标类

        //地图拾取对象
        m.rotmatrix();
        FMMapCoord centerCoord = new FMMapCoord(m.x,m.y);
        //mFMMap.moveToCenter(centerCoord, true);
        if(mImageMarker==null){
        bitmap = BitmapFactory.decodeResource(getResources(), R.drawable.ic_marker_blue);
        mImageMarker = new FMImageMarker(centerCoord, bitmap);
            //设置图片宽高
        mImageMarker.setMarkerWidth(80);
        mImageMarker.setMarkerHeight(80);
            //设置图片垂直偏离距离
        mImageMarker.setFMImageMarkerOffsetMode(FMImageMarker.FMImageMarkerOffsetMode.FMNODE_CUSTOM_HEIGHT);
        mImageMarker.setCustomOffsetHeight(3);
        mImageLayer.addMarker(mImageMarker);
        }
        else
        {
            mImageLayer.removeMarker(mImageMarker);
            mImageMarker=new FMImageMarker(centerCoord, bitmap);
            mImageLayer.addMarker(mImageMarker);
        }
    }




    /**
     * 地图加载失败回调事件
     *
     * @param path      地图所在sdcard路径
     * @param errorCode 失败加载错误码，可以通过{@link FMErrorMsg#getErrorMsg(int)}获取加载地图失败详情
     */
    @Override
    public void onMapInitFailure(String path, int errorCode) {
        //TODO 可以提示用户地图加载失败原因，进行地图加载失败处理
    }

    /**
     * 当{@link FMMap#openMapById(String, boolean)}设置openMapById(String, false)时地图不自动更新会
     * 回调此事件，可以调用{@link FMMap#upgrade(FMMapUpgradeInfo, OnFMDownloadProgressListener)}进行
     * 地图下载更新
     *
     * @param upgradeInfo 地图版本更新详情,地图版本号{@link FMMapUpgradeInfo#getVersion()},<br/>
     *                    地图id{@link FMMapUpgradeInfo#getMapId()}
     * @return 如果调用了{@link FMMap#upgrade(FMMapUpgradeInfo, OnFMDownloadProgressListener)}地图下载更新，
     * 返回值return true,因为{@link FMMap#upgrade(FMMapUpgradeInfo, OnFMDownloadProgressListener)}
     * 会自动下载更新地图，更新完成后会加载地图;否则return false。
     */
    @Override
    public boolean onUpgrade(FMMapUpgradeInfo upgradeInfo) {
        //TODO 获取到最新地图更新的信息，可以进行地图的下载操作
        return false;
    }

    @Override
    public void onClick(View v) {
        Button button = (Button) v;
        int position;
        if(button.getId()==d2)
        {
            position=0;
        }
        else
        position=1;
        setPosition(position);
        setViewMode();
    }

    /**
     * 切换地图显示模式
     */
    private void setViewMode() {
        if (mPosition == 0) {
            mFMMap.setFMViewMode(FMViewMode.FMVIEW_MODE_2D); //设置地图2D显示模式
        } else {
            mFMMap.setFMViewMode(FMViewMode.FMVIEW_MODE_3D); //设置地图3D显示模式
        }
    }

    /**
     * 设置2D、3D选择效果
     *
     * @param position 按钮索引
     */
    private void setPosition(int position) {
        if (mPosition == position) {
            return;
        }
        mButtons[position].setEnabled(false);
        mButtons[mPosition].setEnabled(true);
        mPosition = position;
    }

    /**
     * 地图销毁调用
     */
    @Override
    public void onBackPressed() {
        if (mFMMap != null) {
            mFMMap.onDestroy();
        }
        super.onBackPressed();
    }

    /**
     * 线图层
     */
    protected FMLineLayer mLineLayer;
    /**
     * 导航分析
     */
    protected FMNaviAnalyser mNaviAnalyser;
    /**
     * 地图视图
     */
    protected FMMapCoord stCoord;
    /**
     * 起点楼层
     */
    protected int stGroupId;
    /**
     * 起点图层
     */
    protected FMImageLayer stImageLayer;
    /**
     * 终点坐标
     */
    protected FMMapCoord endCoord;
    /**
     * 终点楼层id
     */
    protected int endGroupId;
    /**
     * 终点图层
     */
    protected FMImageLayer endImageLayer;

    protected void clear() {
        clearLineLayer();
        clearStartImageLayer();
        clearEndImageLayer();
    }


    /**
     * 清除线图层
     */
    protected void clearLineLayer() {
        if (mLineLayer != null) {
            mLineLayer.removeAll();
        }
    }

    /**
     * 清除起点图层
     */
    protected void clearStartImageLayer() {
        if (stImageLayer != null) {
            stImageLayer.removeAll();
            mFMMap.removeLayer(stImageLayer); // 移除图层
            stImageLayer = null;
        }
    }

    /**
     * 清除终点图层
     */
    protected void clearEndImageLayer() {
        if (endImageLayer != null) {
            endImageLayer.removeAll();
            mFMMap.removeLayer(endImageLayer); // 移除图层

            endImageLayer = null;
        }
    }


    /**
     *  添加线标注
     */
    protected void addLineMarker() {
        ArrayList<FMNaviResult> results = mNaviAnalyser.getNaviResults();
        // 填充导航数据
        ArrayList<FMSegment> segments = new ArrayList<>();
        for (FMNaviResult r : results) {
            int groupId = r.getGroupId();
            FMSegment s = new FMSegment(groupId, r.getPointList());
            segments.add(s);
        }
        //添加LineMarker
        FMLineMarker lineMarker = new FMLineMarker(segments);
        lineMarker.setLineWidth(3f);
        mLineLayer.addMarker(lineMarker);
    }

    /**
     * 创建起点图标
     */
    protected void createStartImageMarker() {
        clearStartImageLayer();
        // 添加起点图层
        stImageLayer = new FMImageLayer(mFMMap, stGroupId);
        mFMMap.addLayer(stImageLayer);
        // 标注物样式
        FMImageMarker imageMarker = ViewHelper.buildImageMarker(getResources(), stCoord,R.drawable.start);
        stImageLayer.addMarker(imageMarker);
    }

    /**
     * 创建终点图层
     */
    protected void createEndImageMarker() {
        clearEndImageLayer();
        // 添加起点图层
        endImageLayer = new FMImageLayer(mFMMap, endGroupId);
        mFMMap.addLayer(endImageLayer);
        // 标注物样式
        FMImageMarker imageMarker = ViewHelper.buildImageMarker(getResources(), endCoord, R.drawable.end);
        endImageLayer.addMarker(imageMarker);
    }
    private void analyzeNavigation() {
        int type = mNaviAnalyser.analyzeNavi(stGroupId, stCoord, endGroupId, endCoord,
                FMNaviAnalyser.FMNaviModule.MODULE_SHORTEST);
        if (type == FMNaviAnalyser.FMRouteCalcuResult.ROUTE_SUCCESS) {
            addLineMarker();
            //行走总距离
            //double sceneRouteLength = mNaviAnalyser.getSceneRouteLength();
            //setSceneRouteLength(sceneRouteLength);
        }
    }


    public void onMapClick(float x, float y) {
        // 获取屏幕点击位置的地图坐标
        final FMPickMapCoordResult mapCoordResult = mFMMap.pickMapCoord(x, y);
        if (mapCoordResult == null) {
            return;
        }

        // 起点
        if (stCoord == null) {
            clear();

            stCoord = mapCoordResult.getMapCoord();
            stGroupId = mapCoordResult.getGroupId();
            createStartImageMarker();
            return;
        }

        // 终点
        if (endCoord == null) {
            endCoord = mapCoordResult.getMapCoord();
            endGroupId = mapCoordResult.getGroupId();
            createEndImageMarker();
        }

        analyzeNavigation();

        // 画完置空
        stCoord = null;
        endCoord = null;
    }
}

