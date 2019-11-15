package com.testweb;

import android.app.Activity;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.net.wifi.ScanResult;
import android.net.wifi.WifiManager;
import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.os.PowerManager;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketException;
import java.net.UnknownHostException;
import java.util.ArrayList;
import java.util.List;
import java.util.Timer;

import static android.content.ContentValues.TAG;

public class AndroidClientActivity extends Activity {

    DatagramSocket socket;
    InetAddress serverAddress;
    Timer timer;
    TextView portText;
    int port=8080;
    TextView ip ;
    TextView showNum ;
    boolean ifStart = false;
    Button control ;

    private static String LOG_TAG = "WifiBroadcastActivity";
    private Handler handler;
    int num =0;
    private WifiManager wifiManager;
    private BroadcastReceiver mReceiver;
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
    PowerManager pManager;
    PowerManager.WakeLock mWakeLock;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_android_client);


        try {
            socket = new  DatagramSocket (8080);
        }
        catch (SocketException e)
        {
            e.printStackTrace();
        }
        for(int i=0;i<bssidNum;i++)
        {
            levelList[i]=-100;
        }
        wifiManager=(WifiManager)getSystemService(WIFI_SERVICE);
        ip =(TextView)findViewById(R.id.ip);
        control = (Button) findViewById(R.id.control);
        showNum =(TextView)findViewById(R.id.num);
        portText = (TextView)findViewById(R.id.PORT);

        mReceiver = new BroadcastReceiver() {

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
                    num++;
                    new Thread(networkTask).start();
                    Message msg=new Message();
                    msg.what=num;
                    handler.sendMessage(msg);
                    try {
                        Thread.currentThread().sleep(500);//阻断0.5秒
                    } catch (InterruptedException e) {
                        e.printStackTrace();
                    }
                    wifiManager.startScan();

                }
            }
        };

        handler = new Handler() {

            @Override
            public void handleMessage(Message msg) {
                switch (msg.what) {
                    default:

                        showNum.setText(num+"");

                        break;

                }
            }

        };

        IntentFilter filter = new IntentFilter();
        filter.addAction(WifiManager.SCAN_RESULTS_AVAILABLE_ACTION);
        registerReceiver(mReceiver, filter);
    }

    @Override
    protected void onResume() {
        super.onResume();
        pManager = ((PowerManager) getSystemService(POWER_SERVICE));
        mWakeLock = pManager.newWakeLock(PowerManager.SCREEN_BRIGHT_WAKE_LOCK
                | PowerManager.ON_AFTER_RELEASE, TAG);
        mWakeLock.acquire();
    }

    @Override
    protected void onPause() {
        super.onPause();

        if(null != mWakeLock){
            mWakeLock.release();
        }
    }

    Runnable networkTask = new Runnable() {

        @Override
        public void run() {
            // TODO
            // 在这里进行 http request.网络请求相关操作
            if(serverAddress==null){return;}
            //发送给pc端
            String str = "";
            for(int i = 0;i<20;i++){
                str=str+","+levelList[i];
            }
            str=str+"\n";
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

    public int transBssidToNum(String bssid)
    {
        for(int i=0;i<bssidNum;i++)
        {
            if(bssid.equals(bssidList[i]))return i;
        }
        return -1;
    }
    public void StartOrStop(View view){

        if(ifStart==false) {

            try {
                serverAddress = InetAddress.getByName(""+ip.getText());
            }
            catch (UnknownHostException e)
            {
                e.printStackTrace();
            }
            /*
            timer = new Timer();
            timer.scheduleAtFixedRate(new TimerTask() {
                @Override
                public void run() {
                    wifiManager.startScan();

                }
            }, 0, 3000);
            */

            wifiManager.startScan();
            control.setText("stop");
            ifStart=true;
        }
        else {
            //timer.cancel();
            control.setText("start");
            serverAddress=null;
            ifStart=false;
        }
    }
}