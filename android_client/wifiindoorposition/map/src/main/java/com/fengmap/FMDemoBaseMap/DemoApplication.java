package com.fengmap.FMDemoBaseMap;

import android.app.Application;

import com.fengmap.android.FMMapSDK;

/**
 * @Email hezutao@fengmap.com
 * @Version 2.0.0
 * @Description 应用层初始化
 */
public class DemoApplication extends Application {

    @Override
    public void onCreate() {
        super.onCreate();
        // 在使用 SDK 各组间之前初始化 context 信息，传入 Application
        FMMapSDK.init(this);
    }

}