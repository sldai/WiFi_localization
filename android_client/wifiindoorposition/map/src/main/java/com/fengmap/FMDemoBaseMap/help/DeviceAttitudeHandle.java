package com.fengmap.FMDemoBaseMap.help;

import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;

/**
 * Created by artz on 26/12/14.
 */
public class DeviceAttitudeHandle implements SensorEventListener {

    private SensorManager mSensorManager;
    private Sensor mSensor;
    private float[] mRotationMatrixFromVector = new float[16] ;
    private float[] mRotationMatrix = new float[16];
    private float[] orientationVals = new float[3];

    private float temp0=0,temp1=0,temp2=0;
    private float accX,accY,accZ;
    private float[] acc={0,0,0};

    private int attitude;
    private float[] average0=new float[10];
    private float[] average1=new float[10];
    private float[] average2=new float[10];


    private int num=0;


    private boolean stepFlag=true;
    private float[] m_lastAccels;
    private float thHigh=12f;
    private float thLow=9.5f;


    public DeviceAttitudeHandle(SensorManager sensorM){
        mSensorManager   = sensorM ;
        mSensor          = mSensorManager.getDefaultSensor(Sensor.TYPE_ROTATION_VECTOR);
    }

    public void start(){
        mSensorManager.registerListener(this, mSensor, SensorManager.SENSOR_DELAY_GAME);
        //mSensorManager.registerListener(this, mSensorManager.getDefaultSensor(Sensor.TYPE_STEP_DETECTOR), SensorManager.SENSOR_DELAY_GAME);
    }

    public void stop(){
        mSensorManager.unregisterListener(this);
    }


    @Override
    public void onSensorChanged(SensorEvent event) {

        int type=event.sensor.getType();

        // StackOverFlow
        if (type == Sensor.TYPE_ROTATION_VECTOR) {
            mSensorManager.getRotationMatrixFromVector(mRotationMatrixFromVector, event.values);


            mSensorManager.getOrientation(mRotationMatrixFromVector, orientationVals);


            temp0=0.8f*temp0+0.2f*orientationVals[0];
            temp1=0.8f*temp1+0.2f*orientationVals[1];
            temp2=0.8f*temp2+0.2f*orientationVals[2];
            average0[num]=temp0;
            average1[num]=temp1;
            average2[num]=temp2;
            num=(num+1)%10;

        }

    }

    // getter yaw
    public float getOrientationYaw(){
        float val=0;
        /*
        for(int i=0;i<10;i++){
            val+=average0[i];
        }
        val=val/10;
        val=-2.6f-val;*/
        val=3.4f-orientationVals[0];
        return val ;
    }


    @Override
    public void onAccuracyChanged(Sensor sensor, int accuracy) {

    }

}
