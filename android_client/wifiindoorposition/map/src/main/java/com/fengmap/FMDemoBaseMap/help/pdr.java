package com.fengmap.FMDemoBaseMap.help;

import android.content.Context;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;

import java.util.ArrayList;

import static android.hardware.Sensor.TYPE_ACCELEROMETER;
import static android.hardware.Sensor.TYPE_MAGNETIC_FIELD;
import static android.hardware.Sensor.TYPE_ROTATION_VECTOR;
import static android.hardware.Sensor.TYPE_STEP_COUNTER;
import static android.hardware.Sensor.TYPE_STEP_DETECTOR;


public class pdr implements SensorEventListener {

    SensorManager mSensorManager;
    Sensor mStepDetector;
    Sensor mStepCounter;
    Sensor mAccelerometer;
    Sensor mMagneticField;
    Sensor mRotationVector;


    static final String COUNTED_STEPS = "counted steps";
    static final String DETECTED_STEPS = "detected steps";
    static final String INITIAL_COUNTED_STEPS = "initial detected steps";

    static double stepLengthConstant = 70;
    static double stepLengthHeight = 82;
    double stepLength;

    Boolean lastAccelerometerSet = false;
    Boolean lastMagnetometerSet = false;
    Boolean isOrientationSet = false;

    Boolean stepCountingActive = true;
    int numberOfStepsCounted = 0;
    int numberOfStepsDetected = 0;

    int orientationInDegrees = 0;

    int initialStepCounterValue = 0;

    double distance = 0;
    double distanceHeight = 0;
    double distanceFrequency = 0;
    double detectedStepsSensorValue = 0;
    double countedStepsSensorValue = 0;

    String orientation;

    float [] lastAccelerometer = new float[3];
    float [] lastMagnetometer = new float[3];

    float [] mRotationMatrix = new float[9];
    float [] mOrientationAngles = new float[3];

    double meanOrientationAngles = 0;
    double sumSinAngles = 0;
    double sumCosAngles = 0;
    long counter = 0;

    float [] mRotationMatrixFromVector = new float[16];
    double rotAngle=196/180.0* Math.PI;

    //long[] stepTimeStamp;
    long timeCountingStarted = 0;
    long timeOfStep;
    double stepFrequency = 0;
    long totalTime = 0;

    double stepMeanFrequency = 0;
    double stepMeanTime = 0;
    double stepMeanAccDiff = 0;

    ArrayList<Long> stepTimeStamp = new ArrayList<Long>();

    double accelerationTotalMax = 0;
    double accelerationTotalMin = 0;
    double sumAccData = 0;

    double accelerationTotal = 0;

    static final float ALPHA = 0.25f;
    // test

    private PdrCall call;

    private Context context;

    public void registerCall(PdrCall call){
        this.call=call;
    }

