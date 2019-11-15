package com.fengmap.FMDemoBaseMap.help;

import android.content.Context;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;
import android.util.Log;

import static android.content.ContentValues.TAG;

/**
 * Created by lenovo on 2017/6/25.
 */

public class Db extends SQLiteOpenHelper {

    public static final int VERSION = 1;

    //必须要有构造函数
    public Db(Context context, String name, SQLiteDatabase.CursorFactory factory,
              int version) {
        super(context, name, factory, version);
    }


    // 当第一次创建数据库的时候，调用该方法
    public void onCreate(SQLiteDatabase db) {
//输出创建数据库的日志信息
        //String sql="create table first(location text not null,one text)";
        // "1 text,2 text,3 text,4 text,5 " +
        // "text,6 text,7 text,8 text,9 text,10 text,11 text,12 text,13 text)";
        //Log.i(TAG, "create Database------------->");
//execSQL函数用于执行SQL
        //db.execSQL(sql);
    }

    //当更新数据库的时候执行该方法
    public void onUpgrade(SQLiteDatabase db, int oldVersion, int newVersion) {
//输出更新数据库的日志信息
        Log.i(TAG, "update Database------------->");
    }
}


