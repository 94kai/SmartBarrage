package com.xk.androidappdemo;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;

/**
 * @author xuekai1
 * @date 2019/2/18
 */
public class MBroadcastReceiver extends BroadcastReceiver {
  @Override
  public void onReceive(Context context, Intent intent) {
    System.out.println("  abctest:"+context);
    Intent intent1 = new Intent(context, MainActivity.class);
    intent1.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
    context.startActivity(intent1);
  }
}
