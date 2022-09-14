package a2dp.Vol;

import android.app.Activity;
import android.app.ProgressDialog;
import android.content.Context;
import android.content.Intent;
import android.content.pm.ApplicationInfo;
import android.content.pm.PackageManager;
import android.content.res.Configuration;
import android.graphics.drawable.Drawable;
import android.os.Bundle;
import android.os.Handler;
import android.view.KeyEvent;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.ListAdapter;
import android.widget.ListView;
import android.widget.TextView;
import java.text.Collator;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;

public class AppChooser extends Activity {
    public static final String EXTRA_PACKAGE_NAME = "package_name";
    private List<AppInfoCache> mAppList;
    private Button mBtnClear;
    private Button mBtnSearch;
    public View.OnClickListener mClearBtnListenerListner = new View.OnClickListener() {
        /* class a2dp.Vol.AppChooser.AnonymousClass2 */

        public void onClick(View v) {
            AppChooser.this.mEtFilter.setText("");
            AppChooser.this.doListFilter();
        }
    };
    private EditText mEtFilter;
    private String mFilterText;
    private Runnable mFinishLoadAndSortTask = new Runnable() {
        /* class a2dp.Vol.AppChooser.AnonymousClass7 */

        public void run() {
            AppChooser.this.initAssignListenersAndAdapter();
            AppChooser.this.mLoadingDialog.dismiss();
        }
    };
    private List<AppInfoCache> mFullAppList;
    private final Handler mHandler = new Handler();
    private PackageListAdapter mListAdapter;
    public AdapterView.OnItemClickListener mListItemClickAdapter = new AdapterView.OnItemClickListener() {
        /* class a2dp.Vol.AppChooser.AnonymousClass5 */

        @Override // android.widget.AdapterView.OnItemClickListener
        public void onItemClick(AdapterView<?> adapterView, View view, int position, long id) {
            Intent i = new Intent();
            i.putExtra(AppChooser.EXTRA_PACKAGE_NAME, ((AppInfoCache) AppChooser.this.mAppList.get(position)).getPackageName());
            AppChooser.this.setResult(-1, i);
            AppChooser.this.finish();
        }
    };
    private ListView mListView;
    private Runnable mLoadAppLoadAndSortAppList = new Runnable() {
        /* class a2dp.Vol.AppChooser.AnonymousClass6 */

        public void run() {
            AppChooser.this.mAppList = new ArrayList();
            for (ApplicationInfo appInfo : AppChooser.this.pm.getInstalledApplications(0)) {
                AppChooser.this.mAppList.add(new AppInfoCache(appInfo.loadLabel(AppChooser.this.pm).toString(), appInfo.packageName, appInfo.className));
            }
            Collections.sort(AppChooser.this.mAppList, new AlphaComparator());
            AppChooser.this.mFullAppList = new ArrayList();
            int i = 0;
            for (AppInfoCache appInfo2 : AppChooser.this.mAppList) {
                appInfo2.setPosition(i);
                AppChooser.this.mFullAppList.add(appInfo2);
                i++;
            }
            AppChooser.this.mListAdapter = new PackageListAdapter(AppChooser.this.getBaseContext());
            AppChooser.this.mHandler.post(AppChooser.this.mFinishLoadAndSortTask);
        }
    };
    private ProgressDialog mLoadingDialog;
    public TextView.OnEditorActionListener mSearchActionListener = new TextView.OnEditorActionListener() {
        /* class a2dp.Vol.AppChooser.AnonymousClass3 */

        public boolean onEditorAction(TextView v, int actionId, KeyEvent event) {
            AppChooser.this.doListFilter();
            return false;
        }
    };
    public View.OnKeyListener mSearchBoxKeyListener = new View.OnKeyListener() {
        /* class a2dp.Vol.AppChooser.AnonymousClass4 */

        public boolean onKey(View arg0, int keycode, KeyEvent arg2) {
            if (keycode != 66) {
                return false;
            }
            AppChooser.this.doListFilter();
            return true;
        }
    };
    public View.OnClickListener mSearchBtnListenerListner = new View.OnClickListener() {
        /* class a2dp.Vol.AppChooser.AnonymousClass1 */

        public void onClick(View v) {
            AppChooser.this.doListFilter();
        }
    };
    private PackageManager pm;