    public pdr(SensorManager sensorManager){
        mSensorManager=sensorManager;
        mStepDetector=mSensorManager.getDefaultSensor(Sensor.TYPE_STEP_DETECTOR);
        mStepCounter=mSensorManager.getDefaultSensor(Sensor.TYPE_STEP_COUNTER);
        mAccelerometer=mSensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER);
        mMagneticField=mSensorManager.getDefaultSensor(Sensor.TYPE_MAGNETIC_FIELD);
        mRotationVector=mSensorManager.getDefaultSensor(Sensor.TYPE_ROTATION_VECTOR);

    }

    public void register(){
        mSensorManager.registerListener(this,mStepDetector,SensorManager.SENSOR_DELAY_FASTEST);
        mSensorManager.registerListener(this, mAccelerometer,
                SensorManager.SENSOR_DELAY_UI);
        mSensorManager.registerListener(this, mMagneticField,
                SensorManager.SENSOR_DELAY_UI);
        mSensorManager.registerListener(this, mRotationVector,
                SensorManager.SENSOR_DELAY_UI);
        mSensorManager.registerListener(this, mStepCounter,
                SensorManager.SENSOR_DELAY_FASTEST);

    }

    @Override
    public void onSensorChanged(SensorEvent event) {

        switch (event.sensor.getType()) {
            case TYPE_STEP_DETECTOR:
                if (stepCountingActive) {

                    numberOfStepsDetected++;
                    detectedStepsSensorValue++;

                    distance = distance + stepLengthConstant;
                    distanceHeight = distanceHeight + stepLengthHeight;

                    stepTimeStamp.add(event.timestamp);

                    if (numberOfStepsDetected == 1){
                        timeOfStep = event.timestamp/1000000L - timeCountingStarted;
                        totalTime = 0;
                        distanceFrequency = distanceFrequency + stepLengthHeight;
                    }
                    else {
                        timeOfStep = (event.timestamp - stepTimeStamp.get((stepTimeStamp.size() - 1) - 1))
                                /1000000L;

                        if (timeOfStep > 1000 ){
                            counter = 0;
                            meanOrientationAngles = 0;
                            sumCosAngles = 0;
                            sumSinAngles = 0;
                        }

                        totalTime = totalTime + timeOfStep;
                        stepFrequency = 1000D / timeOfStep;

                        stepLength = 44 * stepFrequency + 4.4;

                        distanceFrequency = distanceFrequency + stepLength;

                        stepMeanFrequency = (detectedStepsSensorValue - 1)* 1000D / totalTime;
                        stepMeanTime = totalTime / (detectedStepsSensorValue -  1);

                        sumAccData = sumAccData + Math.sqrt(accelerationTotalMax - accelerationTotalMin);
                        stepMeanAccDiff = sumAccData / (detectedStepsSensorValue - 1);

                    }


                    if (lastAccelerometerSet && lastMagnetometerSet) {
                        mSensorManager.getRotationMatrix(mRotationMatrix, null, lastAccelerometer, lastMagnetometer);
                        mSensorManager.getOrientation(mRotationMatrix, mOrientationAngles);

                        float azimuthInRadians = mOrientationAngles[0];
                        float pitchInRadians = mOrientationAngles[1];
                        float rollInRadians = mOrientationAngles[2];

                        int azimuthInDegress = (int) (((azimuthInRadians * 180 / (float) Math.PI) + 360) % 360);

                        isOrientationSet = true;

                        //orientation = Float.toString(azimuthInRadians);
                        orientation = "" + azimuthInDegress;

                    }

                    int myOrientation=0;
                    if (counter > 0){
                        myOrientation=((int)Math.toDegrees(Math.atan2(sumSinAngles, sumCosAngles)) +360) % 360;
                    }
                    else{
                        myOrientation=orientationInDegrees;
                    }
                    call.OnStepDetected((float) stepLengthConstant/100,myOrientation);


                    accelerationTotalMax = 0;
                    accelerationTotalMin = 0;
                    counter = 0;
                    meanOrientationAngles = 0;
                    sumCosAngles = 0;
                    sumSinAngles = 0;

                }


                break;

            case TYPE_STEP_COUNTER:
                if (stepCountingActive) {

                    if (initialStepCounterValue < 1) {
                        initialStepCounterValue = (int) event.values[0];
                    }

                    numberOfStepsCounted = (int) event.values[0] - initialStepCounterValue;

                    if (numberOfStepsCounted > numberOfStepsDetected) {

                        distance = distance + (numberOfStepsCounted - numberOfStepsDetected) * stepLengthConstant;
                        distanceHeight = distanceHeight + (numberOfStepsCounted - numberOfStepsDetected) * stepLengthHeight;

                        if (stepFrequency > 0){
                            distanceFrequency += (numberOfStepsCounted - numberOfStepsDetected) * (stepLength);
                        }else {
                            distanceFrequency += (numberOfStepsCounted - numberOfStepsDetected) * stepLengthHeight;
                        }
                        numberOfStepsDetected = numberOfStepsCounted;

                    }

                }
                else {
                    initialStepCounterValue = (int) event.values[0];
                }
                break;

            case TYPE_ACCELEROMETER:
                lastAccelerometerSet = true;

                System.arraycopy(event.values, 0, lastAccelerometer, 0, event.values.length);


                if (stepCountingActive && numberOfStepsDetected > 0){

                    long timeElapsedFromLastStep
                            = event.timestamp - stepTimeStamp.get(stepTimeStamp.size() - 1);


                    if (event.timestamp/1000000L - stepTimeStamp.get(stepTimeStamp.size() - 1)/1000000L
                            < 1500){

                        accelerationTotal =
                                Math.sqrt(Math.pow(event.values[0], 2) +
                                        Math.pow(event.values[1], 2) +
                                        Math.pow(event.values[2], 2));

                        if (accelerationTotalMin == 0){
                            accelerationTotalMin = accelerationTotal;
                        }
                        else if(accelerationTotal < accelerationTotalMin) {
                            accelerationTotalMin = accelerationTotal;

                        }
                        if (accelerationTotalMax == 0){
                            accelerationTotalMax = accelerationTotal;
                        }
                        else if (accelerationTotal > accelerationTotalMax){
                            accelerationTotalMax = accelerationTotal;
                        }
                    }
                    else{
                        accelerationTotalMax = 0;
                        accelerationTotalMin = 0;
                    }


                }

                break;

            case TYPE_MAGNETIC_FIELD:

                lastMagnetometerSet = true;

                System.arraycopy(event.values, 0, lastMagnetometer, 0, event.values.length);

                lastMagnetometer = lowPass(event.values.clone(), lastMagnetometer);

                if (lastAccelerometerSet && lastMagnetometerSet)
                {
                    mSensorManager.getRotationMatrix(mRotationMatrix, null, lastAccelerometer, lastMagnetometer);
                    mSensorManager.getOrientation(mRotationMatrix, mOrientationAngles);

                    float azimuthInRadians = mOrientationAngles[0];
                    float pitchInRadians = mOrientationAngles[1];
                    float rollInRadians = mOrientationAngles[2];

                    int azimuthInDegress = ((int)(azimuthInRadians * 180/(float)Math.PI) + 360) % 360;


                }
                break;

            case TYPE_ROTATION_VECTOR:
                SensorManager.getRotationMatrixFromVector(mRotationMatrixFromVector, event.values);
                SensorManager.getOrientation(mRotationMatrixFromVector, mOrientationAngles);


                orientationInDegrees = ((int)(mOrientationAngles[0] * 180/(float)Math.PI) + 360) % 360;


                if (detectedStepsSensorValue > 0){
                    sumCosAngles += Math.cos(mOrientationAngles[0]);
                    sumSinAngles += Math.sin(mOrientationAngles[0]);
                    meanOrientationAngles += mOrientationAngles[0];
                    counter ++;
                }
                break;

        }
    }


    protected float[] lowPass( float[] input, float[] output ) {
        if ( output == null ) return input;

        for ( int i=0; i<input.length; i++ ) {
            output[i] = output[i] + ALPHA * (input[i] - output[i]);
        }
        return output;
    }

    @Override
    public void onAccuracyChanged(Sensor sensor, int i) {

    }

    public int getStep(){return numberOfStepsDetected;}
    public double getStepLength(){return stepLength;}
    public String getOrientation(){return orientation;}
    public int getOrientationInDegrees(){return orientationInDegrees;}

}
