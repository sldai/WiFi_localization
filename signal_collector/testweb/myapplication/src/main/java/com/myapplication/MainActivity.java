package com.myapplication;

import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.support.v7.app.AppCompatActivity;
import android.widget.TextView;

import java.util.Timer;
import java.util.TimerTask;

public class MainActivity extends AppCompatActivity {

    private KalmanFilter filter;
    private double noise=1;

    double x=0,y=0,dx=0,dy=0,rx=0,ry=0;
    private Handler handler;
    TextView show;
    private int num=0;
    private Timer timer;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        show=(TextView) findViewById(R.id.show);
        filter = new KalmanFilter(4, 4);



        /* Assuming the axes are rectilinear does not work well at the
         poles, but it has the bonus that we don't need to convert between
         lat/long and more rectangular coordinates. The slight inaccuracy
         of our physics model is not too important.
       */
        filter.setStateTransition(1, 0, 1, 0,
                0, 1, 0, 1,
                0, 0, 1, 0,
                0, 0, 0, 1);

        /* We observe (x, y) in each time step */
        filter.setObservationModel(1.0, 0.0, 0.0, 0.0,
                0.0, 1.0, 0.0, 0.0,
                0.0, 0.0, 1.0, 0.0,
                0.0, 0.0, 0.0, 1.0
                );
        /* Noise in the world. */

        filter.setProcessNoiseCovariance(0.01,0.0, 0.0, 0.0,
                0, 0, 0.01, 0.0,
                0.0, 0.0, 0.01, 0.0,
                0.0, 0.0, 0.0, 0.01);

        filter.getObservationNoiseCovariance().setMatrix(0.05, 0,0,0,
                0.0, 0.05,0,0,
                0.0, 0.0,0,0,
                0.0, 0.0,0,0
                );

        // The start position is totally unknown, so give a high variance
        filter.setStateEstimate(0l,0l,02,02);
        filter.getEstimateCovariance().setMatrix(0.1, 0,0,0,
                0.0, 0.1,0,0,
                0.0, 0.0,0.1,0,
                0.0, 0.0,0.0,0.1
        );


        timer = new Timer();



        timer.scheduleAtFixedRate(new TimerTask() {
            @Override
            public void run() {





                x+=dx+1*Math.random()-0.5;
                y+=dy+1*Math.random()-0.5;
                rx+=dx;
                ry+=dy;
                dx=2+1*Math.random()-0.5;
                dy=2+1*Math.random()-0.5;
                filter.setObservation(x, y,dx,dy);

                filter.update();



                Message msg=new Message();
                msg.what=num;
                handler.sendMessage(msg);
            }
        },0,1000);

        handler = new Handler() {

            @Override
            public void handleMessage(Message msg) {
                show.setText(""+(float)x+","+(float)y+"\n"+(float)filter.getStateEstimate().getData()[0][0]+","+(float)filter.getStateEstimate().getData()[1][0]+"\n"+rx+","+ry);
                num++;
            }

        };

    }
}