    public void doListFilter() {
        this.mFilterText = this.mEtFilter.getText().toString().toLowerCase();
        this.mAppList.clear();
        if (this.mFilterText.contentEquals("")) {
            for (AppInfoCache appInfo : this.mFullAppList) {
                this.mAppList.add(appInfo);
            }
        } else {
            for (AppInfoCache appInfo2 : this.mFullAppList) {
                if (appInfo2.getAppName().toLowerCase().contains(this.mFilterText)) {
                    this.mAppList.add(appInfo2);
                }
            }
        }
        this.mListAdapter.notifyDataSetChanged();
    }

    /* access modifiers changed from: protected */
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.app_list);
        setTitle("Select an app...");
        initAttachViewsToVars();
        this.pm = getPackageManager();
        this.mLoadingDialog = new ProgressDialog(this);
        this.mLoadingDialog.setIndeterminate(true);
        this.mLoadingDialog.setMessage("Loading App List...");
        this.mLoadingDialog.setCancelable(false);
        this.mLoadingDialog.show();
        new Thread(this.mLoadAppLoadAndSortAppList).start();
    }

    public void onConfigurationChanged(Configuration newConfig) {
        setContentView(R.layout.app_list);
        initAttachViewsToVars();
        initAssignListenersAndAdapter();
        super.onConfigurationChanged(newConfig);
    }

    private void initAttachViewsToVars() {
        this.mListView = (ListView) findViewById(R.id.m_lv_packages);
        this.mEtFilter = (EditText) findViewById(R.id.m_et_search);
        this.mBtnSearch = (Button) findViewById(R.id.m_btn_search);
        this.mBtnClear = (Button) findViewById(R.id.m_btn_clear);
    }

    /* access modifiers changed from: private */
    /* access modifiers changed from: public */
    private void initAssignListenersAndAdapter() {
        this.mEtFilter.setText(this.mFilterText);
        this.mEtFilter.setOnEditorActionListener(this.mSearchActionListener);
        this.mEtFilter.setOnKeyListener(this.mSearchBoxKeyListener);
        this.mListView.setAdapter((ListAdapter) this.mListAdapter);
        this.mListView.setOnItemClickListener(this.mListItemClickAdapter);
        this.mBtnSearch.setOnClickListener(this.mSearchBtnListenerListner);
        this.mBtnClear.setOnClickListener(this.mClearBtnListenerListner);
    }

    public class PackageListAdapter extends ArrayAdapter<AppInfoCache> {
        Context c;

        public PackageListAdapter(Context context) {
            super(context, (int) R.layout.app_list_item, AppChooser.this.mAppList);
            this.c = context;
        }

        public View getView(int position, View convertView, ViewGroup parent) {
            View v = LayoutInflater.from(this.c).inflate(R.layout.app_list_item, parent, false);
            AppInfoCache ai = (AppInfoCache) getItem(position);
            ((ImageView) v.findViewById(R.id.pi_iv_icon)).setImageDrawable(ai.getIcon());
            ((TextView) v.findViewById(R.id.pi_tv_name)).setText(ai.getAppName());
            return v;
        }
    }

    class AlphaComparator implements Comparator<AppInfoCache> {
        private final Collator sCollator = Collator.getInstance();

        AlphaComparator() {
        }

        public final int compare(AppInfoCache a, AppInfoCache b) {
            return this.sCollator.compare(a.getAppName(), b.getAppName());
        }
    }

    /* access modifiers changed from: package-private */
    public class AppInfoCache {
        private String app_name;
        private String class_name;
        private String package_name;
        private int position = -1;

        public AppInfoCache(String aName, String pName, String cName) {
            this.app_name = aName;
            this.package_name = pName;
            this.class_name = cName;
        }

        public Drawable getIcon() {
            try {
                return AppChooser.this.pm.getApplicationIcon(this.package_name);
            } catch (PackageManager.NameNotFoundException e) {
                return null;
            }
        }

        public int getPosition() {
            return this.position;
        }

        public void setPosition(int pos) {
            this.position = pos;
        }

        public String getAppName() {
            return this.app_name;
        }

        public String getPackageName() {
            return this.package_name;
        }

        public String getClassName() {
            return this.class_name;
        }

        public String toString() {
            return this.app_name;
        }
    }

    /* access modifiers changed from: protected */
    public void onDestroy() {
        super.onDestroy();
    }

    /* access modifiers changed from: protected */
    public void onPause() {
        super.onPause();
    }
}
