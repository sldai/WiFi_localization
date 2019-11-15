package com.nku.heinrich.myapplication;

import android.app.Activity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TextView;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.NetworkInterface;
import java.net.SocketException;
import java.util.Enumeration;

public class MainActivity extends Activity {

    private static String LOG_TAG = "WifiBroadcastActivity";
    private boolean start = true;
    private EditText IPAddress;
    private String address;
    public static final int DEFAULT_PORT = 8080;
    private static final int MAX_DATA_PACKET_LENGTH = 40;
    private byte[] buffer = new byte[MAX_DATA_PACKET_LENGTH];
    Button startButton;
    Button stopButton;
    TextView label;

    private DatagramSocket msocketClient;
    private DatagramPacket Packet_Receive;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        IPAddress = (EditText) this.findViewById(R.id.address);
        startButton = (Button) this.findViewById(R.id.start);
        stopButton = (Button) this.findViewById(R.id.stop);
        label = (TextView) this.findViewById(R.id.label);
        startButton.setEnabled(true);
        stopButton.setEnabled(false);


        //new Thread(new TcpReceive()).start();
        Open();
        address = getLocalIPAddress();
        if (address != null) {
            IPAddress.setText(address);
        } else {
            IPAddress.setText("Can not get IP address");

            return;
        }
        startButton.setOnClickListener(listener);
        stopButton.setOnClickListener(listener);
    }

    private View.OnClickListener listener = new View.OnClickListener() {

        @Override
        public void onClick(View v) {
            label.setText("");
            if (v == startButton) {
                start = true;

                new BroadCastUdp(IPAddress.getText().toString()).start();
                startButton.setEnabled(false);
                stopButton.setEnabled(true);
            } else if (v == stopButton) {
                start = false;
                startButton.setEnabled(true);
                stopButton.setEnabled(false);
            }
        }
    };

    private String getLocalIPAddress() {
        try {
            for (Enumeration<NetworkInterface> en = NetworkInterface
                    .getNetworkInterfaces(); en.hasMoreElements(); ) {
                NetworkInterface intf = en.nextElement();
                for (Enumeration<InetAddress> enumIpAddr = intf
                        .getInetAddresses(); enumIpAddr.hasMoreElements(); ) {
                    InetAddress inetAddress = enumIpAddr.nextElement();
                    if (!inetAddress.isLoopbackAddress()) {
                        return inetAddress.getHostAddress().toString();
                    }
                }
            }
        } catch (SocketException ex) {
            Log.e(LOG_TAG, ex.toString());
        }
        return null;
    }

    public class BroadCastUdp extends Thread {
        private String dataString;
        // private DatagramSocket udpSocket;

        public BroadCastUdp(String dataString) {
            this.dataString = dataString;
        }

        public void run() {
            DatagramPacket dataPacket = null;

            try {
                // udpSocket = new DatagramSocket(DEFAULT_PORT);

                dataPacket = new DatagramPacket(buffer, MAX_DATA_PACKET_LENGTH);
                byte[] data = dataString.getBytes();
                dataPacket.setData(data);
                dataPacket.setLength(data.length);
                dataPacket.setPort(DEFAULT_PORT);

                InetAddress broadcastAddr;

                //  broadcastAddr = InetAddress.getByName("255.255.255.255");
                //这里写目的IP地址
                broadcastAddr = InetAddress.getByName("10.129.227.145");
                dataPacket.setAddress(broadcastAddr);
            } catch (Exception e) {
                Log.e(LOG_TAG, e.toString());
            }
            // while( start ){
            try {
                // udpSocket.send(dataPacket);
                if (msocketClient!=null){
                    msocketClient.send(dataPacket);
                }
                sleep(10);
            } catch (Exception e) {
                Log.e(LOG_TAG, e.toString());
            }
            // }

            // udpSocket.close();

        }
    }

    public void Open() {
        try {
            msocketClient = new DatagramSocket(DEFAULT_PORT);
        } catch (Exception e) {
            e.printStackTrace();
        }
        if (msocketClient != null) {
            new Thread(UdpReceiver).start();
        }
    }

    Runnable UdpReceiver = new Runnable() {
        @Override
        public void run() {
            while (true) {
                byte[] Buffer_Receive = new byte[1024];
                Packet_Receive = new DatagramPacket(Buffer_Receive, 1024);
                if (Packet_Receive != null) {
                    try {
                        msocketClient.receive(Packet_Receive);
                        int length = Packet_Receive.getLength();
                        if (length > 0) {
                            final String data = new String(Packet_Receive.getData());
                            runOnUiThread(new Runnable() {
                                @Override
                                public void run() {
                                    label.setText(data);
                                }
                            });
                        }
                    } catch (IOException e) {
                        e.printStackTrace();
                    }
                }
            }
        }
    };



}
