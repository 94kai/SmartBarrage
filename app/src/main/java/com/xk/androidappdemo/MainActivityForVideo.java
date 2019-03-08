//package com.xk.androidappdemo;
//
//import android.graphics.Bitmap;
//import android.media.MediaMetadataRetriever;
//import android.media.MediaPlayer;
//import android.net.Uri;
//import android.os.Build;
//import android.os.Bundle;
//import android.support.annotation.RequiresApi;
//import android.support.v7.app.AppCompatActivity;
//import android.view.View;
//import android.widget.VideoView;
//
//import java.util.List;
//
//public class MainActivityForVideo extends AppCompatActivity {
//
////    private MViewForVideo mView;
//
//    //res/mipmap目录和assets目录放相同名字的图片和json数据
//    String imageName = "video";
////    private VideoView videoView;
//    public static List<Bitmap> framesAtIndex;
//
//    @RequiresApi(api = Build.VERSION_CODES.P)
//    @Override
//    protected void onCreate(Bundle savedInstanceState) {
//        super.onCreate(savedInstanceState);
//
//        setContentView(R.layout.activity_main1_video);
////        mView = (MViewForVideo) findViewById(R.id.mview);
////        ImageView imageView = (ImageView) findViewById(R.id.image);
////        videoView = (VideoView) findViewById(R.id.videoView);
//
//        videoView.setOnPreparedListener(new MediaPlayer.OnPreparedListener()
//        {
//            @Override
//            public void onPrepared(MediaPlayer mp)
//            {
//                mp.setVideoScalingMode(MediaPlayer.VIDEO_SCALING_MODE_SCALE_TO_FIT);
//                //TODO
//            }
//        });
//
//            String uri = "android.resource://" + getPackageName() + "/" + R.raw.video;
//            videoView.setVideoURI(Uri.parse(uri));
//
//
//        MediaMetadataRetriever mmr = new MediaMetadataRetriever();
//
//        mmr.setDataSource(this, Uri.parse(uri));
//        framesAtIndex = mmr.getFramesAtIndex(0,200);
//
//        System.out.println("====="+framesAtIndex.size());
////        videoView.setOnPreparedListener(new MediaPlayer.OnPreparedListener() {
////            @Override
////            public void onPrepared(MediaPlayer mp) {
////                totalTime = videoView.getDuration();//毫秒
////            }
////        });
////        sbVideo.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
////            @Override
////            public void onProgressChanged(SeekBar seekBar, int progress, boolean fromUser) {
////                if(isTouch){
////                    currentTime = (int)(((float) progress / 100) * totalTime);
////                    videoView.seekTo(currentTime);
////                }
////            }
////
////            @Override
////            public void onStartTrackingTouch(SeekBar seekBar) {
////                isTouch = true;
////            }
////
////            @Override
////            public void onStopTrackingTouch(SeekBar seekBar) {
////                isTouch = false;
////                //获取第一帧图像的bitmap对象 单位是微秒
////                Bitmap bitmap = mmr.getFrameAtTime((long) (currentTime * 1000), OPTION_PREVIOUS_SYNC);
////                ivHead.setImageBitmap(bitmap);
////            }
////        });
////        videoView.setVideoPath(mp4Path);
//
////        imageView.setImageResource(getIdByName(imageName));
////        Drawable drawable = imageView.getDrawable();
////        Bitmap bitmap = ((BitmapDrawable) drawable).getBitmap();
////        mView.setBitmap(videoView, imageName);
//    }
//
////    @Override
////    protected void onCreate(Bundle savedInstanceState) {
////        super.onCreate(savedInstanceState);
////
////        setContentView(R.layout.activity_main1);
////        mView = (MView1) findViewById(R.id.mview);
////        ImageView imageView = (ImageView) findViewById(R.id.image);
////        imageView.setImageResource(getIdByName(imageName));
////        Drawable drawable = imageView.getDrawable();
////        Bitmap bitmap = ((BitmapDrawable) drawable).getBitmap();
////        mView.setBitmap(bitmap, imageName);
////    }
//
//    @Override
//    protected void onResume() {
//        super.onResume();
////        mView.invalidate();
//        videoView.seekTo(0);
//        videoView.start();
//    }
//
//    int getIdByName(String name) {
//        int mipmap = getResources().getIdentifier(name, "mipmap", getPackageName());
//        return mipmap;
//    }
//
//    public void click(View view) {
////        mView.setFrame(-1);
//        videoView.seekTo(0);
//        videoView.start();
//
//    }
//}
