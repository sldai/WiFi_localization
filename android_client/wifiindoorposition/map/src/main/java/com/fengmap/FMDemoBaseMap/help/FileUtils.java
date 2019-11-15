package com.fengmap.FMDemoBaseMap.help;

import android.os.Environment;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;

public class FileUtils {
    private String SDPATH;
    FileOutputStream output ;
    File outfile ;
    public String getSDPATH(){
        return SDPATH;
    }
    //构造函数，得到SD卡的目录，这行函数得到的目录名其实是叫"/SDCARD"
    public FileUtils() {
        SDPATH = Environment.getExternalStorageDirectory() +"/";
    }
    //在SD卡上创建文件
    public File createSDFile(String fileName) throws IOException {
        File file = new File(SDPATH + fileName);
        file.createNewFile();
        return file;
    }
    //在SD卡上创建目录
    public File createSDDir(String dirName){
        File dir = new File(SDPATH + dirName);
        dir.mkdir();
        return dir;
    }
    //判断SD卡上的文件夹是否存在
    public boolean isFileExist(String fileName){
        File file = new File(SDPATH + fileName);
        return file.exists();
    }

    public void open(String path, String fileName){

        try{
            if(!isFileExist(path))createSDDir(path);
            if(!isFileExist(path + "/"+fileName))createSDFile(path + "/"+fileName);

            outfile =new File(SDPATH+path + "/"+fileName);
            output = new FileOutputStream(outfile,true);
        }
        catch(Exception e){
            e.printStackTrace();
        }

    }
    //将一个InputStream里面的数据写入到SD卡中
    //将input写到path这个目录中的fileName文件上
    public void write2SDFromInput(String input){
        try{

            output.write(input.getBytes());
            output.flush();

        }
        catch(Exception e){
            e.printStackTrace();
        }

        return ;
    }

    public boolean destroy(){
        try{
            output.close();
        }
        catch(Exception e){
            e.printStackTrace();
        }
        return true;
    }
}

