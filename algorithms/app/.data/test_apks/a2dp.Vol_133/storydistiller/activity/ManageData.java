package a2dp.Vol;

import android.app.Activity;
import android.app.ProgressDialog;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.Environment;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.nio.channels.FileChannel;
import java.util.Iterator;
import java.util.List;

public class ManageData extends Activity {
    String a2dpDir;
    private MyApplication application;
    private Button exportDbToSdButton;
    private Button exportDbXmlToSdButton;
    private Button exportLoc;
    private Button importDB;
    private TextView output = null;
    private TextView path = null;
    private String pathstr;

    public void finish() {
        setResult(-1, new Intent());
        super.finish();
    }

    /* access modifiers changed from: protected */
    public void onDestroy() {
        setResult(-1, new Intent());
        super.onDestroy();
    }

    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        this.application = (MyApplication) getApplication();
        this.a2dpDir = Environment.getExternalStorageDirectory() + "/A2DPVol";
        setContentView(R.layout.managedata);
        this.output = (TextView) findViewById(R.id.Output);
        this.path = (TextView) findViewById(R.id.Path);
        new SelectDataTask().execute(new String[0]);
        this.exportDbToSdButton = (Button) findViewById(R.id.exportdbtosdbutton);
        this.exportDbToSdButton.setOnClickListener(new View.OnClickListener() {
            /* class a2dp.Vol.ManageData.AnonymousClass1 */

            public void onClick(View v) {
                if (ManageData.this.isExternalStorageAvail()) {
                    new ExportDatabaseFileTask().execute(new String[0]);
                } else {
                    Toast.makeText(ManageData.this, "External storage is not available, unable to export data.", 0).show();
                }
            }
        });
        this.exportDbXmlToSdButton = (Button) findViewById(R.id.exportdbxmltosdbutton);
        this.exportDbXmlToSdButton.setOnClickListener(new View.OnClickListener() {
            /* class a2dp.Vol.ManageData.AnonymousClass2 */

            public void onClick(View v) {
                if (ManageData.this.isExternalStorageAvail()) {
                    new ExportDataAsXmlTask().execute("devices", "A2DPDevices");
                    return;
                }
                Toast.makeText(ManageData.this, "External storage is not available, unable to export data.", 0).show();
            }
        });
        this.importDB = (Button) findViewById(R.id.ImportDBButton);
        this.importDB.setOnClickListener(new View.OnClickListener() {
            /* class a2dp.Vol.ManageData.AnonymousClass3 */

            public void onClick(View v) {
                if (ManageData.this.isExternalStorageAvail()) {
                    new ImportDatabaseFileTask().execute("devices", ManageData.this.a2dpDir);
                    return;
                }
                Toast.makeText(ManageData.this, "External storage is not available, unable to import data.", 0).show();
            }
        });
        this.exportLoc = (Button) findViewById(R.id.ExportLoc);
        this.exportLoc.setOnClickListener(new View.OnClickListener() {
            /* class a2dp.Vol.ManageData.AnonymousClass4 */

            public void onClick(View v) {
                if (ManageData.this.isExternalStorageAvail()) {
                    new ExportLocationTask().execute("My_Last_Location", ManageData.this.a2dpDir);
                    return;
                }
                Toast.makeText(ManageData.this, "External storage is not available, unable to export data.", 0).show();
            }
        });
    }

    public void onPause() {
        super.onPause();
    }

    /* access modifiers changed from: protected */
    public void onRestoreInstanceState(Bundle savedInstanceState) {
        super.onRestoreInstanceState(savedInstanceState);
    }

    /* access modifiers changed from: protected */
    public void onSaveInstanceState(Bundle saveState) {
        super.onSaveInstanceState(saveState);
    }

    /* access modifiers changed from: private */
    /* access modifiers changed from: public */
    private boolean isExternalStorageAvail() {
        return Environment.getExternalStorageState().equals("mounted");
    }

    private class ExportDatabaseFileTask extends AsyncTask<String, Void, Boolean> {
        private final ProgressDialog dialog;

        private ExportDatabaseFileTask() {
            this.dialog = new ProgressDialog(ManageData.this);
        }

        /* access modifiers changed from: protected */
        public void onPreExecute() {
            this.dialog.setMessage("Exporting database...");
            this.dialog.show();
        }

        /* access modifiers changed from: protected */
        public Boolean doInBackground(String... args) {
            File dbFile = new File(ManageData.this.application.getDeviceDB().getDb().getPath());
            File exportDir = new File(ManageData.this.a2dpDir);
            if (!exportDir.exists()) {
                exportDir.mkdirs();
            }
            File file = new File(exportDir, dbFile.getName());
            ManageData.this.pathstr = file.getPath();
            try {
                file.createNewFile();
                copyFile(dbFile, file);
                return true;
            } catch (IOException e) {
                Log.e(MyApplication.APP_NAME, e.getMessage(), e);
                return false;
            }
        }

        /* access modifiers changed from: protected */
        public void onPostExecute(Boolean success) {
            if (this.dialog.isShowing()) {
                this.dialog.dismiss();
            }
            if (success.booleanValue()) {
                Toast.makeText(ManageData.this, "Export successful!", 0).show();
                ManageData.this.path.setText("Exported to: " + ManageData.this.pathstr);
                return;
            }
            Toast.makeText(ManageData.this, "Export failed", 0).show();
            ManageData.this.path.setText("Export Failed");
        }

        /* access modifiers changed from: package-private */
        public void copyFile(File src, File dst) throws IOException {
            FileChannel inChannel = new FileInputStream(src).getChannel();
            FileChannel outChannel = new FileOutputStream(dst).getChannel();
            try {
                inChannel.transferTo(0, inChannel.size(), outChannel);
            } finally {
                if (inChannel != null) {
                    inChannel.close();
                }
                if (outChannel != null) {
                    outChannel.close();
                }
            }
        }
    }

    private class ExportDataAsXmlTask extends AsyncTask<String, Void, String> {
        private final ProgressDialog dialog;

        private ExportDataAsXmlTask() {
            this.dialog = new ProgressDialog(ManageData.this);
        }

        /* access modifiers changed from: protected */
        public void onPreExecute() {
            this.dialog.setMessage("Exporting database as XML...");
            this.dialog.show();
        }

        /* access modifiers changed from: protected */
        public String doInBackground(String... args) {
            DataXmlExporter dm = new DataXmlExporter(ManageData.this.application.getDeviceDB().getDb());
            try {
                String dbName = args[0];
                String exportFileName = args[1];
                dm.export(dbName, exportFileName);
                ManageData.this.pathstr = ManageData.this.a2dpDir + "/" + exportFileName + ".xml";
                return null;
            } catch (IOException e) {
                Log.e(MyApplication.APP_NAME, e.getMessage(), e);
                return e.getMessage();
            }
        }

        /* access modifiers changed from: protected */
        public void onPostExecute(String errMsg) {
            if (this.dialog.isShowing()) {
                this.dialog.dismiss();
            }
            if (errMsg == null) {
                Toast.makeText(ManageData.this, "Export successful!", 0).show();
                ManageData.this.path.setText("Exported to: " + ManageData.this.pathstr);
                return;
            }
            Toast.makeText(ManageData.this, "Export failed - " + errMsg, 0).show();
            ManageData.this.path.setText("Export Failed");
        }
    }

    private class SelectDataTask extends AsyncTask<String, Void, String> {
        private final ProgressDialog dialog;

        private SelectDataTask() {
            this.dialog = new ProgressDialog(ManageData.this);
        }

        /* access modifiers changed from: protected */
        public void onPreExecute() {
            this.dialog.setMessage("Selecting data...");
            this.dialog.show();
        }

        /* access modifiers changed from: protected */
        public String doInBackground(String... args) {
            List<String> names = ManageData.this.application.getDeviceDB().selectAll();
            StringBuilder sb = new StringBuilder();
            Iterator<String> it = names.iterator();
            while (it.hasNext()) {
                sb.append(it.next() + "\n");
            }
            return sb.toString();
        }

        /* access modifiers changed from: protected */
        public void onPostExecute(String result) {
            if (this.dialog.isShowing()) {
                this.dialog.dismiss();
            }
            ManageData.this.output.setText(result);
        }
    }

    private class ImportDatabaseFileTask extends AsyncTask<String, Void, Boolean> {
        private final ProgressDialog dialog;

        private ImportDatabaseFileTask() {
            this.dialog = new ProgressDialog(ManageData.this);
        }

        /* access modifiers changed from: protected */
        public void onPreExecute() {
            this.dialog.setMessage("Importing database...");
            this.dialog.show();
        }

        /* access modifiers changed from: protected */
        public Boolean doInBackground(String... args) {
            File dbFile = new File(ManageData.this.application.getDeviceDB().getDb().getPath());
            File exportDir = new File(ManageData.this.a2dpDir);
            if (!exportDir.exists()) {
                exportDir.mkdirs();
            }
            File file = new File(exportDir, dbFile.getName());
            ManageData.this.pathstr = file.getPath();
            try {
                file.createNewFile();
                copyFile(file, dbFile);
                return true;
            } catch (IOException e) {
                Log.e(MyApplication.APP_NAME, e.getMessage(), e);
                return false;
            }
        }

        /* access modifiers changed from: protected */
        public void onPostExecute(Boolean success) {
            if (this.dialog.isShowing()) {
                this.dialog.dismiss();
            }
            if (success.booleanValue()) {
                ManageData.this.path.setText("Imported from: " + ManageData.this.pathstr);
                Intent itent = new Intent();
                itent.setAction("a2dp.vol.Main.RELOAD_LIST");
                itent.putExtra("device", "");
                ManageData.this.application.sendBroadcast(itent);
                Toast.makeText(ManageData.this, (int) R.string.ImportCompletedText, 0).show();
                return;
            }
            Toast.makeText(ManageData.this, "Import failed", 0).show();
            ManageData.this.path.setText("Import Failed");
        }

        /* access modifiers changed from: package-private */
        public void copyFile(File src, File dst) throws IOException {
            FileChannel inChannel = new FileInputStream(src).getChannel();
            FileChannel outChannel = new FileOutputStream(dst).getChannel();
            try {
                inChannel.transferTo(0, inChannel.size(), outChannel);
            } finally {
                if (inChannel != null) {
                    inChannel.close();
                }
                if (outChannel != null) {
                    outChannel.close();
                }
            }
        }
    }

    private class ExportLocationTask extends AsyncTask<String, Void, Boolean> {
        private final ProgressDialog dialog;

        private ExportLocationTask() {
            this.dialog = new ProgressDialog(ManageData.this);
        }

        /* access modifiers changed from: protected */
        public void onPreExecute() {
            this.dialog.setMessage("Exporting location data...");
            this.dialog.show();
        }

        /* access modifiers changed from: protected */
        public Boolean doInBackground(String... args) {
            File LocFile = ManageData.this.application.getFileStreamPath(args[0]);
            File exportDir = new File(ManageData.this.a2dpDir);
            if (!exportDir.exists()) {
                exportDir.mkdirs();
            }
            File file = new File(exportDir, LocFile.getName() + ".txt");
            ManageData.this.pathstr = file.getPath();
            try {
                file.createNewFile();
                copyFile(LocFile, file);
                return true;
            } catch (IOException e) {
                Log.e(MyApplication.APP_NAME, e.getMessage(), e);
                return false;
            }
        }

        /* access modifiers changed from: protected */
        public void onPostExecute(Boolean success) {
            if (this.dialog.isShowing()) {
                this.dialog.dismiss();
            }
            if (success.booleanValue()) {
                ManageData.this.path.setText("Exported to: " + ManageData.this.pathstr);
                Toast.makeText(ManageData.this, "Location data exported", 1).show();
                return;
            }
            Toast.makeText(ManageData.this, "Export failed", 0).show();
            ManageData.this.path.setText("Export Failed");
        }

        /* access modifiers changed from: package-private */
        public void copyFile(File src, File dst) throws IOException {
            FileChannel inChannel = new FileInputStream(src).getChannel();
            FileChannel outChannel = new FileOutputStream(dst).getChannel();
            try {
                inChannel.transferTo(0, inChannel.size(), outChannel);
            } finally {
                if (inChannel != null) {
                    inChannel.close();
                }
                if (outChannel != null) {
                    outChannel.close();
                }
            }
        }
    }
}
