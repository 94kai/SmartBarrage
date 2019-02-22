package com.xk.androidappdemo;

import android.content.ContentProvider;
import android.content.ContentValues;
import android.content.Intent;
import android.database.Cursor;
import android.net.Uri;
import android.support.annotation.NonNull;
import android.support.annotation.Nullable;
import android.util.Log;

/**
 * @author xuekai1
 * @date 2019/2/18
 */
public class MContentProvider extends ContentProvider {
  @Override
  public boolean onCreate() {
    Log.i("MContentProvider", "onCreate-->" + getContext()
    );
    Intent intent1 = new Intent(getContext(), MainActivity.class);
    intent1.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
    getContext().startActivity(intent1);
    return false;
  }

  @Nullable
  @Override
  public Cursor query(@NonNull Uri uri, @Nullable String[] projection, @Nullable String selection, @Nullable String[] selectionArgs, @Nullable String sortOrder) {
    Log.i("MContentProvider", "query-->");
    return null;
  }

  @Nullable
  @Override
  public String getType(@NonNull Uri uri) {
    Log.i("MContentProvider", "getType-->");
    return null;
  }

  @Nullable
  @Override
  public Uri insert(@NonNull Uri uri, @Nullable ContentValues values) {
    return null;
  }

  @Override
  public int delete(@NonNull Uri uri, @Nullable String selection, @Nullable String[] selectionArgs) {
    return 0;
  }

  @Override
  public int update(@NonNull Uri uri, @Nullable ContentValues values, @Nullable String selection, @Nullable String[] selectionArgs) {
    return 0;
  }
}
