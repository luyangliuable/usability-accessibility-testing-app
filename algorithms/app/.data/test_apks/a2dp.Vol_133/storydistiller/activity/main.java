package a2dp.Vol;

import android.app.Activity;
import android.app.AlertDialog;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.IBluetooth;
import android.content.BroadcastReceiver;
import android.content.ComponentName;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.IntentFilter;
import android.content.SharedPreferences;
import android.content.pm.PackageManager;
import android.content.res.Resources;
import android.media.AudioManager;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.os.CountDownTimer;
import android.os.Environment;
import android.os.IBinder;
import android.os.RemoteException;
import android.preference.PreferenceManager;
import android.support.v4.app.NotificationManagerCompat;
import android.support.v4.view.GravityCompat;
import android.support.v4.view.MotionEventCompat;
import android.support.v4.widget.ExploreByTouchHelper;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.ListAdapter;
import android.widget.ListView;
import android.widget.Toast;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.lang.reflect.Method;
import java.util.Set;
import java.util.Vector;

public class main extends Activity {
    static final int CHECK_TTS = 3;
    static final int EDITED_DATA = 4;
    static final int ENABLE_BLUETOOTH = 1;
    private static final String LOG_TAG = "A2DP_Volume";
    public static final String PREFS_NAME = "btVol";
    static final int RELOAD = 2;
    static AudioManager am = null;
    private static int resourceID = 17367043;
    static Button serv;
    boolean TTSignore = false;
    private String a2dpDir = "";
    String activebt = null;
    private MyApplication application;
    boolean carMode = false;
    int connects;
    boolean enableTTS = false;
    boolean headsetPlug = false;
    boolean homeDock = false;
    ArrayAdapter<String> ladapt;
    String[] lstring = null;
    ListView lvl = null;
    private final BroadcastReceiver mReceiver5 = new BroadcastReceiver() {
        /* class a2dp.Vol.main.AnonymousClass11 */

        public void onReceive(Context context2, Intent intent2) {
            main.this.getConnects();
            main.this.refreshList(main.this.loadFromDB());
        }
    };
    private final BroadcastReceiver mReceiver6 = new BroadcastReceiver() {
        /* class a2dp.Vol.main.AnonymousClass12 */

        public void onReceive(Context context2, Intent intent2) {
            boolean carModeOld = main.this.carMode;
            boolean homeDockOld = main.this.homeDock;
            boolean headsetPlugOld = main.this.headsetPlug;
            boolean powerOld = main.this.power;
            try {
                main.this.carMode = main.this.preferences.getBoolean("car_mode", false);
                main.this.homeDock = main.this.preferences.getBoolean("home_dock", false);
                main.this.headsetPlug = main.this.preferences.getBoolean("headset", false);
                main.this.power = main.this.preferences.getBoolean("power", false);
                main.this.enableTTS = main.this.preferences.getBoolean("enableTTS", false);
                if (main.this.preferences.getBoolean("useLocalStorage", false)) {
                    main.this.a2dpDir = main.this.getFilesDir().toString();
                } else {
                    main.this.a2dpDir = Environment.getExternalStorageDirectory() + "/A2DPVol";
                }
                File exportDir = new File(main.this.a2dpDir);
                if (!exportDir.exists()) {
                    exportDir.mkdirs();
                }
            } catch (Exception e2) {
                e2.printStackTrace();
                Log.e(main.LOG_TAG, "error" + e2.getMessage());
            }
            if ((!carModeOld && main.this.carMode) || ((!homeDockOld && main.this.homeDock) || ((!headsetPlugOld && main.this.headsetPlug) || (!powerOld && main.this.power)))) {
                main.this.getBtDevices(0);
            }
            if (main.this.enableTTS) {
                try {
                    Intent checkIntent = new Intent();
                    checkIntent.setAction("android.speech.tts.engine.CHECK_TTS_DATA");
                    main.this.startActivityForResult(checkIntent, 3);
                } catch (Exception e) {
                    e.printStackTrace();
                }
                Boolean listenerEnabled = false;
                for (String item : NotificationManagerCompat.getEnabledListenerPackages(main.this.getBaseContext())) {
                    if (item.equalsIgnoreCase(BuildConfig.APPLICATION_ID)) {
                        listenerEnabled = true;
                    }
                }
                if (main.this.preferences.getBoolean("enableGTalk", false) && !listenerEnabled.booleanValue()) {
                    main.this.startActivity(new Intent("android.settings.ACTION_NOTIFICATION_LISTENER_SETTINGS"));
                }
            }
        }
    };
    private DeviceDB myDB;
    boolean power = false;
    SharedPreferences preferences;
    Resources res;
    private final BroadcastReceiver sRunning = new BroadcastReceiver() {
        /* class a2dp.Vol.main.AnonymousClass13 */

        public void onReceive(Context arg0, Intent arg1) {
            try {
                if (service.run) {
                    main.this.servrun = true;
                    main.serv.setText(R.string.StopService);
                    main.this.getConnects();
                } else {
                    main.this.servrun = false;
                    main.serv.setText(R.string.StartService);
                    main.this.connects = 0;
                }
            } catch (Exception x) {
                x.printStackTrace();
                main.this.servrun = false;
                main.serv.setText(R.string.StartService);
                main.this.connects = 0;
                Log.e(main.LOG_TAG, "error" + x.getMessage());
            }
            main.this.refreshList(main.this.loadFromDB());
        }
    };
    boolean servrun = false;
    boolean toasts = true;
    Vector<btDevice> vec = new Vector<>();

    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.menu, menu);
        return true;
    }

    public boolean onOptionsItemSelected(MenuItem item) {
        switch (item.getItemId()) {
            case R.id.prefs:
                startActivity(new Intent(this, Preferences.class));
                return true;
            case R.id.DelData:
                AlertDialog.Builder builder = new AlertDialog.Builder(this);
                builder.setMessage(R.string.DeleteDataMsg).setCancelable(false).setPositiveButton(17039379, new DialogInterface.OnClickListener() {
                    /* class a2dp.Vol.main.AnonymousClass2 */

                    public void onClick(DialogInterface dialog, int id) {
                        main.this.myDB.deleteAll();
                        main.this.refreshList(main.this.loadFromDB());
                    }
                }).setNegativeButton(17039369, new DialogInterface.OnClickListener() {
                    /* class a2dp.Vol.main.AnonymousClass1 */

                    public void onClick(DialogInterface dialog, int id) {
                        dialog.cancel();
                    }
                });
                builder.create().show();
                return true;
            case R.id.Manage_data:
                this.myDB.getDb().close();
                startActivityForResult(new Intent(getBaseContext(), ManageData.class), 2);
                return true;
            case R.id.Exit:
                stopService(new Intent(this, service.class));
                finish();
                return true;
            case R.id.help:
                startActivity(new Intent("android.intent.action.VIEW", Uri.parse("https://github.com/jroal/a2dpvolume/wiki")));
                return true;
            case R.id.packages:
                startActivity(new Intent(this, PackagesChooser.class));
                return true;
            default:
                return false;
        }
    }

    public void onCreate(Bundle savedInstanceState) {
        this.res = getResources();
        setContentView(R.layout.main);
        String ver = null;
        try {
            ver = getPackageManager().getPackageInfo(new ComponentName(BuildConfig.APPLICATION_ID, "main").getPackageName(), 0).versionName;
        } catch (PackageManager.NameNotFoundException e) {
            Log.e(LOG_TAG, "error" + e.getMessage());
        }
        setTitle(this.res.getString(R.string.app_name) + " Version: " + ver);
        this.application = (MyApplication) getApplication();
        this.preferences = PreferenceManager.getDefaultSharedPreferences(this.application);
        try {
            if (this.preferences.getBoolean("useLocalStorage", false)) {
                this.a2dpDir = getFilesDir().toString();
            } else {
                this.a2dpDir = Environment.getExternalStorageDirectory() + "/A2DPVol";
            }
            File exportDir = new File(this.a2dpDir);
            if (!exportDir.exists()) {
                exportDir.mkdirs();
            }
            this.carMode = this.preferences.getBoolean("car_mode", true);
            this.homeDock = this.preferences.getBoolean("home_dock", false);
            this.headsetPlug = this.preferences.getBoolean("headset", false);
            this.power = this.preferences.getBoolean("power", false);
            this.enableTTS = this.preferences.getBoolean("enableTTS", false);
            this.toasts = this.preferences.getBoolean("toasts", true);
            this.TTSignore = this.preferences.getBoolean("TTSignore", false);
        } catch (Exception e2) {
            Log.e(LOG_TAG, "error" + e2.getMessage());
        }
        this.connects = 0;
        am = (AudioManager) getSystemService("audio");
        Button btn = (Button) findViewById(R.id.Button01);
        Button locbtn = (Button) findViewById(R.id.Locationbtn);
        serv = (Button) findViewById(R.id.ServButton);
        try {
            registerReceiver(this.sRunning, new IntentFilter("a2dp.vol.service.RUNNING"));
        } catch (Exception e22) {
            e22.printStackTrace();
        }
        try {
            registerReceiver(this.sRunning, new IntentFilter("a2dp.vol.service.STOPPED_RUNNING"));
        } catch (Exception e23) {
            e23.printStackTrace();
        }
        registerReceiver(this.mReceiver5, new IntentFilter("a2dp.Vol.main.RELOAD_LIST"));
        registerReceiver(this.mReceiver6, new IntentFilter("a2dp.vol.preferences.UPDATED"));
        this.lstring = new String[]{this.res.getString(R.string.NoData)};
        this.myDB = new DeviceDB(this.application);
        if (savedInstanceState == null) {
            int devicemin = 1;
            if (this.carMode) {
                devicemin = 1 + 1;
            }
            if (this.homeDock) {
                devicemin++;
            }
            try {
                if (this.myDB.getLength() < devicemin) {
                    getBtDevices(1);
                }
            } catch (Exception e1) {
                Log.e(LOG_TAG, "error" + e1.getMessage());
            }
            serv.setText(R.string.StartService);
            startService(new Intent(this, service.class));
            if (this.enableTTS) {
                try {
                    Intent checkIntent = new Intent();
                    checkIntent.setAction("android.speech.tts.engine.CHECK_TTS_DATA");
                    startActivityForResult(checkIntent, 3);
                } catch (Exception e3) {
                    e3.printStackTrace();
                }
            }
            startService(new Intent(this, NotificationCatcher.class));
        }
        this.ladapt = new ArrayAdapter<>(this.application, resourceID, this.lstring);
        this.lvl = (ListView) findViewById(R.id.ListView01);
        this.lvl.setAdapter((ListAdapter) this.ladapt);
        btn.setOnClickListener(new View.OnClickListener() {
            /* class a2dp.Vol.main.AnonymousClass3 */

            public void onClick(View v) {
                main.this.getBtDevices(1);
            }
        });
        this.lvl.setOnItemLongClickListener(new AdapterView.OnItemLongClickListener() {
            /* class a2dp.Vol.main.AnonymousClass4 */

            @Override // android.widget.AdapterView.OnItemLongClickListener
            public boolean onItemLongClick(AdapterView<?> adapterView, View view, int position, long id) {
                String mesg;
                if (main.this.vec.isEmpty()) {
                    return false;
                }
                BluetoothAdapter mBTA = BluetoothAdapter.getDefaultAdapter();
                new btDevice();
                btDevice bt = main.this.vec.get(position);
                BluetoothDevice btd = null;
                if (mBTA != null) {
                    for (BluetoothDevice device : mBTA.getBondedDevices()) {
                        if (device.getAddress().equalsIgnoreCase(bt.mac)) {
                            btd = device;
                        }
                    }
                }
                AlertDialog.Builder builder = new AlertDialog.Builder(main.this);
                builder.setTitle(bt.toString());
                final String car = bt.toString();
                if (btd != null) {
                    String mesg2 = bt.desc1 + "\n" + bt.mac + "\n" + main.this.res.getString(R.string.Bonded);
                    switch (btd.getBondState()) {
                        case ExploreByTouchHelper.INVALID_ID /*{ENCODED_INT: -2147483648}*/:
                            mesg2 = mesg2 + " = " + main.this.res.getString(R.string.Error);
                            break;
                        case 10:
                            mesg2 = mesg2 + " = " + main.this.res.getString(R.string.NotBonded);
                            break;
                        case 11:
                            mesg2 = mesg2 + " = " + main.this.res.getString(R.string.Bonding);
                            break;
                        case MotionEventCompat.AXIS_RX /*{ENCODED_INT: 12}*/:
                            mesg2 = mesg2 + " = " + main.this.res.getString(R.string.Bonded);
                            break;
                    }
                    mesg = ((mesg2 + "\n" + main.this.res.getString(R.string.Class) + " = " + main.this.getBTClassDev(btd)) + "\nMajor " + main.this.res.getString(R.string.Class) + " = " + main.this.getBTClassDevMaj(btd)) + "\nService " + main.this.res.getString(R.string.Class) + " = " + main.this.getBTClassServ(btd);
                } else {
                    mesg = (String) main.this.getText(R.string.btNotOn);
                }
                builder.setMessage(mesg);
                builder.setPositiveButton("OK", (DialogInterface.OnClickListener) null);
                builder.setNeutralButton(R.string.LocationString, new DialogInterface.OnClickListener() {
                    /* class a2dp.Vol.main.AnonymousClass4.AnonymousClass1 */

                    public void onClick(DialogInterface dialog, int which) {
                        File exportDir = new File(main.this.a2dpDir);
                        if (exportDir.exists()) {
                            Uri uri = Uri.parse(new String("file:///" + exportDir.getPath() + "/" + car.replaceAll(" ", "_") + ".html").trim());
                            Intent intent = new Intent();
                            intent.setAction("android.intent.action.VIEW");
                            intent.setDataAndType(uri, "text/html");
                            try {
                                main.this.getPackageManager().getPackageInfo("com.android.chrome", 0);
                                intent.setClassName("com.android.chrome", "com.google.android.apps.chrome.Main");
                            } catch (PackageManager.NameNotFoundException e1) {
                                intent.setClassName("com.android.browser", "com.android.browser.BrowserActivity");
                                e1.printStackTrace();
                            }
                            try {
                                main.this.startActivity(intent);
                            } catch (Exception e) {
                                Toast.makeText(main.this.application, e.toString(), 1).show();
                                e.printStackTrace();
                            }
                        }
                    }
                });
                builder.show();
                return true;
            }
        });
        this.lvl.setOnItemClickListener(new AdapterView.OnItemClickListener() {
            /* class a2dp.Vol.main.AnonymousClass5 */

            @Override // android.widget.AdapterView.OnItemClickListener
            public void onItemClick(AdapterView<?> adapterView, View view, int position, long id) {
                if (!main.this.vec.isEmpty()) {
                    final btDevice bt = main.this.vec.get(position);
                    final btDevice bt2 = main.this.myDB.getBTD(bt.mac);
                    AlertDialog.Builder builder = new AlertDialog.Builder(main.this);
                    builder.setTitle(bt.toString());
                    builder.setMessage(bt2.desc1 + "\n" + bt2.desc2 + "\n" + bt2.mac);
                    builder.setPositiveButton(17039370, (DialogInterface.OnClickListener) null);
                    builder.setNegativeButton(R.string.Delete, new DialogInterface.OnClickListener() {
                        /* class a2dp.Vol.main.AnonymousClass5.AnonymousClass1 */

                        public void onClick(DialogInterface dialog, int which) {
                            main.this.myDB.delete(bt2);
                            main.this.refreshList(main.this.loadFromDB());
                        }
                    });
                    builder.setNeutralButton(R.string.Edit, new DialogInterface.OnClickListener() {
                        /* class a2dp.Vol.main.AnonymousClass5.AnonymousClass2 */

                        public void onClick(DialogInterface dialog, int which) {
                            Intent i = new Intent(main.this, EditDevice.class);
                            i.putExtra("btd", bt.mac);
                            main.this.startActivityForResult(i, 4);
                        }
                    });
                    builder.show();
                }
            }
        });
        locbtn.setOnClickListener(new View.OnClickListener() {
            /* class a2dp.Vol.main.AnonymousClass6 */

            public void onClick(View v) {
                main.this.Locationbtn();
            }
        });
        locbtn.setOnLongClickListener(new View.OnLongClickListener() {
            /* class a2dp.Vol.main.AnonymousClass7 */

            public boolean onLongClick(View v) {
                try {
                    byte[] buff = new byte[250];
                    FileInputStream fs = main.this.openFileInput("My_Last_Location2");
                    fs.read(buff);
                    fs.close();
                    String st = new String(buff).trim();
                    Toast.makeText(main.this, st, 1).show();
                    main.this.startActivity(new Intent("android.intent.action.VIEW", Uri.parse(st)));
                    return false;
                } catch (FileNotFoundException e) {
                    Toast.makeText(main.this, (int) R.string.NoData, 1).show();
                    Log.e(main.LOG_TAG, "error" + e.getMessage());
                    return false;
                } catch (IOException e2) {
                    Toast.makeText(main.this, "Some IO issue", 1).show();
                    Log.e(main.LOG_TAG, "error" + e2.getMessage());
                    return false;
                }
            }
        });
        serv.setOnClickListener(new View.OnClickListener() {
            /* class a2dp.Vol.main.AnonymousClass8 */

            public void onClick(View v) {
                if (main.this.servrun) {
                    main.this.stopService(new Intent(main.this, service.class));
                } else {
                    main.this.startService(new Intent(main.this, service.class));
                }
            }
        });
        new CountDownTimer(2000, 1000) {
            /* class a2dp.Vol.main.AnonymousClass9 */

            public void onTick(long millisUntilFinished) {
                try {
                    if (service.run) {
                        main.this.servrun = true;
                        main.serv.setText(R.string.StopService);
                        return;
                    }
                    main.this.servrun = false;
                    main.serv.setText(R.string.StartService);
                } catch (Exception x) {
                    main.this.servrun = false;
                    main.serv.setText(R.string.StartService);
                    Log.e(main.LOG_TAG, "error" + x.getMessage());
                }
            }

            public void onFinish() {
                try {
                    if (service.run) {
                        main.this.servrun = true;
                        main.serv.setText(R.string.StopService);
                        main.this.getConnects();
                        main.this.refreshList(main.this.loadFromDB());
                        return;
                    }
                    main.this.servrun = false;
                    main.serv.setText(R.string.StartService);
                } catch (Exception x) {
                    main.this.servrun = false;
                    main.serv.setText(R.string.StartService);
                    Log.e(main.LOG_TAG, "error" + x.getMessage());
                }
            }
        }.start();
        getConnects();
        refreshList(loadFromDB());
        super.onCreate(savedInstanceState);
    }

    /* access modifiers changed from: private */
    /* access modifiers changed from: public */
    private void getConnects() {
        if (this.servrun) {
            this.connects = service.connects.intValue();
        } else {
            this.connects = 0;
        }
    }

    /* access modifiers changed from: protected */
    public void onStop() {
        super.onStop();
    }

    /* access modifiers changed from: protected */
    public void onDestroy() {
        try {
            unregisterReceiver(this.sRunning);
            unregisterReceiver(this.mReceiver5);
            unregisterReceiver(this.mReceiver6);
        } catch (Exception e) {
            e.printStackTrace();
        }
        this.myDB.getDb().close();
        super.onDestroy();
    }

    /* access modifiers changed from: protected */
    public void onPause() {
        super.onPause();
    }

    /* access modifiers changed from: protected */
    public void onResume() {
        getConnects();
        refreshList(loadFromDB());
        super.onResume();
    }

    /* access modifiers changed from: protected */
    public void onRestart() {
        super.onRestart();
    }

    public void Locationbtn() {
        try {
            byte[] buff = new byte[250];
            FileInputStream fs = openFileInput("My_Last_Location");
            fs.read(buff);
            fs.close();
            String st = new String(buff).trim();
            Intent i = new Intent("android.intent.action.VIEW");
            i.setData(Uri.parse(st));
            startActivity(i);
        } catch (FileNotFoundException e) {
            Toast.makeText(this, (int) R.string.NoData, 1).show();
            Log.e(LOG_TAG, "error" + e.getMessage());
        } catch (IOException e2) {
            Toast.makeText(this, "Some IO issue", 1).show();
            Log.e(LOG_TAG, "error" + e2.getMessage());
        }
    }

    /* access modifiers changed from: private */
    /* access modifiers changed from: public */
    private int getBtDevices(int mode) {
        String name;
        int i = 0;
        this.vec.clear();
        if (this.carMode) {
            btDevice fbt = new btDevice();
            String str = getString(R.string.carDockName);
            fbt.setBluetoothDevice(str, str, "1", am.getStreamMaxVolume(3));
            btDevice fbt2 = this.myDB.getBTD(fbt.mac);
            if (fbt2.mac == null) {
                fbt.setIcon(R.drawable.car2);
                this.myDB.insert(fbt);
                this.vec.add(fbt);
            } else {
                this.vec.add(fbt2);
            }
            refreshList(loadFromDB());
        }
        if (this.homeDock) {
            btDevice fbt3 = new btDevice();
            String str2 = getString(R.string.homeDockName);
            fbt3.setBluetoothDevice(str2, str2, "2", am.getStreamMaxVolume(3));
            btDevice fbt22 = this.myDB.getBTD(fbt3.mac);
            if (fbt22.mac == null) {
                fbt3.setGetLoc(false);
                fbt3.setIcon(R.drawable.usb);
                this.myDB.insert(fbt3);
                this.vec.add(fbt3);
            } else {
                this.vec.add(fbt22);
            }
            refreshList(loadFromDB());
        }
        if (this.headsetPlug) {
            btDevice fbt4 = new btDevice();
            String str3 = getString(R.string.audioJackName);
            fbt4.setBluetoothDevice(str3, str3, "3", am.getStreamMaxVolume(3));
            btDevice fbt23 = this.myDB.getBTD(fbt4.mac);
            if (fbt23.mac == null) {
                fbt4.setGetLoc(false);
                fbt4.setIcon(R.drawable.jack);
                this.myDB.insert(fbt4);
                this.vec.add(fbt4);
            } else {
                this.vec.add(fbt23);
            }
            refreshList(loadFromDB());
        }
        if (this.power) {
            btDevice fbt5 = new btDevice();
            String str4 = getString(R.string.powerPlugName);
            fbt5.setBluetoothDevice(str4, str4, "4", am.getStreamMaxVolume(3));
            btDevice fbt24 = this.myDB.getBTD(fbt5.mac);
            if (fbt24.mac == null) {
                fbt5.setGetLoc(false);
                fbt5.setIcon(R.drawable.usb);
                this.myDB.insert(fbt5);
                this.vec.add(fbt5);
            } else {
                this.vec.add(fbt24);
            }
            refreshList(loadFromDB());
        }
        if (mode >= 1) {
            BluetoothAdapter mBTA = BluetoothAdapter.getDefaultAdapter();
            if (mBTA == null) {
                Toast.makeText(this.application, (int) R.string.NobtSupport, 1).show();
                return 0;
            } else if (!mBTA.isEnabled()) {
                try {
                    startActivityForResult(new Intent("android.bluetooth.adapter.action.REQUEST_ENABLE"), 1);
                } catch (Exception e) {
                    e.printStackTrace();
                }
                return 0;
            } else {
                if (mBTA != null) {
                    Set<BluetoothDevice> pairedDevices = mBTA.getBondedDevices();
                    if (pairedDevices.size() > 0) {
                        IBluetooth ibta = getIBluetooth();
                        for (BluetoothDevice device : pairedDevices) {
                            if (device.getAddress() != null) {
                                btDevice bt = new btDevice();
                                i++;
                                if (Build.VERSION.SDK_INT < 14 || Build.VERSION.SDK_INT > 16) {
                                    name = device.getName();
                                } else {
                                    try {
                                        name = ibta.getRemoteAlias(device.getAddress());
                                    } catch (RemoteException e2) {
                                        name = device.getName();
                                        e2.printStackTrace();
                                    }
                                    if (name == null) {
                                        name = device.getName();
                                    }
                                }
                                bt.setBluetoothDevice(device, name, am.getStreamMaxVolume(3));
                                if (Build.VERSION.SDK_INT > 15) {
                                    bt.setSetV(false);
                                }
                                btDevice bt2 = this.myDB.getBTD(bt.mac);
                                if (bt2.mac == null) {
                                    this.myDB.insert(bt);
                                    this.vec.add(bt);
                                } else {
                                    this.vec.add(bt2);
                                }
                            }
                        }
                    }
                }
                refreshList(loadFromDB());
                Toast.makeText(this.application, "Found " + i + " Bluetooth Devices", 1).show();
            }
        }
        return i;
    }

    /* access modifiers changed from: protected */
    public void onActivityResult(int requestCode, int resultCode, Intent data) {
        if (resultCode == -1) {
            switch (requestCode) {
                case 1:
                    if (resultCode == 0) {
                        Toast.makeText(this.application, (int) R.string.btEnableFail, 1).show();
                        refreshList(loadFromDB());
                        break;
                    } else {
                        int test = getBtDevices(1);
                        if (test > 0) {
                            this.lstring = new String[test];
                            for (int i = 0; i < test; i++) {
                                this.lstring[i] = this.vec.get(i).toString();
                            }
                            refreshList(loadFromDB());
                            break;
                        }
                    }
                    break;
                case 2:
                    refreshList(loadFromDB());
                    break;
            }
        }
        if (requestCode == 4) {
            this.enableTTS = this.preferences.getBoolean("enableTTS", false);
            if (this.enableTTS) {
                try {
                    Intent checkIntent = new Intent();
                    checkIntent.setAction("android.speech.tts.engine.CHECK_TTS_DATA");
                    startActivityForResult(checkIntent, 3);
                } catch (Exception e) {
                    Toast.makeText(this.application, "TTS missing fault", 1).show();
                }
            }
        }
        if (requestCode == 3) {
            switch (resultCode) {
                case -3:
                    if (this.toasts) {
                        Toast.makeText(this.application, "TTS Missing Volume", 0).show();
                        return;
                    }
                    return;
                case -2:
                    if (!this.TTSignore) {
                        AlertDialog.Builder builder = new AlertDialog.Builder(this);
                        builder.setTitle(getString(R.string.app_name));
                        builder.setPositiveButton(R.string.Yes, new DialogInterface.OnClickListener() {
                            /* class a2dp.Vol.main.AnonymousClass10 */

                            public void onClick(DialogInterface dialog, int which) {
                                Intent installIntent = new Intent();
                                installIntent.setAction("android.speech.tts.engine.INSTALL_TTS_DATA");
                                main.this.startActivityForResult(installIntent, 3);
                            }
                        });
                        builder.setNegativeButton(R.string.No, (DialogInterface.OnClickListener) null);
                        builder.setNeutralButton(R.string.ignoreTTSMissing, setIgnore());
                        builder.setMessage(R.string.needTTS);
                        builder.show();
                        return;
                    }
                    return;
                case -1:
                    if (this.toasts) {
                        Toast.makeText(this.application, "TTS Bad Data", 0).show();
                        return;
                    }
                    return;
                case 0:
                    if (this.toasts) {
                        Toast.makeText(this.application, "TTS Voice data fail", 0).show();
                        return;
                    }
                    return;
                case 1:
                    if (this.toasts) {
                        Toast.makeText(this.application, (int) R.string.TTSready, 0).show();
                        return;
                    }
                    return;
                default:
                    return;
            }
        }
    }

    private DialogInterface.OnClickListener setIgnore() {
        SharedPreferences.Editor editor = this.preferences.edit();
        this.TTSignore = true;
        editor.putBoolean("TTSignore", true);
        editor.commit();
        return null;
    }

    /* access modifiers changed from: private */
    /* access modifiers changed from: public */
    private void refreshList(int test) {
        if (test > 0) {
            this.lstring = new String[test];
            for (int i = 0; i < test; i++) {
                this.lstring[i] = this.vec.get(i).toString();
                if (this.connects > 0 && this.servrun) {
                    for (int j = 0; j < service.btdConn.length; j++) {
                        if (service.btdConn[j] != null && this.vec.get(i).getMac().equalsIgnoreCase(service.btdConn[j].getMac())) {
                            StringBuilder sb = new StringBuilder();
                            String[] strArr = this.lstring;
                            strArr[i] = sb.append(strArr[i]).append(" **").toString();
                        }
                    }
                }
            }
        } else {
            this.lstring = new String[]{"no data"};
        }
        this.ladapt = new ArrayAdapter<>(this.application, resourceID, this.lstring);
        this.lvl.setAdapter((ListAdapter) this.ladapt);
        this.ladapt.notifyDataSetChanged();
        this.lvl.invalidateViews();
        this.lvl.forceLayout();
    }

    /* access modifiers changed from: private */
    /* access modifiers changed from: public */
    private int loadFromDB() {
        this.myDB.getDb().close();
        if (!this.myDB.getDb().isOpen()) {
            try {
                this.myDB = new DeviceDB(this.application);
            } catch (Exception e) {
                e.printStackTrace();
                return 0;
            }
        }
        try {
            this.vec = this.myDB.selectAlldb();
            if (this.vec.isEmpty() || this.vec == null) {
                return 0;
            }
            return this.vec.size();
        } catch (Exception e2) {
            e2.printStackTrace();
            return 0;
        }
    }

    /* access modifiers changed from: private */
    /* access modifiers changed from: public */
    private String getBTClassServ(BluetoothDevice btd) {
        String temp = "";
        if (btd == null) {
            return temp;
        }
        if (btd.getBluetoothClass().hasService(2097152)) {
            temp = "Audio, ";
        }
        if (btd.getBluetoothClass().hasService(4194304)) {
            temp = temp + "Telophony, ";
        }
        if (btd.getBluetoothClass().hasService(GravityCompat.RELATIVE_LAYOUT_DIRECTION)) {
            temp = temp + "Information, ";
        }
        if (btd.getBluetoothClass().hasService(8192)) {
            temp = temp + "Limited Discoverability, ";
        }
        if (btd.getBluetoothClass().hasService(131072)) {
            temp = temp + "Networking, ";
        }
        if (btd.getBluetoothClass().hasService(1048576)) {
            temp = temp + "Object Transfer, ";
        }
        if (btd.getBluetoothClass().hasService(65536)) {
            temp = temp + "Positioning, ";
        }
        if (btd.getBluetoothClass().hasService(262144)) {
            temp = temp + "Render, ";
        }
        if (btd.getBluetoothClass().hasService(524288)) {
            temp = temp + "Capture, ";
        }
        if (temp.length() > 5) {
            temp = temp.substring(0, temp.length() - 2);
        }
        return temp;
    }

    /* access modifiers changed from: private */
    /* access modifiers changed from: public */
    private String getBTClassDev(BluetoothDevice btd) {
        String temp;
        String temp2 = "";
        if (btd == null) {
            return temp2;
        }
        if (btd.getBluetoothClass().getDeviceClass() == 1056) {
            temp2 = "Car Audio, ";
        }
        if (btd.getBluetoothClass().getDeviceClass() == 1032) {
            temp2 = temp2 + "Handsfree, ";
        }
        if (btd.getBluetoothClass().getDeviceClass() == 1048) {
            temp2 = temp2 + "Headphones, ";
        }
        if (btd.getBluetoothClass().getDeviceClass() == 1064) {
            temp2 = temp2 + "HiFi Audio, ";
        }
        if (btd.getBluetoothClass().getDeviceClass() == 1044) {
            temp2 = temp2 + "Loudspeaker, ";
        }
        if (btd.getBluetoothClass().getDeviceClass() == 1052) {
            temp2 = temp2 + "Portable Audio, ";
        }
        if (btd.getBluetoothClass().getDeviceClass() == 1076) {
            temp2 = temp2 + "Camcorder, ";
        }
        if (btd.getBluetoothClass().getDeviceClass() == 1060) {
            temp2 = temp2 + "Set Top Box, ";
        }
        if (btd.getBluetoothClass().getDeviceClass() == 1084) {
            temp2 = temp2 + "A/V Display/Speaker, ";
        }
        if (btd.getBluetoothClass().getDeviceClass() == 1080) {
            temp2 = temp2 + "Video Monitor, ";
        }
        if (btd.getBluetoothClass().getDeviceClass() == 1068) {
            temp2 = temp2 + "VCR, ";
        }
        if (btd.getBluetoothClass().getDeviceClass() == 516) {
            temp2 = temp2 + "Cellular Phone, ";
        }
        if (btd.getBluetoothClass().getDeviceClass() == 524) {
            temp2 = temp2 + "Smart Phone, ";
        }
        if (btd.getBluetoothClass().getDeviceClass() == 520) {
            temp2 = temp2 + "Cordless Phone, ";
        }
        if (btd.getBluetoothClass().getDeviceClass() == 532) {
            temp2 = temp2 + "ISDN Phone, ";
        }
        if (btd.getBluetoothClass().getDeviceClass() == 528) {
            temp2 = temp2 + "Phone Modem/Gateway, ";
        }
        if (btd.getBluetoothClass().getDeviceClass() == 512) {
            temp2 = temp2 + "Other Phone, ";
        }
        if (btd.getBluetoothClass().getDeviceClass() == 1028) {
            temp2 = temp2 + "Wearable Headset, ";
        }
        if (btd.getBluetoothClass().getDeviceClass() == 1024) {
            temp2 = temp2 + "Uncategorized A/V, ";
        }
        if (btd.getBluetoothClass().getDeviceClass() == 512) {
            temp2 = temp2 + "Uncategorized Phone, ";
        }
        if (btd.getBluetoothClass().getDeviceClass() == 2048) {
            temp2 = temp2 + "Incategorized Toy, ";
        }
        if (btd.getBluetoothClass().getDeviceClass() == 260) {
            temp2 = temp2 + "Desktop PC, ";
        }
        if (btd.getBluetoothClass().getDeviceClass() == 272) {
            temp2 = temp2 + "Handheld PC, ";
        }
        if (btd.getBluetoothClass().getDeviceClass() == 268) {
            temp2 = temp2 + "Laptop PC, ";
        }
        if (btd.getBluetoothClass().getDeviceClass() == 276) {
            temp2 = temp2 + "Palm Sized PC/PDA, ";
        }
        if (btd.getBluetoothClass().getDeviceClass() == 280) {
            temp2 = temp2 + "Wearable PC, ";
        }
        if (btd.getBluetoothClass().getDeviceClass() == 264) {
            temp2 = temp2 + "Server PC, ";
        }
        if (btd.getBluetoothClass().getDeviceClass() == 256) {
            temp2 = temp2 + "Computer, ";
        }
        if (temp2.length() > 3) {
            temp = temp2.substring(0, temp2.length() - 2);
        } else {
            temp = "other";
        }
        return temp;
    }

    /* access modifiers changed from: private */
    /* access modifiers changed from: public */
    private String getBTClassDevMaj(BluetoothDevice btd) {
        String temp;
        String temp2 = "";
        if (btd == null) {
            return temp2;
        }
        if (btd.getBluetoothClass().getMajorDeviceClass() == 1024) {
            temp2 = "Audio Video, ";
        }
        if (btd.getBluetoothClass().getMajorDeviceClass() == 256) {
            temp2 = temp2 + "Computer, ";
        }
        if (btd.getBluetoothClass().getMajorDeviceClass() == 2304) {
            temp2 = temp2 + "Health, ";
        }
        if (btd.getBluetoothClass().getMajorDeviceClass() == 0) {
            temp2 = temp2 + "Misc, ";
        }
        if (btd.getBluetoothClass().getMajorDeviceClass() == 768) {
            temp2 = temp2 + "Networking, ";
        }
        if (btd.getBluetoothClass().getMajorDeviceClass() == 1280) {
            temp2 = temp2 + "Peripheral, ";
        }
        if (btd.getBluetoothClass().getMajorDeviceClass() == 512) {
            temp2 = temp2 + "Phone, ";
        }
        if (btd.getBluetoothClass().getMajorDeviceClass() == 7936) {
            temp2 = temp2 + "Uncategorized, ";
        }
        if (btd.getBluetoothClass().getMajorDeviceClass() == 1792) {
            temp2 = temp2 + "Wearable, ";
        }
        if (btd.getBluetoothClass().getMajorDeviceClass() == 2048) {
            temp2 = temp2 + "Toy, ";
        }
        if (btd.getBluetoothClass().getMajorDeviceClass() == 1536) {
            temp2 = temp2 + "Imaging, ";
        }
        if (temp2.length() >= 3) {
            temp = temp2.substring(0, temp2.length() - 2);
        } else {
            temp = "other";
        }
        return temp;
    }

    private IBluetooth getIBluetooth() {
        try {
            IBinder b = (IBinder) Class.forName("android.os.ServiceManager").getDeclaredMethod("getService", String.class).invoke(null, "bluetooth");
            Log.d(LOG_TAG, "Test2: " + b.getInterfaceDescriptor());
            Method m = Class.forName("android.bluetooth.IBluetooth").getDeclaredClasses()[0].getDeclaredMethod("asInterface", IBinder.class);
            m.setAccessible(true);
            return (IBluetooth) m.invoke(null, b);
        } catch (Exception e) {
            Log.e(LOG_TAG, "Error " + e.getMessage());
            return null;
        }
    }
}
