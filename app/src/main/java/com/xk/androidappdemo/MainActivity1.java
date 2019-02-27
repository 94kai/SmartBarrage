package com.xk.androidappdemo;

import android.graphics.Bitmap;
import android.graphics.drawable.BitmapDrawable;
import android.graphics.drawable.Drawable;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.widget.ImageView;

public class MainActivity1 extends AppCompatActivity {

    private MView1 mView;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setContentView(R.layout.activity_main1);
        mView = (MView1) findViewById(R.id.mview);
        ImageView imageView = (ImageView) findViewById(R.id.image);
        Drawable drawable = imageView.getDrawable();
        Bitmap bitmap = ((BitmapDrawable) drawable).getBitmap();
        mView.setBitmap(bitmap);
    }

    @Override
    protected void onResume() {
        super.onResume();
        mView.invalidate();
    }
}
