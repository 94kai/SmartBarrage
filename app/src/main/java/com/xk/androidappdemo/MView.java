package com.xk.androidappdemo;

import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.BitmapShader;
import android.graphics.Canvas;
import android.graphics.Matrix;
import android.graphics.Paint;
import android.graphics.Path;
import android.graphics.Shader;
import android.graphics.drawable.BitmapDrawable;
import android.support.annotation.Nullable;
import android.util.AttributeSet;
import android.view.View;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;

/**
 * @author xuekai1
 * @date 2019/2/22
 */
public class MView extends View {

    private float[] shape;
    private Bitmap bitmap;
    private Paint paint;
    private BitmapDrawable bitmapDrawable;

    public MView(Context context) {
        super(context);
    }

    public MView(Context context, @Nullable AttributeSet attrs) {
        super(context, attrs);
        paint = new Paint();
    }

    public MView(Context context, @Nullable AttributeSet attrs, int defStyleAttr) {
        super(context, attrs, defStyleAttr);
    }

    @Override
    protected void onDraw(Canvas canvas) {
        super.onDraw(canvas);
        paint.reset();
        paint.setStyle(Paint.Style.FILL);
//        paint.setColor(Color.RED);
//        paint.setStrokeWidth(5);
        Shader shader = new BitmapShader(bitmap, Shader.TileMode.CLAMP, Shader.TileMode.CLAMP);
        int width = bitmap.getWidth();
        int height = bitmap.getHeight();
        int measuredWidth = getMeasuredWidth();
        int measuredHeight = getMeasuredHeight();

        Matrix shaderMatrix = new Matrix();

        float scaleX = width * 1.0f / measuredWidth;
        float scaleY = height * 1.0f / measuredHeight;
        shaderMatrix.setScale(1f / scaleX, 1f / scaleY);
        shader.setLocalMatrix(shaderMatrix);
        paint.setShader(shader);
        Path path = new Path();


        String[] split = handleData();

        for (int i = 0; i < split.length; i++) {
            String s = split[i];
            String[] split1 = s.split(",");
            System.out.println("   :" + measuredWidth / 181f * Float.parseFloat(split1[1]) + " " + measuredHeight / 139f * Float.parseFloat(split1[0]));
            if (i == 0) {
                path.moveTo(measuredWidth / shape[1] * Float.parseFloat(split1[1]), measuredHeight / shape[0] * Float.parseFloat(split1[0]));
            } else {
                path.lineTo(measuredWidth / shape[1] * Float.parseFloat(split1[1]), measuredHeight / shape[0] * Float.parseFloat(split1[0]));
            }
        }
        path.close();
        canvas.drawPath(path, paint);
    }

    private String[] handleData() {
        try {
            InputStream data = getContext().getAssets().open("data");
            BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(data));
            String line = null;
            StringBuffer sb = new StringBuffer();
            if ((line = bufferedReader.readLine()) != null) {
                sb.append(line);
            }
            String str = sb.toString();


            String[] split1 = str.split("##");
            String s1 = split1[0];
            String[] split2 = s1.replace("(", "").replace(")", "").split(",");
            str = split1[1];
            shape = new float[]{Float.parseFloat(split2[0]), Float.parseFloat(split2[1])};
            str = str.replace("'", "");
            str = str.substring(1, str.length() - 1);
            String[] split = str.split("\\), \\(");
            for (int i = 0; i < split.length; i++) {
                String s = split[i];
                s = s.replace("(", "");
                s = s.replace(")", "");
                split[i] = s;
            }
            return split;
        } catch (IOException e) {
            e.printStackTrace();
        }
        return null;
    }

    public void setBitmap(Bitmap bitmap) {
        this.bitmap = bitmap;
        invalidate();
    }
}

