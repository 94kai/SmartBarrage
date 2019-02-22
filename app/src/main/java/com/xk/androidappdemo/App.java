package com.xk.androidappdemo;

import android.app.Application;

import com.facebook.soloader.SoLoader;

/**
 * @author xuekai1
 * @date 2019/2/18
 */
public class App extends Application {
    @Override
    public void onCreate() {
        super.onCreate();
        SoLoader.init(this, false);
    }
}
