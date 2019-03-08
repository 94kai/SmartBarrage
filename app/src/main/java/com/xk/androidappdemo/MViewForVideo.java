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
import android.widget.VideoView;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.InputStream;
import java.io.InputStreamReader;


/**
 * @author xuekai1
 * @date 2019/2/22
 */
public class MViewForVideo extends View {

    private float[] shape = new float[2];
    private VideoView videoView;
    private Bitmap bitmap;
    private Paint paint;
    private BitmapDrawable bitmapDrawable;
    private int measuredWidth;
    private int measuredHeight;
    private int width;
    private int height;
    private Shader shader;
    private String dataFileName;
    private JSONArray framesData;
    private double v;

    public MViewForVideo(Context context) {
        super(context);
    }

    public MViewForVideo(Context context, @Nullable AttributeSet attrs) {
        super(context, attrs);
        paint = new Paint();
//
        InputStream data = null;
        try {
            data = getContext().getAssets().open("video");

            BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(data));
            String line = null;
            StringBuffer sb = new StringBuffer();
            while ((line = bufferedReader.readLine()) != null) {
                sb.append(line);
            }
            String json = sb.toString();

            JSONObject jsonObject = new JSONObject(json);

            //总时长的0.6
            framesData = jsonObject.getJSONArray("framesData");


        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public MViewForVideo(Context context, @Nullable AttributeSet attrs, int defStyleAttr) {
        super(context, attrs, defStyleAttr);
    }

    long time = 0;

    @Override
    protected void onDraw(Canvas canvas) {
        super.onDraw(canvas);
        if (bitmap == null) {
            return;
        }
        width = bitmap.getWidth();
        height = bitmap.getHeight();
        measuredWidth = getMeasuredWidth();
        measuredHeight = getMeasuredHeight();

        paint.reset();
        paint.setStyle(Paint.Style.FILL);
//        paint.setColor(Color.RED);
//        paint.setStrokeWidth(5);
//        bitmap = MainActivity1.getGoodBitmap(getContext(), R.drawable.zhuchiren1, measuredWidth, measuredWidth);

        shader = new BitmapShader(bitmap, Shader.TileMode.CLAMP, Shader.TileMode.CLAMP);


        float scaleX = width * 1.0f / measuredWidth;
        float scaleY = height * 1.0f / measuredHeight;
        Matrix shaderMatrix = new Matrix();
        shaderMatrix.setScale(1f / scaleX, 1f / scaleY);
        shader.setLocalMatrix(shaderMatrix);
        paint.setShader(shader);
        drawContoursByData(canvas);
    }

    int currentFrame = -1;

    /**
     * 绘制所有轮廓
     *
     * @param canvas
     */
    private void drawContoursByData(Canvas canvas) {
        try {

            JSONObject jsonObject = (JSONObject) framesData.get((int) (framesData.length() * v));
//            InputStream data = getContext().getAssets().open(dataFileName);
//            BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(data));
//            String line = null;
//            StringBuffer sb = new StringBuffer();
//            while ((line = bufferedReader.readLine()) != null) {
//                sb.append(line);
//            }
//            String json = sb.toString();
//
//            JSONObject jsonObject = new JSONObject(json);
            JSONArray shape = jsonObject.getJSONArray("shape");
            this.shape[0] = (int) shape.get(0);
            this.shape[1] = (int) shape.get(1);
            JSONArray contours = jsonObject.getJSONArray("contours");
            for (int i = 0; i < contours.length(); i++) {
                drawContour(contours.getJSONArray(i), canvas);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    /**
     * 绘制一个轮廓遮罩
     *
     * @param points
     * @param canvas
     */
    private void drawContour(JSONArray points, Canvas canvas) {
        try {
            Path path = new Path();
            for (int i = 0; i < points.length(); i++) {
                JSONArray jsonArray = points.getJSONArray(i);

                if (i == 0) {
                    path.moveTo((float) (measuredWidth / shape[1] * (double) jsonArray.get(0)), (float) (measuredHeight / shape[0] * (double) jsonArray.get(1)));
                } else {
                    path.lineTo((float) (measuredWidth / shape[1] * (double) jsonArray.get(0)), (float) (measuredHeight / shape[0] * (double) jsonArray.get(1)));
                }
            }
            path.close();
            paint.setShader(shader);
            canvas.drawPath(path, paint);
        } catch (JSONException e) {
            e.printStackTrace();
        }
    }

    public void setBitmap(Bitmap bitmap, String dataFileName, double v) {
        this.bitmap = bitmap;
        this.dataFileName = dataFileName;
        this.v = v;
        invalidate();
    }

    public void setFrame(int i) {
        currentFrame = i;
        invalidate();
    }
}

