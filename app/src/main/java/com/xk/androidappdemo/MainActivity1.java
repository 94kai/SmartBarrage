package com.xk.androidappdemo;

import android.graphics.Bitmap;
import android.graphics.drawable.BitmapDrawable;
import android.graphics.drawable.Drawable;
import android.os.Bundle;
import android.support.v7.app.AppCompatActivity;
import android.widget.ImageView;

public class MainActivity1 extends AppCompatActivity {

    private MView1 mView;

    //res/mipmap目录和assets目录放相同名字的图片和json数据
    String imageName = "bangongshi1";
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        setContentView(R.layout.activity_main1);
        mView = (MView1) findViewById(R.id.mview);
        ImageView imageView = (ImageView) findViewById(R.id.image);
        imageView.setImageResource(getIdByName(imageName));
        Drawable drawable = imageView.getDrawable();
        Bitmap bitmap = ((BitmapDrawable) drawable).getBitmap();
        mView.setBitmap(bitmap, imageName);
    }

    @Override
    protected void onResume() {
        super.onResume();
        mView.invalidate();
    }

    int getIdByName(String name) {
        int mipmap = getResources().getIdentifier(name, "mipmap", getPackageName());
        return mipmap;
    }
}
