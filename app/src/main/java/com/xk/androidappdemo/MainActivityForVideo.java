package com.xk.androidappdemo;

import android.graphics.Bitmap;
import android.media.MediaMetadataRetriever;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.support.annotation.RequiresApi;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.ImageView;
import android.widget.VideoView;

import java.io.FileOutputStream;
import java.io.IOException;
import java.util.List;

import static android.media.MediaMetadataRetriever.OPTION_CLOSEST;

public class MainActivityForVideo extends AppCompatActivity {

    private static final String TAG = "MainActivityForVideo";
    private MViewForVideo mView;

    //res/mipmap目录和assets目录放相同名字的图片和json数据
    String imageName = "video2";
    private VideoView videoView;
    public static List<Bitmap> framesAtIndex;
    private ImageView imageView;
    private String uri;
    private Thread screenShootThread;

    @RequiresApi(api = Build.VERSION_CODES.P)
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main1_video);
        findView();
        uri = "android.resource://" + getPackageName() + "/" + R.raw.video;
//        videoView.setMediaController(null);
        videoView.setVideoURI(Uri.parse(uri));


        screenShootThread = new Thread(new Runnable() {
            @Override
            public void run() {
                MediaMetadataRetriever metadataRetriever = new MediaMetadataRetriever();
                metadataRetriever.setDataSource(MainActivityForVideo.this, Uri.parse(uri));
                while (videoView.isPlaying()) {
                    final Bitmap bitmap = metadataRetriever.
                            getFrameAtTime((videoView.getCurrentPosition()+1000) * 1000, MediaMetadataRetriever.OPTION_CLOSEST);
                    FileOutputStream fileOutputStream = null;
                    try {
                        runOnUiThread(new Runnable() {
                            @Override
                            public void run() {
                                int currentTime = (videoView.getCurrentPosition()) ;
                                double v = currentTime / (videoView.getDuration() * 0.6);

//                                imageView.setImageBitmap(bitmap);
                                mView.setBitmap(bitmap, imageName,v);
                            }
                        });
                    } catch (Exception e) {
                        e.printStackTrace();
                    } finally {
                        if (fileOutputStream != null) {
                            try {
                                fileOutputStream.close();
                            } catch (IOException e) {
                                e.printStackTrace();
                            }
                        }
                    }
//                    bitmap.recycle();
                }
            }
        });

//        startGetFrames(uri);

//
    }

    private void startGetFrames(final String uri) {
        new Thread(new Runnable() {
            @RequiresApi(api = Build.VERSION_CODES.P)
            @Override
            public void run() {

                final MediaMetadataRetriever mmr = new MediaMetadataRetriever();
                mmr.setDataSource(MainActivityForVideo.this, Uri.parse(uri));
                //380帧
//                final Bitmap frameAtIndex = mmr.getFrameAtIndex(379);
                final Bitmap frameAtTime = mmr.getFrameAtTime(10 * 1000 * 15, OPTION_CLOSEST);
                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        int cloun = 19;
                        mView.setBitmap(frameAtTime, imageName, 1);
                        imageView.setImageBitmap(frameAtTime);
                    }
                });
            }
        }).start();
    }

    private void findView() {
        mView = (MViewForVideo) findViewById(R.id.mview);
        imageView = (ImageView) findViewById(R.id.imageview);
        videoView = (VideoView) findViewById(R.id.videoView);
    }

    @Override
    protected void onResume() {
        super.onResume();
//        startGetFrames(uri);

//        mView.invalidate();
//        videoView.seekTo(0);
//        videoView.start();
    }

    int getIdByName(String name) {
        int mipmap = getResources().getIdentifier(name, "mipmap", getPackageName());
        return mipmap;
    }

    public void click(View view) {
        videoView.start();
        videoView.requestFocus();
        screenShootThread.start();

//        mView.setFrame(-1);
//        videoView.seekTo(0);
//        videoView.start();

    }
}
