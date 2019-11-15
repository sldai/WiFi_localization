package com.fengmap.FMDemoBaseMap.utils;

/**
 * @Email hezutao@fengmap.com
 * @Version 2.0.0
 * @Description 任务执行过滤
 */
public class TaskFilter {
    private static final long INTERVAL = 500L; // 任务执行时间间隔
    private static long mLastClickTime = 0L; // 上一次执行的时间

    /**
     * 任务过滤
     *
     * @return
     */
    public static boolean filter() {
        long time = System.currentTimeMillis();
        long diffTime = time - mLastClickTime;
        if (diffTime > INTERVAL) {
            mLastClickTime = time;
            return true;
        }
        return false;
    }
}
