package com.fengmap.FMDemoBaseMap.widget;

import android.app.Activity;
import android.content.Context;
import android.content.res.TypedArray;
import android.util.AttributeSet;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.ImageView;
import android.widget.RelativeLayout;
import android.widget.TextView;

import com.fengmap.FMDemoBaseMap.R;


/**
 * @Email hezutao@fengmap.com
 * @Version 2.0.0
 * @Description 自定义标题栏视图组件
 */
public class NavigationBar extends RelativeLayout {

    Context mContext;
    TextView mTitleTxt;
    ImageView mLeftImage;

    public NavigationBar(Context context) {
        super(context);
        initView(context, null);
    }

    public NavigationBar(Context context, AttributeSet attrs) {
        super(context, attrs);
        initView(context, attrs);
    }

    public NavigationBar(Context context, AttributeSet attrs, int defStyle) {
        super(context, attrs, defStyle);
        initView(context, attrs);
    }


    /**
     * 初始化资源
     */
    private void initView(Context context, AttributeSet attrs) {
        this.mContext = context;
        LayoutInflater.from(context).inflate(R.layout.widget_navigationbar, this,
                true);
        mLeftImage = (ImageView) findViewById(R.id.img_left);
        mTitleTxt = (TextView) findViewById(R.id.txt_title);

        TypedArray typeArray = context.obtainStyledAttributes(attrs,
                R.styleable.NavigationBar);
        if (typeArray == null) {
            return;
        }
        // 对包含的ImageView和TextView赋值
        int count = typeArray.getIndexCount();
        for (int i = 0; i < count; i++) {
            int index = typeArray.getIndex(i);
            switch (index) {
                case R.styleable.NavigationBar_title:
                    mTitleTxt.setText(typeArray.getText(index));
                    break;
                default:
                    break;
            }
        }
        typeArray.recycle();

        mLeftImage.setOnClickListener(mDefaultClickListener);
        this.setBackgroundResource(R.color.blue);
    }

    private OnClickListener mDefaultClickListener = new OnClickListener(){

        @Override
        public void onClick(View v) {
            ((Activity)mContext).onBackPressed();
        }
    };

    /*---------------------------------以下方法为公开接口方法---------------------------------------*/
    /**
     * 设置左侧按钮点击事件
     *
     * @param listener 点击监听事件
     */
    public void setLeftButtonListener(OnClickListener listener) {
        mLeftImage.setOnClickListener(listener);
    }

    /**
     * 设置标题栏文本
     *
     * @param titleResId 文本资源ID
     */
    public void setTitle(int titleResId) {
        String title = mContext.getString(titleResId);
        this.setTitle(title);
    }

    /**
     * 设置标题栏文本
     *
     * @param title 文本字符串
     */
    public void setTitle(String title) {
        mTitleTxt.setText(title);
    }



}
